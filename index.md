---
layout: default
---
# Index

1. [Installation](./index.md#1-installation)  
    <ol type="a">
      <li>Python installation</li>
      <li>Git installation</li>
      <li>Launcher</li>
    </ol>
2. [Utilization](./index.md#2-utilization)  
    <ol type="a">
      <li>Set the metadata and data</li>
      <li>Split parameters</li>
      <li>Machine Learning parameters</li>
      <li>Look at the results for each algorithms</li>
      <li>Compare algorithms results</li>
      <li>Restore previous experiment</li>
    </ol>
3. [Implementation](./index.md#3-installation)  
    <ol type="a">
      <li>Architecture</li>
      <li>Controller interface</li>
    </ol>
  

# 1. Installation

DONE BY VINCE

# 2. Utilization
Welcome into the MetaboDashboard!

The following sections will resume how to run a experiment and explore each parameters you can set.

The image in Home tab give a great insight of how the pipeline works.

![](imgs/Figure_home_wider.png)
*Pipeline explanation schema in Home tab*

## A. Set the metadata and data

Go to the Splits tab.

![](imgs/2022-06-06-17-55-12.png)
*Tab list with the Splits tab opened*

The following instruction are for the ```A) FILES``` section.

If you use Progenesis abundance file, you can choose to use the raw data (instead of the normalized)

To upload the data, drag and drop your data file in the ```DATA FILE(S)``` section 

![](imgs/2022-06-06-17-58-03.png)
*```DATA FILE(S)``` section*

You can also clic on the ```UPLOAD FILE``` button and choose the right file.

**You can repeat the operation for the metadata in the ```METADATA FILE``` section.**

![](imgs/2022-06-07-11-16-23.png)
*```MEATADATA FILE``` section*

## B. Split parameters

### 1. Define Experimental designs

The following instruction are for the ```B) DEFINE EXPERIMENTAL DESIGNS``` section.

With the board, you can run multiple experimental design, under certain conditions. Theses conditions are:
- use the same split parameters
- use the same Machine Learning (ML) algorithms
- use the same ML parameters

First of all, you need to select the target column. To clarify,  the target column contains the values that the algorithms will try to predict. A typical exemple is the column that contain the diagnosis.

The columns name prompted in the following figure are the column in the metadata file previously uploaded. If there are not the ones expected, please retry uploading the metadata in [this section](index.md#a-set-the-metadata-and-data)

![](imgs/2022-06-07-11-35-52.png)
*Targets column selection panel*

After setting the target column, we need to set the samples column. This column have to contains **unique IDs** for each samples.

![](imgs/2022-06-07-11-44-48.png)
*Samples column selection panel*

The main of the experimental designs configuration section is divided in two panel, respectively the *repository* and the *configuration* panel

Once the target column are defined, the possible labels are updated in the *configuration* panel as shown in the following figure.

![](imgs/2022-06-07-11-56-46.png)
*Updated possible labels in the* configuration *panel*

To build a binary design, you need to define the classes, in other words, to choose what you want to be opposed. An exemple using the previous values could be the identification of the sick person, opposing persons tagged with "Sickness A" and "Sickness B" and persons tagged "Control".

Add the experimental design by clicking on the ```ADD``` button.

![](imgs/2022-06-07-11-57-26.png)
*Example of a experimental design*

Note that you need to set a name, a label, for each class. Also, you need to set at least one possible target per class but you don't need to assigned all possible targets.

Once the designs are created, they will appear in the *repository* panel.

![](imgs/2022-06-07-11-56-28.png)
Repository *panel with two experimental design*

The ```RESET``` button will delete all the designs.

### 2. Data fusion

### 3. Define split

 - You have to enter the proportion of samples that are used for tests.
 - You have to enter the number of splits

### 4. Other preprocessing

### 5. Generate file

## C. Machine Learning parameters

### 1. Define learning configurations

 - CV search type  

 - Number of croos validation folds  

 - Number of processes  

### 2. Define learning algorithms

 - You have to choose the algorithms you want to use in the list of available algorithms.
 - Add sklearn algorithms

## D. Look at the results for each algorithms

## E. Compare algorithms results

## F. Restore previous experiment

































