---
layout: base
title:  About
cover:  true
---

# About
_ _ _ _

The **Me**tabolomics **D**ashboard for **I**nterpretable **C**lassification (MeDIC) is a tool to democratize machine learning (ML) for metabolomics.

![](logo.png){:height="15%" width="15%"}

It must be installed on a computer and possesses a visual interface which can be used to perform an ML experiment, from uploading the data to analysing the results. 
Advanced users will find that a script `automate.py` allows the steps from uploading data to training the algorithms to be run directly with a terminal (command prompt). The output file can then be loaded into the MeDIC interface for results analysis.
Expert users will find that the `automate` script can be run on a distant server (need to : install the environment on the server, understand nodes/parallelization, know how much resources it will need to run.)


Warning : Throughout the interface, when clicking on something, if the expected effect is not displayed immediately, check the title of the web navigator tab. If an action has indeed been triggered it will be written "Updating...".
{: .note title="Warning"}

License
: <a href="https://github.com/ElinaFF/MeDIC">Metabolomic Dashboard for Interpretable Classification (MeDIC)</a> © 2025 by <a href="https://creativecommons.org">Elina Francovic-Fontaine</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>


## Requirements
The recommended configuration considers the user will need the computer while the experiment is runing. 

| Basic requirements | Recommended requirements |
|--------------------|--------------------------|
| 4 core processor | 8 core processor |
| 8GB RAM | 16GB RAM |


###### Parallelization
Enabling multithreading allows MeDIC to use all the performance of the CPU. It reduces dramatically the compute time of the experiment. The speed increase depends on the CPU’s performances (number of core and speed).


## Benchmarks
Here are some example of machine setups vs compute times. They are all refering to the experiment described in the paper of all controls vs all cases and are all using parallelization.

###### Linux
1. Debian 12 with XXgb RAM and 4 core : ~35 minutes
2. In docker container, Fedora with 6gb VRAM and X core : ~15 minutes
3. In WSL, Ubuntu with 8 gb RAM and 6 core : ~40 minutes

###### Mac
1. MacOS 14.6.1 with 16gb RAM and 8 core : ~10 minutes
2. MacOS 15.5 with M4 chip 32gb RAM and 10 core : ~5 minutes

###### Windows
1. Windows 10 version 10.0.19045 with 16 gb RAM and 8 core : ~15min
