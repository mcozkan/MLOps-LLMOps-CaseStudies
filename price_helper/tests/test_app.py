"""Tests for the pricing helper."""

import pytest

from app import calculate_discounted_price


def test_calculate_discounted_price_regular_discount() -> None:
    assert calculate_discounted_price(100, 15) == 85.0


def test_calculate_discounted_price_rounds_to_two_decimals() -> None:
    assert calculate_discounted_price(99.99, 12.5) == 87.49


def test_calculate_discounted_price_zero_discount() -> None:
    assert calculate_discounted_price(120, 0) == 120.0


def test_calculate_discounted_price_invalid_discount_raises_error() -> None:
    with pytest.raises(ValueError, match="discount_percent must be between 0 and 100"):
        calculate_discounted_price(100, 150)


def test_calculate_discounted_price_invalid_type_raises_error() -> None:
    with pytest.raises(TypeError, match="price must be a number"):
        calculate_discounted_price("100", 10)
