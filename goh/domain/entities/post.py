"""Post domain entity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Post:
    id: int
    author_id: int
    content: str
    post_type: str = "text"
    image_url: str | None = None
    created_at: str = ""
    updated_at: str = ""
    # Joined fields
    author_username: str = ""
    author_display_name: str = ""
    author_avatar: str | None = None

    @staticmethod
    def from_row(row: dict) -> Post:
        return Post(
            id=row["id"],
            author_id=row["author_id"],
            content=row["content"],
            post_type=row.get("post_type", "text"),
            image_url=row.get("image_url"),
            created_at=row.get("created_at", ""),
            updated_at=row.get("updated_at", ""),
            author_username=row.get("author_username", ""),
            author_display_name=row.get("author_display_name", ""),
            author_avatar=row.get("author_avatar"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "author_id": self.author_id,
            "content": self.content,
            "post_type": self.post_type,
            "image_url": self.image_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "author": {
                "username": self.author_username,
                "display_name": self.author_display_name,
                "avatar": self.author_avatar,
            },
        }
