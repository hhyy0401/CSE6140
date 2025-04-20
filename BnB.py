"""
BnB.py

Branch & Bound for Minimum Set Cover, seeded with an O(log n)-approximation
and pruned by the LP-relaxation lower bound at each node.

Exports:
    branch_and_bound_min_set_cover(universe, subsets, cutoff)

Requires:
    scipy.optimize.linprog
"""

import time
import math
import numpy as np
from scipy.optimize import linprog
from Approx import greedy_set_cover

# Globals for incumbent & tracing
best_solution = None  # list of 0-based subset indices
best_solution_size = float('inf')
trace_data = []  # (elapsed_sec, cover_size)
start_time = 0.0
cutoff_time = 0.0

# Lower bound: LP-relaxation
def fractional_lower_bound(uncovered, subsets):
    """
    Solve the LP-relaxation of set-cover on the uncovered elements.

    minimize   sum_j x_j
      s.t.     for each e in uncovered: sum_{j:e in S_j} x_j >= 1
               0 <= x_j <= 1

    Returns the LP optimal value (a fractional lower bound).
    Falls back to the trivial bound if LP fails.
    """
    m = len(subsets)
    # Map each uncovered element to a row index
    elems = list(uncovered)
    elem_index = {e: i for i, e in enumerate(elems)}
    num_rows = len(elems)

    # Build constraint matrix A_ub * x <= b_ub for Ax >= 1 → -A x <= -1
    A_ub = np.zeros((num_rows, m))
    for j, S in enumerate(subsets):
        for e in S:
            if e in elem_index:
                A_ub[elem_index[e], j] = -1.0

    b_ub = -np.ones(num_rows)
    c = np.ones(m)
    bounds = [(0, 1) for _ in range(m)]

    try:
        res = linprog(
            c,
            A_ub=A_ub, b_ub=b_ub,
            bounds=bounds,
            method='highs',
            options={'presolve': True}
        )
        if res.success:
            # res.fun is the fractional optimum
            return res.fun
    except Exception:
        pass

    # fallback: trivial bound
    if not uncovered:
        return 0
    max_cover = max(len(s) for s in subsets)
    return math.ceil(len(uncovered) / max_cover)


# Recursive Branch & Bound
def branch_and_bound(universe, subsets, current_cover, current_solution):
    global best_solution, best_solution_size, trace_data, start_time, cutoff_time

    # 1) Time cutoff
    if time.time() - start_time > cutoff_time:
        return

    # 2) Feasible check
    if current_cover == universe:
        if len(current_solution) < best_solution_size:
            best_solution_size = len(current_solution)
            best_solution = current_solution.copy()
            elapsed = round(time.time() - start_time, 2)
            trace_data.append((elapsed, best_solution_size))
        return

    # 3) LP-based pruning
    uncovered = universe - current_cover
    lb = fractional_lower_bound(uncovered, subsets)
    if len(current_solution) + lb >= best_solution_size:
        return

    # 4) Choose branching element: fewest covering subsets
    freq = {e: 0 for e in uncovered}
    for s in subsets:
        for e in s:
            if e in freq:
                freq[e] += 1
    e_min = min(uncovered, key=lambda e: freq[e])

    # 5) Branch on subsets covering e_min
    candidates = [j for j, s in enumerate(subsets) if e_min in s]
    # try those covering more of uncovered first
    candidates.sort(key=lambda j: len(subsets[j] & uncovered), reverse=True)

    for j in candidates:
        current_solution.append(j)
        branch_and_bound(
            universe, subsets,
            current_cover.union(subsets[j]),
            current_solution
        )
        current_solution.pop()


# Minimum Set Cover for BnB
def branch_and_bound_min_set_cover(universe, subsets, cutoff):
    """
    1) Run greedy_set_cover to get an initial upper bound.
    2) Log that incumbent.
    3) Recursively branch & bound using LP-relaxation pruning.
    """
    global best_solution, best_solution_size, trace_data, start_time, cutoff_time

    # reset
    best_solution = None
    best_solution_size = float('inf')
    trace_data = []
    start_time = time.time()
    cutoff_time = cutoff

    # --- INITIAL UPPER BOUND via Approximation ---
    approx_sol, approx_time = greedy_set_cover(universe, subsets)
    best_solution = approx_sol.copy()
    best_solution_size = len(approx_sol)
    trace_data.append((round(time.time() - start_time, 2), best_solution_size))

    # --- BRANCH & BOUND SEARCH ---
    branch_and_bound(universe, subsets, set(), [])

    return best_solution, trace_data
