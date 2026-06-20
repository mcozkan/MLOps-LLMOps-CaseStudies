"""Small pricing helper application used for CI/CD homework."""


def calculate_discounted_price(price: float, discount_percent: float) -> float:
    """Return the final price after applying a percentage discount.

    Args:
        price: Original product price. Must be greater than or equal to 0.
        discount_percent: Discount percentage. Must be between 0 and 100.

    Returns:
        Discounted price rounded to two decimals.

    Raises:
        TypeError: If inputs are not int or float.
        ValueError: If price or discount_percent is outside the valid range.
    """
    if not isinstance(price, (int, float)):
        raise TypeError("price must be a number")

    if not isinstance(discount_percent, (int, float)):
        raise TypeError("discount_percent must be a number")

    if price < 0:
        raise ValueError("price must be greater than or equal to 0")

    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("discount_percent must be between 0 and 100")

    discounted_price = price * (1 - discount_percent / 100)
    return round(discounted_price, 2)
