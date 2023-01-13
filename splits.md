---
layout: post
title:  Splits
---

1. Define Experimental designs
The following instructions are for the B) DEFINE EXPERIMENTAL DESIGNS section.

With the board, you can run multiple experimental design, under certain conditions. These conditions are:

use the same split parameters
use the same Machine Learning (ML) algorithms
use the same ML parameters
First, you need to select the target column. To clarify, the target column contains the values that the algorithms will try to predict. A typical example is the column that contain the diagnosis.

The columns name prompted in the following figure are the column in the metadata file previously uploaded. If there are not the ones expected, please retry uploading the metadata in the section A. Set the metadata and data in the Home tab



Targets column selection panel

After setting the target column, we need to set the samples' column. This column has to contain unique IDs for each sample.



Samples column selection panel

The main part of the experimental designs configuration section is divided in two panel, respectively the repository and the configuration panel

Once the target columns are defined, the possible labels are updated in the configuration panel as shown in the following figure.



Updated possible labels in the configuration panel

To build a binary design, you need to define the classes, in other words, to choose what you want to be opposed. An example using the previous values could be the identification of the sick person, opposing persons tagged with "Sickness A" and "Sickness B" and persons tagged "Control".

Add the experimental design by clicking on the ADD button.



Example of a experimental design

Note that you need to set a name, a label, for each class. Also, you need to set at least one possible target per class, but you don't need to assign all possible targets.

Once the designs are created, they will appear in the repository panel.



Repository panel with two experimental design

The RESET button will delete all the designs.

2. Data fusion
Warning Not implemented yet

Pos and Neg pairing allows to prevent the separation of positive and negative ionization and prevent the ML algorithms to learn the link between positive and negative ionization.

You can also use any other pattern for pairing with Other pairing.

3. Define split
The following instructions are for the D) DEFINE SPLITS section.



DEFINE SPLITS splits section

If you don't feel conformable with these parameters, the minimum you need to know is:

the proportion is quite standard, it will suit most of the time
5 splits is quick to run but some samples may never be used to test the algorithms. A more complete run will take 15 to 25 splits.
In the other case, the splits are made by copying the dataset and applying a random separation with a different random seed at each time. This principle is called bootstrap.

Most of the time, medical data are fat data ,i.e. contains many features (characteristic) for few samples, which can lead to many large when the training set is changed.

Moreover, as the cross validation (explained in further details in section 1. Define learning configurations in the Machine Learning tab), it allows the model(s) to be tested on most of the samples.

If you want to achieve it, the probability that all samples are seen in the test set, i.e. the probability that a sample is never in the test set, follow a Markov chain. With an example of 5 samples with 80-20 train-test repartition, the chain is as follows:





P(X<1) (values) as a function of the number of splits n (1:nbr_limit) with m=250 samples and a test proportion of 0.2 (k=50)

4. Other preprocessing
Warning Not implemented yet

This section is for LDTD support.

You can show all the processing parameter by clicking on the OPEN button.

5. Generate file
These finals instructions are for the F) GENERATE FILE section.

Once all the parameters, the samples id and target columns, and at least one experimental design are set, you can run the splits' computation by clicking on the CREATE button.



GENERATE FILE section