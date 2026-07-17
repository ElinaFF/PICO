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

METADATA_PATH = "data/MTBLS7337_metadata.csv"
DATAMATRIX_PATH = "data/MTBLS7337_4DatamatricesCombined_forML.csv"


##############################
#      Setup experiment      #
##############################

def SPLITS_setup_files(controller):
    """
    controller : Controller object
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
    # If Not Progenesis, removing RT before 1min should part of preprocessing prior to using the PICO
    controller.set_raw_use_for_data(False)
    controller.set_data_matrix_remove_rt(False)
    controller.set_data_matrix_from_path(DATAMATRIX_PATH, from_base64=False)
    controller.set_metadata(METADATA_PATH, from_base64=False)

def SPLITS_setup_classification_designs(controller):
    """
    controller : Controller object
    """
    controller.set_id_column("Sample_Name")
    #controller.set_target_columns(["Factor Value[Outcome]"])
    controller.set_target_columns(["Factor Value[Disease Staging]", "Factor Value[Disease severity]", "Factor Value[Outcome]"])
    #controller.set_target_columns(["Factor Value[Sample Type]", "Factor Value[Smoking]"])

    # Designs are defined as dict with labels as keys and classes(if multiple link with "__") as values
    # The classes should correspond to values found in the column(s) defined in controller.set_target_columns() function. 
    #controller.add_classification_design({"0_ctrls": ["Healthy Control"], "1_acute": ["Acute"]})
    #controller.add_classification_design({"NEG_Case_Current": ["Case__Current Smoker"], "Ctrl_Current": ["Control__Current Smoker"]})
    #controller.add_classification_design({"NEG_Case_Former": ["Case__Former Smoker"], "Ctrl_Former": ["Control__Former Smoker"]})
    #controller.add_classification_design({"NEG_Case_Never": ["Case__Never Smoker"], "Ctrl_Never": ["Control__Never Smoker"]})
    controller.add_classification_design({"0_convalescence": ["convalescence__non-severe COVID-20__With Event", 
                                                                "convalescence__non-severe COVID-20__Event-Free", 
                                                                "convalescence__severe COVID-19__Event-Free", 
                                                                "convalescence__recovered__Event-Free", 
                                                                "convalescence__severe COVID-19__With Event", 
                                                                "convalescence__recovered__With Event"], 
                                        "1_acute": ["Acute__non-severe COVID-20__Event-Free", "Acute__severe COVID-19__Event-Free",
                                                     "Acute__recovered__Event-Free", "Acute__recovered__With Event", 
                                                     "Acute__non-severe COVID-20__With Event", "Acute__severe COVID-19__With Event"]})
    #controller.add_classification_design({"0_recovered": ["convalescence__recovered__Event-Free", "convalescence__recovered__With Event", 
    #                                                        "Acute__recovered__With Event", "Acute__recovered__Event-Free"],
    #                                    "1_NonSevere": ["Acute__non-severe COVID-20__Event-Free", "convalescence__non-severe COVID-20__With Event", 
    #                                                    "convalescence__non-severe COVID-20__Event-Free", "Acute__non-severe COVID-20__With Event"]})
    #controller.add_classification_design({"0_NonSevere": ["Acute__non-severe COVID-20__Event-Free", "convalescence__non-severe COVID-20__With Event", 
    #                                                        "convalescence__non-severe COVID-20__Event-Free", "Acute__non-severe COVID-20__With Event"],
     #                                   "1_Severe": ["Acute__severe COVID-19__Event-Free", "convalescence__severe COVID-19__Event-Free", 
      #                                                  "convalescence__severe COVID-19__With Event", "Acute__severe COVID-19__With Event"]})
    #controller.add_classification_design({"0_recovered": ["convalescence__recovered__Event-Free", "convalescence__recovered__With Event", 
    #                                                        "Acute__recovered__Event-Free", "Acute__recovered__With Event"], 
    #                                    "1_Severe_EventFree": ["Acute__severe COVID-19__Event-Free", "convalescence__severe COVID-19__Event-Free"]})
    #controller.add_classification_design({"0_NonSevere_WithEvent": ["convalescence__non-severe COVID-20__With Event", "Acute__non-severe COVID-20__With Event"],
    #                                    "1_Severe_WithEvent": ["convalescence__severe COVID-19__With Event", "Acute__severe COVID-19__With Event"]})
    #controller.add_classification_design({"0_Severe_EventFree": ["Acute__severe COVID-19__Event-Free", "convalescence__severe COVID-19__Event-Free"],
     #                                   "1_Severe_WithEvent": ["convalescence__severe COVID-19__With Event", "Acute__severe COVID-19__With Event"]})
    #controller.add_classification_design({"0_Controls": ["Healthy Control__Healthy Control__"],
    #                                    "1_recovered_EventFree": ["convalescence__recovered__Event-Free", "Acute__recovered__Event-Free"]})
    #controller.add_classification_design({"Event-Free": ["Event-Free"],
    #                                    "With_Event": ["With Event"]})


def SPLITS_setup_splits_and_balancing(controller, proportion_splits, nbr_splits=None, split_from_seed=None):
    """
    controller : Controller object
    proportion_splits : proportion of sample in test set in decimal (0 to 1)
    nbr_splits : number of splits to compute
    split_from_seed : setting a seed to run only one split with this particular seed
    """
    controller.set_train_test_proportion(proportion_splits)
    #controller.set_pairing_group_column("SUPP_subject_id")

    # The balance correction is specific to a design, refer to a design by its name (LABEL1_vs_LABEL2)
    # Choosing balance correction value : see documentation for explanation
    #controller.set_balance_correction_for_experiment("Event-Free_vs_With_Event", 15)
    controller.set_balance_correction_for_experiment("0_convalescence_vs_1_acute", 0)
    #controller.set_balance_correction_for_experiment("0_recovered_vs_1_NonSevere", 0)
    #controller.set_balance_correction_for_experiment("0_NonSevere_vs_1_Severe", 6)
    #controller.set_balance_correction_for_experiment("0_recovered_vs_1_Severe_EventFree", 0)
    #controller.set_balance_correction_for_experiment("0_NonSevere_WithEvent_vs_1_Severe_WithEvent", 10)
    #controller.set_balance_correction_for_experiment("0_Severe_EventFree_vs_1_Severe_WithEvent", 2)
    #controller.set_balance_correction_for_experiment("0_Controls_vs_1_recovered_EventFree", 6)
    

    if nbr_splits is not None and split_from_seed is not None:
        print("There is two competing arguments to define the number of splits to use. Choose only nbr_splits or split_from_seed.")
    elif nbr_splits is not None:
        controller.set_number_of_splits(nbr_splits)
        controller.create_splits()
    elif split_from_seed is not None:
        controller.create_test_split_from_seed(split_from_seed)
    else:
        print("An argument is missing to specify the number of splits to run.")


def ML_setup_CV_and_algo(controller, cv_algo):
    """
    controller : Controller object
    cv_algo : Either GridSearchCV(default) or RandomizedSearchCV
    """
    controller.set_multithreading(True)

    # Available defaults : ["DecisionTree", "RandomForest", "SCM", "RandomSCM"]
    controller.set_selected_models(["DecisionTree", "RandomForest", "SCM", "RandomSCM"])
    
    # (if GridSearch you can simply comment the line)
    controller.set_cv_type(cv_algo)
    
    # Needed if RandomizedSearchCV is chosen
    # list of values for required parameters of CV algorithm, randomSearch requires n_iter arg : the default here is 10
    # (if GridSearch you can simply comment the line)
    #controller.set_cv_algorithm_configuration([20])
    
    controller.set_cv_folds(5)
    controller.learn()


def SAVE_setups_and_results(controller, experiment_path):
    """
    controller : Controller object
    experiment_path :  
        -   'pico_splits' the save of only splits parameters, after the "splits tab"
        -   'pico_ml' the save of all parameters and results, after the "ml tab"
        This argument should not take a different path from the two above, it risks breaking the code. 
    """
    metabo_expe_filename = Utils.get_metabo_experiment_path(experiment_path) # Get save file path
    metabo_expe_obj = controller.generate_save()
    Utils.dump_metabo_expe(metabo_expe_obj) # Dump the classification design to the dump folder
    Utils.dump_metabo_expe(metabo_expe_obj, metabo_expe_filename) # Save the classification design
    # free memory from object
    del metabo_expe_obj


def run_an_experiment(nbr_splits):
    start_time = datetime.now()
    logger.info(f"---> Starting at : {start_time}")
    controller = Controller()

    SPLITS_setup_files(controller)
    SPLITS_setup_classification_designs(controller)
    SPLITS_setup_splits_and_balancing(controller, 0.2, nbr_splits=nbr_splits)
    SAVE_setups_and_results(controller, "pico_splits")

    ML_setup_CV_and_algo(controller, "GridSearchCV")
    SAVE_setups_and_results(controller, "pico_ml")

    end_time = datetime.now()
    logger.info(f"---> Duration of run : {end_time - start_time}")

###############################
#        Main function        #
###############################

@log_exceptions(logger)
def main():

    #run_an_experiment(1)
    #run_an_experiment(10)
    #run_an_experiment(20)
    run_an_experiment(30)
    #run_an_experiment(40)
    #run_an_experiment(50)
    #run_an_experiment(100)

if __name__ == "__main__":
    main()
