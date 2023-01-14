---
layout: base
title:  Machine Learning
---


1. Define learning configurations
The following instructions are for the DEFINE LEARNING CONFIGS section.

If you're not comfortable with these parameters, you can safely keep the default values and jump to the next section.

First, before choosing a Cross Validation (CV) search type, you need to understand the principle of CV.

The method consist in separating the dataset in n sections. At each iteration, the first or the next section will be used as the test set and the other sections will form the training set. It allows us to train and test the model on all the dataset. Furthermore, the mean accuracy over the folds is a better measurement of the performance of the models.

The number of folds defines the number of time the model(s) will be trained, and the number of division in the dataset.

We use CV in order to make sure the model doesn't overfit, we keep a sample of the dataset to test it at the end. If the algorithm is overfitting, it will make a lot of errors when presented a new set of data. This also allows us to make sure the algorithm is tested on all samples.

For more details, see this explanation.

The ability of a search algorithm is to train a set of models with a set of parameters, and compute a metric tested combination. This metric is most of the time the accuracy (the number of correct predictions over the total number of predictions (the number of samples)).

After the computation, the algorithm is able to find the model combined with the parameters that perform best, in the tested combinations.

The GridSearchCV is a search algorithm using CV that test every possible combination of parameters, like in a grid. This method is effective but may take a long time to run and may test useless combination.

The RandomizedSearchCV comes as a counterpoint and take random combinations of parameters. This method allow more values to be tested and runs faster but isn't as rigorous as the GridSearchCV.

In the SELECT CV SEARCH TYPE panel, you can choose either GridSearchCV or RandomizedSearchCV.

You can set the number of folds in the NUMBER OF CROSS VALIDATION FOLDS.

The number of processes in the Number of processes field is the number of parallel job you want to run. Two is enough to increase the speed of computation. More processes might slow down to crash your PC.

2. Define learning algorithms
The following instructions are for the DEFINE LEARNING ALGORITHMS section.

The AVAILABLE ALGORITHMS are:

Decision Tree
Random Forest
SCM
Random SCM
The first classifier implement a regular decision tree. To make a prediction, the data is the input of the root node. The root node, as the others, has a threshold for one feature : for example
cholesterol≥2
. If the value validate the threshold, it goes to the right node, otherwise it goes to the left, until it reach a leaf. The leaf assigns a class to the sample.

The second classifier, the random forest, is a decision tree (DT) ensemble that classify independently the sample. Each DT vote the class of the sample. The class that has the most vote is assign to the sample.

The Set Covering Machine (SCM) is a combination of rules. For example, if the cholesterol is greater than 2 g/l OR insulin is greater than 140 mg/dL AND insulin is less than 199 mg/dL.

The last classifier is the Random SCM. As the random forest is a voting decision tree ensemble, the random SCM is a voting SCM ensemble.

You have to tick at least one algorithms.

But because of their differences, some may perform better than others on different datasets. It is advised to take at least one SCM-type and one DecisionTree-type algorithms.

If you want to add scikit-learn algorithms that isn't in the available algorithms, you can in the ADD SKLEARN ALGORITHMS.

You need to complete the import and specify the grid search parameter (for the CV search algorithm).



To add a full custom model, you need to add it to the configuration file located at metabodashboard/conf/SupportedModel.py.
Add a dictionary containing the NON-INSTANTIATED class and the param grid. Format is the following ( change only the attribute xxx)
~~~  
    "_Printedname": {
          "function": _non-instantiatedclass,
          "ParamGrid": {
              "p1": [0.5, 1., 2.],
              "p2": [1, 2, 3, 4, 5],
              ...
          }
      },
~~~  
After adding your configuration, reboot MeDIC by stopping and restarting the launcher.
The algorithm should be in the AVAILABLE ALGORITHMS section with his printed name.
Note, the custom model are in the save file (.mtxp) and will be restored.

