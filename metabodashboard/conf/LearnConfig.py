import numpy as np
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors

LEARN_CONFIG={
    "Nsplit": 40,
    "UseNormalized": True,
    "CV_folds": 5,
    "Algos":{
        "DecisionTree":{
            "function": DecisionTreeClassifier,
            "ParamGrid": {
                "max_depth": [1, 2, 3, 4, 5, 10],
                "min_samples_split": [2, 4, 6, 8, 10]
            }
        },
        "RandomForest":{
            "function": RandomForestClassifier,
            "ParamGrid": {
                "n_estimators": [1, 2, 4, 10, 30, 70, 100, 500, 1000]
            }
        },
        "SVM_L1":{
            "function": LinearSVC,
            "ParamGrid": {
                "C": np.logspace(-5, 5, 20)
            }
        },
    }
}








