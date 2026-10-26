"""
Step 1/2 of the k-folds comparison : create the repeated k-folds splits and save them in a pico .mtxp file.

Equivalent of generate10k_splits.py, but with repeated k-folds instead of the pico splits.
The data files and classification design are taken from generate10k_splits.py,
so both experiments are built on exactly the same samples and classes.

Run (from anywhere) :
    python comparison_k-folds/generate_kfold_splits.py

Output : ~/pico_files/saves/pico_splits_kfold_<date>_<time>.mtxp
Then use this file in run_kfold_learning.py (step 2/2).
"""
import os
import sys
from datetime import datetime

# The pico scripts and the data paths (e.g. "test_data/...") are relative to the repository root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)
os.chdir(REPO_ROOT)

from override_Controller import Controller
from pico.service import init_logger, log_exceptions
from generate10k_splits import SPLITS_setup_files, SPLITS_setup_classification_designs, SAVE_setups_and_results
from kfold_splits import create_repeated_kfold_splits

logger = init_logger()


##############################
#         Parameters         #
##############################

# 400 x 5-folds = 2000 splits, with 1/5 = 20% of the samples in test, like the pico splits with 0.2
NUMBER_OF_REPETITIONS = 2
NUMBER_OF_FOLDS = 5

# Column of the metadata used to keep samples of the same entity (e.g. subject) in the same fold.
# Set to "" for no pairing.
PAIRING_COLUMN = "SUPP_subject_id"


##############################
#      Setup experiment      #
##############################

def SPLITS_setup_pairing(controller, pairing_column):
    """
    controller : Controller object
    pairing_column : name of the metadata column used for pairing, "" for no pairing
    """
    if pairing_column != "":
        controller.set_pairing_group_column(pairing_column)


def run_kfold_splits_creation(number_of_repetitions, number_of_folds, pairing_column):
    start_time = datetime.now()
    logger.info(f"---> Starting at : {start_time}")
    controller = Controller()

    SPLITS_setup_files(controller)
    SPLITS_setup_classification_designs(controller)
    SPLITS_setup_pairing(controller, pairing_column)
    create_repeated_kfold_splits(controller, number_of_repetitions, number_of_folds)
    SAVE_setups_and_results(controller, "pico_splits_kfold")

    end_time = datetime.now()
    logger.info(f"---> Duration of run : {end_time - start_time}")


###############################
#        Main function        #
###############################

@log_exceptions(logger)
def main():
    run_kfold_splits_creation(NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS, PAIRING_COLUMN)


if __name__ == "__main__":
    main()
