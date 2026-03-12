---
layout: base
title:  Machine Learning tab
---

# Machine Learning tab
{: .no_toc}
_ _ _ _

The machine learning tab is divided in two sections : the hyperparameters (HP) optimization and the selection of algorithms.
If you're not comfortable with the HPs exploration, you can safely keep the default values and jump to the next section.

* toc
{:toc}

### Cross validation

Hyperparameters (HPs)
: Parameters that can be changed before the learning phase and will impact the prediction performances.

Cross validation (CV)
: Process that divides the data in *k* parts (k-folds) and each part will be used to test a model while the remaining parts are used to train the model with a combination of HPs.

GridSearch
: Method that will test every HPs combination possible in what was given to explore. It is the standard default method. It is effective but may take a long time to run and may test useless combination.

RandomSearch
: Method that will sample a distribution to choose values to test for each HP listed. It has the reputation to better cover the space of HPs. It allows more values to be tested and runs faster but isn't as rigorous as the GridSearchCV.

Bayesian optimization
: Another method of HPs combination. **NOT IMPLEMENTED YET**.


We use CV in order to make sure the model doesn't overfit, we use the validation set to optimize the HPs and keep the test set unseen by the model. 
To select the best HP combination, the search algorithm will compute a metric (often the accuracy) on each combination and choose the best.


###### Example

For a 5-folds CV, the train set defined earlier in the splits section will be divided in 5 sections. One by one, each of the section will become the validation set on which a combination of HPs will be tested.
In case of a Gridsearch, the HP to test would look something like this :
~~~
{
    p1: [1, 3, 6],
    p2: [10, 50]
}
~~~

Then 6 combinations would each be tested 5 times (on the 5-folds).

In case of a RandomSearch, the HP would look something like this:
~~~
{
    p1: Normal(0.1, 8), ## A reviser, pas ok
    p2: Normal(0, 75)
}
~~~
Then X combinations would be tested 5 times, and the values in the combinations would be picked according to the distributions.



### Algorithms

The AVAILABLE ALGORITHMS are:

* Decision Tree (DT)
* Random Forest
* Set Covering Machine (SCM)
* Random Set Covering Machine (RandomSCM)

For some computers on Windows there is an error that occurs when trying to run the SCM or the RandomSCM (<a href="https://github.com/ElinaFF/PICO/issues/134">issue 134</a>). The cause is still unknown.
{: .note title="Warning"}

The first classifier implement a regular **decision tree**. To make a prediction, the data is the input of the root node. The root node, as the others, has a threshold for one feature : for example
cholesterol ≥ 2. If the value validate the threshold, it goes to the right node, otherwise it goes to the left, until it reach a leaf. The leaf assigns a class to the sample.

The second classifier, the **random forest**, is a DT ensemble that classify independently the sample. Each DT vote the class of the sample. The class that has the most vote is assign to the sample.

The **Set Covering Machine (SCM)** is a combination of rules. For example, if the cholesterol is greater than 2 g/l OR insulin is greater than 140 mg/dL AND insulin is less than 199 mg/dL.

The last classifier is the **Random SCM**. As the random forest is a voting decision tree ensemble, the random SCM is a voting SCM ensemble.

You have to tick at least one algorithm.
Because of their differences, some may perform better than others on different datasets. It is advised to take at least one SCM-type and one DecisionTree-type algorithms, as well as one ensemble type.


###### Add scikit-learn algorithm

The PICO support the addition of Sklearn models as long as they have a method to extract the importance of features in the prediction.
After clicking on the button to add a Sklearn algorithms, the user must give the import information of the algorithm. The PICO will try to import and verify that it is compatible. If it is, the user can choose to add the HP to explore by using the table provided by the PICO, or to do it manually.
The user must also select which attribute contains the features importances.

###### Add custom algorithm

To add a full custom model, you need to add it to the configuration file located at `pico/conf/SupportedModel.py`.
Add a dictionary containing the NON-INSTANTIATED class and the param grid. Format is the following :
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
After adding your configuration, reboot the PICO by stopping and restarting.
The algorithm should be in the AVAILABLE ALGORITHMS section with his printed name.
Note, the custom model are in the save file (.mtxp) and will be restored.

