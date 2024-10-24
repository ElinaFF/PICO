import numpy as np
from pyscm.scm import SetCoveringMachineClassifier
from randomscm.randomscm import RandomScmClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

LEARN_CONFIG_GS = {
    "DecisionTree": {
        "function": DecisionTreeClassifier,
        "ParamGrid": {
            "max_depth": [1, 2, 3, 4, 5, 6],
            "min_samples_split": [2, 4, 6, 8, 10],
            "max_features": ["sqrt", "log2"],
        },
        "importance_attribute": "feature_importances_",
    },
    "RandomForest": {
        "function": RandomForestClassifier,
        "ParamGrid": {
            "n_estimators": [5, 10, 30, 70, 100, 200, 500],
            "max_depth": [1, 2, 3, 4, 5],
            "min_samples_split": [2, 4, 6, 8, 10],
        },
        "importance_attribute": "feature_importances_",
    },
    "SCM": {
        "function": SetCoveringMachineClassifier,
        "ParamGrid": {
            "p": np.linspace(0.01, 3, 10),
            "max_rules": np.linspace(1, 60, 10, dtype=int),
            "model_type": ["conjunction", "disjunction"],
            "max_features": ["auto", "sqrt", "log2"],
        },
        "importance_attribute": "feature_importances_",
    },
    "RandomSCM": {
        "function": RandomScmClassifier,
        "ParamGrid": {
            "p": np.linspace(0.01, 3, 10),
            "n_estimators": np.linspace(20, 80, 10, dtype=int),
            "model_type": ["conjunction", "disjunction"],
            "max_features": ["auto", "sqrt", "log2"],
            "max_samples": np.linspace(0.2, 1, 10),
        },
        "importance_attribute": "feature_importances_",
    },
}


LEARN_CONFIG_RS = {
    "DecisionTree": {
        "function": DecisionTreeClassifier,
        "ParamGrid": {
            "max_depth": np.arange(1, 7, step=1, dtype=int), #[1, 2, 3, 4, 5, 6],
            "min_samples_split": np.arange(2, 20, step=2, dtype=int), #[2, 4, 6, 8, 10],
            "max_features": ["sqrt", "log2"],
        },
        "importance_attribute": "feature_importances_",
    },
    "RandomForest": {
        "function": RandomForestClassifier,
        "ParamGrid": {
            "n_estimators": np.arange(5, 400, step=10, dtype=int), #[5, 10, 30, 70, 100, 200, 500],
            "max_depth": np.arange(1, 6, step=1, dtype=int), #[1, 2, 3, 4, 5],
            "min_samples_split": np.arange(2, 20, step=2, dtype=int), #[2, 4, 6, 8, 10],
        },
        "importance_attribute": "feature_importances_",
    },
    "SCM": {
        "function": SetCoveringMachineClassifier,
        "ParamGrid": {
            "p": np.linspace(0.01, 3, 10),
            "max_rules": np.linspace(1, 60, 10, dtype=int),
            "model_type": ["conjunction", "disjunction"],
        },
        "importance_attribute": "feature_importances_",
    },
    "RandomSCM": {
        "function": RandomScmClassifier,
        "ParamGrid": {
            "p": np.linspace(0.01, 3, 10),
            "n_estimators": np.arange(5, 200, step=10, dtype=int)
            "model_type": ["conjunction", "disjunction"],
        },
        "importance_attribute": "feature_importances_",
    },
}
