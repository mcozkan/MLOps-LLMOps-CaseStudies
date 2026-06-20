"""Command line entrypoint for the Docker image."""

from app import calculate_discounted_price


def main() -> None:
    """Run a tiny demo and exit successfully."""
    price = 250.0
    discount = 20.0
    final_price = calculate_discounted_price(price, discount)
    print(f"Original price: {price}")
    print(f"Discount: {discount}%")
    print(f"Final price: {final_price}")


if __name__ == "__main__":
    main()
