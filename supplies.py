from __future__ import annotations


SUPPLY_PRICES = {
    "bandages": 2.00,
    "water": 1.50,
    "batteries": 3.25,
    "blankets": 4.75,
    "medkits": 12.00,
}


def calculate_supply_cost(order):
    """Return the total cost of a RescueBot supply order.

    Args:
        order: A list of (supply_name, quantity) pairs.

    Return None if any requested supply name is not in
    SUPPLY_PRICES. Otherwise return the numeric total cost.
    """
    total = 0.0
    for supply_name, quantity in order:
        if supply_name not in SUPPLY_PRICES:
            return None
        total += SUPPLY_PRICES[supply_name] * quantity
    return total
