import matplotlib.pyplot as plt
import argparse
import numpy as np
import os
import glob

plt.rcParams.update({
    'font.size': 24,          
    'axes.titlesize': 20,     
    'axes.labelsize': 20,    
    'xtick.labelsize': 20,   
    'ytick.labelsize': 20,    
    'legend.fontsize': 20, 
})

colors = {
    'BnB': 'blue',
    'Approx': 'orange',
    'LS1': 'green',
    'LS2': 'red'
}

marker_styles = {
    'BnB': 'o',
    'Approx': 's',
    'LS1': 'D',
    'LS2': '^'
}

def find_matching_files(inst, alg, cutoff_time, folder='result'):
    full_pattern = os.path.join(folder, f"{inst}_{alg}_{cutoff_time}*.trace")
    matched_files = glob.glob(full_pattern)
    return matched_files

def load_trace(filename):
    with open(filename, 'r') as f:
        return [tuple(map(float, line.strip().split(' '))) for line in f if line.strip()]

def load_opt(filename):
    with open("data/"+filename+".out", 'r') as f:
        opt = int(f.readline().strip())  
    return opt

def evaluate_solutions(solutions, opt):
    times, collection_sizes, rel_errors = [], [], []

    for sol in solutions:
        time, value = sol[-1]  
        times.append(time)
        collection_sizes.append(value)
        rel_error = (value - opt) / opt
        rel_errors.append(rel_error)

    avg_time = round(sum(times) / len(times), 2)
    avg_rel_error = round(sum(rel_errors) / len(rel_errors), 2)
    avg_collection_size = round(sum(collection_sizes) / len(collection_sizes), 2)

    return avg_time, avg_collection_size, avg_rel_error

def plot_qrtd_sqd_combined(solutions_dict, opt, inst, q_star=0.25, max_time=20):
    fig, (ax_qrtd, ax_sqd) = plt.subplots(1, 2, figsize=(18, 6))

    for alg in solutions_dict:
        solutions = solutions_dict[alg]

        # QRTD
        threshold = opt * (1 + q_star)
        solve_times = []
        for run in solutions:
            for t, val in run:
                if val <= threshold:
                    solve_times.append(t)
                    break
            else:
                solve_times.append(float('inf'))
        time_points = np.linspace(0, max_time, 10)
        y_values = [sum(1 for st in solve_times if st <= t) / len(solutions) for t in time_points]
        ax_qrtd.plot(time_points, y_values, color=colors[alg], marker=marker_styles[alg], linewidth=3, markersize=12, label=alg)

        # SQD
        rel_errors = [(run[-1][1] - opt) / opt for run in solutions if run[-1][0] <= max_time]
        rel_errors.sort()
        y_vals = np.linspace(0, 1, len(rel_errors))
        ax_sqd.plot(rel_errors, y_vals, color=colors[alg], marker=marker_styles[alg], linewidth=3, markersize=12, label=alg)

    ax_qrtd.set_title(f'QRTD - {inst}')
    ax_qrtd.set_xlabel('Time (s)')
    ax_qrtd.set_ylabel('Fraction solved')
    ax_qrtd.grid(True)

    ax_sqd.set_title(f'SQD - {inst}')
    ax_sqd.set_xlabel('Relative Error')
    ax_sqd.set_ylabel('Fraction of runs')
    ax_sqd.grid(True)
    fig.subplots_adjust(bottom=0.2)  
    fig.legend(solutions_dict, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.05))

    plt.savefig(f"plot/qrtd_sqd_{inst}.pdf", dpi=300, bbox_inches='tight')
    plt.close()

def plot_box_all(solutions_dict, inst):
    plt.figure(figsize=(10, 6))
    data = [[run[-1][0] for run in solutions_dict[alg]] for alg in solutions_dict]
    bplot = plt.boxplot(data, patch_artist=True, boxprops=dict(linewidth=2),
                        tick_labels=solutions_dict.keys(),
                        medianprops=dict(color='black', linewidth=2))

    for patch, alg in zip(bplot['boxes'], solutions_dict.keys()):
        patch.set_facecolor(colors[alg])

    plt.ylabel('Running Time (s)')
    plt.title(f'Box Plot of Running Times for {inst}')
    plt.tight_layout()
    plt.savefig(f"plot/box_{inst}.pdf", dpi=300)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', required=True, help='Input filename')
    parser.add_argument('-time', required=True, type=float, help='Cutoff time in seconds')
    args = parser.parse_args()

    q_value = 0.25
    opt = load_opt(args.inst)
    solutions_dict = {}

    for alg in ['LS1', 'LS2']:
        solutions = []
        match_files = find_matching_files(args.inst, alg, args.time)
        for file in match_files:
            solutions.append(load_trace(file))
        solutions_dict[alg] = solutions

        avg_time, avg_collection_size, avg_rel_error = evaluate_solutions(solutions, opt)
        print(f"[{alg}] Time (s) & collection size & RelErr")
        print(f"{avg_time} & {avg_collection_size} & {avg_rel_error}\n")

    print("[Plot QRTD + SQD]")
    plot_qrtd_sqd_combined(solutions_dict, opt, args.inst)

    print("[Plot Box]")
    plot_box_all(solutions_dict, args.inst)

if __name__ == "__main__":
    main()