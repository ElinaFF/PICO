import pickle
from datetime import datetime
import numpy as np
import pandas as pd
import pickle as pkl
import umap
#import plotly.express as px

from metabodashboard.domain import MetaboController
#import dash_bootstrap_components as dbc
from collections import Counter
from metabodashboard.service import Utils
from sys import getsizeof
import time
start = time.process_time()
# your code here    
print(time.process_time() - start)


METADATA_PATH = "sample_metadata_corrige.csv"
DATAMATRIX_PATH = "DataMatrix.csv"


def main():
    start_time = datetime.now()
    print("Starting the MetaboDashboard")
    metabo_controller = MetaboController()
    metabo_controller.set_raw_use_for_data(False)

    metabo_controller.set_data_matrix_from_path(DATAMATRIX_PATH, from_base64=False)
    metabo_controller.set_metadata(METADATA_PATH, from_base64=False)
    print("Metadata and DataMatrix are set_from_path")

    metabo_controller.set_id_column("Sample")
    #metabo_controller.set_target_columns(["diet"])
    metabo_controller.set_multithreading(False)
    save_filename = 'multiFalse'
    metabo_controller.set_target_columns(["study", "TX"])
    metabo_controller.set_pairing_group_column("subject")
    #metabo_controller.add_experimental_design({"NA": ["NA"], "MED": ["MED", "MED/w"]})
    metabo_controller.add_experimental_design({"A": ["ALI__A", "MED__A"], "B": ["ALI__B", "MED__B"]})
    save_filename += 'AvsB'
    #metabo_controller.add_experimental_design({"aliA": ["ALI__A"], "aliB": ["ALI__B"]})
    #save_filename += 'aliAvsaliB'
    #metabo_controller.add_experimental_design({"medA": ["MED__A"], "medB": ["MED__B"]})
    #save_filename += 'medAvsmedB'
    #metabo_controller.add_experimental_design({"aliA": ["ALI__A"], "medA": ["MED__A"]})
    #save_filename += 'aliAvsmedA'
    print("Experimental design added")

    metabo_controller.set_train_test_proportion(0.2)
    
    n_splits = 3 ## 25
    metabo_controller.set_number_of_splits(n_splits)
    save_filename += str(n_splits) + 'split'
    
    metabo_controller.create_splits()
    #metabo_controller.set_selected_models(["DecisionTree"])
    
    models, marker = ["DecisionTree"], "DT"
    #models, marker = ["DecisionTree", "RandomForest"], "DT-RF"
    #models, marker = ["DecisionTree", "RandomForest", "SCM", "RandomSCM"], "DT-RF-SCM-rSCM"
    metabo_controller.set_selected_models(models)
    save_filename += marker

    print("Learning starts...")
    metabo_controller.set_cv_folds(5)
    metabo_controller.learn()
    print("finished")
    time_2 = datetime.now()
    print("Learning duration: {}".format(time_2 - start_time))
    #
    #print(metabo_controller.get_all_results())
    #pickle.dump(metabo_controller.get_all_results(), open("test_graham1_ML.mtxp", "wb"))
    save_object = metabo_controller.generate_save()
    time_3 = datetime.now()
    print("Generating save duration: {}".format(time_3 - time_2))
    print("size of save_truc : {} btyes".format(getsizeof(save_object)))
    dumped_object = pickle.dumps(save_object)
    size = len(dumped_object)
    print("size of dumped_truc : {} btyes".format(size))
    Utils.dump_metabo_expe(save_object, save_filename)

    end_time = datetime.now()
    print("Saving duration: {}".format(end_time - time_2))
    print("Total Duration: {}".format(end_time - start_time))
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

