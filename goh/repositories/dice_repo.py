"""Dice roll repository — raw SQL data access."""

from __future__ import annotations

import json
import sqlite3

from goh.domain.entities.dice import DiceRoll


def save(
    db: sqlite3.Connection,
    *,
    user_id: int,
    expression: str,
    results: list[int],
    total: int,
    campaign_id: int | None = None,
) -> DiceRoll:
    cursor = db.execute(
        "INSERT INTO dice_rolls (user_id, expression, results, total, campaign_id) VALUES (?, ?, ?, ?, ?)",
        (user_id, expression, json.dumps(results), total, campaign_id),
    )
    db.commit()
    roll_id = cursor.lastrowid
    row = db.execute("SELECT * FROM dice_rolls WHERE id = ?", (roll_id,)).fetchone()
    assert row is not None
    return DiceRoll.from_row(row)


def history(
    db: sqlite3.Connection, user_id: int, limit: int = 20, campaign_id: int | None = None
) -> list[DiceRoll]:
    if campaign_id is not None:
        rows = db.execute(
            "SELECT * FROM dice_rolls WHERE user_id = ? AND campaign_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, campaign_id, limit),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM dice_rolls WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    return [DiceRoll.from_row(r) for r in rows]
