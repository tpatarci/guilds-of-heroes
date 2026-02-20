"""User domain entity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    username: str
    email: str
    display_name: str
    role: str = "player"  # player, dm, admin
    avatar: str | None = None
    bio: str = ""
    email_verified: bool = False
    created_at: str = ""
    updated_at: str = ""

    @staticmethod
    def from_row(row: dict) -> User:
        return User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            display_name=row["display_name"],
            role=row["role"],
            avatar=row.get("avatar"),
            bio=row.get("bio", ""),
            email_verified=bool(row.get("email_verified", 0)),
            created_at=row.get("created_at", ""),
            updated_at=row.get("updated_at", ""),
        )

    def to_public_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "display_name": self.display_name,
            "role": self.role,
            "avatar": self.avatar,
            "bio": self.bio,
            "created_at": self.created_at,
        }

    def to_private_dict(self) -> dict:
        d = self.to_public_dict()
        d["email"] = self.email
        d["email_verified"] = self.email_verified
        d["updated_at"] = self.updated_at
        return d
