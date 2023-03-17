---
layout: base
title:  Home tab
---

# Home tab
{: .no_toc}
_ _ _ _
The 'Home' tab of the tool provides the link to this official documentation, the possibility to load results files, and gives small
explanations of each step of the pipeline.

* toc
{:toc}


## Results file (Load MetaboExperiment)
To allow a better modularity of the experiments, the two major steps of MeDIC are saved independently into a file after each step. 
Moreover, the data and metadata are only saved (dumps) in a local repository, not in the saving file, which allow the sharing of 
the results file to outside collaborators. 

To continue an experiment and/or visualize results, MeDIC offers the possibility 
to load a saving file in the first tab (Home). However, to prevent any problem between a local data saving and a 
potential different saving file, a hashing process takes place to compare the file being loaded and the local dumps of data.

Load results
: Select this option if you only want to visualize the results of a previous experiment. No need to provide data or metadata.

Partial restore
: Select this option if you want to use the same splits parameters (except classification design, targets and sample id columns), but with other designs or data. It means you have to go through the Splits tab and specify missing informations (designs, data matrix, etc.).

Full restore
: Select this option if you want to fully reproduce an experiment, you will need to give the same data and metadata matrices as the original experiment.

Once an option is selected, and no warning message appeared, the disappearance of the modal indicates that everything is correctly loaded and ready to use.
{:.note}

## Analysis pipeline
In the 'Splits' tab, the user gives the data file and a metadata file (optional). Then there is the selection different options
and parameters, and definition of classification designs. A first saving file is created. Then in the 'Machine leanring' tab the user can
choose the machine learning algorithms and the options for the hyperparameters optimization. A second saving file is created.
At the end, the user can analyse its results with the two last tabs : 'Results' and 'Results aggregated'.

![](imgs/update_figure_steps_MeDIC_4.svg)

