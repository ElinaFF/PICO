import pickle
from datetime import datetime
import numpy as np
import pandas as pd
import pickle as pkl
import umap

from medic.domain import MetaboController
from medic.service import Utils
import dash_bootstrap_components as dbc
import plotly.express as px
from collections import Counter


#METADATA_PATH = "../medic_otherThanPackage/s_MTBLS28_merged.csv"
#DATAMATRIX_PATH = "../medic_otherThanPackage/MTBLS28_CombinedData2_forML.csv"

METADATA_PATH = "../medic_otherThanPackage/s_MTBLS28_NEG.csv"
DATAMATRIX_PATH = "../medic_otherThanPackage/MTBLS28_data_NEG_forML.csv"


def main():
    start_time = datetime.now()
    print("Starting MeDIC at : ", start_time)
    metabo_controller = MetaboController()
    metabo_controller.set_raw_use_for_data(False)
    metabo_controller.set_data_matrix_remove_rt(False)
    metabo_controller.set_multithreading(True)

    metabo_controller.set_data_matrix_from_path(DATAMATRIX_PATH, from_base64=False)
    metabo_controller.set_metadata(METADATA_PATH, from_base64=False)
    print("Metadata and DataMatrix are set_from_path")

    metabo_controller.set_id_column("Sample_Name")
    metabo_controller.set_target_columns(["Factor Value[Sample Type]"])
    metabo_controller.add_experimental_design({"NEG_Case": ["Case"], "Ctrl": ["Control"]})
    #metabo_controller.set_target_columns(["Factor Value[Sample Type]", "Factor Value[Smoking]"])
    #metabo_controller.add_experimental_design({"NEG_Case_Current": ["Case__Current Smoker"], "Ctrl_Current": ["Control__Current Smoker"]})
    #metabo_controller.add_experimental_design({"NEG_Case_Former": ["Case__Former Smoker"], "Ctrl_Former": ["Control__Former Smoker"]})
    #metabo_controller.add_experimental_design({"NEG_Case_Never": ["Case__Never Smoker"], "Ctrl_Never": ["Control__Never Smoker"]})
    print("Classification design added")

    metabo_controller.set_train_test_proportion(0.2)
    metabo_controller.set_number_of_splits(20)

    ### Choosing balance correction value : see documentation for explanation
    metabo_controller.set_balance_correction_for_experiment("NEG_Case_vs_Ctrl", 0)
    #metabo_controller.set_balance_correction_for_experiment("NEG_Case_Current_vs_Ctrl_Current", 15)
    #metabo_controller.set_balance_correction_for_experiment("NEG_Case_Former_vs_Ctrl_Former", 0)
    #metabo_controller.set_balance_correction_for_experiment("NEG_Case_Never_vs_Ctrl_Never", 21)
    metabo_controller.create_splits()

    metabo_expe_filename = Utils.get_metabo_experiment_path("medic_splits") # Get save file path
    metabo_expe_obj = metabo_controller.generate_save()
    Utils.dump_metabo_expe(metabo_expe_obj) # Dump the classification design to the dump folder
    Utils.dump_metabo_expe(metabo_expe_obj, metabo_expe_filename) # Save the classification design
    del metabo_expe_obj

    metabo_controller.set_selected_models(["DecisionTree", "RandomForest", "SCM", "RandomSCM"])
    print("Learning starts...")
    metabo_controller.set_cv_folds(5)
    metabo_controller.learn()
    print("finished")
    
    metabo_expe_filename = Utils.get_metabo_experiment_path("medic_ml") # Get save file path
    metabo_expe_obj = metabo_controller.generate_save()
    Utils.dump_metabo_expe(metabo_expe_obj) # Dump the classification design to the dump folder
    Utils.dump_metabo_expe(metabo_expe_obj, metabo_expe_filename) # Save the classification design
    del metabo_expe_obj
    print("saved in file")

    end_time = datetime.now()
    print("Duration: {}".format(end_time - start_time))
   

if __name__ == "__main__":
    main()
