from __future__ import annotations

import argparse
import importlib
import json
import math
import sys
import traceback
from pathlib import Path


TOTAL_POINTS = 10

CODE_CASE_POINTS = {
    "q1": 2.5 / 5,
    "q2": 2.5 / 7,
    "q3": 2.5 / 7,
    "q4": 2.5 / 7,
}


def format_points(value):
    value = float(value)
    if value.is_integer():
        return str(int(value))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def result(name, score, max_score, output=""):
    status = "passed" if score == max_score else "failed"
    return {
        "name": name,
        "score": score,
        "max_score": max_score,
        "status": status,
        "output": output,
    }


def make_case(qid, name, _max_score, fn):
    return {"qid": qid, "name": name, "max_score": CODE_CASE_POINTS[qid], "fn": fn}


def import_fresh(module_name):
    if module_name in sys.modules:
        return importlib.reload(sys.modules[module_name])
    return importlib.import_module(module_name)


def assert_close(actual, expected, label="value"):
    if not math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9):
        raise AssertionError(f"Expected {label} {expected!r}, got {actual!r}.")


def assert_equal(actual, expected, label="value"):
    if actual != expected:
        raise AssertionError(f"Expected {label} {expected!r}, got {actual!r}.")


def station_names(stations):
    return [station.get_name() for station in stations]


def build_tests():
    return [
        make_case("q1", "Q1.1 add positive integers", 1, lambda: assert_equal(import_fresh("warmup").add(1, 1), 2, "add(1, 1)")),
        make_case("q1", "Q1.2 add negative and positive numbers", 1, lambda: assert_equal(import_fresh("warmup").add(-3, 10), 7, "add(-3, 10)")),
        make_case("q1", "Q1.3 add floats", 1, lambda: assert_close(import_fresh("warmup").add(2.5, 0.75), 3.25, "add(2.5, 0.75)")),
        make_case("q1", "Q1.4 returns the computed value", 1, lambda: assert_equal(import_fresh("warmup").add(100, -40), 60, "add(100, -40)")),
        make_case("q1", "Q1.5 uses Python's plus operator behavior", 1, lambda: assert_equal(import_fresh("warmup").add("Rescue", "Bot"), "RescueBot", "add('Rescue', 'Bot')")),

        make_case("q2", "Q2.1 calculate a standard supply order", 1, test_q2_standard_order),
        make_case("q2", "Q2.2 handle repeated supplies", 1, test_q2_repeated_supplies),
        make_case("q2", "Q2.3 empty order costs zero", 1, test_q2_empty_order),
        make_case("q2", "Q2.4 unavailable supply returns None", 1, test_q2_unknown_supply),
        make_case("q2", "Q2.5 fractional quantities work", 1, test_q2_fractional_quantities),
        make_case("q2", "Q2.6 order list is not mutated", 1, test_q2_no_mutation),
        make_case("q2", "Q2.7 all provided supply names work", 1, test_q2_all_supplies),

        make_case("q3", "Q3.1 choose the cheaper station", 1, test_q3_cheaper_first),
        make_case("q3", "Q3.2 choose a later cheaper station", 1, test_q3_cheaper_later),
        make_case("q3", "Q3.3 keep first station on a tie", 1, test_q3_tie_keeps_first),
        make_case("q3", "Q3.4 skip stations missing a supply", 1, test_q3_skip_missing),
        make_case("q3", "Q3.5 return None if no station can fill the order", 1, test_q3_none_if_no_station),
        make_case("q3", "Q3.6 empty order chooses the first station", 1, test_q3_empty_order),
        make_case("q3", "Q3.7 station list is not mutated", 1, test_q3_no_mutation),

        make_case("q4", "Q4.1 choose the highest rescue score", 1, test_q4_highest_score),
        make_case("q4", "Q4.2 battery limit filters routes", 1, test_q4_battery_filter),
        make_case("q4", "Q4.3 score tie chooses lower cost", 1, test_q4_tie_lower_cost),
        make_case("q4", "Q4.4 full tie keeps first route", 1, test_q4_full_tie_first),
        make_case("q4", "Q4.5 no feasible route returns None", 1, test_q4_none_if_infeasible),
        make_case("q4", "Q4.6 zero-survivor route can still be feasible", 1, test_q4_zero_survivor_feasible),
        make_case("q4", "Q4.7 route list is not mutated", 1, test_q4_no_mutation),
    ]


