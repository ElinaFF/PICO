import os
import pickle

import sklearn
from sklearn.model_selection import GridSearchCV

#TODO: implement randomSearch
#TODO : get_specific_results, retourne les attributs nécessaires de feat importance pour n'importe quel algo sklearn
#TODO : (suite) , faire un genre de moule d'algo, goulot d'étranglement de nom de méthode
class MetaboModel:
    def __init__(self, model: sklearn, grid_search_configuration: dict):
        self.grid_search_param = grid_search_configuration
        self.model = model

    def train(self, folds: int, X_train: list, y_train: list) -> sklearn:
        gridsearch = GridSearchCV(self.model(), self.grid_search_param, cv=folds)
        gridsearch.fit(X_train, y_train)
        return gridsearch.best_estimator_


#TODO: dump best model ?
