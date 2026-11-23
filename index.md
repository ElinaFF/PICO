---
layout: base
title:  About
cover:  true
---

# About
_ _ _ _

The **P**ipeline of **I**nterpretable **C**lassification for **O**mics (PICO) is a tool to democratize machine learning (ML) for omics data.

![](logoName_pico.png){:height="15%" width="15%"}

It must be installed on a computer and possesses a visual interface which can be used to perform an ML experiment, from uploading the data to analysing the results. 
Advanced users will find that a script `automate.py` allows the steps from uploading data to training the algorithms to be run directly with a terminal (command prompt). The output file can then be loaded into the PICO interface for results analysis.
Expert users will find that the `automate` script can be run on a distant server (need to : install the environment on the server, understand nodes/parallelization, know how much resources it will need to run.)


Throughout the interface, when clicking on something, if the expected effect is not displayed immediately, check the title of the web navigator tab. If an action has indeed been triggered it will be written "Updating...".
{: .note title="Warning"}


License
: <a href="https://github.com/ElinaFF/PICO">Pipeline for Interpretable Classification of Omics (PICO)</a> © 2025 by <a href="https://creativecommons.org">Elina Francovic-Fontaine</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>

## Related works

| Tools | Splits | FAIR | Crossover studies | Agnostic Features | Balancing | Classification designs | Accessible | Interpretability |
|-------|--------|------|-------------------|-------------------|-----------|------------------------|------------|------------------|
| PICO (our tool)| +++ | +++ | +++ | +++ | ++ | +++ | ++ | +++ |
| CRANK-MS | + | No | No | No | No | No | + | + |
| SPARSENN | + | No | No | + | No | No | + | - |
| AutoXAIOmics | No | No | No | No | +++ | + | No | + |
| MetaboAnalyst | - | - | + | ++ | - | - | +++ | +++ |
| ExplainerDashboard | No | + | - | - | - | - | + | ++ |
| LipidSig | No | No | No | No | No | No | +++ | + |
| 3D Intelligenes | No | +++ | No | ++ | No | No | +++ | ++ |
| OmicLearn | + | + | No | No | No | No | +++ | +++ |


Splits  
: +++ : yes, variable, with statistics supporting decision, ++ : option not present in literature, +: yes, fixed number.

FAIR   
: +++ : implementation of at least one concept in each FAIR ``letter", also built to facilitate research collaborations while maintaining privacy of data, ++ : option not present in literature, + : implement minimum FAIR principles OR support for research collaborations.

Crossover studies  
: +++ : handling pairing of variable number of samples, ++ : option not present in literature, + : handling pairing of two samples only (minimal way of supporting pairing).

Agnostic features  
: +++ : analyze important features across splits and algorithms, ++ : analyze important features across algorithms, + : analyze important features across splits.

Balancing  
: +++ : multiple methods of balancing (oversampling, undersampling, synthetic data, etc), ++ : one method of balancing, + : option not present in literature.

Classification Design  
: +++ : Support creating multiple custom designs for binary classification, ++ : option not present in literature, + : support only one design.

Accessible  
: +++ : visual interface for computing and results, ++ : visual just for results, no need ML knowledge, + : need ML knowledge.

Interpretability  
: +++ : pure interpretability, focus on using it for features selection, ++ :  XAI like SHAP of LIME, plus a little bit of importances, + : only XAI.


## Requirements
The recommended configuration considers the user will need the computer while the experiment is runing. 

| Minimal requirements | Recommended requirements |
|----------------------|--------------------------|
| 8 threads/core processor | 12 threads/core processor |
| 8GB RAM | 16GB RAM |


###### Parallelization
Enabling multithreading allows PICO to use all the performance of the CPU. It reduces dramatically the compute time of the experiment. The speed increase depends on the CPU’s performances (number of threads/core and speed).


## Benchmarks
Here are some example of machine setups vs compute times. They are all refering to the experiment described in the paper of all controls vs all cases and are all using parallelization.
Many things can factors into the variations of speed, like the cache memory, the speed of the processor (Hz), the use of the computer while the experiment is running and more. The following benchmarks are simply to give an overview with simple references.

###### Linux
1. Debian 12 with 16gb RAM and 8 threads : ~35 minutes
2. In WSL, Ubuntu with 8 gb RAM and 12 threads : ~40 minutes
3. In docker container, Fedora with 6gb VRAM and 12 threads : ~15 minutes

###### Mac
1. MacOS 14.6.1 with 16gb RAM and 8 core : ~10 minutes
2. MacOS 15.5 with M4 chip 32gb RAM and 10 core : ~5 minutes

###### Windows
1. Windows 10 version 10.0.19045 with 16 gb RAM and 8 core : ~15min