def test_q2_standard_order():
    supplies = import_fresh("supplies")
    order = [("bandages", 2), ("water", 3), ("blankets", 1)]
    assert_close(supplies.calculate_supply_cost(order), 13.25, "standard order cost")


def test_q2_repeated_supplies():
    supplies = import_fresh("supplies")
    order = [("batteries", 2), ("batteries", 3)]
    assert_close(supplies.calculate_supply_cost(order), 16.25, "repeated batteries cost")


def test_q2_empty_order():
    supplies = import_fresh("supplies")
    assert_close(supplies.calculate_supply_cost([]), 0.0, "empty order cost")


def test_q2_unknown_supply():
    supplies = import_fresh("supplies")
    order = [("bandages", 2), ("solar panels", 1)]
    assert_equal(supplies.calculate_supply_cost(order), None, "unknown supply result")


def test_q2_fractional_quantities():
    supplies = import_fresh("supplies")
    order = [("water", 1.5), ("medkits", 0.5)]
    assert_close(supplies.calculate_supply_cost(order), 8.25, "fractional order cost")


def test_q2_no_mutation():
    supplies = import_fresh("supplies")
    order = [("bandages", 1), ("water", 2)]
    original = list(order)
    supplies.calculate_supply_cost(order)
    assert_equal(order, original, "order list after calculate_supply_cost")


def test_q2_all_supplies():
    supplies = import_fresh("supplies")
    order = [("bandages", 1), ("water", 1), ("batteries", 1), ("blankets", 1), ("medkits", 1)]
    assert_close(supplies.calculate_supply_cost(order), 23.5, "all supplies order cost")


def sample_stations():
    stations_mod = import_fresh("stations")
    return [
        stations_mod.SupplyStation("North Depot", {"bandages": 2.0, "water": 1.0, "batteries": 3.5}),
        stations_mod.SupplyStation("East Cache", {"bandages": 1.5, "water": 2.0, "batteries": 3.25, "blankets": 4.0}),
        stations_mod.SupplyStation("South Base", {"bandages": 2.0, "water": 1.0, "batteries": 4.0, "medkits": 10.0}),
    ]


def test_q3_cheaper_first():
    dispatch = import_fresh("dispatch")
    stations = sample_stations()
    order = [("bandages", 2), ("water", 2)]
    assert_equal(dispatch.choose_best_station(order, stations).get_name(), "North Depot", "best station name")


def test_q3_cheaper_later():
    dispatch = import_fresh("dispatch")
    stations = sample_stations()
    order = [("bandages", 2), ("blankets", 1)]
    assert_equal(dispatch.choose_best_station(order, stations).get_name(), "East Cache", "best station name")


def test_q3_tie_keeps_first():
    dispatch = import_fresh("dispatch")
    stations_mod = import_fresh("stations")
    stations = [
        stations_mod.SupplyStation("Alpha", {"water": 1.0}),
        stations_mod.SupplyStation("Beta", {"water": 1.0}),
    ]
    assert_equal(dispatch.choose_best_station([("water", 2)], stations).get_name(), "Alpha", "tie result")


def test_q3_skip_missing():
    dispatch = import_fresh("dispatch")
    stations = sample_stations()
    order = [("medkits", 1), ("water", 1)]
    assert_equal(dispatch.choose_best_station(order, stations).get_name(), "South Base", "station with complete order")


def test_q3_none_if_no_station():
    dispatch = import_fresh("dispatch")
    stations = sample_stations()
    assert_equal(dispatch.choose_best_station([("radio", 1)], stations), None, "no station result")


def test_q3_empty_order():
    dispatch = import_fresh("dispatch")
    stations = sample_stations()
    assert_equal(dispatch.choose_best_station([], stations).get_name(), "North Depot", "empty order station")


