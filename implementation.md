---
layout: base
title:  Implementation
---

# Implementation
{: .no_toc}
_ _ _ _
PICO was built with modularity in mind. The software is organized in five packages, the three principals being Domain, UI and Service. The target audience being biologists unfamiliar with coding, the interface was central during development, but we still tried to keep the tool practical for ML users and coders.

* toc
{:toc}

## Practical informations

### Interface
The transition between different experiment on the interface is not optimized. If results are loaded from a previous experiment while the interface is already displaying results, make sure to click on the "load" button in the "Results" and "Results aggregated" tabs because the figures will not be cleared when loading a different experiement. To avoid any kind of confusion, it is best to restart the interface in between.

### Logs and results savings
Both are saved in a directory called `pico_files` in the home directory of USER.
  - Linux : /home/USER/pico_files/
  - Windows : C:\Users\USER\pico_files\
  - Mac : /Users/USER/pico_files

#### Logs
Logs will be in `pico_files/logs`.
There is one file per day, with the extension `.log`. In the event of multiple experiments in one day, each will be added at the end of the file every time (the content of the file is chronologically ordered). 

There is no automatic cleaning of this directory, once in a while you might want to deleted unnecessary/older files.
{: .note title="Warning"}

#### Results
The `.mtxp` results files will be in `pico_files/saves`. 
For a complete experiment there is two files. The name structure is `pico_STEP_YYYYMMDD_HHMMSS.mtxp`, where STEP is either "splits" or "ml".

### Memory usage
The tool is not optimizing the memory for a high number of samples. It means that depending on the specifications of the computer used, a certain high number of samples might be impossible to run. The higher the performances, the higher the possible number of samples. This considers a fat dataset with at **least** 2-3 times more features than samples. Experiments with ~3000 features for ~1000 samples and ~15 000 features for ~200 samples have been performed on a personnal computer without trouble.
For bigger datasets, it is recommended to run the experiment on a server.


## Packages

Domain (backend)
: It contains all the logic that composes PICO. This package can access freely the Service package. All the communication with the UI package must pass by the controller. This allows us to modify the Domain if necessary without having to modify the UI too.

User Interface (frontend)
: It contains all the classes that are used to display the web interface of PICO. It manages only the interface and connects to the Domain by the controller only.

Service
: It can be accessed by both other packages and contains methods that are frequently used in different classes. 

Command Line Interface (CLI)
: Provides the structure to interact with the PICO by command line.

Tests
: Contains all tests run with `pytest`


## Controller interface : MetaboController bottleneck
This section can be used as a high-level documentation of the MetaboController class that serves as bottleneck between the frontend and backend.
This class can be used to integrate PICO in a Python script.

### Main methods description

```set_metadata(filename: str, data=None, from_base64=True)```  
This function sets the metadata using the path specified in parameter. The from_base64 parameter must be set to false if your file isn't encoded (csv, xlsx, ...).

```set_data_matrix_from_path(path_data_matrix, data=None, use_raw=False, from_base64=True)```  
This function sets the data matrix the same way as the metadata.

```set_id_column(id_column: str)```  
This function sets the name of the column containing the unique IDs.

```set_target_column(target_column: str)```  
This function sets the name of the column containing the targets.

```add_experimental_design(classes_design: dict)```  
This function adds an experimental design. The input dictionary must follow the format :
```json
{
  "class1": ["target1", "target2"],
  "class2": ["target3"]
}
```
{:width="75%"}

```set_train_test_proportion(train_test_proportion: float)```  
This function sets the proportion of the data that will be used as tests after the training.

```set_number_of_splits(number_of_splits: int)```  
This function sets the number of splits.

```create_splits() ```  
Once all the parameters are set, this function creates all the splits at the same time.

```set_selected_models(selected_models: list)```  
Set the list of models that will be trained.

```learn(folds: int)```  
Start the training of all the models on all splits. Folds is used for the cross-validation process (explained in Define learning configuration)

```get_all_results() ```  
Return all the data about the results, and the best model.

### Script example

Check the `automate.py` script to get more detailed comments.

```python
from metabodashboard.domain import MetaboController
from pico.service import Utils

DATAMATRIX_PATH = "path/to/data_matrix"
METADATA_PATH = "path/to/metadata"

metabo_controller = MetaboController()
metabo_controller.set_raw_use_for_data(False)
metabo_controller.set_data_matrix_remove_rt(False)
metabo_controller.set_data_matrix_from_path(DATAMATRIX_PATH, from_base64=False)
metabo_controller.set_metadata(METADATA_PATH, from_base64=False)

metabo_controller.set_id_column("samples_name")
metabo_controller.set_target_columns(["targets"])
metabo_controller.set_pairing_group_column("pairing")
metabo_controller.add_classification_design({"class1": ["target1", "target2"], "class2": ["target3"]})

metabo_controller.set_train_test_proportion(0.2)
metabo_controller.set_number_of_splits(25)
metabo_controller.set_balance_correction_for_experiment("class1_vs_class2", 0)
metabo_controller.create_splits()

metabo_expe_filename = Utils.get_metabo_experiment_path("pico_splits")
metabo_expe_obj = metabo_controller.generate_save()
Utils.dump_metabo_expe(metabo_expe_obj) # Dump the classification design to the dump folder
Utils.dump_metabo_expe(metabo_expe_obj, metabo_expe_filename) # Save the classification design
# free memory from object
del metabo_expe_obj

metabo_controller.set_multithreading(True)
metabo_controller.set_selected_models(["DecisionTree", "RandomForest", "SCM", "RandomSCM"])
metabo_controller.set_cv_type("RandomizedSearchCV")
metabo_controller.set_cv_algorithm_configuration([15])
metabo_controller.set_cv_folds(5)
metabo_controller.learn()

metabo_expe_filename = Utils.get_metabo_experiment_path("pico_ml")
metabo_expe_obj = metabo_controller.generate_save()
Utils.dump_metabo_expe(metabo_expe_obj) # Dump the classification design to the dump folder
Utils.dump_metabo_expe(metabo_expe_obj, metabo_expe_filename) # Save the classification design
# free memory from object
del metabo_expe_obj

```
{:width="75%"}
