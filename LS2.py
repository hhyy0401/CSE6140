import time
import numpy as np
import random

def greedy_cover(universe, subsets):
    uncovered = set(universe)
    cover_indices = []
    subset_indices = list(range(len(subsets)))

    while uncovered:
        best_idx = max(subset_indices, key=lambda i: len(uncovered & subsets[i]))
        cover_indices.append(best_idx)
        uncovered -= subsets[best_idx]

    return cover_indices

def random_cover(universe, subsets):
    uncovered = set(universe)
    cover_indices = []
    subset_indices = list(range(len(subsets)))

    while uncovered:
        valid_indices = [i for i in subset_indices if subsets[i] & uncovered]
        if not valid_indices:
            break 

        chosen_idx = random.choice(valid_indices)
        cover_indices.append(chosen_idx)
        uncovered -= subsets[chosen_idx]

    return cover_indices

def hill_climbing_min_set_cover(universe, subsets, cutoff_time):
    start_time = time.time()
    n = len(universe)

    element_to_subsets = {e: [] for e in universe}
    for idx, s in enumerate(subsets):
        for e in s:
            element_to_subsets[e].append(idx)

    #current_cover = greedy_cover(universe, subsets)
    current_cover = random_cover(universe, subsets)

    # Build count table
    count_table = np.zeros(n, dtype=int)
    for idx in current_cover:
        for e in subsets[idx]:
            count_table[e-1] += 1

    history = [(round(time.time() - start_time, 2), len(current_cover))]
    # cover_idx = random.choice(current_cover)
    #cover_idx = min(current_cover, key=lambda idx: len(subsets[idx]))
   
    tabu_set = set()  

    while time.time() - start_time < cutoff_time:

        cover_idx = random.choice(current_cover)
        if cover_idx in tabu_set:
            continue

        cover_set = subsets[cover_idx]
        neighbor_indices = set()
        for e in cover_set:
            neighbor_indices.update(element_to_subsets[e])
        neighbor_indices -= set(current_cover)
        neighbor_indices.discard(cover_idx)

        sorted_neighbors = sorted(neighbor_indices, key=lambda i: len(subsets[i]), reverse=True)
        improved = False

        for new_idx in sorted_neighbors:

            temp_count = count_table.copy()

            for e in subsets[cover_idx]:
                temp_count[e - 1] -= 1
            for e in subsets[new_idx]:
                temp_count[e - 1] += 1

            if np.all(temp_count > 0):
                current_cover.remove(cover_idx)
                current_cover.append(new_idx)
                count_table = temp_count
                improved = True

                tabu_set.add(cover_idx)
                tabu_set.add(new_idx)

                to_remove = []
                reduced = False
                for idx in current_cover:
                    temp_count = count_table.copy()
                    for e in subsets[idx]:
                        temp_count[e - 1] -= 1
                    if np.all(temp_count > 0):
                        count_table = temp_count
                        to_remove.append(idx)
                        reduced = True

                for idx in to_remove:
                    current_cover.remove(idx)

                if reduced:
                    elapsed = round(time.time() - start_time, 2)
                    history.append((elapsed, len(current_cover)))
                    break

        if not improved:
            continue
    return sorted(current_cover), history