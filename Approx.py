import sys
import time
import argparse

def read_instance(filename):
    """Read the instance from the given file."""
    with open(filename, 'r') as f:
        n, m = map(int, f.readline().strip().split())
        subsets = []
        for _ in range(m):
            line = list(map(int, f.readline().strip().split()))
            size = line[0]
            subset = set(line[1:size+1])
            subsets.append(subset)
    
    universe = set(range(1, n+1))
    return universe, subsets

def greedy_set_cover(universe, subsets):
    """
    Implements a greedy approximation algorithm for the Minimum Set Cover problem.
    
    Args:
        universe: A set of all elements (the universe U)
        subsets: A list of sets, where each set is a subset of the universe
    
    Returns:
        A list of indices of the chosen subsets (0-indexed)
    """
    start_time = time.time()
    # Elements that still need to be covered
    elements_remaining = set(universe)
    
    # Indices of the chosen subsets (0-indexed)
    solution = []
    
    # Continue until all elements are covered
    while elements_remaining:
        # Find the subset that covers the most uncovered elements
        best_subset_index = -1
        best_subset_coverage = -1
        
        for i, subset in enumerate(subsets):
            # Skip if this subset is already in our solution
            if i in solution:
                continue
            
            # Calculate how many new elements this subset would cover
            coverage = len(subset.intersection(elements_remaining))
            
            if coverage > best_subset_coverage:
                best_subset_coverage = coverage
                best_subset_index = i
        
        # If we found a subset that covers some remaining elements
        if best_subset_coverage > 0:
            # Add the best subset to our solution
            solution.append(best_subset_index)
            # Remove the covered elements
            elements_remaining -= subsets[best_subset_index]
        else:
            # This should not happen if the problem instance is valid
            # (i.e., if all elements can be covered by the given subsets)
            break
    
    timeSpent = round(time.time() - start_time,2)
    
    return solution, timeSpent

def write_solution(filename, algorithm, cutoff_time, seed, solution_indices, subsets):
    """Write the solution to the output file."""
    # Convert to 1-indexed for output
    one_indexed_solution = [i + 1 for i in solution_indices]
    
    # Format the output filename
    if algorithm in ['LS1', 'LS2']:
        output_filename = f"{filename}_{algorithm}_{cutoff_time}_{seed}.sol"
    else:
        output_filename = f"{filename}_{algorithm}_{cutoff_time}.sol"
    
    with open(output_filename, 'w') as f:
        # Write the quality (number of sets used)
        f.write(f"{len(solution_indices)}\n")
        
        # Write the indices of selected subsets
        f.write(' '.join(map(str, one_indexed_solution)))

def main():
    
    parser = argparse.ArgumentParser(description='Minimum Set Cover Solver')
    parser.add_argument('-inst', type=str, required=True, help='Instance file path')
    parser.add_argument('-alg', type=str, required=True, choices=['BnB', 'Approx', 'LS1', 'LS2'], 
                        help='Algorithm to use')
    parser.add_argument('-time', type=int, required=True, help='Cutoff time in seconds')
    parser.add_argument('-seed', type=int, required=True, help='Random seed')
    
    args = parser.parse_args()
    
    # Extract the base filename without path and extension
    filename = args.inst.split('/')[-1]
    if '.' in filename:
        filename = filename.split('.')[0]
    
    # Read the instance
    universe, subsets = read_instance(args.inst)
    
    start_time = time.time()
    
    
    if args.alg == 'Approx':
        # Run the approximation algorithm
        solution_indices = greedy_set_cover(universe, subsets)
        
        # Write the solution
        write_solution(filename, args.alg, args.time, args.seed, solution_indices, subsets)
        
        print(filename)
    else:
        print(f"Algorithm {args.alg} is not implemented in this script.")
        sys.exit(1)
    
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")
    
    
if __name__ == "__main__":
    main()