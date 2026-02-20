"""Dice service — roll dice, save rolls, history."""

from __future__ import annotations

import sqlite3

import structlog

from goh.domain.entities.dice import parse_and_roll
from goh.domain.exceptions import ValidationError
from goh.observability.timing import timed
from goh.repositories import dice_repo

logger = structlog.get_logger(__name__)


@timed
def roll(
    db: sqlite3.Connection,
    *,
    user_id: int,
    expression: str,
    campaign_id: int | None = None,
    save: bool = True,
) -> dict:
    """Roll dice and optionally save the result."""
    try:
        results, total = parse_and_roll(expression)
    except ValueError as e:
        raise ValidationError(str(e)) from e

    logger.info(
        "dice.rolled", user_id=user_id, expression=expression,
        results=results, total=total,
    )

    if save:
        roll_record = dice_repo.save(
            db, user_id=user_id, expression=expression,
            results=results, total=total, campaign_id=campaign_id,
        )
        return roll_record.to_dict()

    return {
        "expression": expression,
        "results": results,
        "total": total,
    }


@timed
def get_history(
    db: sqlite3.Connection,
    user_id: int,
    limit: int = 20,
    campaign_id: int | None = None,
) -> list[dict]:
    rolls = dice_repo.history(db, user_id, limit, campaign_id)
    return [r.to_dict() for r in rolls]
