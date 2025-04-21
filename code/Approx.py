"""
Approx.py - Minimum Set Cover Problem Solver

This script implements a solver for the Minimum Set Cover Problem (MSCP).
It reads problem instances from files, solves them using selected algorithms,
and outputs solutions to files.

-> Side Note: Other algorithm support is deprecated (another group mate made one at the same time)

The Minimum Set Cover Problem is a classic NP-hard optimization problem where:
- Given a universe U of elements and a collection S of subsets of U
- Find the smallest sub-collection of S such that the union of the subsets covers all elements in U

Usage:
    python set_cover_solver.py -inst <instance_file> -alg <algorithm> -time <cutoff_time> -seed <random_seed>

Arguments:
    -inst: Path to the problem instance file
    -alg: Algorithm to use (BnB, Approx, LS1, LS2)
    -time: Cutoff time in seconds
    -seed: Random seed for stochastic algorithms
"""
import sys
import time
import argparse

def read_instance(filename):
    """
    Read the Minimum Set Cover Problem instance from the given file.
    
    The file format is expected to be:
    - First line: n m (n = number of elements in universe, m = number of subsets)
    - Next m lines: size elem1 elem2 ... elemSize (each representing a subset)
    
    Args:
        filename (str): Path to the instance file
        
    Returns:
        tuple: (universe, subsets)
            - universe: A set of all elements (integers from 1 to n)
            - subsets: A list of sets, where each set is a subset of the universe
    """
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
    
    The greedy algorithm works as follows:
    1. Start with an empty solution and the complete set of uncovered elements
    2. In each iteration, choose the subset that covers the most uncovered elements
    3. Add this subset to the solution and remove the newly covered elements
    4. Repeat until all elements are covered
    
    This is a polynomial-time algorithm that achieves an approximation ratio of H(d),
    where H(d) is the d-th harmonic number and d is the size of the largest subset.
    In the worst case, this gives an O(log n) approximation.
    
    Args:
        universe (set): A set of all elements (the universe U)
        subsets (list): A list of sets, where each set is a subset of the universe
    
    Returns:
        tuple: (solution, time_spent)
            - solution: A list of indices of the chosen subsets (0-indexed)
            - time_spent: The time spent executing the algorithm, in seconds
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
            # by finding the intersection with remaining uncovered elements
            coverage = len(subset.intersection(elements_remaining))
            
            if coverage > best_subset_coverage:
                best_subset_coverage = coverage
                best_subset_index = i
        
        # If we found a subset that covers some remaining elements
        if best_subset_coverage > 0:
            # Add the best subset to our solution
            solution.append(best_subset_index)
            # Remove the covered elements from our remaining set
            elements_remaining -= subsets[best_subset_index]
        else:
            # This should not happen if the problem instance is valid
            # (i.e., if all elements can be covered by the given subsets)
            break
    
    timeSpent = round(time.time() - start_time,2)
    
    return solution, timeSpent

def write_solution(filename, algorithm, cutoff_time, seed, solution_indices, subsets):
    """
    Write the solution to the output file.
    
    The output file format is:
    - First line: Number of sets used in the solution
    - Second line: Space-separated list of indices of the selected subsets (1-indexed)
    
    The output filename is constructed based on the input parameters:
    - For LS1 and LS2: <instance>_<algorithm>_<cutoff_time>_<seed>.sol
    - For others: <instance>_<algorithm>_<cutoff_time>.sol
    
    Args:
        filename (str): Base name of the instance file (without path and extension)
        algorithm (str): Algorithm used (BnB, Approx, LS1, LS2)
        cutoff_time (int): Cutoff time in seconds
        seed (int): Random seed used
        solution_indices (list): List of indices of the chosen subsets (0-indexed)
        subsets (list): List of sets, where each set is a subset of the universe
    """
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
    """
    Main function that parses command-line arguments, reads the problem instance,
    calls the appropriate algorithm, and writes the solution to a file.
    """
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