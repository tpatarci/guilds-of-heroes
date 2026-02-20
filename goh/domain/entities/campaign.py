"""Campaign and session log domain entities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Campaign:
    id: int
    dm_id: int
    name: str
    description: str = ""
    status: str = "active"
    max_players: int = 6
    created_at: str = ""
    updated_at: str = ""
    dm_username: str = ""

    @staticmethod
    def from_row(row: dict) -> Campaign:
        return Campaign(
            id=row["id"],
            dm_id=row["dm_id"],
            name=row["name"],
            description=row.get("description", ""),
            status=row.get("status", "active"),
            max_players=row.get("max_players", 6),
            created_at=row.get("created_at", ""),
            updated_at=row.get("updated_at", ""),
            dm_username=row.get("dm_username", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "dm_id": self.dm_id,
            "dm_username": self.dm_username,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "max_players": self.max_players,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class SessionLog:
    id: int
    campaign_id: int
    author_id: int
    session_number: int
    title: str
    summary: str = ""
    session_date: str = ""
    created_at: str = ""
    author_username: str = ""

    @staticmethod
    def from_row(row: dict) -> SessionLog:
        return SessionLog(
            id=row["id"],
            campaign_id=row["campaign_id"],
            author_id=row["author_id"],
            session_number=row.get("session_number", 0),
            title=row["title"],
            summary=row.get("summary", ""),
            session_date=row.get("session_date", ""),
            created_at=row.get("created_at", ""),
            author_username=row.get("author_username", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "author_id": self.author_id,
            "author_username": self.author_username,
            "session_number": self.session_number,
            "title": self.title,
            "summary": self.summary,
            "session_date": self.session_date,
            "created_at": self.created_at,
        }