def test_q3_no_mutation():
    dispatch = import_fresh("dispatch")
    stations = sample_stations()
    original_names = station_names(stations)
    dispatch.choose_best_station([("bandages", 1)], stations)
    assert_equal(station_names(stations), original_names, "station order after choose_best_station")


def sample_routes():
    return [
        {"name": "atrium", "cost": 5, "survivors": 1, "risk": 1},
        {"name": "clinic", "cost": 8, "survivors": 2, "risk": 5},
        {"name": "loading-bay", "cost": 11, "survivors": 3, "risk": 2},
    ]


def test_q4_highest_score():
    dispatch = import_fresh("dispatch")
    assert_equal(dispatch.choose_rescue_route(sample_routes(), 12)["name"], "loading-bay", "best route")


def test_q4_battery_filter():
    dispatch = import_fresh("dispatch")
    assert_equal(dispatch.choose_rescue_route(sample_routes(), 8)["name"], "clinic", "best feasible route")


def test_q4_tie_lower_cost():
    dispatch = import_fresh("dispatch")
    routes = [
        {"name": "north", "cost": 9, "survivors": 2, "risk": 4},
        {"name": "east", "cost": 6, "survivors": 2, "risk": 4},
    ]
    assert_equal(dispatch.choose_rescue_route(routes, 10)["name"], "east", "lower-cost tie route")


def test_q4_full_tie_first():
    dispatch = import_fresh("dispatch")
    routes = [
        {"name": "alpha", "cost": 6, "survivors": 1, "risk": 0},
        {"name": "beta", "cost": 6, "survivors": 1, "risk": 0},
    ]
    assert_equal(dispatch.choose_rescue_route(routes, 10)["name"], "alpha", "full tie route")


def test_q4_none_if_infeasible():
    dispatch = import_fresh("dispatch")
    routes = [{"name": "long", "cost": 12, "survivors": 3, "risk": 1}]
    assert_equal(dispatch.choose_rescue_route(routes, 5), None, "no feasible route")


def test_q4_zero_survivor_feasible():
    dispatch = import_fresh("dispatch")
    routes = [
        {"name": "scan", "cost": 2, "survivors": 0, "risk": 0},
        {"name": "dash", "cost": 3, "survivors": 0, "risk": 2},
    ]
    assert_equal(dispatch.choose_rescue_route(routes, 4)["name"], "scan", "zero-survivor feasible route")


def test_q4_no_mutation():
    dispatch = import_fresh("dispatch")
    routes = sample_routes()
    original = [dict(route) for route in routes]
    dispatch.choose_rescue_route(routes, 12)
    assert_equal(routes, original, "routes after choose_rescue_route")


def run_case(case):
    try:
        case["fn"]()
    except Exception as exc:
        details = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        return result(case["name"], 0, case["max_score"], details)
    return result(case["name"], case["max_score"], case["max_score"], "passed")


def main():
    parser = argparse.ArgumentParser(description="Project 0 local autograder")
    parser.add_argument("-q", "--question", choices=["q1", "q2", "q3", "q4"], help="run only one question")
    parser.add_argument("--json-output", default="results.json", help="path for Gradescope-compatible results JSON")
    args = parser.parse_args()

    tests = build_tests()
    if args.question:
        tests = [case for case in tests if case["qid"] == args.question]

    results = [run_case(case) for case in tests]

    score = round(sum(item["score"] for item in results), 6)
    max_score = round(sum(item["max_score"] for item in results), 6)
    if not args.question:
        max_score = TOTAL_POINTS
    summary = f"Score: {format_points(score)} / {format_points(max_score)}"

    print(summary)
    for item in results:
        earned = format_points(item["score"])
        possible = format_points(item["max_score"])
        print(f"[{item['status']}] {item['name']}: {earned}/{possible}")
        if item["status"] != "passed" and item.get("output"):
            print(f"  {item['output']}")

    payload = {
        "score": score,
        "max_score": max_score,
        "output": summary,
        "tests": results,
    }
    Path(args.json_output).write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
