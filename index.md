---
layout: base
title:  About
cover:  true
---

# About
_ _ _ _

The **Me**tabolomics **D**ashboard for **I**nterpretable **C**lassification (MeDIC) is a tool to democratize machine learning (ML) for metabolomics.

![](logo.png){:.lead width="100" height="100" loading="lazy"}

It must be installed on a local computer and possess a visual interface which can be used to perform an ML experiment, from uploading the data to analysing the results. 
Advanced users will find that a script *automate.py* allows the steps from uploading data to training the algorithms to be run directly with a terminal (command prompt). The output file can then be loaded into the MeDIC interface for results analysis.
Expert users will find that the *automate* script can be run on a distant server (need to : install the environment on the server, understand nodes/parallelization, know how much resources it will need to run.)



## Requirements


| Minimal requirements                 | Recommended requirements |
|--------------------------------------|--------------------------|
| Dual-core processor                  | 4 core processor |
| Maximum of 2GB or 1GB + dataset size | 8GB RAM |


###### With option to parallelize as *False*
The recommended configuration keeps some power free to allow parallel use of the computer. For the time being, a better configuration will not improve the running time of the MeDIC but more power will be available for other uses.
In fact, MeDIC will use at most 700 MB of RAM and will never exceed 1GB in running time. Please note that the MeDIC needs to load the dataset in memory at the beginning, so it needs at least the size of the dataset of RAM. For example, a 3 GB dataset requires at least 4 GB of RAM. The rest is free for other uses.
If the available RAM is 4GB or less, MeDIC will run, but experiments may take a long time to execute.
For example, with a dataset of 210 samples per 15000 features and the recommended parameters, the experiment will take about 6 hours to run.

###### With option to parallelize as *True*
The implementation of multithreading will allow MeDIC to use all available resources to speed up the computation.
The speed of the experiment and memory usage will depend on the available resources.
