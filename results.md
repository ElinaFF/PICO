---
layout: base
title:  Results tab
---

# Results tab
{: .no_toc}
_ _ _ _
There is two dropdown menus automatically detecting the classification designs and the algorithms that were used. The user can select which design and which algorithm to explore, and then click on the load button to update the figures and tables.
The “current experiment info” bloc displays the number of samples used, the repartition of samples as percentages, and the number of samples in each class (to see potential unbalanced classes).
All graphs can be saved and will be saved by default in SVG format. This can be changed in the ResultTab.py file at the beginning of the file.

Important to note for all figures and results exploration where a certain number of features is displayed : if the number of used features in the model is smaller than the number of features (or) top features displayed,
the first features will be in the indicated order, and the rest will be features randomly selected. For example, if an SCM model uses only 3 features to make its prediction, the swarm plot in the Results > Features section will still display
10 features, but only the first three will be relevant. The other 7 used to complete the figure were randomly selected and are not specifically important.
{:.note title="Attention"}

* toc
{:toc}
  
## Data
The idea of this section is to detect if the classes are visually distributed in different clusters. It also allows the user to have an overview of the pertinence of the features selected by the model.

The slider under the figure allows the visualization of the PCA computed on a certain number of features (indicated on the slider). The ‘used’ indicator refers to the number of features used by the model to give a prediction. The ‘all’ indicator refers to the PCA computed on all the data.

##### PCA
The PCA extracts the dimensions with the bigger variances to highlight the clusters in the data. The PCA detects *linear* relationships in the data. For more information see the [wikipedia article](https://en.wikipedia.org/wiki/Principal_component_analysis).
 
##### UMAP
The UMAP is a dimensionality reduction technique to highlight the *non-linear* relationships in the data. For more detail see the official page. The UMAP can be used in the same way as the tSNE but is generally considered better. One of the differences is the random initialisation for the tSNE as opposed to the Graph Laplacian for the UMAP. Another problem of tSNE is the use of the Kullback-Leibler (KL) divergence which makes it impossible to preserve global distances, see more here.
It is important to consider non-linear relationships in biological data, because it has many complex phenomena and interactions.

##### 2D & 3D
Those two figures are only meant to visualize the two and three most important features without transformations.

## Algorithm
This section provides basic performance metrics of the model. It helps determine if the model is reliable enough to continue the analysis. 

##### Accuracy plot
It displays the train accuracy and the test accuracy for each split. This way, the user can know which model is more or less performant on the learning data. Moreover, the type of graph can show if the results are stable. If not, it indicates errors (like wrong labeling) or important variability in the data. Because of the fat data situation often encountered in metabolomics, it can also be a sign that the models have trouble learning a representation (due to a lack of samples).

Overfitting can also be detected by this plot, when the accuracy on the train data is close to 100%, and the test accuracy is much lower. There is no clear threshold to identify overfitting, but generally a difference of at least 15-20% gives a good sign. Overfitting is not good because it means that the model has learned very well the training distribution, but will not be able to generalize this comprehension. Its predictive performance on new data will be poor. See this [link](https://machinelearningmastery.com/overfitting-machine-learning-models/) for more details.

##### Metrics table
This table gives the mean and standard deviation of multiple metrics of the models. 

Accuracy
: The accuracy is the proportion of correctly predicted samples. See scikit-learn’s documentation on [accuracy](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score)

Balanced accuracy 
: takes into account the asymmetrical repartition of the samples through the classes. See scikit-learn’s documentation on [balanced accuracy](https://scikit-learn.org/stable/modules/model_evaluation.html#balanced-accuracy-score).

Precision and Recall
: “Intuitively, precision is the ability of the classifier not to label as positive a sample that is negative, and recall is the ability of the classifier to find all the positive samples.” [SKlearn documentation](https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics). 

F1-score
: The f1_score is the mean of the precision and the recall.

ROC curve
: The ROC curve compares the true positive rate and the false positive rate. If the AUC (Area Under the Curve) is high, it means that the model is able to produce a lot of correct positive predictions for few false positives. The opposite means that the model has a hard time making true positive predictions. [For more details.](https://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics)


##### Splits number for Confusion matrix
In this section, the user can select one particular split with the dropdown menu to display the confusion matrix of the model. The values are normalized so it shows the repartition of predictions for each class. Also, it can show if the model detects/undertsands better one class versus the other. Because in that case, there is a proportion of the less understood class that is predicted as the better understood class.

We are working to add a table with the hyperparameters of the model in this section.
{:.note}


## Features

##### Table of 10 features
Throughout the splits, the uses and the importances of features can change. However, when a feature is frequently used and has great mean importance, it means that the feature is a useful marker to identify the class of a sample. In biological terms, it 
means that this feature might be a potential biomarker that behaves differently in the two samples group.
Thus, the table presents the top 10 most important features, the number of times they were used and their mean importances.

The 'export' button allows the user to download a file with the entire list of features (even those not used by the models), with their number of use and their mean importance. 

##### Swarmplot of features
The figure has the same top10 features as the table just beside it (with the most important on the left, and the least on the right). So on the *x* axis there is the 10 features and on the *y* axis it is the normalized abundance of hte features.
each point represents the abundance of a corresponding feature for a sample. Thus, visually exploring the difference between the cluster of samples (points) in each class for a feature can help determine if the specific feature is of interest.
For example, the top 1 feature could have a cluster near 0 for the samples of the control group, and a cluster near an abundance of 3 for the compared group.

## DT Tree
Decision tree algorithms are easy to visualize and the sklean implementation can produce a representation of the process used to make the prediction. It displays the best model of all splits and is mostly to help neophytes understand a little bit better how this specific algorithm works.














