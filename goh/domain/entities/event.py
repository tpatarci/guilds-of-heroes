"""Event and RSVP domain entities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    id: int
    organizer_id: int
    title: str
    description: str = ""
    event_type: str = "one_shot"
    location: str | None = None
    start_time: str = ""
    end_time: str | None = None
    min_players: int = 1
    max_players: int | None = None
    status: str = "upcoming"
    campaign_id: int | None = None
    created_at: str = ""
    updated_at: str = ""
    # Joined
    organizer_username: str = ""

    @staticmethod
    def from_row(row: dict) -> Event:
        return Event(
            id=row["id"],
            organizer_id=row["organizer_id"],
            title=row["title"],
            description=row.get("description", ""),
            event_type=row.get("event_type", "one_shot"),
            location=row.get("location"),
            start_time=row.get("start_time", ""),
            end_time=row.get("end_time"),
            min_players=row.get("min_players", 1),
            max_players=row.get("max_players"),
            status=row.get("status", "upcoming"),
            campaign_id=row.get("campaign_id"),
            created_at=row.get("created_at", ""),
            updated_at=row.get("updated_at", ""),
            organizer_username=row.get("organizer_username", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "organizer_id": self.organizer_id,
            "organizer_username": self.organizer_username,
            "title": self.title,
            "description": self.description,
            "event_type": self.event_type,
            "location": self.location,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "min_players": self.min_players,
            "max_players": self.max_players,
            "status": self.status,
            "campaign_id": self.campaign_id,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class RSVP:
    id: int
    event_id: int
    user_id: int
    status: str = "going"
    created_at: str = ""
    # Joined
    username: str = ""
    display_name: str = ""

    @staticmethod
    def from_row(row: dict) -> RSVP:
        return RSVP(
            id=row["id"],
            event_id=row["event_id"],
            user_id=row["user_id"],
            status=row.get("status", "going"),
            created_at=row.get("created_at", ""),
            username=row.get("username", ""),
            display_name=row.get("display_name", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "status": self.status,
            "username": self.username,
            "display_name": self.display_name,
            "created_at": self.created_at,
        }
