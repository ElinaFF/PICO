---
layout: base
title:  Implementation
---

# Implementation
{: .no_toc}
_ _ _ _
MeDIC software is organized in five main packages.

* toc
{:toc}

## Packages

Domain (backend)
: It contains all the logic that composes MeDIC. This package can access freely the Service package. All the communication with the UI package must pass by the controller. This allows us to modify the Domain if necessary without having to modify the UI too.

User Interface (frontend)
: It contains all the classes that are used to display the web interface of MeDIC. It manages only the interface and connects to the Domain by the controller only.

Service
: It can be accessed by both other packages and contains methods that are frequently used in different classes. 

Command Line Interface (CLI)
: Provides the structure to interact with the MeDIC by command line.

Tests
: Contains all tests run with `pytest`



## Controller interface : MetaboController bottleneck
This section can be used as a high-level documentation of the MetaboController class that serves as bottleneck between the frontend and backend.
This class can be used to integrate MeDIC in a Python script.

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
from medic.service import Utils

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

metabo_expe_filename = Utils.get_metabo_experiment_path("medic_splits")
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

metabo_expe_filename = Utils.get_metabo_experiment_path("medic_ml")
metabo_expe_obj = metabo_controller.generate_save()
Utils.dump_metabo_expe(metabo_expe_obj) # Dump the classification design to the dump folder
Utils.dump_metabo_expe(metabo_expe_obj, metabo_expe_filename) # Save the classification design
# free memory from object
del metabo_expe_obj

```
{:width="75%"}
