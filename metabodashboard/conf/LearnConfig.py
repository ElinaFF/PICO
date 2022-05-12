import numpy as np
from pyscm.scm import SetCoveringMachineClassifier
from randomscm.randomscm import RandomScmClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

LEARN_CONFIG = {
    "Nsplit": 40,
    "UseNormalized": True,
    "CV_folds": 5,
    "Algos": {
        "DecisionTree": {
            "function": DecisionTreeClassifier,
            "ParamGrid": {
                "max_depth": [1, 2, 3, 4, 5, 10],
                "min_samples_split": [2, 4, 6, 8, 10]
            }
        },
        "RandomForest": {
            "function": RandomForestClassifier,
            "ParamGrid": {
                "n_estimators": [1, 2, 4, 10, 30, 70, 100, 500, 1000]
            }
        },
        "SVM_L1": {
            "function": LinearSVC,
            "ParamGrid": {
                "C": np.logspace(-5, 5, 20)
            }
        },
        "SCM": {
            "function": SetCoveringMachineClassifier,
            "ParamGrid": {
                "p": [0.5, 1., 2.],
                "max_rules": [1, 2, 3, 4, 5],
                "model_type": ["conjunction", "disjunction"]
            }
        },
        "RandomSCM": {
            "function": RandomScmClassifier,
            "ParamGrid": {
                "p": [0.5, 1., 2.],
                "max_rules": [1, 2, 3, 4, 5],
                "model_type": ["conjunction", "disjunction"]
            }
        },
    }
}
