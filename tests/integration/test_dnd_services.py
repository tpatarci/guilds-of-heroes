"""Integration tests for D&D services — characters, campaigns, session logs, dice."""

from __future__ import annotations

import sqlite3

import pytest

from goh.domain.exceptions import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
)
from goh.repositories import user_repo
from goh.services import (
    campaign_service,
    character_service,
    dice_service,
    session_log_service,
)


def _create_user(db: sqlite3.Connection, username: str = "player1", role: str = "player") -> int:
    user = user_repo.create(
        db, username=username, email=f"{username}@test.com",
        password_hash="fakehash", display_name=username.title(), role=role,
    )
    return user.id


class TestCharacterService:
    def test_create_character(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        char = character_service.create_character(
            db, owner_id=uid, name="Gandalf", race="Human", char_class="Wizard",
            level=20, intelligence=20,
        )
        assert char["name"] == "Gandalf"
        assert char["class"] == "Wizard"
        assert char["ability_scores"]["intelligence"] == 20

    def test_create_character_empty_name(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        with pytest.raises(ValidationError, match="name"):
            character_service.create_character(db, owner_id=uid, name="  ")

    def test_create_character_invalid_level(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        with pytest.raises(ValidationError, match="Level"):
            character_service.create_character(db, owner_id=uid, name="Test", level=21)

    def test_list_characters(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        character_service.create_character(db, owner_id=uid, name="Char1")
        character_service.create_character(db, owner_id=uid, name="Char2")
        chars = character_service.list_characters(db, uid)
        assert len(chars) == 2

    def test_delete_character(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        char = character_service.create_character(db, owner_id=uid, name="Temp")
        character_service.delete_character(db, char["id"], uid)
        with pytest.raises(NotFoundError):
            character_service.get_character(db, char["id"])

    def test_delete_character_not_owner(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "alice")
        uid2 = _create_user(db, "bob")
        char = character_service.create_character(db, owner_id=uid1, name="MyChar")
        with pytest.raises(ForbiddenError):
            character_service.delete_character(db, char["id"], uid2)


class TestCampaignService:
    def test_create_campaign(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Curse of Strahd")
        assert camp["name"] == "Curse of Strahd"
        assert camp["dm_username"] == "dm1"

    def test_join_campaign(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        player = _create_user(db, "player1")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Test")
        result = campaign_service.join_campaign(db, camp["id"], player)
        assert result["joined"] is True

        details = campaign_service.get_campaign(db, camp["id"])
        assert details["member_count"] == 2  # DM + player

    def test_join_already_member(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        player = _create_user(db, "player1")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Test")
        campaign_service.join_campaign(db, camp["id"], player)
        with pytest.raises(ConflictError, match="Already"):
            campaign_service.join_campaign(db, camp["id"], player)

    def test_leave_campaign(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        player = _create_user(db, "player1")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Test")
        campaign_service.join_campaign(db, camp["id"], player)
        result = campaign_service.leave_campaign(db, camp["id"], player)
        assert result["left"] is True

    def test_dm_cannot_leave(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Test")
        with pytest.raises(ForbiddenError, match="DM"):
            campaign_service.leave_campaign(db, camp["id"], dm)

    def test_archive_campaign(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Test")
        result = campaign_service.archive_campaign(db, camp["id"], dm)
        assert result["status"] == "archived"

    def test_archive_not_dm(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        player = _create_user(db, "player1")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Test")
        with pytest.raises(ForbiddenError):
            campaign_service.archive_campaign(db, camp["id"], player)


class TestSessionLogService:
    def test_create_session_log(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Test")
        log = session_log_service.create_session_log(
            db, campaign_id=camp["id"], author_id=dm,
            session_number=1, title="The Beginning",
            summary="Heroes met at a tavern", session_date="2026-01-15",
        )
        assert log["title"] == "The Beginning"
        assert log["session_number"] == 1

    def test_list_session_logs(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Test")
        session_log_service.create_session_log(
            db, campaign_id=camp["id"], author_id=dm,
            session_number=1, title="Session 1", session_date="2026-01-15",
        )
        session_log_service.create_session_log(
            db, campaign_id=camp["id"], author_id=dm,
            session_number=2, title="Session 2", session_date="2026-01-22",
        )
        logs = session_log_service.list_session_logs(db, camp["id"])
        assert len(logs) == 2

    def test_non_member_cannot_create(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm1", "dm")
        outsider = _create_user(db, "outsider")
        camp = campaign_service.create_campaign(db, dm_id=dm, name="Test")
        with pytest.raises(ForbiddenError):
            session_log_service.create_session_log(
                db, campaign_id=camp["id"], author_id=outsider,
                session_number=1, title="Nope", session_date="2026-01-15",
            )


class TestDiceService:
    def test_roll_basic(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        result = dice_service.roll(db, user_id=uid, expression="1d20")
        assert "results" in result
        assert "total" in result
        assert 1 <= result["total"] <= 20

    def test_roll_with_modifier(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        result = dice_service.roll(db, user_id=uid, expression="2d6+3")
        assert len(result["results"]) == 2
        assert result["total"] == sum(result["results"]) + 3

    def test_roll_invalid(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        with pytest.raises(ValidationError):
            dice_service.roll(db, user_id=uid, expression="banana")

    def test_roll_history(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        dice_service.roll(db, user_id=uid, expression="1d20")
        dice_service.roll(db, user_id=uid, expression="2d6+3")
        history = dice_service.get_history(db, uid)
        assert len(history) == 2

    def test_roll_no_save(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        result = dice_service.roll(db, user_id=uid, expression="1d20", save=False)
        assert "id" not in result or result.get("id") == 0
        history = dice_service.get_history(db, uid)
        assert len(history) == 0
