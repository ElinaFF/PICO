---
layout: base
title:  Splits
---
# Splits
{: .no_toc}
_ _ _ _

This tab is used to define all the parameters affecting the samples : the matrices, the classes, the pairing, the number of splits, etc.

This step exists in the pipeline mainly because of the nature of metabolomic data, or more generally biological data : it has few samples, but hundreds or thousands of features per sample. This situation is called *fat data*, as 
opposed to *big data* where there is tens of thousands of samples to learn from and each of them is of a reasonable size. See more below in the Splits section.

* toc
{:toc}


## Files

For data and metadata, the supported files are excel or csv.
If the error "*Rows must have an equal number of columns*" occurs when loading a file, it means that some lines don't have cells for all columns.

Normalization for Progenesis
: Use this to specify if you are using a matrix produced by Progenesis or another matrix with samples as lines and features as columns. Also, if it is from Progenesis, it can be either the raw abundance values or the normalized.

Retention time below 1min
: Progenesis produced matrices identify their features with the retention time and the m/z ratio. It allows a filtering on features detected before 1 minute of acquisition (most likely noise, artefacts, other non-biologically relevent element). It prevents potential bias.

Data
: Data matrix input

Metadata
: Metadata matrix input, is optional but recommended for pairing, and often clearer labels.


## Define Classification designs
   
For now, the MeDIC only allows binary classification, so the classification designs add more flexibility.
So first here are some definitions

Classes
: Classes are the name of samples group in the data. A typical example is the column that contains a diagnosis.

Labels
: Labels are often considered the same as the classes. In the MeDIC, because of the multiple classification designs, labels simply designate the transition between the classes and the targets. 

Targets
: Targets are the values or names the models will output as prediction 


By default, if the user provides a Progenesis output file as data, the MeDIC will parse the file and select the second header of the table as classes. (The first header being Raw abundance and Normalized abundance, and the third header being the name of the samples.)
Otherwise, the MeDIC will read the metadata file and displays the columns names. If there are not the column names expected, please retry uploading the metadata in the section A. The user can then choose which (one or multiple) column(s) to use as class(es). In other word, which information the model will try to predict. If the user choose multiple columns, the classes will be a combination of the values of those columns.
Then, if the user gave a metadata file, he will need to also select which column of the metadata file contains the unique ID or sample names. It is used by the MeDIC to link the metadata information to each unique sample in the data.

After this step, starts the creation of classification designs. With each 'class' column the user chose, this section updates and displays the possibilities (original classes are separated from each other by '__').
Only one class can be selected to be designated by a label. 
The user has to name the new group of classes by defining a label.
Once it is filled, clicking on the '*Add*' button will adde this new design to the setup of the experiment and clear the fields. The user can then repeat the process to define a new design.
The '*Reset*' button in the block of defined classification designs will erase all design already defined.

All the designs will be run with the same:
* Number of splits
* Percentage of samples in the test set
* Pairing group
* Algorithms


### Samples pairing   

This section allows the user to select a column in the metadata that will be used to fine-tune the division of train and test set. 
Indeed, sample pairing is meant to deal with a situation common in clinical studies: the crossover design. In these studies, the experimental design will include multiple sampling of each participant, each sampling corresponding to a different treatment. In those cases, we must ensure that all samples belonging to one individual are either used to train or to test the model. This prevents biasing the algorithm towards learning the specificities of each participant instead of what distinguishes the classes. The pairing section aims to group samples that are identified as a cluster by a selected column in the metadata.
(from the paper)


### Splits

To apply machine learning to fat data, the strategy used here is to produce multiple splits. It is not a widespread practice in common machine learning applications, some confusion might arise when talking about it to machine learners.
(It might be confused with cross-validations folds or boostrap aggregating.)
The splitting process we are implementing here is the production of multiple train-test dataset division completely independent of each other.
{: #explainationOfSplits}

The train-test repartition of 20% of samples in test set and 80% in train set is quite common for metabolomic datasets. Often machine learning experiments will use a ratio closer to 30%-70%, but it always depend on the number of samples needed to train the model.

For the number of splits, a more complete run will be around 15 to 25 splits. Using 5 splits can be interesting when doing small tests of the parameters because it will be faster. However, it will not cover all the samples in a testing setting.
We determined that the appropriate number of splits for an experiment can be found using a Markov chain process. Indeed, the probability that all samples are seen in the test set, i.e. the probability that a sample is never in the test set, follow a Markov chain.

**Math example with equations and figure**

P(X<1) (values) as a function of the number of splits n (1:nbr_limit) with m=250 samples and a test proportion of 0.2 (k=50)


### Generate the splits file

Once all the parameters, the samples id and target columns, and at least one experimental design are set, you can run the splits' computation by clicking on the CREATE button.
All the parameters will be saved and for each splits, the unique identification of the samples belonging in the train or test set will be saved. No data or metadata is saved, the matrices for the machine learing are retrieved with the samples unique identification when needed.