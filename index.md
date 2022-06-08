---
layout: default
---
# Index

1. [Installation](#1-installation)  
    <ol type="A">
      <li><a href="#a-python-installation">Python installation</a></li>
      <li><a href="#b-git-installation">Git installation</a></li>
      <li><a href="#c-launcher">Launcher</a></li>
    </ol>
2. [Utilization](#2-utilization)  
    <ol type="A">
      <li><a href="#a-set-the-metadata-and-data">Set the metadata and data</a></li>
      <li><a href="#b-split-parameters">Split parameters</a></li>
      <ol>
        <li><a href="#1-define-experimental-designs">Define Experimental designs</a></li>
        <li><a href="#2-data-fusion">Data fusion</a></li>
        <li><a href="#3-define-split">Define split</a></li>
        <li><a href="#4-other-preprocessing">Other preprocessing</a></li>
        <li><a href="#5-generate-file">Generate file</a></li>
      </ol>
      <li><a href="#c-machine-learning-parameters">Machine Learning parameters</a></li>
      <ol>
        <li><a href="#1-define-learning-configurations">Define learning configurations</a></li>
        <li><a href="#2-define-learning-algorithms">Define learning algorithms</a></li>
      </ol>
      <li><a href="#d-look-at-the-results-for-each-algorithms">Look at the results for each algorithms</a></li>
      <li><a href="#e-compare-algorithms-results">Compare algorithms results</a></li>
      <li><a href="#f-restore-previous-experiment">Restore previous experiment</a></li>
    </ol>
3. [Implementation](#3-implementation)  
    <ol type="A">
      <li><a href="#a-architecture">Architecture</a></li>
      <li><a href="#b-controller-interface">Controller interface</a></li>
      <li><a href="#c-full-class-diagram">Full class diagram</a></li>
    </ol>
  

# 1. Installation

The first step to use the Metabodahsboard is to install Python (METTRE UN LIEN ICI VERS PYTHON) and install git. This way the launcher file will be able to do all the installation steps for you.

A launcher has been made for the metabodashboard to facilitate the installation process. This launcher can be used for the installation and to start the Metabodashboard.
### A. Normal installation

 - (LIEN DE DOWNLOAD DIRECT DU LAUNCHER)
 - Download launcher.py on our github (https://github.com/ElinaFF/MetaboDashboard) and run it on your computer with the command : <a href="#note1">*</a> 
 ```
    python launcher.py
 ```

 <h5 id="note1"> * You just need to execute the command ‘python launcher.py’ after opening a terminal in the folder where you downloaded the launcher.py. <br>No need to clone the repository, we will install everything we need. If you still want to do so and don’t want the launcher to redownload it during the installation process, make sure to clone the repository in the same folder as the launcher.<br> Metabodashboard uses conda for his environment, if you don’t have mini Conda installed on your machine, the launcher will install it.<br> All the dependencies necessary will be installed in the conda environment.</h5>

 ### B. Clone repository and normal installation
 -	Clone the github repository and run launcher.py with the commands.
  ```
    git clone https://github.com/ElinaFF/MetaboDashboard
    python launcher.py
  ```
  TIP: Don't forget to move to the folder Metabodashboard, with the command cd, before starting the launcher. 
  ___

  <details>
  <summary> C. Manual installation</summary>
  
 If you chose to install manually the Metabodashboard, considering you already cloned the git, you have to create a conda environement and install all the packages in the requirements.txt file.
</details>   

___

## Metabodashboard launcher options

Thoses commands are optionals but may help you to use the launcher in an easier way.  
They can be combine or use indepedently.

### 1. Use an environnement you already have
 - The content of the metadashboard envrionment can be installed in another environment, if you don't want to create a new one, with the command : <a href="#note2">**</a> 
  ```
    python launcher.py --environment <environment_name>
    python launcher.py -e <environment_name> 
  ```
  <h5 id="note2"> ** It is recommanded not to create the metadashboard environment into another environment as it may causes problems.</h5>

### 2. Fast launch for every day use
 - The Metabodashboard can be launch faster without any verifications of the environment with the command :
  ```
    python launcher.py --no-check
    python launcher.py -c
  ```

### 3. Installing the Metabodashboard for later use
  - The Metabodashboard can be installed without launching it at the end with the command :
  ```
    python launcher.py --no-launch
    python launcher.py -l
  ```

### 4. Update the Matabodashboard to the latest version
  - The Metabodashboard can be updated with the command :  
  ```
    python launcher.py --update
    python launcher.py -u
  ```
  Note: This will verify the environnement and download pakcages if necessary, it also won't start the Metabodashboard.

# 2. Utilization
> [Go back to index](#index)

## Saving file
Before explaining the interface, lets see how the experiments are saved and shareable. To allow a better modularity of the experiments, the three major steps of the Metabodashboard are saved independently into a file after each step. Moreover, the data and metadata are only saved in local repository, not in the saving file, which allow the sharing of the file to outside collaborators. To continue an experiments and/or visualize its results, the Metabodashboard offers the possibility to load a saving file in the first tab (Home). However, to prevent any problem between a local data saving and a potentiel different saving file, a hashing process takes place to compare the file being loaded and the local dumps of data. To get more details on the hashing process see this resource (LIEN). 



Welcome into the MetaboDashboard!

The following sections will resume how to run a experiment and explore each parameters you can set.

>The image in Home tab give a great insight of how the pipeline works.
>
> ![](imgs/Figure_home_wider.png)

*Pipeline explanation schema in Home tab*

## A. Set the metadata and data
> [Go back to index](#index)

Go to the Splits tab.

> ![](imgs/2022-06-06-17-55-12.png)

*Tab list with the Splits tab opened*

The following instructions are for the ```A) FILES``` section.

If you use Progenesis abundance file, you can choose to use the raw data (instead of the normalized)

To upload the data, drag and drop your data file in the ```DATA FILE(S)``` section 

> ![](imgs/2022-06-06-17-58-03.png)
>
> *```DATA FILE(S)``` section*

You can also clic on the ```UPLOAD FILE``` button and choose the right file.

**You can repeat the operation for the metadata in the ```METADATA FILE``` section.**

> ![](imgs/2022-06-07-11-16-23.png)
>
> *```MEATADATA FILE``` section*

## B. Split parameters
> [Go back to index](#index)

### 1. Define Experimental designs
> [Go back to index](#index)

The following instructions are for the ```B) DEFINE EXPERIMENTAL DESIGNS``` section.

With the board, you can run multiple experimental design, under certain conditions. Theses conditions are:
- use the same split parameters
- use the same Machine Learning (ML) algorithms
- use the same ML parameters

First of all, you need to select the target column. To clarify,  the target column contains the values that the algorithms will try to predict. A typical exemple is the column that contain the diagnosis.

The columns name prompted in the following figure are the column in the metadata file previously uploaded. If there are not the ones expected, please retry uploading the metadata in [this section](index.md#a-set-the-metadata-and-data)

> ![](imgs/2022-06-07-11-35-52.png)
>
> *Targets column selection panel*

After setting the target column, we need to set the samples column. This column have to contains **unique IDs** for each samples.

> ![](imgs/2022-06-07-11-44-48.png)
>
> *Samples column selection panel*

The main of the experimental designs configuration section is divided in two panel, respectively the *repository* and the *configuration* panel

Once the target column are defined, the possible labels are updated in the *configuration* panel as shown in the following figure.

> ![](imgs/2022-06-07-11-56-46.png)
> 
> *Updated possible labels in the* configuration *panel*

To build a binary design, you need to define the classes, in other words, to choose what you want to be opposed. An exemple using the previous values could be the identification of the sick person, opposing persons tagged with "Sickness A" and "Sickness B" and persons tagged "Control".

Add the experimental design by clicking on the ```ADD``` button.

> ![](imgs/2022-06-07-11-57-26.png)
>
> *Example of a experimental design*

Note that you need to set a name, a label, for each class. Also, you need to set at least one possible target per class but you don't need to assigned all possible targets.

Once the designs are created, they will appear in the *repository* panel.

> ![](imgs/2022-06-07-11-56-28.png)
>
> Repository *panel with two experimental design*

The ```RESET``` button will delete all the designs.

### 2. Data fusion
> [Go back to index](#index)

> **Warning**
> Not implemented yet


```Pos and Neg pairing``` allows to prevent the separation of positive and negative ionization and prevent the ML algorithms to learn the link between positive and negative ionization.

You can also use any other pattern for pairing with ```Other pairing```.

### 3. Define split
> [Go back to index](#index)

The following instructions are for the ```D) DEFINE SPLITS``` section.

> ![](imgs/2022-06-07-13-59-10.png)
>
> *```DEFINE SPLITS``` splits section*

If you don't feel confortable with theses parameters, the minimum you need to know is:
- the proportion is quite standard, it will suit most of the time
- 5 splits is quick to run but some samples may never be used to test the algorithms. If you want a complete run, 15 to 25 splits should be enough.

In the other case, the splits are made by copying the dataset and applying a random separation with a different random seed at each time. This principle is called bootstrap.

Most of the time, medical data are fat data ,i.e. contains may features (characteristic) for few samples, which can lead to many large when the training set is changed.

Moreover, as the cross validation (explained further in [2.C.1](#1-define-learning-configurations)), it allow the model(s) to be tested on most of the samples.

If you want to achieve it, the probability that all samples are seen in the test set, i.e. the probability that a sample is never in the test set, follow a <a href="https://en.wikipedia.org/wiki/Markov_chain" target="_blank">Markov chain</a>. With a example of 5 samples with 80-20 train-test repartition, the chain is as follow:
- The initial state $$V_1=\begin{pmatrix} 0 & 1 & 0 & 0 & 0 \end{pmatrix}$$
- $$P(s_{t+1}=j|s_t=i)=\frac{\begin{pmatrix} m-i \\ j-i \end{pmatrix}\begin{pmatrix} i \\ k-(j-i) \end{pmatrix}}{\begin{pmatrix} m \\ k \end{pmatrix}}$$ with $$s_t$$ a state at a $$t$$ moment, $$m$$ the total number of samples and $$k$$ the number of samples in the test set (test proportion$$\times m$$).
- $$M$$ the $$5\times 5$$ matrix of $$P(s_{t+1}=j\|s_t=i)$$
- $$V_n=V_1\times M^{n-1}$$ with $$n$$ the number of splits
- $$P(X \gt 1) = 1-V_n[5]$$ where $$X$$ is a random variable that model the number of samples that are never in the test set

The figure hereunder show $$P(X \gt 1)$$ (valeurs) as a function of the number of splits $$n$$ (1:nbr_limit) with $$m=250$$ samples and a test proportion of $$0.2$$ ($$k=50$$)


> ![](imgs/2022-06-07-14-02-37.png)
>
> *$$P(X \gt 1)$$ (valeurs) as a function of the number of splits $$n$$ (1:nbr_limit) with $$m=250$$ samples and a test proportion of $$0.2$$ ($$k=50$$)*

### 4. Other preprocessing
> [Go back to index](#index)

> **Warning**
> Not implemented yet

This section is for LDTD support.

You can show all the processing parameter by clicking on the ```OPEN``` button.


### 5. Generate file
> [Go back to index](#index)

These finals instructions are for the ```F) GENERATE FILE``` section.

Once all the parameter, the samples id and target column, and **at least one** experimental design are set, you can run the splits computation by clicking on the ```CREATE``` button.

> ![](imgs/2022-06-07-16-02-36.png)
>
> *```GENERATE FILE``` section*

## C. Machine Learning parameters
> [Go back to index](#index)

### 1. Define learning configurations
> [Go back to index](#index)

The following instructions are for the ```DEFINE LEARNING CONFIGS``` section.

If you're not confortable with theses parameters, you can safely keep the default values and jump to the [next section](#2-define-learning-algorithms).

First, before choosing a Cross Validation (CV) search type, you need to understand the principle of CV.

The method consist in separating the dataset in $$n$$ sections. At each iteration, the first or the next section will be used as the test set and the other sections will formed the training set. It allows us to train **and** test the model on all the dataset. Furthermore, the mean accurracy over

The number of folds define the number of time the model(s) will be trained, and the number of division in the dataset.

We use CV in order to make sure the model doesn't overfit, we keep a sample of the dataset to test it at the end. If the algorithm is overfitting, it will make a lot of errors when presented a new set of data. This also allows us to make sure the algorithm is tested on all samples.

For more details, see [here](https://learn.g2.com/cross-validation).

The ability of a search algorithm is to train a set of models with a set of parameters, and compute a metric tested combination. This metric is most of the time the accuracy (the number of correct predictions on the total number of predictions (the number of samples)).

After the computation, the algorithm is able to find the model combined with the parameters that perform best, in the tested combinations.

The ```GridSearchCV``` is a search algorithm using CV that test every possible combination of parameters, like in a grid. This method is effective but may take a long time to run and may test useless combination.

The ```RandomizedSearchCV``` come as a counterpoint and take random combinations of parameters. This method allow more values to be tested and run quicker but isn't as rigorous as the ```GridSearchCV```.  

In the ```SELECT CV SEARCH TYPE``` panel, you can choose either ```GridSearchCV``` or ```RandomizedSearchCV```.

You can set the number of folds in the ```NUMBER OF CROSS VALIDATION FOLDS```.

The number of processes in the ```Number of processes``` is the number of parallel job you want to run. 2 is enough to increase the speed of computation. More processes might slow your PC.

### 2. Define learning algorithms
> [Go back to index](#index)

 - You have to choose the algorithms you want to use in the list of available algorithms.
 - Add sklearn algorithms

## D. Look at the results for each algorithms
> [Go back to index](#index)

## E. Compare algorithms results
> [Go back to index](#index)

## F. Restore previous experiment
> [Go back to index](#index)

# 3. Implementation
> [Go back to index](#index)

## A. Architecture
> [Go back to index](#index)

The Methabodashboards software is organize in three main package.
 - The Domain package :  
 It contains all the logic that compose the Metabodashboard.  
 This package can access freely the Service package.  
 All of the communication with the UI package must pass by the controller. This allows us to modify the Domain if necessary without having to modify the UI too.
 - The User Interface (UI) package :  
 It contains all the classes that are used to display the web interface of the Metabodashboard.  
 It manages only the interface and connects to the Domain by the controller only.
 - The Service package :  
 It can be access by both other packages and contains methods that are frequently used in different classes.

Here is a diagram that represents the communications between all three packages. 

> ![](imgs/2022-06-07-15-17-45.png)
>
> Package diagram

This diagram shows all the classes that compose the Domain package of the Methabodashboard and the interaction between them.

> ![](imgs/2022-06-07-16-37-38.png)
>
> Simplified class diagram of the Domain package

This diagram shows all the classes that compose the UI package of the Methabodashboard and the interaction between them.

> ![](imgs/2022-06-07-16-37-55.png)
>
> Simplified class diagram of the UI package

## B. Controller interface
> [Go back to index](#index)

This section can be use as a high-level documentation of the MetaboController class that serves of controller in the Metabodashboard.

This class can be used to integrate the MetaboDashboard in a Python script.

The explanation of the concepts and the pipelines are in the ["2. Utilization"](#2-utilization) section. Don't hesitate to go back to this section while reading this one.

```Python
  set_metadata(filename: str, data=None, from_base64=True)
```
This function sets the metadata using the path specified in parameter.
The from_base64 parameter must be set to false if your file isn't encoded (csv, xlsx, ...).


```Python
  set_data_matrix_from_path(path_data_matrix, data=None, use_raw=False, from_base64=True)
```
This function sets the data matrix the same way as the metadata.


```Python
  set_id_column(id_column: str)
```
This function sets the name of the column containing the **unique** IDs.

```Python
  set_target_column(target_column: str)
```
This function sets the name of the column containing the targets.

```Python
  add_experimental_design(classes_design: dict)
```
This function adds an experimental design. The input dictionary must follow the format : 
```Python
  {
    "class1": ["target1", "target2"],
    "class2": ["target3"]
  }
```

```Python
  set_train_test_proportion(train_test_proportion: float)
```
This function sets the proportion of the data that will be used as tests after the training.

```Python
  set_number_of_splits(number_of_splits: int)
```
This function sets the number of splits as explain in ["Define split"](#3-define-split)

```Python
  create_splits()
```
Once all the splits are set, this function creates all the splits at the same time.

```Python
  set_selected_models(selected_models: list)
```

```Python
  learn(folds: int)
```

```Python
  get_all_results()
```

## C. Full class diagram

> [Go back to index](#index)

![](imgs/2022-06-08-16-51-32.png)






























