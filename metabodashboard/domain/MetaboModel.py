import os
import pickle

import sklearn
from sklearn.model_selection import GridSearchCV


class MetaboModel:
    def __init__(self, grid_search_configuration: dict, model: sklearn):
        self.grid_search_param = grid_search_configuration
        self.model = model

    def train(self, folds: int, X_train: list, y_train: list) -> sklearn:
        gridsearch = GridSearchCV(self.model, self.grid_search_param, cv=folds)
        gridsearch.fit(X_train, y_train)
        return gridsearch.best_estimator_


#TODO: dump model in constructor
