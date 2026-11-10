---
layout: base
title:  Tutorial
cover:  true
---

# Tutorial
{: .no_toc}
_ _ _ _

This tutorial walks through a complete PICO experiment, from loading the data to exploring the results.
It can be done in two ways:
- **with the interface**, recommended for most users;
- **with the `automate.py` script**, for users comfortable with a terminal and Python, or to run an experiment on a distant server.

Both ways produce the same `.mtxp` result files, and those files can always be opened in the interface for the analysis of the results.

This tutorial assumes PICO is already installed, see the [Installation](installation.html) page.
{: .note}

<!-- TODO: provide a small public example dataset (e.g. reduced MTBLS7337) and a download link, so every step below can be reproduced with concrete values. -->

* toc
{:toc}

## Launching the interface

### 1. Open a terminal

| Windows | Mac | Linux (or WSL) |
|---------|-----|----------------|
| Command Prompt (`cmd`) | Terminal | Terminal |

### 2. Go into your project directory and activate the environment

The project directory is the one where you created the virtual environment during the installation (here called `pico_project`, with an environment named `.venv`).

Windows
```
cd pico_project
.venv\Scripts\activate
```

Mac and Linux
```
cd pico_project
source .venv/bin/activate
```

When the environment is active, its name appears at the beginning of the line in the terminal, for example `(.venv)`.

### 3. Start PICO

```
pico ui
```

A starting message appears in the terminal and, after a few seconds, the interface opens automatically in your default web browser.
If it does not, scroll up to the starting message and copy-paste the address into the address bar of your browser. By default it is:
```
http://127.0.0.1:5000
```

The terminal must stay open while you use PICO: closing it stops the interface. To stop PICO properly, go back to the terminal and press `Ctrl+C`.
{: .note title="Warning"}

### Changing the port

If the port 5000 is already used by another program, the interface will not start. Choose another port with the `--port` option, then use that port in the address:
```
pico ui --port 8050
```
and open `http://127.0.0.1:8050`.

On Mac, the port 5000 is used by default by the *AirPlay Receiver*. Either use another port as shown above, or disable AirPlay Receiver in *System Settings > General > AirDrop & Handoff*.
{: .note}

### With Docker

<!-- TODO: verify the exact command against the Dockerfile and Docker Hub image -->
```
docker run -p 5000:5000 elinaff/medic
```
Then open `http://127.0.0.1:5000` in your browser.

### Updating PICO

From the activated environment:
```
pico update
```
Use `pico --version` to check the version currently installed.


## Running an experiment with the interface

Throughout the interface, when you click on something and nothing seems to happen, look at the title of the browser tab. If an action is running, it displays "Updating...". Some steps (especially the learning) can take several minutes.
{: .note title="Warning"}

### Step 1 - Home tab

The Home tab is the starting point. For a **new experiment**, there is nothing to do here, go directly to the Splits tab.

