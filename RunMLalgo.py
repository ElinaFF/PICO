import importlib, os
from sklearn.model_selection import GridSearchCV
import pickle as pkl



class runAlgo:
    def __init__(self, algo_name, cv_folds, params, algo_import=""):
        self.name = algo_name  # Name of the algorithm, ex: DecisionTreeClassifier
        self.imp = algo_import  # modules imports to get the algo
        if self.imp != "":
            self.algo = self._import_the_algorithm()
        self.gs = 0
        self.params = params  # (dictionary) parameters to explore with the gridsearch
        self.cv_folds = cv_folds  # number of folds to do gridsearch


    def learn(self, options_dict):
        """
        Will be the function to be parallelized through processes
        :param options_dict: Dictionary containing the split options to run an algo on a split's dataset
        :return: Nothing, saves results to file
        """

        Xtrain = options_dict["Xtrain"]
        Xtest = options_dict["Xtest"]
        ytrain = options_dict["ytrain"]
        ytest = options_dict["ytest"]
        design_name = options_dict["design_name"]  # name of the explored design, ex: ctrl_vs_sick, pos_vs_neg
        split_no = options_dict["split_no"]  # number of the split

        # do GridSearchCV and save results to file
        train_predict, test_predict = self._gridSearch(self.params, self.cv_folds, Xtrain, Xtest, ytrain)
        self._save_results_to_file(design_name, split_no, train_predict, test_predict, ytrain, ytest)

    def _import_the_algorithm(self):
        imports = self.imp.split(".")

        m = importlib.import_module("." + imports[0], package="sklearn")
        for i in imports[1:]:
            m = getattr(m, i)

        a = getattr(m, self.name)
        return a

    def _gridSearch(self, params, folds, Xtrain, Xtest, ytrain):
        self.gs = GridSearchCV(self.algo, params, cv=folds)
        self.gs.fit(Xtrain, ytrain)
        # Predict on train.
        train_predict = self.gs.predict(Xtrain)
        # Predict on test.
        test_predict = self.gs.predict(Xtest)
        return train_predict, test_predict

    def _save_results_to_file(self, design_name, split_no, train_predict, test_predict, train_targets, test_targets):
        # Save to file.
        with open(os.path.join("Results", "{}_{}_{}.pkl".format(design_name, split_no, self.name)), "wb") as fo:
            pkl.dump(self.gs, fo)
            pkl.dump(train_predict, fo)
            pkl.dump(test_predict, fo)
            pkl.dump(train_targets, fo)
            pkl.dump(test_targets, fo)

