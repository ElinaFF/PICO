---
layout: base
title:  Implementation
---

# Implementation
{: .no_toc}
_ _ _ _
MeDIC software is organized in three main packages.

* toc
{:toc}

## Packages

Domain
: It contains all the logic that compose MeDIC. This package can access freely the Service package. All the communication with the UI package must pass by the controller. This allows us to modify the Domain if necessary without having to modify the UI too.

User Interface (UI)
: It contains all the classes that are used to display the web interface of MeDIC. It manages only the interface and connects to the Domain by the controller only.

Service
: It can be accessed by both other packages and contains methods that are frequently used in different classes. 

Here is a diagram that represents the communications between all three packages.
![](imgs/2022-06-07-15-17-45.png){:width="40%"}

## Package diagram

This diagram shows all the classes that compose the Domain package of MeDIC and the interaction between them.
![](imgs/2022-06-07-16-37-38.png){:width="70%"}

This diagram shows all the classes that compose the UI package of MeDIC and the interaction between them.
![](imgs/2022-06-07-16-37-55.png){:width="50%"}

(diagrams last updated in june 2022)
{:.note title="Attention"}


## Controller interface
This section can be use as a high-level documentation of the MetaboController class that serves of controller in MeDIC.

This class can be used to integrate MeDIC in a Python script.

The explanation of the concepts and the pipelines are in the Home tab. Don't hesitate to go back to this section while reading this one.

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
{:width="104%"}

```set_train_test_proportion(train_test_proportion: float)```
This function sets the proportion of the data that will be used as tests after the training.

```set_number_of_splits(number_of_splits: int)```
This function sets the number of splits as explain in the section 3. Define split in the Split tab

```create_splits() ```
Once all the splits are set, this function creates all the splits at the same time.

```set_selected_models(selected_models: list)```
Set the list of models that will be trained.

```learn(folds: int)```
Start the training of all the models on all splits. Folds is used for the cross-validation process (explained in Define learning configuration)

```get_all_results() ```
Return all the data about the results, and the best model.

### Implementation example

```python
from metabodashboard.domain import MetaboController
import pickle

DATAMATRIX_PATH = "path/to/data_matrix"
METADATA_PATH = "path/to/metadata"

metabo_controller = MetaboController()
metabo_controller.set_raw_use_for_data(False)

metabo_controller.set_data_matrix_from_path(DATAMATRIX_PATH, from_base64=False)
metabo_controller.set_metadata(METADATA_PATH, from_base64=False)

metabo_controller.set_id_column("sample")
metabo_controller.set_target_columns(["target"])
metabo_controller.set_pairing_group_column("pairing")
metabo_controller.add_experimental_design({
  "class1": ["target1", "target2"],
  "class2": ["target3"]
})

metabo_controller.set_train_test_proportion(0.2)
metabo_controller.set_number_of_splits(25)
metabo_controller.create_splits()
metabo_controller.set_selected_models(["DecisionTree", "RandomForest", "SCM", "RandomSCM"])

metabo_controller.learn()

save = metabo_controller.generate_save()
pickle.dump(save, open("save.mtxp", "wb"))

```
{:width="104%"}

## Full class diagram
![](imgs/2022-06-08-16-51-32.png)