To **continue or look at a previous experiment**, see [Step 5](#step-5---reload-a-previous-experiment).

### Step 2 - Splits tab

This tab defines everything related to the samples. Fill the sections from top to bottom. The details of each option are on the [Splits tab](splits.html) page.

1. **Files**
   - Choose the type of data matrix: *Not Progenesis* for a matrix with samples as lines and features as columns, or one of the Progenesis options (raw or normalized) if the matrix comes from Progenesis.
   - Upload the data matrix (csv or excel).
   - Upload the metadata file. It is optional, but needed for pairing and often gives clearer classes.

2. **Define Classification designs**
   - Select the column containing the sample identifiers (the names that link the metadata to the data matrix).
   - Select one or more *target columns*: the columns containing the classes, for example a diagnosis column.
   - Create a design by selecting the classes of each of the two labels, and give a name to each label.
   - Add as many designs as needed, each design is an independent binary classification.

   <!-- TODO: concrete example with the example dataset, e.g. ID column, target column, design "0_controls_vs_1_cases" + screenshot -->

3. **Class balancing** (optional): corrects an imbalance between the number of samples of the two labels of a design.

4. **Sample pairing** (optional): select the metadata column identifying samples that come from the same subject, so they are always kept together in the train set or in the test set.

5. **Define splits**: choose the proportion of samples in the test set (e.g. 0.2 for 20%) and the number of splits (e.g. 30).

6. **Other Preprocessing** (optional).

7. **Generate file**: click the button to create the splits. <!-- TODO: exact button label -->

A first file is saved: `pico_splits_YYYYMMDD_HHMMSS.mtxp`, in the `pico_files/saves` directory of your home directory (see [Logs and results savings](implementation.html#logs-and-results-savings)).

### Step 3 - Machine Learning tab

The details of each option are on the [Machine Learning tab](ml.html) page. If you are not comfortable with hyperparameters optimization, the default values are a safe choice.

1. **Define Learning configs**
   - Choose the search method: GridSearch (default) or RandomSearch.
   - Choose the number of folds of the cross validation (default 5).
   - Enable multithreading to use all the processor cores. It reduces the computing time a lot.

2. **Define Learning Algorithms**: select the algorithms to train (Decision Tree, Random Forest, SCM, RandomSCM).

3. Start the learning. <!-- TODO: exact button label -->
   A pop-up with the message "The learning is completed." appears at the end.
   The computing time depends on the size of the data, the number of splits and the computer, from a few minutes to more than an hour (see [Benchmarks](index.html#benchmarks)).

A second file is saved: `pico_ml_YYYYMMDD_HHMMSS.mtxp`, in the same `pico_files/saves` directory. This file contains all the parameters **and** the results of the experiment.

### Step 4 - Explore the results

**Results tab** ([details](results.html))
- Select a classification design and an algorithm in the dropdown menus, then click on the Load button.
- Suggested starting points:
  - the *accuracy plot*, to check the models are reliable and do not overfit;
  - the *metrics table*, for the mean performances over all splits;
  - the *top 10 features* table, for the features most used by the models (potential biomarkers).

**Results aggregated tab** ([details](aggresults.html))
- Select a classification design and click on Load to compare all the algorithms together.

Most figures can be saved in SVG with the camera icon that appears when hovering the figure.

<!-- TODO: screenshots of the Results tab with the example dataset -->

### Step 5 - Reload a previous experiment

In the Home tab, use *Load MetaboExperiment* and select a `.mtxp` file, then choose:
- **Load results**: only to explore the results again, no data needed. This is the option to use for a `pico_ml_...mtxp` file produced by the `automate.py` script or shared by a collaborator.
- **Partial restore**: reuse the splits parameters with other designs or data.
- **Full restore**: reproduce exactly an experiment, with the same data and metadata.

See the [Home tab](home.html) page for details.

If results are already displayed when you load another file, click again on the Load buttons of the Results tabs, the figures are not cleared automatically. Restarting the interface between experiments avoids any confusion.
{: .note}


## Running an experiment with the `automate.py` script

The `automate.py` script runs an experiment without the interface: it creates the splits and trains the algorithms, then saves the same `.mtxp` files. It is useful to:
- run long experiments without keeping a browser open;
- run experiments on a distant server (computing cluster);
- run many experiments with different parameters in a row.

The results cannot be visualized in the terminal: the `pico_ml_...mtxp` file produced must be opened in the interface (see [Step 5](#step-5---reload-a-previous-experiment)).

### Get the script

The script is **not** installed with `pip install pico-ml`. Download [`automate.py`](https://github.com/ElinaFF/MeDIC/blob/main/automate.py) from the GitHub repository and put it in your project directory.
<!-- TODO: check the link once the script is cleaned up on main -->

### Run the script

After editing the script (see below), from the activated environment:
```
python automate.py
```
Progress and errors are written in the log files in `pico_files/logs` (one file per day).

### How the script is organized

The script follows the same steps as the interface. Each step is a function, and the function `run_an_experiment` calls them in order:

| Function | Equivalent in the interface |
|----------|-----------------------------|
| `SPLITS_setup_files` | Splits tab > Files |
| `SPLITS_setup_classification_designs` | Splits tab > Define Classification designs |
| `SPLITS_setup_splits_and_balancing` | Splits tab > Class balancing, Sample pairing, Define splits |
| `SAVE_setups_and_results(controller, "pico_splits")` | Splits tab > Generate file |
| `ML_setup_CV_and_algo` | Machine Learning tab |
| `SAVE_setups_and_results(controller, "pico_ml")` | automatic save at the end of the learning |

Most of the customization is done **inside** those functions, so read each of them before running the script.
{: .note title="Warning"}

### Splits

**Files** — at the top of the script, give the paths to your files:
```python
METADATA_PATH = "data/my_metadata.csv"
DATAMATRIX_PATH = "data/my_datamatrix.csv"
```
Then, in `SPLITS_setup_files`, choose the type of data matrix:

| Data matrix | `set_raw_use_for_data` | `set_data_matrix_remove_rt` |
|-------------|------------------------|-----------------------------|
| Not Progenesis | `False` | `False` |
| Progenesis, raw | `True` | `True` |
| Progenesis, normalized | `False` | `True` |

If your matrix is not from Progenesis, removing the features with a retention time below 1 minute should be done beforehand, as a preprocessing step.

**Classification designs** — in `SPLITS_setup_classification_designs`:
```python
controller.set_id_column("Sample_Name")
controller.set_target_columns(["Diagnosis"])
controller.add_classification_design({"0_controls": ["Control"],
                                      "1_cases": ["Case"]})
```
- `set_id_column`: the metadata column with the sample identifiers.
- `set_target_columns`: list of the metadata columns containing the classes.
- `add_classification_design`: a dictionary with the **labels** as keys, and the list of **classes** of each label as values. The classes must be values found in the target columns.
  - When several target columns are selected, a class is the combination of the values of each column, joined by `__` in the same order as in `set_target_columns`. For example, with `["Study", "Diagnosis"]`, a class is `"studyA__Case"`.
  - The `0_` and `1_` prefixes are optional, they decide which label gets the target 0 and which gets the target 1.
  - The design is then named `LABEL0_vs_LABEL1`, for example `0_controls_vs_1_cases`. This name is needed for the class balancing.
- Call `add_classification_design` once per design.

**Splits, balancing and pairing** — in `SPLITS_setup_splits_and_balancing`:
```python
controller.set_train_test_proportion(proportion_splits)
controller.set_pairing_group_column("subject_id")          # optional
controller.set_balance_correction_for_experiment("0_controls_vs_1_cases", 0)
```
- `proportion_splits`: proportion of samples in the test set (between 0 and 1), given when calling the function in `run_an_experiment`.
- `set_pairing_group_column`: optional, the metadata column identifying the samples from the same subject. Remove the line if there is no pairing.
- `set_balance_correction_for_experiment`: one line per design, using the design name. `0` means no correction. See the [Splits tab](splits.html) page to choose the value.
- The number of splits is given when calling the function, with **only one** of the two arguments:
  - `nbr_splits=30` to create 30 splits;
  - `split_from_seed=42` to create only one split from a given seed (useful to reproduce a specific split).

### Machine learning

In `ML_setup_CV_and_algo`:
```python
controller.set_multithreading(True)
controller.set_selected_models(["DecisionTree", "RandomForest", "SCM", "RandomSCM"])
controller.set_cv_type("GridSearchCV")
controller.set_cv_folds(5)
controller.learn()
```
- `set_selected_models`: any subset of `"DecisionTree"`, `"RandomForest"`, `"SCM"`, `"RandomSCM"`.
- `set_cv_type`: `"GridSearchCV"` (default) or `"RandomizedSearchCV"`. With `"RandomizedSearchCV"`, also give the number of combinations to test:
  ```python
  controller.set_cv_algorithm_configuration([20])
  ```
- `set_cv_folds`: number of folds of the cross validation.
- `set_multithreading(True)`: uses all the processor cores. On a shared server, make sure it matches the resources you requested.

### Results

`SAVE_setups_and_results` saves the experiment in `pico_files/saves`:
- after the splits, with `"pico_splits"`: file `pico_splits_YYYYMMDD_HHMMSS.mtxp`;
- after the learning, with `"pico_ml"`: file `pico_ml_YYYYMMDD_HHMMSS.mtxp`.

Only use `"pico_splits"` or `"pico_ml"` as argument, another value can break the loading of the file.
{: .note title="Warning"}

To analyse the results, copy the `pico_ml_...mtxp` file on a computer with PICO installed, launch the interface and use **Load results** in the Home tab (see [Step 5](#step-5---reload-a-previous-experiment)). The data files are not needed for this.

### Running on a server

The script can run without a screen, so it can be launched on a distant server. You need to:
1. install PICO in a virtual environment on the server (see [Installation](installation.html));
2. copy your data files and the edited `automate.py` on the server;
3. launch the script so that it keeps running after you disconnect.

Simple server, with `nohup`:
```
source .venv/bin/activate
nohup python automate.py > automate.out 2>&1 &
```

Computing cluster using SLURM, example of job script (adapt the resources to your experiment and your cluster):
```bash
#!/bin/bash
#SBATCH --job-name=pico
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=pico_%j.out

source ~/pico_project/.venv/bin/activate
python automate.py
```
submitted with `sbatch job_pico.sh`.

The `pico_files` directory (saves and logs) is created in the home directory of the user on the server.
