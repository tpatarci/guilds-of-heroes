"""Character domain entity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Character:
    id: int
    owner_id: int
    name: str
    race: str = "Human"
    char_class: str = "Fighter"
    level: int = 1
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    hit_points: int = 10
    armor_class: int = 10
    backstory: str = ""
    portrait: str | None = None
    campaign_id: int | None = None
    created_at: str = ""
    updated_at: str = ""

    @staticmethod
    def from_row(row: dict) -> Character:
        return Character(
            id=row["id"],
            owner_id=row["owner_id"],
            name=row["name"],
            race=row.get("race", "Human"),
            char_class=row.get("class", "Fighter"),
            level=row.get("level", 1),
            strength=row.get("strength", 10),
            dexterity=row.get("dexterity", 10),
            constitution=row.get("constitution", 10),
            intelligence=row.get("intelligence", 10),
            wisdom=row.get("wisdom", 10),
            charisma=row.get("charisma", 10),
            hit_points=row.get("hit_points", 10),
            armor_class=row.get("armor_class", 10),
            backstory=row.get("backstory", ""),
            portrait=row.get("portrait"),
            campaign_id=row.get("campaign_id"),
            created_at=row.get("created_at", ""),
            updated_at=row.get("updated_at", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "name": self.name,
            "race": self.race,
            "class": self.char_class,
            "level": self.level,
            "ability_scores": {
                "strength": self.strength,
                "dexterity": self.dexterity,
                "constitution": self.constitution,
                "intelligence": self.intelligence,
                "wisdom": self.wisdom,
                "charisma": self.charisma,
            },
            "hit_points": self.hit_points,
            "armor_class": self.armor_class,
            "backstory": self.backstory,
            "portrait": self.portrait,
            "campaign_id": self.campaign_id,
            "created_at": self.created_at,
        }
