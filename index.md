---
layout: base
title:  About
cover:  true
---

# About
_ _ _ _

The **Me**tabolomics **D**ashboard for **I**nterpretable **C**lassification (MeDIC) is a tool to democratize machine learning (ML) for metabolomics.

![](logo.png){:height="15%" width="15%"}

It must be installed on a local computer and possess a visual interface which can be used to perform an ML experiment, from uploading the data to analysing the results. 
Advanced users will find that a script *automate.py* allows the steps from uploading data to training the algorithms to be run directly with a terminal (command prompt). The output file can then be loaded into the MeDIC interface for results analysis.
Expert users will find that the *automate* script can be run on a distant server (need to : install the environment on the server, understand nodes/parallelization, know how much resources it will need to run.)



## Requirements


| Minimal requirements                 | Recommended requirements |
|--------------------------------------|--------------------------|
| Dual-core processor                  | 4 core processor |
| Maximum of 2GB or 1GB + dataset size | 8GB RAM |


###### With option to parallelize as *False*
The recommended configuration keeps some power available to allow the user to keep using his computer.
In fact, MeDIC will use at most 700 MB of RAM and will never exceed 1GB at run time. Please note that the MeDIC needs to load the dataset in memory at the beginning, so it needs at least the size of the dataset of RAM. For example, a 3 GB dataset requires at least 4 GB of RAM. The remaining RAM stays available to the user.

If the available RAM is 4GB or less, MeDIC will run, but experiments may take a long time to execute.
For example, with a dataset of 210 samples with 15000 features each and the recommended parameters, the experiment will take about 6 hours to compute.

###### With option to parallelize as *True*
Enabling multithreading allows MeDIC to use all the performance of the CPU. This allows to reduce the compute time of the experiment. The speed increase depends on the CPU’s performances.
