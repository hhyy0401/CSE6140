import random
import math
import time

def simulated_annealing(universe, subsets, cutoff_time=10, start_temp=100.0, cooling_rate=0.99, seed=0):
    random.seed(seed)
    start = time.time()

    current_solution = greedy_cover(universe, subsets)
    best_solution = current_solution[:]
    current_temp = start_temp

    trace = [(0.0, len(best_solution))]

    while time.time() - start < cutoff_time:
        neighbor = perturb_solution_idx(current_solution, subsets, universe)
        curr_cost = len(current_solution)
        neighbor_cost = len(neighbor)

        if neighbor_cost < curr_cost:
            current_solution = neighbor
            if neighbor_cost < len(best_solution):
                best_solution = neighbor
                trace.append((round(time.time() - start, 2), neighbor_cost))
        else:
            prob = math.exp(-(neighbor_cost - curr_cost) / current_temp)
            if random.random() < prob:
                current_solution = neighbor

        current_temp *= cooling_rate

    return best_solution, trace

def greedy_cover(universe, subsets):
    uncovered = set(universe)
    cover_indices = []
    subset_indices = list(range(len(subsets)))
    
    while uncovered:
        # Select the subset index that covers the most uncovered elements.
        best_idx = max(subset_indices, key=lambda i: len(uncovered & subsets[i]))
        cover_indices.append(best_idx)
        uncovered -= subsets[best_idx]
    return cover_indices

def perturb_solution_idx(solution, subsets, universe):
    new_solution = solution[:]
    if len(new_solution) > 1:
        new_solution.remove(random.choice(new_solution))
    
    covered = set()
    for idx in new_solution:
        covered |= subsets[idx]
    missing = set(universe) - covered

    all_indices = list(range(len(subsets)))
    while missing:
        best_idx = max(all_indices, key=lambda i: len(missing & subsets[i]))
        new_solution.append(best_idx)
        missing -= subsets[best_idx]
    return new_solution