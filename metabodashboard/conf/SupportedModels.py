import numpy as np
from pyscm.scm import SetCoveringMachineClassifier
from randomscm.randomscm import RandomScmClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

LEARN_CONFIG = {
    "DecisionTree": {
        "function": DecisionTreeClassifier,
        "ParamGrid": {
            "max_depth": np.linspace(1, 10, dtype=int),
            "min_samples_split": np.linspace(0.01, 1, 10),
            "max_features": ["auto", "sqrt", "log2"],
        },
        "importance_attribute": "feature_importances_",
    },
    "RandomForest": {
        "function": RandomForestClassifier,
        "ParamGrid": {
            "n_estimators": np.linspace(20, 80, dtype=int),
            "max_depth": np.linspace(1, 5, dtype=int),
            "min_samples_split": np.linspace(0.01, 1, 10),
            "max_features": ["auto", "sqrt", "log2"],
            "max_samples": np.linspace(0.2, 1, 10),
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
