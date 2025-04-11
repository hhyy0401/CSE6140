import time

def greedy_cover(universe, subsets):
    uncovered = universe.copy()
    cover = []
    while uncovered:
        best_subset = max(subsets, key=lambda s: len(s & uncovered))
        cover.append(best_subset)
        uncovered -= best_subset
    return cover

def is_cover(universe, cover):
    return set().union(*cover) == universe


def prune_cover(cover_indices, subsets, universe):
    pruned = cover_indices.copy()
    for idx in cover_indices:
        temp = pruned.copy()
        temp.remove(idx)
        temp_sets = [subsets[i] for i in temp]
        if is_cover(universe, temp_sets):
            pruned = temp
    return pruned

def hill_climbing_min_set_cover(universe, subsets, cutoff_time):
    start_time = time.time()

    greedy_solution = greedy_cover(universe, subsets)
    current_cover = [subsets.index(s) for s in greedy_solution]  

    improved = True

    history = []
    history.append((round(time.time() - start_time, 2), len(current_cover))) 

    while improved and time.time() - start_time < cutoff_time:
        improved = False
        for s_out_idx in current_cover:
            for s_in_idx in range(len(subsets)):
                if s_in_idx not in current_cover:
                    
                    new_cover = current_cover.copy()
                    new_cover.remove(s_out_idx)
                    new_cover.append(s_in_idx)

                    candidate_sets = [subsets[idx] for idx in new_cover]
                    if is_cover(universe, candidate_sets):

                        pruned_cover = prune_cover(new_cover, subsets, universe)

                        if len(pruned_cover) < len(current_cover):
                            current_cover = pruned_cover
                            improved = True
                            elapsed = round(time.time() - start_time, 2)
                            history.append((elapsed, len(current_cover))) 
                            break
            if improved:
                break

    return sorted(current_cover), history