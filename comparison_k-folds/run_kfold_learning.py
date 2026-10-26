"""
Step 2/2 of the k-folds comparison : train the models on the k-folds splits and save the results.

Equivalent of automate_1k_splits.py : the models, hyperparameters search and number of inner folds
are taken from automate_1k_splits.py, so both experiments are trained in exactly the same way.

Run (from anywhere) :
    python comparison_k-folds/run_kfold_learning.py

Output : ~/pico_files/saves/pico_ml_kfold_<date>_<time>.mtxp
It is a regular pico results file : it can be analysed like the pico results
(e.g. with analyze_results_1k_paired_splits.ipynb) or opened in the pico interface.
"""
import os
import sys
from datetime import datetime

# The pico scripts and the data paths (e.g. "test_data/...") are relative to the repository root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)
os.chdir(REPO_ROOT)

from override_Controller import Controller
from pico.service import Utils, init_logger, log_exceptions
from automate_1k_splits import ML_setup_CV_and_algo, SAVE_setups_and_results

logger = init_logger()


##############################
#         Parameters         #
##############################

# File created by generate_kfold_splits.py (path relative to the repository root, or absolute)
KFOLD_SPLITS_PATH = "test_data/pico_splits_kfold_20261026_134658_testing2rep5folds.mtxp"

# Range of splits to learn on : split_start included, split_end excluded (None = up to the last split).
# Split i is the fold (i % 5) of the repetition (i // 5) : choose multiples of the number of folds
# so that only complete repetitions are learned (e.g. 0 to 500 = repetitions 0 to 99 with 5 folds).
SPLIT_START = 0
SPLIT_END = 1


##############################
#      Run experiment        #
##############################

def finish_a_kfold_experiment(kfold_splits_path, split_start, split_end):
    start_time = datetime.now()
    logger.info(f"---> Starting at : {start_time}")
    controller = Controller()

    dto = Utils.load_metabo_expe(kfold_splits_path)
    controller.full_restore(dto)

    ML_setup_CV_and_algo(controller, "GridSearchCV", split_start, split_end)
    SAVE_setups_and_results(controller, "pico_ml_kfold")

    end_time = datetime.now()
    logger.info(f"---> Duration of run : {end_time - start_time}")


###############################
#        Main function        #
###############################

@log_exceptions(logger)
def main():
    finish_a_kfold_experiment(KFOLD_SPLITS_PATH, SPLIT_START, SPLIT_END)


if __name__ == "__main__":
    main()
