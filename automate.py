from datetime import datetime
from pico.domain import Controller
from pico.service import Utils, init_logger, log_exceptions

logger = init_logger()

##############################
#        Informations        #
##############################

# This file has been divided in functions in an attempt to make it more digestible/clear
# It tries to resemble the UI version, in the order and division of tasks
# There is parameters to adjust in the main function,
# But most of the customization happens in the body of smaller functions, 
# so be carefull not to forget anything.


##############################
#   Define paths variables   #
##############################

METADATA_PATH = "../medic_otherThanPackage/s_MTBLS28_merged.csv"
DATAMATRIX_PATH = "../medic_otherThanPackage/MTBLS28_CombinedData2_forML.csv"


##############################
#      Setup experiment      #
##############################

def SPLITS_setup_files(mtb_ctrl):
    """
    mtb_ctrl : Controller object
    """

    # The UI has three options of file input : "Raw" (from progenesis), "Normalized" (from progenesis), Not Progenesis
    # To input a data matrix not corresponding to progenesis format :
    #    - set_raw_use_for_data(False)
    #    - set_data_matrix_remove_rt(False)
    # To input "Raw" :
    #    - set_raw_use_for_data(True)
    # To input "Normalized" :
    #    - set_raw_use_for_data(False)
    # The option of "set_data_matrix_remove_rt" should be True if Progenesis format, select False to your own risks
    # If Not Progenesis, removing RT before 1min should part of preprocessing prior to using the MeDIC
    mtb_ctrl.set_raw_use_for_data(False)
    mtb_ctrl.set_data_matrix_remove_rt(False)
    mtb_ctrl.set_data_matrix_from_path(DATAMATRIX_PATH, from_base64=False)
    mtb_ctrl.set_metadata(METADATA_PATH, from_base64=False)

def SPLITS_setup_classification_designs(mtb_ctrl):
    """
    mtb_ctrl : Controller object
    """
    mtb_ctrl.set_id_column("Sample_Name")
    mtb_ctrl.set_target_columns(["Factor Value[Sample Type]"])
    #mtb_ctrl.set_target_columns(["Factor Value[Sample Type]", "Factor Value[Smoking]"])

    # Designs are defined as dict with labels as keys and classes(if multiple link with "__") as values
    # The classes should correspond to values found in the column(s) defined in mtb_ctrl.set_target_columns() function. 
    mtb_ctrl.add_classification_design({"1TotalCases": ["Case"], "0TotalCtrls": ["Control"]})
    #mtb_ctrl.add_classification_design({"NEG_Case_Current": ["Case__Current Smoker"], "Ctrl_Current": ["Control__Current Smoker"]})
    #mtb_ctrl.add_classification_design({"NEG_Case_Former": ["Case__Former Smoker"], "Ctrl_Former": ["Control__Former Smoker"]})
    #mtb_ctrl.add_classification_design({"NEG_Case_Never": ["Case__Never Smoker"], "Ctrl_Never": ["Control__Never Smoker"]})


def SPLITS_setup_splits_and_balancing(mtb_ctrl, proportion_splits , nbr_splits):
    """
    mtb_ctrl : Controller object
    proportion_splits : proportion of sample in test set in decimal (0 to 1)
    nbr_splits : number of splits to compute
    """
    mtb_ctrl.set_train_test_proportion(proportion_splits)
    mtb_ctrl.set_number_of_splits(nbr_splits)

    # The balance correction is specific to a design, refer to a design by its name (LABEL1_vs_LABEL2)
    # Choosing balance correction value : see documentation for explanation
    mtb_ctrl.set_balance_correction_for_experiment("1TotalCases_vs_0TotalCtrls", 0)
    #mtb_ctrl.set_balance_correction_for_experiment("NEG_Case_Current_vs_Ctrl_Current", 15)
    #mtb_ctrl.set_balance_correction_for_experiment("NEG_Case_Former_vs_Ctrl_Former", 0)
    #mtb_ctrl.set_balance_correction_for_experiment("NEG_Case_Never_vs_Ctrl_Never", 21)
    mtb_ctrl.create_splits()


def ML_setup_CV_and_algo(mtb_ctrl, cv_algo):
    """
    mtb_ctrl : Controller object
    cv_algo : Either GridSearchCV(default) or RandomizedSearchCV
    """
    mtb_ctrl.set_multithreading(True)

    # Available defaults : ["DecisionTree", "RandomForest", "SCM", "RandomSCM"]
    mtb_ctrl.set_selected_models(["DecisionTree", "RandomForest", "SCM", "RandomSCM"])
    
    # (if GridSearch you can simply comment the line)
    mtb_ctrl.set_cv_type(cv_algo)
    
    # Needed if RandomizedSearchCV is chosen
    # list of values for required parameters of CV algorithm, randomSearch requires n_iter arg : the default here is 10
    # (if GridSearch you can simply comment the line)
    #mtb_ctrl.set_cv_algorithm_configuration([20])
    
    mtb_ctrl.set_cv_folds(5)
    mtb_ctrl.learn()


def SAVE_setups_and_results(mtb_ctrl, experiment_path):
    """
    mtb_ctrl : Controller object
    experiment_path :  
        -   'medic_splits' the save of only splits parameters, after the "splits tab"
        -   'medic_ml' the save of all parameters and results, after the "ml tab"
        This argument should not take a different path from the two above, it risks breaking the code. 
    """
    metabo_expe_filename = Utils.get_metabo_experiment_path(experiment_path) # Get save file path
    metabo_expe_obj = mtb_ctrl.generate_save()
    Utils.dump_metabo_expe(metabo_expe_obj) # Dump the classification design to the dump folder
    Utils.dump_metabo_expe(metabo_expe_obj, metabo_expe_filename) # Save the classification design
    # free memory from object
    del metabo_expe_obj


###############################
#        Main function        #
###############################

@log_exceptions(logger)
def main():
    start_time = datetime.now()
    logger.info(f"---> Starting at : {start_time}")
    metabo_controller = Controller()

    SPLITS_setup_files(metabo_controller)
    SPLITS_setup_classification_designs(metabo_controller)
    SPLITS_setup_splits_and_balancing(metabo_controller, 0.2, 15)
    SAVE_setups_and_results(metabo_controller, "medic_splits")
    
    ML_setup_CV_and_algo(metabo_controller, "GridSearchCV")
    SAVE_setups_and_results(metabo_controller, "medic_ml")

    end_time = datetime.now()
    logger.info(f"---> Duration of run : {end_time - start_time}")   

if __name__ == "__main__":
    main()
