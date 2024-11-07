import pandas as pd
import sklearn
from sklearn.model_selection import RandomizedSearchCV
from ..service import init_logger, log_exceptions

# TODO: implement randomSearch
# TODO : get_specific_results, retourne les attributs nécessaires de feat importance pour n'importe quel algo sklearn
# TODO : (suite) , faire un genre de moule d'algo, goulot d'étranglement de nom de méthode


class MetaboModel:
    def __init__(self, model: sklearn, grid_search_configuration: dict, importance_attribute: str):
        self._logger = init_logger()
        self.train = log_exceptions(self._logger)(self.train)  # Apply log_exception decorator
        self.grid_search_param = grid_search_configuration
        self.model = model

        self.importance_attribute = importance_attribute

    def train(
        self,
        folds: int,
        X_train: pd.DataFrame,
        y_train: list,
        cv_algorithms: sklearn.model_selection,
        cv_algorithm_config,
        number_of_processes: int, seed: int
    ) -> sklearn:
        if cv_algorithms == RandomizedSearchCV:
            search = cv_algorithms(
                self.model(random_state=seed),
                self.grid_search_param,
                cv=folds,
                random_state=seed,
                n_jobs=number_of_processes,
                n_iter=cv_algorithm_config[0]["value"],
            )
        else:
            search = cv_algorithms(
                self.model(random_state=seed),
                self.grid_search_param,
                cv=folds,
                n_jobs=number_of_processes,
            )
        
        spacer: str = f"\n{'-'*30}\n"
        header: str = f"\n***** train.search.fit {cv_algorithms = }{spacer}"
        message: str = f"{header}cv{folds:d} folds | X_train (2 first rows / {len(X_train)}):\n{X_train.head(2)}{spacer}{y_train = }\nLength = {len(y_train)}{spacer}"
        try:
            self._logger.debug(f"{header} {cv_algorithms = } launched ...")
            search.fit(X_train, y_train)
        except Exception as e:
            self._logger.error(message)
            raise
        else:
            self._logger.debug(message + "Completed")
        
        return search.best_estimator_

    def get_importance_attribute(self):
        return self.importance_attribute

# TODO: dump best model ?
