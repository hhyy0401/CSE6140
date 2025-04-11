
# Project Goal

This project implements **Branch and Bound / Approximation / Local Search I / Local Search II algorithms** to solve the **Minimum Set Cover** problem.

---

# How to Run exec.py

```bash
python exec.py -inst {dataset} -alg {algorithm} -time {cutoff_time} -seed {random_seed}
```

### Arguments

| Argument     | Description                                                  |
|--------------|--------------------------------------------------------------|
| `-inst`      | Name of the dataset file (e.g., `small1.in`, )               |
| `-alg`       | Algorithm to run (one of `BnB`, `Approx`, `LS1`, `LS2`)      |
| `-time`      | Cutoff time in seconds for the algorithm to run              |
| `-seed`      | Random seed for reproducibility (used by stochastic methods) |

---

## Dataset Format

All datasets are placed in the `data/` directory.

- **First line**:  
  Two integers — the size of the universe `n` and the number of subsets `m`  
  *(separated by a space)*

- **From the second line onward**:  
  Each line represents one subset:
  - First number: size of the subset
  - Followed by the elements in the subset (space-separated)


## Output

Outputs are generated in the `results/` folder with two files:

### 1. `*.sol` — **Solution File**
- First line: the size of the final set cover
- Second line: comma-separated list of indices of selected subsets

#### Example:
```
3
1 3 7
```

### 2. `*.trace` — **Trace File**
- Logs the timestamp and the cover size whenever it improves

#### Example:
```
0.00 5
1.47 4
2.21 3
```

---

## Example Command

```bash
python exec.py -inst small1.in -alg LS2 -time 10 -seed 42
```

This runs the hill climbing algorithm on the dataset `small1.in.txt` with a time limit of 10 seconds and random seed 42.


---

# How to run plots.py

plots.py is a visualization script for analyzing and comparing the performance of four algorithms: BnB, Approx, LS1, and LS2. It processes multiple .trace files (produced by running each algorithm with different random seeds) and generates the following plots and statistics:

1. Comprehensive Performance Table
  - Before plotting, the script computes and prints a summary table showing:
  - Average runtime over all runs.
  - Average solution value (collection size).
  - Average relative error, computed as: \text{Relative Error} = \frac{\text{Solution Value} - \text{Optimal}}{\text{Optimal}}

  This table gives a concise overview of each algorithm’s efficiency and solution quality across multiple runs.


2. Qualified Runtime Distribution (QRTD)
  - Shows the fraction of runs that reached a solution within a certain relative error threshold (q*) by a given time.
  - Useful for assessing how quickly each algorithm gets “good enough” solutions, relative to the known optimum.

3. Solution Quality Distribution (SQD)
  - Displays the distribution of final relative errors achieved by each algorithm at the end of the given cutoff time.
  - Helpful to understand which algorithms consistently find better solutions.

4. Box Plot of Running Times
  - Illustrates the spread and variance of the running times across all seeds.
  - Gives insight into the stability and runtime behavior of each method.

## Output
Plots will be saved in the plot/ folder:
- qrtd.pdf: QRTD plot combining all four algorithms
- sqd.pdf: SQD plot combining all four algorithms
- box.pdf: Box plot comparing the runtime distributions

## Example Command
```bash
python plots.py -inst test4 -time 600
```
- inst: the instance name (without extension), e.g., test4 for test4.graph
- time: cutoff time for each algorithm run (in seconds)

The script will search for .trace files in the result/ folder that match the pattern {inst}\_{alg}\_{cutoff_time}*.trace.


## Project Structure

```
.
├── data/             # Input datasets
├── results/          # Output solution and trace files
├── exec.py           # Main script to run experiments
├── plots.py          # Script to plot QRTD, SQD, BOX
├── README.md         # Project documentation
```

---

## Dependencies

- Python 3.7+





