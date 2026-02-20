"""Integration tests for social services — posts, follows, notifications, users."""

from __future__ import annotations

import sqlite3

import pytest

from goh.domain.exceptions import ForbiddenError, NotFoundError, ValidationError
from goh.repositories import user_repo
from goh.services import follow_service, notification_service, post_service, user_service


def _create_user(db: sqlite3.Connection, username: str = "testuser") -> int:
    user = user_repo.create(
        db, username=username, email=f"{username}@test.com",
        password_hash="fakehash", display_name=username.title(),
    )
    return user.id


class TestPostService:
    def test_create_post(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        post = post_service.create_post(db, author_id=uid, content="Hello D&D world!")
        assert post["content"] == "Hello D&D world!"
        assert post["author"]["username"] == "testuser"

    def test_create_post_empty_content(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        with pytest.raises(ValidationError, match="empty"):
            post_service.create_post(db, author_id=uid, content="  ")

    def test_list_posts(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        post_service.create_post(db, author_id=uid, content="Post 1")
        post_service.create_post(db, author_id=uid, content="Post 2")
        posts = post_service.list_posts(db, uid)
        assert len(posts) == 2

    def test_get_post(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        created = post_service.create_post(db, author_id=uid, content="Test")
        fetched = post_service.get_post(db, created["id"])
        assert fetched["id"] == created["id"]

    def test_get_post_not_found(self, db: sqlite3.Connection) -> None:
        with pytest.raises(NotFoundError):
            post_service.get_post(db, 9999)

    def test_delete_post(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        post = post_service.create_post(db, author_id=uid, content="To delete")
        post_service.delete_post(db, post["id"], uid)
        with pytest.raises(NotFoundError):
            post_service.get_post(db, post["id"])

    def test_delete_post_forbidden(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "user1")
        uid2 = _create_user(db, "user2")
        post = post_service.create_post(db, author_id=uid1, content="My post")
        with pytest.raises(ForbiddenError):
            post_service.delete_post(db, post["id"], uid2)

    def test_feed(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "alice")
        uid2 = _create_user(db, "bob")
        uid3 = _create_user(db, "charlie")

        # Alice follows Bob
        follow_service.follow_user(db, uid1, uid2)

        post_service.create_post(db, author_id=uid2, content="Bob's post")
        post_service.create_post(db, author_id=uid3, content="Charlie's post")
        post_service.create_post(db, author_id=uid1, content="Alice's post")

        feed = post_service.get_feed(db, uid1)
        # Feed should contain Bob's and Alice's own posts, but not Charlie's
        authors = {p["author"]["username"] for p in feed}
        assert "bob" in authors
        assert "alice" in authors
        assert "charlie" not in authors

    def test_timeline(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "user1")
        uid2 = _create_user(db, "user2")
        post_service.create_post(db, author_id=uid1, content="Post 1")
        post_service.create_post(db, author_id=uid2, content="Post 2")
        timeline = post_service.get_timeline(db)
        assert len(timeline) == 2


class TestFollowService:
    def test_follow_and_unfollow(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "alice")
        uid2 = _create_user(db, "bob")

        follow_service.follow_user(db, uid1, uid2)
        assert follow_service.check_following(db, uid1, uid2) is True

        follow_service.unfollow_user(db, uid1, uid2)
        assert follow_service.check_following(db, uid1, uid2) is False

    def test_follow_self(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        with pytest.raises(ValidationError, match="yourself"):
            follow_service.follow_user(db, uid, uid)

    def test_follow_nonexistent(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        with pytest.raises(NotFoundError):
            follow_service.follow_user(db, uid, 9999)

    def test_follow_creates_notification(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "alice")
        uid2 = _create_user(db, "bob")
        follow_service.follow_user(db, uid1, uid2)

        notifs = notification_service.list_notifications(db, uid2)
        assert len(notifs) == 1
        assert notifs[0]["type"] == "follow"

    def test_followers_following_lists(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "alice")
        uid2 = _create_user(db, "bob")
        uid3 = _create_user(db, "charlie")

        follow_service.follow_user(db, uid1, uid2)
        follow_service.follow_user(db, uid3, uid2)

        followers = follow_service.get_followers(db, uid2)
        assert len(followers) == 2

        following = follow_service.get_following(db, uid1)
        assert len(following) == 1
        assert following[0]["username"] == "bob"


class TestNotificationService:
    def test_count_unread(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "alice")
        uid2 = _create_user(db, "bob")
        follow_service.follow_user(db, uid1, uid2)

        assert notification_service.count_unread(db, uid2) == 1

    def test_mark_read(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "alice")
        uid2 = _create_user(db, "bob")
        follow_service.follow_user(db, uid1, uid2)

        notifs = notification_service.list_notifications(db, uid2)
        notification_service.mark_read(db, notifs[0]["id"], uid2)
        assert notification_service.count_unread(db, uid2) == 0

    def test_mark_all_read(self, db: sqlite3.Connection) -> None:
        uid1 = _create_user(db, "alice")
        uid2 = _create_user(db, "bob")
        uid3 = _create_user(db, "charlie")
        follow_service.follow_user(db, uid1, uid2)
        follow_service.follow_user(db, uid3, uid2)

        assert notification_service.count_unread(db, uid2) == 2
        notification_service.mark_all_read(db, uid2)
        assert notification_service.count_unread(db, uid2) == 0


class TestUserService:
    def test_get_profile(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        profile = user_service.get_profile(db, uid)
        assert profile["username"] == "testuser"
        assert "followers_count" in profile

    def test_update_profile(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        result = user_service.update_profile(db, uid, display_name="New Name", bio="Adventurer")
        assert result["display_name"] == "New Name"
        assert result["bio"] == "Adventurer"

    def test_search_users(self, db: sqlite3.Connection) -> None:
        _create_user(db, "gandalf")
        _create_user(db, "aragorn")
        results = user_service.search_users(db, "gan")
        assert len(results) == 1
        assert results[0]["username"] == "gandalf"
