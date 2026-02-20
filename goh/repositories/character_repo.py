"""Character repository — raw SQL data access."""

from __future__ import annotations

import sqlite3

from goh.domain.entities.character import Character


def create(
    db: sqlite3.Connection,
    *,
    owner_id: int,
    name: str,
    race: str = "Human",
    char_class: str = "Fighter",
    level: int = 1,
    strength: int = 10,
    dexterity: int = 10,
    constitution: int = 10,
    intelligence: int = 10,
    wisdom: int = 10,
    charisma: int = 10,
    hit_points: int = 10,
    armor_class: int = 10,
    backstory: str = "",
    campaign_id: int | None = None,
) -> Character:
    cursor = db.execute(
        """INSERT INTO characters
           (owner_id, name, race, class, level, strength, dexterity, constitution,
            intelligence, wisdom, charisma, hit_points, armor_class, backstory, campaign_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (owner_id, name, race, char_class, level, strength, dexterity, constitution,
         intelligence, wisdom, charisma, hit_points, armor_class, backstory, campaign_id),
    )
    db.commit()
    char = find_by_id(db, cursor.lastrowid)
    assert char is not None
    return char


def find_by_id(db: sqlite3.Connection, char_id: int | None) -> Character | None:
    row = db.execute("SELECT * FROM characters WHERE id = ?", (char_id,)).fetchone()
    return Character.from_row(row) if row else None


def list_by_owner(db: sqlite3.Connection, owner_id: int) -> list[Character]:
    rows = db.execute(
        "SELECT * FROM characters WHERE owner_id = ? ORDER BY created_at DESC", (owner_id,)
    ).fetchall()
    return [Character.from_row(r) for r in rows]


def list_by_campaign(db: sqlite3.Connection, campaign_id: int) -> list[Character]:
    rows = db.execute(
        "SELECT * FROM characters WHERE campaign_id = ? ORDER BY name", (campaign_id,)
    ).fetchall()
    return [Character.from_row(r) for r in rows]


def update(
    db: sqlite3.Connection, char_id: int, **fields: object
) -> None:
    allowed = {
        "name", "race", "class", "level", "strength", "dexterity", "constitution",
        "intelligence", "wisdom", "charisma", "hit_points", "armor_class", "backstory",
        "portrait", "campaign_id",
    }
    updates: list[str] = []
    params: list = []
    for key, val in fields.items():
        if key in allowed and val is not None:
            updates.append(f"[{key}] = ?")
            params.append(val)
    if not updates:
        return
    updates.append("updated_at = datetime('now')")
    params.append(char_id)
    db.execute(f"UPDATE characters SET {', '.join(updates)} WHERE id = ?", params)
    db.commit()


def delete(db: sqlite3.Connection, char_id: int) -> None:
    db.execute("DELETE FROM characters WHERE id = ?", (char_id,))
    db.commit()
