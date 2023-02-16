---
layout: base
title:  Results
---

# Results

PCA(relation linéaires) umap(relation non lihnéaire) graphique accuracy (graphic pour chaque split), tableau de résultat (descr metrics comment les intèrbpéter) matrice de confusion (ce que ça veut dire) feature importance (tableau utilisation) strip chart
All graphs can be saved and will be saved by default in SVG format. This can be changed in the ResultAgregatedTab.py file at the beginning of the file.



## Choice of results to explore
There is two dropdown menus automatically detecting the classification designs and the algorithms that were used. The user can select which design and which algorithm to explore, and then click on the load button to update the figures and tables.
The “current experiment info” bloc displays the number of samples used, the repartition of samples as percentages, and the number of samples in each class (to see potential unbalanced classes).

## Data
The idea of this section is to detect if the classes (colors) are visually distributed in different clusters. It also allows the user to have an overview of the pertinence of the features selected by the model.

##### PCA
The PCA extracts the dimensions with the bigger variance to highlight the clusters in the data. The PCA detects linear relationships in the data. For more information see the wikipedia article.
The slider under the figure allows the visualization of the PCA computed on a certain number of features (indicated on the slider). The ‘used’ indicator refers to the number of features used by the model to give a prediction. The ‘all’ indicator refers to the PCA computed on all the data. 
##### UMAP
The UMAP is a dimensionality reduction technique to highlight the non-linear relationships in the data. For more detail see the official page. The UMAP can be used in the same way as the tSNE but is generally considered better. One of the differences is the random initialisation for the tSNE as opposed to the Graph Laplacian for the UMAP. Another problem of tSNE is the use of the Kullback-Leibler (KL) divergence which makes it impossible to preserve global distances, see more here.
It is important to consider non-linear relationships in biological data, which is composed of complex phenomenon.
##### 2D & 3D
Those two figures are only meant to visualize the two and three most important features without further modifications.

## Algorithm
This section tries to provide basic performance metrics about the model. It helps determine if the model is reliable enough to continue the analysis. 

##### Accuracy plot
It displays the train accuracy and the test accuracy for each split. This way, the user can know which model is more or less performant on the learning data. Moreover, the type of graph can show if the results are stable. If not, it indicates errors (like wrong labeling) or important variability in the data. Because of the fat data situation often encountered in metabolomics, it can also be a sign that the models have trouble learning a representation (often due to a lack of samples).

Overfitting can also be detected by this plot, when the accuracy on the train data is often 100% or close to that, and the test accuracy is much lower. There is no clear threshold to identify overfitting, but generally a difference of at least 15-20% gives a good sign. Overfitting is not good because it means that the model has learned very well the training data, but will not be able to generalize this comprehension and its predictive performance on new data will be poor. See this link for more details (https://machinelearningmastery.com/overfitting-machine-learning-models/).

##### Metrics table
Table that gives the mean and standard deviation of multiple metrics on the models. The accuracy is the proportion of correctly predicted samples. Balanced accuracy takes into account the asymmetrical repartition of the samples through the classes. To see more, see scikit-learn’s documentation on accuracy (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score) and on balanced accuracy (https://scikit-learn.org/stable/modules/model_evaluation.html#balanced-accuracy-score)

“Intuitively, precision is the ability of the classifier not to label as positive a sample that is negative, and recall is the ability of the classifier to find all the positive samples.” (https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics). The f1_score is the mean of the precision and the recall seen before.

The ROC curve compares the true positive rate and the false positive rate. If the AUC (Area Under the Curve) is high, it means that the model is able to produce a lot of correct positive predictions for few false positives. The opposite means that the model has a hard time making true positive predictions. For more details, see (https://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics)


##### Splits number for Confusion matrix
In this section, the user can select one particular split with the dropdown menu to display the confusion matrix of the model. The values are normalized so it shows the repetition of the prediction for each class. Also, it can shows if the model can detect/undertsand better one class versus the other. Because in this case, there is a greater proportion of the less understood class predicted as the better understood class.

We are working to add a table with the hyperparameter of the model in this section.


## Features

##### Table of 10 features
Through all the splits, the uses and the importances of the features can change. However, when a feature is frequently used, and/or has great mean importance, it means that the feature can be a useful marker to identify the class of a sample.
Thus, the table presents the top 10 most important features and the number of times they were used.

##### Stripchart of feature
The stripchart is divided in parts (colors), where each part represents a class. Moreover, each part is the stack of the values of the data for the associated class. Thus, it helps to identify a feature where the values greatly differ for each class.

## DT Tree
Decision tree algorithms can produce a representation of the process used to make the prediction. (mettre une photo/exemple ^^)














