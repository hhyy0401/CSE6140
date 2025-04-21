# Project Goal

The CSE 6140 project implements **Branch and Bound / Approximation / Local Search I / Local Search II algorithms** to solve the **Minimum Set Cover** problem.


Okay, here's a refined version of that section, incorporating the run.sh information and adding a bit more clarity:

# How to Run Experiments

There are two primary ways to run the experiments:

### 1. Running `exec.py` Directly

Execute individual experiments using the `exec.py` script from your terminal within `code` directory:

```bash
python exec.py -inst {dataset} -alg {algorithm} -time {cutoff_time} -seed {random_seed}
```


### 2. Using the run.sh Script

A shell script run.sh is provided in `code` directory, likely for running a batch of predefined experiments (e.g., multiple algorithms on one dataset, or one algorithm across multiple datasets).


### Arguments

| Argument     | Description                                                  |
|--------------|--------------------------------------------------------------|
| `-inst`      | Name of the dataset file (e.g., `small1.in`)                 |
| `-alg`       | Algorithm to run (one of `BnB`, `Approx`, `LS1`, `LS2`)      |
| `-time`      | Cutoff time in seconds for the algorithm to run              |
| `-seed`      | Random seed for reproducibility (used by stochastic methods) |

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

Outputs are generated in the `output/` folder with two files:

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



# How to run plots.py

`plots.py` in `code` directory is a visualization script used to analyze and compare the performance of four algorithms—BnB, Approx, LS1, and LS2—with a particular focus on comparing LS1 and LS2 through various plots. It processes multiple `.trace` files (produced by running each algorithm with different random seeds) and generates the following plots and statistics:

1. **Comprehensive Performance Table**
   - Before plotting, the script computes and prints a summary table showing:
   - Average runtime over all runs.
   - Average solution value (collection size).
   - Average relative error, computed as: $\text{Relative Error} = \frac{\text{Solution Value} - \text{Optimal}}{\text{Optimal}}$
   - This table gives a concise overview of each algorithm’s efficiency and solution quality across multiple runs.

2. **Qualified Runtime Distribution (QRTD)**
   - Shows the fraction of runs that reached a solution within a certain relative error threshold (q*) by a given time.
   - Useful for assessing how quickly each algorithm gets “good enough” solutions, relative to the known optimum.

3. **Solution Quality Distribution (SQD)**
   - Displays the distribution of final relative errors achieved by each algorithm at the end of the given cutoff time.
   - Helpful to understand which algorithms consistently find better solutions.

4. **Box Plot of Running Times**
   - Illustrates the spread and variance of the running times across all seeds.
   - Gives insight into the stability and runtime behavior of each method.

## Output
Plots will be saved in the `plot/` folder:
- `qrtd.pdf`: QRTD plot combining all four algorithms
- `sqd.pdf`: SQD plot combining all four algorithms
- `box.pdf`: Box plot comparing the runtime distributions

## Example Command
```bash
python plots.py -inst test4 -time 600
```
- `inst`: the instance name (without extension), e.g., `test4` for `data/test4.in`
- `time`: cutoff time used for the algorithm runs (in seconds) whose traces are being analyzed

The script will search for `.trace` files in the `output/` folder that match the pattern `{inst}_{alg}_{time}*.trace`.


## Project Structure

```
.
├── code/ # Contains all source code and execution scripts
│ ├── run.sh # Shell script potentially used for batch experiments
│ ├── exec.py # Main script to run experiments
│ ├── Approx.py # Approximation algorithm implementation
│ ├── BnB.py # Branch and Bound algorithm implementation
│ ├── LS1.py # Local Search I algorithm implementation
│ ├── LS2.py # Local Search II algorithm implementation
│ ├── plots.py # Script to generate performance plots
│ ├── plots.sh # Shell script potentially used for batch plotting
│ ├── README.md # Project documentation (this file)
├── data/ # Input datasets (.in files)
├── output/ # Output solution (.sol) and trace (.trace) files
├── plot/ # Generated plots (.pdf files)
├── report.pdf # Our project report

```

---

## Software Environment

The software environment was set up as follows:
*   **Language:** Python 3.12.17
*   **Compiler/Interpreter:** CPython 3.12.17
*   **Libraries:**
    *   `NumPy` for array operations
    *   `SciPy` (v1.12+) for linear programming (LP-relaxation)
    *   `time` and `math` for timing and utility functions
