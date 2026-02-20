"""Dice roll domain entity and parser."""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class DiceRoll:
    id: int = 0
    user_id: int = 0
    expression: str = ""
    results: list[int] = field(default_factory=list)
    total: int = 0
    campaign_id: int | None = None
    created_at: str = ""

    @staticmethod
    def from_row(row: dict) -> DiceRoll:
        results = json.loads(row.get("results", "[]"))
        return DiceRoll(
            id=row["id"],
            user_id=row["user_id"],
            expression=row["expression"],
            results=results,
            total=row["total"],
            campaign_id=row.get("campaign_id"),
            created_at=row.get("created_at", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "expression": self.expression,
            "results": self.results,
            "total": self.total,
            "campaign_id": self.campaign_id,
            "created_at": self.created_at,
        }


# Dice expression pattern: NdM[+/-X] e.g. 2d6+3, 1d20, 4d8-2
_DICE_RE = re.compile(r"^(\d+)d(\d+)([+-]\d+)?$", re.IGNORECASE)


def parse_and_roll(expression: str) -> tuple[list[int], int]:
    """Parse a dice expression and roll. Returns (individual results, total).

    Supported: NdM, NdM+X, NdM-X
    Examples: 1d20, 2d6+3, 4d8-2
    """
    expression = expression.strip().lower().replace(" ", "")
    match = _DICE_RE.match(expression)
    if not match:
        raise ValueError(f"Invalid dice expression: {expression}")

    num_dice = int(match.group(1))
    die_size = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0

    if num_dice < 1 or num_dice > 100:
        raise ValueError("Number of dice must be 1-100")
    if die_size < 2 or die_size > 100:
        raise ValueError("Die size must be 2-100")

    results = [random.randint(1, die_size) for _ in range(num_dice)]
    total = sum(results) + modifier
    return results, total
