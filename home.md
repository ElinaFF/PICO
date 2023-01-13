---
layout: post
title:  Home
---


Saving file    
=======    

Before explaining the interface, lets see how the experiments are saved and how you can share them. To allow a better modularity of the experiments, the three major steps of MeDIC are saved independently into a file after each step. Moreover, the data and metadata are only saved in local repository, not in the saving file, which allow the sharing of the file to outside collaborators. To continue an experiments and/or visualize its results, MeDIC offers the possibility to load a saving file in the first tab (Home). However, to prevent any problem between a local data saving and a potential different saving file, a hashing process takes place to compare the file being loaded and the local dumps of data.

Welcome into MeDIC!

The following sections will resume how to run an experiment and explore each parameter you can set.

The image in Home tab give a great insight of how the pipeline works.



Pipeline explanation schema in Home tab

A. Set the metadata and data
Go to the Splits tab.



Tab list with the Splits tab opened

The following instructions are for the A) FILES section.

If you use Progenesis abundance file, you can choose to use the raw data (instead of the normalized).

To upload the data, drag and drop your data file in the DATA FILE(S) section.



DATA FILE(S) section

You can also click on the UPLOAD FILE button and choose the right file.

You can repeat the operation for the metadata in the METADATA FILE section.



MEATADATA FILE section

The supported files are excel, odt or csv.

If the error "Rows must have an equal number of columns" occurred, it means that some lines don't have cells for all columns.
