import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.decomposition import PCA
#import umap


class Results:
    """
    Contains all results of an experimental design, is an attribute of class Experimental_design, and gives info to class "Plotter".
    Has results of all algorithms for all splits on one experimental design (so almost only numbers/floats/ints).
    Can be kept in RAM as it is not supposed to be too big, and prevents the reading/writing of models and splits files.
    """
    def __init__(self, algos_name: list, splits_number: list):
        self.algos_name = algos_name
        self.splits_number = splits_number
        self.results = {}
        self._initialise_results_dict()

    def _initialise_results_dict(self):
        self.results = {a for a in self.algos_name}
        for key in list(self.results.keys()):
            self.results[key] = {s for s in self.splits_number}

    def add_results_from_one_algo_on_one_split(self, model, X, y_train_true: list, y_train_pred: list,
                                               y_test_true: list, y_test_pred: list, algo_name: str, split_number: str):
        """
        Besoin modèle pour extraire features, features importance
        Besoin des y_true, des y_pred, des noms de samples pour le train et le test
        """
        self.results[algo_name][split_number]["train_accuracy"] = accuracy_score(y_train_true, y_train_pred)
        self.results[algo_name][split_number]["test_accuracy"] = accuracy_score(y_test_true, y_test_pred)

        self.results[algo_name][split_number]["feature_importances"] = self._get_features_importances(model)

        self.results[algo_name][split_number]["PCA"] = self._produce_PCA(X)
        self.results[algo_name][split_number]["UMAP_2D"] = self._produce_UMAP_2D(X)
        self.results[algo_name][split_number]["Confusion_matrix"] = self._produce_conf_matrix(X)



    def _get_features_importances(self, model):
        features = model.feature_names_in_
        importances = model.feature_importances_
        return {f: importances[i] for i, f in enumerate(features)}

    def _produce_PCA(self, X: pd.DataFrame):
        x = X.to_numpy()
        pca = PCA(n_components=2)
        return pca.fit_transform(x)

    def _produce_UMAP_2D(self, X: pd.DataFrame):
        x = X.to_numpy()
        umap_2d = umap.UMAP(n_components=2, init='random', random_state=13)
        return umap_2d.fit_transform(x)

    def _produce_conf_matrix(self, y_test_true: list, y_test_pred: list):
        labels = list(set(y_test_true))
        return confusion_matrix(y_test_true, y_test_pred, labels=labels)
