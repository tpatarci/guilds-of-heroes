"""Unit tests for dice expression parser."""

from __future__ import annotations

import pytest

from goh.domain.entities.dice import parse_and_roll


class TestDiceParser:
    def test_basic_d20(self) -> None:
        results, total = parse_and_roll("1d20")
        assert len(results) == 1
        assert 1 <= results[0] <= 20
        assert total == results[0]

    def test_multiple_dice(self) -> None:
        results, total = parse_and_roll("4d6")
        assert len(results) == 4
        assert all(1 <= r <= 6 for r in results)
        assert total == sum(results)

    def test_with_positive_modifier(self) -> None:
        results, total = parse_and_roll("2d6+3")
        assert len(results) == 2
        assert total == sum(results) + 3

    def test_with_negative_modifier(self) -> None:
        results, total = parse_and_roll("1d8-2")
        assert len(results) == 1
        assert total == results[0] - 2

    def test_case_insensitive(self) -> None:
        results, total = parse_and_roll("1D20")
        assert len(results) == 1

    def test_invalid_expression(self) -> None:
        with pytest.raises(ValueError, match="Invalid"):
            parse_and_roll("not_dice")

    def test_too_many_dice(self) -> None:
        with pytest.raises(ValueError, match="1-100"):
            parse_and_roll("101d6")

    def test_die_too_large(self) -> None:
        with pytest.raises(ValueError, match="2-100"):
            parse_and_roll("1d101")

    def test_d1_invalid(self) -> None:
        with pytest.raises(ValueError, match="2-100"):
            parse_and_roll("1d1")

    def test_zero_dice(self) -> None:
        with pytest.raises(ValueError, match="1-100"):
            parse_and_roll("0d6")

    def test_spaces_stripped(self) -> None:
        results, total = parse_and_roll(" 1d20 ")
        assert len(results) == 1
