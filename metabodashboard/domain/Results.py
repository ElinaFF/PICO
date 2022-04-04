import numpy as np
import pandas as pd
from abc import abstractmethod

import sklearn
from sklearn.metrics import accuracy_score, confusion_matrix
from collections import Counter

class Results:
    """
    Contains all results of an experimental design, is an attribute of class Experimental_design, and gives info to class "Plotter".
    Has results of all algorithms for all splits on one experimental design (so almost only numbers/floats/ints).
    Can be kept in RAM as it is not supposed to be too big, and prevents the reading/writing of models and splits files.
    """
    def __init__(self, splits_number: int):
        self.splits_number = [str(s) for s in range(splits_number)]
        self.results = {s: {} for s in self.splits_number}

    @abstractmethod
    def _get_features_importance(self, model):
        """
        retrieve features and their importance from a model to save it in the Results dict after each split
        """
        pass

    @abstractmethod
    def _aggregate_features_info(self):
        """
        When all splits are done and saved, aggregate feature info from every split to compute stats
        from all splits, concatenate in the same list the name of features, and another list their importance
        """
        pass

    def add_results_from_one_algo_on_one_split(self, model, y_train_true: list, y_train_pred: list,
                                               y_test_true: list, y_test_pred: list, algo_name: str, split_number: str):
        """
        Besoin modèle pour extraire features, features importance
        Besoin des y_true, des y_pred, des noms de samples pour le train et le test

        Fonction appelée à chq fois qu'un split a fini de rouler, pour stocker les info nécessaires à la production des
        graphique pour l'onglet résultat
        X : entièreté du dataset (autant train que test) c'est simplement pour voir le clustering de tous les individus
        """
        self.results[split_number]["train_accuracy"] = accuracy_score(y_train_true, y_train_pred)
        self.results[split_number]["test_accuracy"] = accuracy_score(y_test_true, y_test_pred)
        self.results[split_number]["feature_importances"] = self._get_features_importance(model)
        self.results[split_number]["Confusion_matrix"] = self._produce_conf_matrix(y_test_true, y_test_pred)

        if split_number == self.splits_number[-1]:
            self.results["info_expe"] = self._produce_info_expe(y_train_true, y_test_true)
            self.results["features_table"] = self.produce_features_importance_table()
            self.results["accuracies_table"] = self.produce_accuracy_plot_all()

    def __format_name_and_associated_values(self, names, values):
        """
        from a Counter dict, modify
        """
        count = Counter(names)
        for n in count.keys():
            count[n] = list(count[n])
            liste_val = []
            for idx, j in enumerate(names):
                if n == j:
                    liste_val.append(values[idx])
            count[n].append(np.mean(liste_val))
        return count

    def _produce_conf_matrix(self, y_test_true: list, y_test_pred: list):
        labels = list(set(y_test_true))
        return confusion_matrix(y_test_true, y_test_pred, labels=labels)

    def _produce_info_expe(self, y_train_true, y_test_true):
        """
        produce dataframe with basic information about the dataset/experiment, like number of samples and the train-test
        proprotion, the number of class, etc.
        """
        nbr_train = len(y_train_true)
        nbr_test = len(y_test_true)
        tot = nbr_train + nbr_test
        nom_stats = ["Number of samples (proportion train:test)"]
        valeurs_stats = [str(tot) +" ("+ str(nbr_train/tot*100) +":"+ str(nbr_test/tot*100) +")"]
        y = y_train_true + y_test_true
        c = Counter(y)
        for k in c.keys():
            nom_stats.append("Number of class {}".format(k))
            valeurs_stats.append("{}".format(c[k]))

        d = {"stats": nom_stats, "numbers": valeurs_stats}
        df = pd.DataFrame(data=d)
        return df

    def produce_features_importance_table(self):
        """
        Fonction qui réccupère les features et leurs importances de chq split sur le train et le test pour en faire un dataframe.
        Est donnée à la fonction de plotting correspondante (après que l'instance ait été complétée avec tous
        les résultats de splits)
        """
        features, times_used_all_splits, importance_or_usage_or_ = self._aggregate_features_info()

        d = {"features": features, "times_used": times_used_all_splits, "importance_usage": importance_or_usage_or_}
        df = pd.DataFrame(data=d)
        return df

    def produce_accuracy_plot_all(self):
        """
        Fonction qui réccupère les résultats (accuracies) de chq split sur le train et le test pour en faire un dataframe.
        Est donnée à la fonction de plotting correspondante (après que l'instance ait été complétée avec tous
        les résultats de splits)
        """
        x_splits_num = []
        y_splits_acc = []
        traces = []
        for s in self.splits_number:
            x_splits_num.append(str(s))
            x_splits_num.append(str(s))
            y_splits_acc.append(self.results[s]["train_accuracy"])
            traces.append("train")
            y_splits_acc.append(self.results[s]["test_accuracy"])
            traces.append("test")

        d = {"splits": x_splits_num, "accuracies": y_splits_acc, "color": traces}
        df = pd.DataFrame(data=d)

        return df


