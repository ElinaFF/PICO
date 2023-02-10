---
layout: base
title:  Home
---

# Home
The 'Home' tab of the tool provides the link to this official documentation, the possibility to load results files, and gives small
explanations of each step of the tool.

* toc
{:toc}


## Results file
To allow a better modularity of the experiments, the two major steps of MeDIC are saved independently into a file after each step. 
Moreover, the data and metadata are only saved (dumps) in a local repository, not in the saving file, which allow the sharing of 
the results file to outside collaborators. To continue an experiments and/or visualize its results, MeDIC offers the possibility 
to load a saving file in the first tab (Home). However, to prevent any problem between a local data saving and a 
potential different saving file, a hashing process takes place to compare the file being loaded and the local dumps of data.


## Analysis pipeline
In the 'Splits' tab, the user starts by giving the data file and a metadata file (optional). Then the user can select different options
and parameters, and define the classification designs. A first saving file is created. Then in the 'Machine leanring' tab the user can
choose the machine learning algorithmes and the options for the hyperparameters optimization. A second saving file is created.
At the end, the user can analyse its results with the two last tabs : 'Results' and 'Results aggregated'.




MEATADATA FILE section

The supported files are excel, odt or csv.

If the error "Rows must have an equal number of columns" occurred, it means that some lines don't have cells for all columns.
