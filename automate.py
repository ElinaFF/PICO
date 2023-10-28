import pickle
from datetime import datetime
import numpy as np
import pandas as pd
import pickle as pkl
import umap

from metabodashboard.domain import MetaboController
import dash_bootstrap_components as dbc
import plotly.express as px
from collections import Counter


METADATA_PATH = "sample_metadata_corrigé.xlsx"
DATAMATRIX_PATH = "DataMatrix.csv"


def main():
    start_time = datetime.now()
    print("Starting the MetaboDashboard at : ",start_time)
    metabo_controller = MetaboController()
    metabo_controller.set_raw_use_for_data(False)
    metabo_controller.set_data_matrix_remove_rt(True)
    metabo_controller.set_multithreading(False)

    metabo_controller.set_data_matrix_from_path(DATAMATRIX_PATH, from_base64=False)
    metabo_controller.set_metadata(METADATA_PATH, from_base64=False)
    print("Metadata and DataMatrix are set_from_path")

    metabo_controller.set_id_column("Sample")
    metabo_controller.set_target_columns(["study", "TX"])
    metabo_controller.set_pairing_group_column("subject")
    metabo_controller.add_experimental_design({"NorthA": ["ALI__A", "MED__A"], "Med": ["ALI__B", "MED__B"]})
    metabo_controller.add_experimental_design({"AliA": ["ALI__A"], "AliB": ["ALI__B"]})
    metabo_controller.add_experimental_design({"MedA": ["MED__A"], "MedB": ["MED__B"]})
    metabo_controller.add_experimental_design({"AliA": ["ALI__A"], "MedA": ["MED__A"]})
    print("Classification designs added")

    metabo_controller.set_train_test_proportion(0.2)
    metabo_controller.set_number_of_splits(30)
    metabo_controller.create_splits()
    metabo_controller.set_selected_models(["DecisionTree", "RandomForest", "SCM", "RandomSCM"])

    print("Learning starts...")
    metabo_controller.set_cv_folds(5)
    metabo_controller.learn()
    print("learning step finished at : ", datetime.now())
    #
    #print(metabo_controller.get_all_results())
    pickle.dump(metabo_controller.get_all_results(), open("rez_by_script_1.p", "wb"))
    print("saved in file")

    end_time = datetime.now()
    print("Total duration: {}".format(end_time - start_time))
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