class ResultsDT(Results):
    """
    Contains all results of an experimental design, is an attribute of class Experimental_design, and gives info to class "Plotter".
    Has results of all algorithms for all splits on one experimental design (so almost only numbers/floats/ints).
    Can be kept in RAM as it is not supposed to be too big, and prevents the reading/writing of models and splits files.
    """

    def _get_features_importance(self, model):
        """
        retrieve features and their importance from a model to save it in the Results dict after each split
        """
        features = model.feature_names_in_
        importances = model.feature_importances_
        zipped = zip(features, importances)
        return zipped

    def _aggregate_features_info(self):
        """
        When all splits are done and saved, aggregate feature info from every split to compute stats
        from all splits, concatenate in the same list the name of features, and another list their importance
        """
        features = []
        imp = []
        # Get values of all splits in two lists
        for split in self.results.keys():
            f, i = zip(*self.results[split]["feature_importances"])
            features.extend(f)
            imp.extend(i)

        # Store the mean importance, and the number of time used, per feature
        count_f = self.__format_name_and_associated_values(self, features, imp)

        features = [f for f in count_f.keys()]
        times_used_all_splits = [count_f[f][0] for f in count_f.keys()]
        importance_or_usage_or_ = [count_f[f][1] for f in count_f.keys()]
        return features, times_used_all_splits, importance_or_usage_or_


class ResultsRF(Results):
    """
    Contains all results of an experimental design, is an attribute of class Experimental_design, and gives info to class "Plotter".
    Has results of all algorithms for all splits on one experimental design (so almost only numbers/floats/ints).
    Can be kept in RAM as it is not supposed to be too big, and prevents the reading/writing of models and splits files.
    """

    def _get_features_importance(self, model):
        features = []
        importances = []
        for DT in model.estimators_:
            f = DT.feature_names_in_
            i = DT.feature_importances_
            zipped = list(zip(f, i))
            feat_sort = sorted(zipped, key=lambda x: x[1])
            top_five = feat_sort[:5]
            f, i = zip(*top_five)
            features.extend(f)
            importances.extend(i)
        zipped = zip(features, importances)
        zipped_complet = zip(model.feature_names_in_, model.feature_importances_)
        return zipped, zipped_complet

    def _aggregate_features_info(self):
        """
        When all splits are done and saved, aggregate feature info from every split to compute stats
        from all splits, concatenate in the same list the name of features, and another list their importance
        """
        features = []
        imp = []
        features_complet = []
        imp_complet = []
        # Get values of all splits in two lists
        for split in self.results.keys():
            f, i = zip(*self.results[split]["feature_importances"][0])
            features.extend(f)
            imp.extend(i)
            f_complet, i_complet = zip(*self.results[split]["feature_importances"][1])
            features_complet.extend(f_complet)
            imp_complet.extend(i_complet)

        # Store the mean importance, and the number of time used, per feature
        dict_top = self.__format_name_and_associated_values(self, features, imp)
        dict_complet = self.__format_name_and_associated_values(self, features_complet, imp_complet)

        # Top 5 of sub-classifier (DT) for features, and times_used
        # Top 5 of sub-classifier (DT) for importance_(mean global importance in RF)
        features = [f for f in dict_top.keys()]
        times_used_all_splits = [dict_top[f][0] for f in dict_top.keys()]
        importance_or_usage_or_ = [str(dict_top[f][1]) + "_(" + str(dict_complet[f][1]) + ")" for f in dict_top.keys()]
        return features, times_used_all_splits, importance_or_usage_or_



