from __future__ import annotations


class SupplyStation:
    """A small helper object used by Project 0 dispatch tests."""

    def __init__(self, name, prices):
        self.name = name
        self.prices = dict(prices)

    def get_name(self):
        return self.name

    def get_cost_per_unit(self, supply_name):
        return self.prices.get(supply_name)

    def get_order_cost(self, order):
        total = 0.0
        for supply_name, quantity in order:
            unit_cost = self.get_cost_per_unit(supply_name)
            if unit_cost is None:
                return None
            total += unit_cost * quantity
        return total

    def __repr__(self):
        return f"<SupplyStation: {self.name}>"
