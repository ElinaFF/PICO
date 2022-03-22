import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from collections import Counter



class Results:
    """
    Contains all results of an experimental design, is an attribute of class Experimental_design, and gives info to class "Plotter".
    Has results of all algorithms for all splits on one experimental design (so almost only numbers/floats/ints).
    Can be kept in RAM as it is not supposed to be too big, and prevents the reading/writing of models and splits files.
    """
    def __init__(self, algos_name: list, splits_number: int):
        self.algos_name = algos_name
        self.splits_number = [str(s) for s in range(splits_number)]
        self.results = {}
        self._initialise_results_dict()

    def _initialise_results_dict(self):
        self.results = {a for a in self.algos_name}
        for key in list(self.results.keys()):
            self.results[key] = {s for s in self.splits_number}

    def add_results_from_one_algo_on_one_split(self, model, y_train_true: list, y_train_pred: list,
                                               y_test_true: list, y_test_pred: list, algo_name: str, split_number: str):
        """
        Besoin modèle pour extraire features, features importance
        Besoin des y_true, des y_pred, des noms de samples pour le train et le test

        Fonction appelée à chq fois qu'un split a fini de rouler, pour stocker les info nécessaires à la production des
        graphique pour l'onglet résultat
        X : entièreté du dataset (autant train que test) c'est simplement pour voir le clustering de tous les individus
        """
        self.results[algo_name][split_number]["train_accuracy"] = accuracy_score(y_train_true, y_train_pred)
        self.results[algo_name][split_number]["test_accuracy"] = accuracy_score(y_test_true, y_test_pred)

        self.results[algo_name][split_number]["feature_importances"] = self._get_features_importances(model, algo_name)

        self.results[algo_name][split_number]["Confusion_matrix"] = self._produce_conf_matrix(y_test_true, y_test_pred)

        if split_number == self.splits_number[-1]:
            self.results["info_expe"] = self._produce_info_expe
            self.results[algo_name]["features_table"] = self.produce_features_importance_table(model, algo_name)



    def _produce_conf_matrix(self, y_test_true: list, y_test_pred: list):
        labels = list(set(y_test_true))
        return confusion_matrix(y_test_true, y_test_pred, labels=labels)

    def produce_info_expe(self, y_train_true, y_test_true):
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

    def _get_features_importances(self, model, algo_name):
        if algo_name == "DecisionTree":
            return self._get_features_importance_DecisionTree(model)
        elif algo_name == "RandomForest":
            return self._get_features_importance_RandomForest(model)
        elif algo_name == "SVM":
            return
        elif algo_name == "SCM":
            return
        elif algo_name == "randomSCM":
            return
        else:
            #TODO : implement method to deal with non-default algorithms
            raise NotImplementedError("the algorithm name ({}) does not correspond to a method".format(algo_name))


    def _get_features_importance_DecisionTree(self, model):
        features = model.feature_names_in_
        importances = model.feature_importances_
        zipped = list(zip(features, importances))
        #{f: importances[i] for i, f in enumerate(features)}
        return zipped

    def _aggregate_features_info_DecisionTree(self):
        features = []
        times_used_all_splits = []
        importance_or_usage_or_ = []
        return features, times_used_all_splits, importance_or_usage_or_

    def _get_features_importance_RandomForest(self, model):
        for DT in model.estimators_:
            features = DT.feature_names_in_
            importances = DT.feature_importances_

        return

    def produce_features_importance_table(self, model, algo_name: str):
        features = []
        times_used_all_splits = []
        importance_or_usage_or_ = []
        if algo_name == "DecisionTreeClassifier":
            features, times_used_all_splits, importance_or_usage_or_ = self._aggregate_features_info_DecisionTree()


        d = {"features": features, "times_used": times_used_all_splits, "importance_usage": importance_or_usage_or_}
        df = pd.DataFrame(data=d)
        return df

    def produce_accuracy_plot_all(self, name_algo: str):
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
            y_splits_acc.append(self.results[name_algo][s]["train_accuracy"])
            traces.append("train")
            y_splits_acc.append(self.results[name_algo][s]["test_accuracy"])
            traces.append("test")

        d = {"splits": x_splits_num, "accuracies": y_splits_acc, "color": traces}
        df = pd.DataFrame(data=d)

        return df
