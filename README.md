#  AI Assignments 4 – Constraint Satisfaction Problems (CSP)

This repository contains implementations of **Constraint Satisfaction Problems (CSP)** using a common reusable backtracking solver in Python.

---

## Core — `csp.py`

All problems share a common CSP engine that provides:

- **`is_consistent(var, value, assignment, neighbors)`** — checks whether assigning a value to a variable violates any constraint with already-assigned neighbors.
- **`select_unassigned_variable(...)`** — implements the **MRV (Minimum Remaining Values)** heuristic, selecting the variable with the fewest legal values remaining.
- **`backtrack(variables, domain, neighbors, assignment)`** — recursive backtracking search that returns a complete valid assignment, or `None` if unsolvable.

---

## Problems

### 1. Australia Map Coloring — `Australia-CSP.py`

Colors the 7 states/territories of Australia using 3 colors (Red, Green, Blue) such that no two adjacent regions share the same color.

**Run:**
```bash
python3 Australia-CSP.py
```

**Output:**
```
Solution Found:

WA           → Red
NT           → Green
SA           → Blue
...
```

---

### 2. Telangana Map Coloring — `Telangana-CSP.py`

Colors all 33 districts of Telangana using 4 colors, then renders the result as a geographic map using `matplotlib` and a GeoJSON boundary file.

**Requirements:**
```bash
pip3 install matplotlib numpy
```

You also need the GeoJSON file at `telangana_docs/telangana_district.geojson`.

**Run:**
```bash
python3 Telangana-CSP.py
```

**Output:** A PNG map saved to `telangana_docs/telangana_csp_map.png`.

CSP-based map coloring of Telangana districts:
<p align="center">
  <img src="telangana_docs/telangana_csp_map.png" width="500"/>
</p>

---

### 3. Sudoku Solver — `Sudoku-CSP.py`

Solves a 9×9 Sudoku puzzle by modelling each cell as a CSP variable with domain `[1–9]`, subject to row, column, and 3×3 box constraints.

**Run:**
```bash
python3 Sudoku-CSP.py
```

**Output:**
```
Unsolved Sudoku:

5 3 . | . 7 . | . . .
...

Solved Sudoku:

5 3 4 | 6 7 8 | 9 1 2
...
```

To solve a different puzzle, edit the `board` list in `Sudoku-CSP.py` (use `0` for empty cells).

---

### 4. Cryptarithmetic — `crypt-analysis-CSP.py`

Solves the classic puzzle:

```
  TWO
+ TWO
-----
 FOUR
```

Each letter maps to a unique digit (0–9), with leading digits non-zero. The solver uses column-wise carry constraints in addition to the standard CSP engine.

**Run:**
```bash
python3 crypt-analysis-CSP.py
```

**Output:**
```
Cryptarithmetic CSP
Problem: TWO + TWO = FOUR

Letter Assignments:
 T = 7, W = 3, O = 4, F = 1, U = 4, R = 8

Verification:
 734 + 734 = 1468
```

> Note: This file defines its own `backtrack` that uses the cryptarithmetic constraint on top of the base CSP engine.

---

## How It Works

All problems follow the same pattern:

1. **Variables** — the things to assign (states, cells, letters).
2. **Domains** — the possible values for each variable.
3. **Neighbors** — which variables are constrained with each other.
4. **Backtracking** — the function tries values one by one, pruning branches that violate constraints early via `is_consistent`, and uses MRV to pick the most constrained variable next.
   
## Clone the repository to run 

**git clone https://github.com/adarsh684/AI-assignments-4.git**  
**cd AI-assignments-4**
