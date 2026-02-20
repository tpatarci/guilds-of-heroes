"""Notification domain entity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    id: int
    user_id: int
    type: str
    title: str
    body: str = ""
    link: str | None = None
    is_read: bool = False
    source_user_id: int | None = None
    created_at: str = ""

    @staticmethod
    def from_row(row: dict) -> Notification:
        return Notification(
            id=row["id"],
            user_id=row["user_id"],
            type=row["type"],
            title=row["title"],
            body=row.get("body", ""),
            link=row.get("link"),
            is_read=bool(row.get("is_read", 0)),
            source_user_id=row.get("source_user_id"),
            created_at=row.get("created_at", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "title": self.title,
            "body": self.body,
            "link": self.link,
            "is_read": self.is_read,
            "source_user_id": self.source_user_id,
            "created_at": self.created_at,
        }
