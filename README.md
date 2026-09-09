# Rescue Robot Project 0

This is the Python warmup for the Rescue Robot project series. It covers
addition, loops, dictionaries, supply costs, and route selection. The four
functions are complete. The project is worth 10 points, with 2.5 points
for each question.

The assignment is described on the [course project page](https://sites.wustl.edu/amtabakhi/project0/).

## Branches

- `main` has the complete project, including the helper class and local tests.
- `submission` has only `warmup.py`, `supplies.py`, and `dispatch.py`.
  Choose this branch when submitting through GitHub in Gradescope.

Use `main` when you want to run the project on your computer. The
`submission` branch leaves out the support files because Gradescope
provides them.

## Files

| File | What it contains |
| --- | --- |
| `warmup.py` | Q1: adding two values |
| `supplies.py` | Q2: calculating the cost of a supply order |
| `dispatch.py` | Q3: choosing a supply station; Q4: choosing a rescue route |
| `stations.py` | The original `SupplyStation` helper class |
| `autograder.py` | The original local autograder and public tests |
| `README.md` | Setup, assignment details, and submission instructions |

The `.gitignore` file keeps Python cache files and generated test results
out of the repository. The helper class and autograder are unchanged
from the starter ZIP.

## Get started

The course uses Python 3.13. The autograder also supports Python 3.10 and
later. No external packages are needed.

Clone the repository and open its folder:

```bash
git clone https://github.com/ghoshsaurav/rescue-robot.git
cd rescue-robot
```

Check your Python version and run the tests:

```bash
python3.13 --version
python3.13 autograder.py
```

On Windows, you can use the Python launcher instead:

```powershell
py -3.13 --version
py -3.13 autograder.py
```

If your supported Python installation uses the command `python`, replace
`python3.13` with `python` in these commands.

## What each function does

**Q1: `add(a, b)`** returns `a + b`. It returns the result to the caller
instead of printing it.

**Q2: `calculate_supply_cost(order)`** reads a list of
`(supply_name, quantity)` pairs. It multiplies each quantity by the price
in `SUPPLY_PRICES` and adds the costs. It returns `None` if any requested
supply is unavailable.

**Q3: `choose_best_station(order, stations)`** calls
`station.get_order_cost(order)` for each station. It skips stations that
return `None` and returns the station with the lowest cost. If costs tie,
the first station wins. It returns `None` if no station can fill the order.

**Q4: `choose_rescue_route(routes, battery_limit)`** reads route
dictionaries with `name`, `cost`, `survivors`, and `risk` keys. It skips
routes whose cost exceeds the battery limit. For each remaining route,
it calculates:

```text
survivors * 10 - risk
```

The highest score wins. If scores tie, the lower cost wins. If both are
equal, the first route wins. The function returns the winning route
dictionary, or `None` if no route fits the battery limit.

## Run the tests

Run every question with `python3.13 autograder.py`, or choose one question:

```bash
python3.13 autograder.py -q q1
python3.13 autograder.py -q q2
python3.13 autograder.py -q q3
python3.13 autograder.py -q q4
```

The autograder prints the result of each test and writes `results.json`.
That file is generated locally and should not be submitted. Passing the
public tests does not guarantee a particular Gradescope result.

If a test fails, its question number points to the function to check:

| Failed tests | What to check |
| --- | --- |
| Q1.1-Q1.5 | Return the computed value from `add`. |
| Q2.1-Q2.7 | Count every order item and return `None` for unknown supplies. |
| Q3.1-Q3.7 | Skip incomplete stations and keep the first station on a cost tie. |
| Q4.1-Q4.7 | Check the battery limit, then score, cost, and input order. |

## Submit to Gradescope

For a GitHub submission, select `ghoshsaurav/rescue-robot` and choose the
`submission` branch. This branch contains exactly the three required files.

For a file upload, select only:

```text
warmup.py
supplies.py
dispatch.py
```

Follow the course page and upload the individual files. Do not upload the
whole project, the ZIP, support files, or `results.json`.

If you edit a solution on `main` later, run the tests and copy the updated
solution files to `submission` before submitting again. Changes on one
branch do not automatically update the other.

## Course collaboration rules

The course allows students to discuss Python syntax, error messages, and
assignment instructions with classmates. Submitted code must be the
student's own work, and the student must understand every line.
