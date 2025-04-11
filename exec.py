import argparse
import random
import time

from LS2 import hill_climbing_min_set_cover

def load_dataset(filename):
    with open("data/"+filename+".in", 'r') as f:
        lines = f.readlines()
    n, _ = list(map(int, lines[0].strip().split(" ")))
    universe = set(range(1, n + 1))
    subsets = [set(map(int, line.strip().split(" ")[1:])) for line in lines[1:]]

    return universe, subsets

def save_dataset(filename, result, intermediate_results):

    with open("result/"+filename+".sol", 'w') as f:
        f.write(f"{len(result)}\n")
        f.write(" ".join(str(s+1) for s in result))
    
    with open("result/"+filename+".trace", 'w') as f:
        for s in intermediate_results:
            f.write(f"{s[0]} {s[1]}\n")
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', required=True, help='Input filename')
    parser.add_argument('-alg', required=True, choices=['BnB', 'Approx', 'LS1', 'LS2'])
    parser.add_argument('-time', required=True, type=float, help='Cutoff time in seconds')
    parser.add_argument('-seed', required=True, type=int, help='Random seed')
    args = parser.parse_args()

    random.seed(args.seed)

    universe, subsets = load_dataset(args.inst) 

    if args.alg == 'BnB':
        solution_filename = f"{args.inst}_{args.alg}_{args.time}"
        pass
    elif args.alg == 'Approx':
        solution_filename = f"{args.inst}_{args.alg}_{args.time}_{args.seed}"
        pass
    elif args.alg == 'LS1':
        solution_filename = f"{args.inst}_{args.alg}_{args.time}_{args.seed}"
        pass
    elif args.alg == 'LS2':
        result, intermediate_results = hill_climbing_min_set_cover(universe, subsets, args.time)
        solution_filename = f"{args.inst}_{args.alg}_{args.time}"
    else:
        print(f"Algorithm '{args.alg}' is not implemented in this file.")

    save_dataset(solution_filename, result, intermediate_results)

if __name__ == "__main__":
    main() 