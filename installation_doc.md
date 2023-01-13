---
layout: base
title:  Installation
---

Prerequisites
=========

The first step, to use MeDIC, is to install Python and Git. You also need to make sure that Microsoft Visual C++ is correctly installed if you're using Windows. Note that we only support Windows and Linux for now and only Python 3.8, 3.9 and 3.10

### Python installation
In order to install Python, you need to go to this link and select your operating system.

##### For Windows
You can download the latest version or a previous one if you prefer (Note : MeDIC supports python 3.10, 3.9 and 3.8). You just have to double-click and follow the installation instructions. You can also follow this tutorial for further details.

WARNING : Don't forget the select Add Python 3.X to PATH on the first page !

To verify that Python is inb the PATH, you can open a new terminal, type Python and enter. If you get something like this, it's all good. addToPath Otherwise, you have to double-click again on the python.exe file you downloaded at the beginning and click repair. Then click on Next. Then you can click on add to path and install.
{:.note}

##### For Linux
You can select the latest Python source release for python3 or a stable release for 3.8 to 3.10. You can also follow this tutorial for further details

### Git installation
In order to install Git, you need to go to this link and select your operating system.

##### For Windows
You can then choose the Standalone Installer (most computers now use the 64 bits). After downloading the .exe file, double-click on it and follow the installation instructions.

Note : You'll have a lot of choices, leave them as default if you are not familiar.

##### For Linux
Open a terminal and run the command :
                                        sudo apt-get install git
                                    Enter your root password and follow the installation instructions. For more details follows this link.

### Microsoft Visual C++ requirement
To make sure MeDIC and all it's dependencies works properly you need Microsoft Visual C++ 14.0 or later. To check if the correct version of Microsoft Visual C++ is installed or your computer you can open the Control Panel from the start menu, click on "uninstall app" and scroll down to see which version, if any, of Microsoft Visual C++ is installed.

    
##### Install new version
In order to install Microsoft Visual C++, you need to go to this link and select Visual Studio 2022 Community.

Select "Desktop development in C++" and go to the "Individual components" tab and scroll down to select "C++ V14.32(17.2) MFC for Build Tools v143 (x86 & x64)" or later and click install (It may take a while depending on your internet download speed).


A launcher has been made for MeDIC to facilitate the installation process. This launcher can be used for the installation and to start MeDIC.
The launcher file needs Git and Python to be able to do all the installation steps for you. {:.note title="Info"}    



Normal installation   
=========   

Download launcher.py on our github
Open a terminal (*cmd* in Windows)
Run the launcher on your computer with the command : *python launcher.py

* No need to clone the repository, we will install everything we need. If you still want to do so and don’t want the launcher to redownload it during the installation process, make sure to clone the repository in the same folder as the launcher.
MeDIC uses conda for his environment, if you don’t have any Conda instance installed on your machine, the launcher will install one (Miniconda3).
All the dependencies necessary will be installed in the conda environment.    
  

Clone repository and normal installation    
==========    

Open a terminal (cmd in Windows)
Clone the Github repository.
git clone https://github.com/ElinaFF/MetaboDashboard
Move inside the repository
cd MetaboDashboard
Run the launcher
python launcher.py


Manual installation   
==========   

Install Miniconda following the documentation
Open a terminal ("cmd" in Windows not "Powershell")
Create an environment with Conda:
conda create medic
Enter in the environment
conda activate medic
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



MeDIC launcher options     
=========     

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