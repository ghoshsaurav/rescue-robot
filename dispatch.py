from __future__ import annotations

from stations import SupplyStation


def choose_best_station(order, stations):
    """Return the SupplyStation that can fill the order most cheaply.

    Args:
        order: A list of (supply_name, quantity) pairs.
        stations: A list of SupplyStation objects.

    Ignore stations that cannot fill the complete order. If two
    stations tie, keep the station that appears earlier in the list.
    Return None if no station can fill the complete order.
    """
    best_station = None
    best_cost = None

    for station in stations:
        cost = station.get_order_cost(order)
        if cost is None:
            continue

        # Only a strictly lower cost replaces the first station on a tie.
        if best_station is None or cost < best_cost:
            best_station = station
            best_cost = cost

    return best_station


def choose_rescue_route(routes, battery_limit):
    """Return the best feasible route dictionary for RescueBot.

    Each route is a dictionary with these keys:
        name: route label
        cost: battery units needed
        survivors: survivor markers reached
        risk: risk estimate

    A route is feasible when cost <= battery_limit. Among feasible
    routes, maximize survivors * 10 - risk. If routes tie on that
    score, choose the one with lower cost. If they still tie, keep
    the route that appears earlier in the input list. Return None
    when no route is feasible.
    """
    best_route = None
    best_score = None

    for route in routes:
        if route["cost"] > battery_limit:
            continue

        score = route["survivors"] * 10 - route["risk"]
        if (
            best_route is None
            or score > best_score
            or (score == best_score and route["cost"] < best_route["cost"])
        ):
            best_route = route
            best_score = score

    return best_route
