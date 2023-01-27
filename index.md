---
layout: base
title:  Installation
cover:  true
---

# Installation


The MeDIC is a tool that must be installed locally. The visual interface is made with Dash from Plotly and can be 
open in the majority of web browser. To install the MeDIC, the principal method is manually. A launcher file to automate 
the installation is currently under development, and a beta version is available.
Note that we only support Windows and Linux for now, and only Python 3.8, 3.9 and 3.10.

* toc
{:toc}

## Prerequisites
The first step, to use MeDIC, is to install Python and Git. You also need to make sure that Microsoft Visual C++ is correctly installed.

### Linux installation

#### Python
In order to install Python, you need to go to this [link](https://www.python.org/downloads/source/). Download your 
prefered version (or the latest 3.10 stable version) and proceed with the installation.
You can also follow this [tutorial](https://www.scaler.com/topics/python/install-python-on-linux/) for further details.
#### Git
Open a terminal and run the command :
~~~
sudo apt-get install git
~~~
Then enter your root password and follow the installation instructions. 
For more details follow this [link](https://git-scm.com/download/linux).


### Windows installation
Don't forget to make sure that Microsoft Visual C++ is correctly installed.

#### Python
In order to install Python, you need to go to this [link](https://www.python.org/downloads/windows/). Download your 
prefered version (or the latest 3.10 stable version) and proceed with the installation.
You can also follow this [tutorial](https://phoenixnap.com/kb/how-to-install-python-3-windows) for further details.

WARNING : Don't forget the select Add Python 3.X to PATH on the first page !
![](imgs/addToPath.png)

To verify that Python is in the PATH, you can open a new terminal (cmd prompt), type Python and press Enter. If you get something like this, 
it's all good. 
![](imgs/cmdOk.png)

Otherwise, you have to double-click again on the python.exe file you downloaded at the beginning and click repair. 
Then click on Next. Then you can click on add to path and install.
![](imgs/addToPathAfterRepair.png)

#### Git installation
In order to install Git, you need to go to this [link](https://git-scm.com/download/win) and choose the Standalone Installer (64 bits).
After downloading the .exe file, double-click on it and follow the installation instructions.
Note : You'll have a lot of choices, leave them as default if you are not familiar with what they do or impact.

#### Microsoft Visual C++ requirement
To make sure MeDIC and all it's dependencies work properly, you need Microsoft Visual C++ 14.0 or later. 
To check if the correct version of Microsoft Visual C++ is installed on your computer, you can open the Control Panel from the start menu, 
click on "uninstall app" and scroll down to see which version, if any, of Microsoft Visual C++ is installed.

##### Install new version
In order to install Microsoft Visual C++, you need to go to this [link](https://visualstudio.microsoft.com/downloads/) 
and select Visual Studio 2022 Community.
Then, select "Desktop development in C++" and go to the "Individual components" tab. 
Scroll down to select "C++ V14.32(17.2) MFC for Build Tools v143 (x86 & x64)" or later and click install 
(It may take a while depending on your internet download speed).


***


## Manual installation

1. Install Miniconda following the [documentation](https://docs.conda.io/en/latest/miniconda.html)
2. Open a terminal ("cmd" in Windows not "Powershell")
3. Create an environment with Conda `conda create medic`
4. Enter in the environment `conda activate medic`


Info

If the command worked, you should see the name "medic" written at the beginning of your prompt
Clone the Github repository and move inside.
  git clone https://github.com/ElinaFF/MeDIC
  cd MeDIC
Install the dependencies:
python -m pip install -r requirements.txt
Warning

If you have an error for ParmEd, pyscm or randomscm, it may be a C++ compilation problem (see here) return here to install, or update, Microsoft Visual C++.
Launch the Web interface
python main.py


Installation on WSL (Windows Subsystem for Linux)    
==========   

During the normal installation, you may have a problem with the Path variable. We haven't found a solution yet. You may need to go through the Manual installation.


## Beta version launcher installation

A launcher has been made for MeDIC to facilitate the installation process. This launcher can be used for the installation and to start MeDIC.
The launcher file needs Git and Python to be able to do all the installation steps for you. {:.note title="Info"}    

### Launcher 
1. Download launcher.py on our github
2. Open a terminal (*cmd* in Windows)
3. Run the launcher on your computer with the command : *python launcher.py

* No need to clone the repository, we will install everything we need. If you still want to do so and don’t want the launcher to redownload it 
  during the installation process, make sure to clone the repository in the same folder as the launcher. MeDIC uses conda for his environment, 
  if you don’t have any Conda instance installed on your machine, the launcher will install one (Miniconda3). 
  All the necessary dependencies will be installed in the conda environment.    
  

### Clone repository and use the launcher  

1. Open a terminal (cmd in Windows)
2. Clone the Github repository `git clone https://github.com/ElinaFF/MeDIC`
3. Move inside the repository `cd MetaboDashboard`
4. Run the launcher `python launcher.py`


### Launcher options

Those commands are optionals but allow more flexibility.
They can be combined or used independently.

1. Existing environment
MeDIC can be installed or launch from an existing environment ** with :
 python launcher.py --environment <environment_name>
 python launcher.py -e <environment_name>
** It is recommended not to create MeDIC environment into another environment as it may cause problems.
2. Fast launch for everyday use
MeDIC can be launched faster without any verifications of the environment with :
 python launcher.py --no-check
 python launcher.py -c
3. Installing MeDIC for later use
MeDIC can be installed without launching it at the end with :
python launcher.py --no-launch
python launcher.py -l
4. Update MeDIC to the latest version
MeDIC can be updated with the command :
python launcher.py --update
python launcher.py -u
Info

This will retrieve updates from the github repository, verify the environment and download packages if necessary, but it won't start MeDIC.