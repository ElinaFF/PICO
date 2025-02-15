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


METADATA_PATH = "../medic_otherThanPackage/s_MTBLS28_merged.csv"
DATAMATRIX_PATH = "../medic_otherThanPackage/MTBLS28_CombinedData2_forML.csv"


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
    metabo_controller.set_target_columns(["Factor Value[Sample Type]", "Factor Value[Smoking]"])
    metabo_controller.add_experimental_design({"Case_Current": ["Case__Current Smoker"], "Ctrl_Current": ["Control__Current Smoker"]})
    metabo_controller.add_experimental_design({"Case_Former": ["Case__Former Smoker"], "Ctrl_Former": ["Control__Former Smoker"]})
    metabo_controller.add_experimental_design({"Case_Never": ["Case__Never Smoker"], "Ctrl_Never": ["Control__Never Smoker"]})
    print("Classification design added")

    metabo_controller.set_train_test_proportion(0.2)
    metabo_controller.set_number_of_splits(5)
    ### Choosing balance correction value : see documentation for explanation
    metabo_controller.set_balance_correction_for_experiment("Case_Current_vs_Ctrl_Current", 15)
    metabo_controller.set_balance_correction_for_experiment("Case_Former_vs_Ctrl_Former", 0)
    metabo_controller.set_balance_correction_for_experiment("Case_Never_vs_Ctrl_Never", 21)
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
    #
    # r = pkl.load(open("big_results.p", "rb"))
    #
    # df = r[list(r.keys())[0]]["DecisionTree"].results["features_table"]
    # #classes = r[list(r.keys())[0]]["DecisionTree"].results["umap_data"][0]
    # print(df)

    # a = r[list(r.keys())[0]]["DecisionTree"].results["0"]["train_accuracy"]
    # b = r[list(r.keys())[0]]["DecisionTree"].results["0"]["test_accuracy"]
    # print("len train : {}".format(len(a)))
    # print("len test : {}".format(len(b)))

    # print("list(r.keys())[0] : {}".format(list(r.keys())[0]))
    # print(dbc.__version__)
    # r = pkl.load(open("big_results.p", "rb"))
    # X = r[list(r.keys())[0]]["DecisionTree"].results["0"]["Confusion_matrix"]

    # a = np.array([[9, 5],
    #               [1, 7]])
    # b = np.array([[10, 6],
    #               [3, 9]])
    #
    # #print(a*b) # element-wise
    # #print(a@b)
    #
    # answer = np.mean([a, b], axis=0)
    # std = np.std([a, b], axis=0)
    # print(answer)
    # print(std)
    # text_mat = []
    # print("---")
    # for i, line in enumerate(answer):
    #     print(line)
    #     text_mat.append([])
    #     for j, col in enumerate(line):
    #         print(col)

    # def format_name_and_associated_values(names, values):
    #     """
    #     from a Counter dict, modify
    #     """
    #     count = Counter(names)
    #     for n in count.keys():
    #         count[n] = [0]
    #         liste_val = []
    #         for idx, j in enumerate(names):
    #             if n == j and values[idx] > 0:
    #                 count[n][0] += 1
    #                 liste_val.append(values[idx])
    #         count[n].append(np.mean(liste_val))
    #     return count
    #
    # n = ["a", "b", "c", "b", "b", "a"]
    # v = [0.5, 0, 0, 0.2, 0.4, 0.7]
    # print(format_name_and_associated_values(n, v))


if __name__ == "__main__":
    main()
