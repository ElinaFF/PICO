from datetime import datetime
from override_Controller import Controller
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

METADATA_PATH = "test_data/MTBLS7337_metadata.csv"
DATAMATRIX_PATH = "test_data/MTBLS7337_4DatamatricesCombined_forML.csv"


##############################
#      Setup experiment      #
##############################




def ML_setup_CV_and_algo(controller, cv_algo, split_start, split_end):
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
    controller.learn(split_start, split_end)


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


def finish_an_experiment(split_start, split_end):
    start_time = datetime.now()
    logger.info(f"---> Starting at : {start_time}")
    controller = Controller()

    dto = Utils.load_metabo_expe("test_data/pico_splits_20261015_121327_paired10ksplits.mtxp")
    controller.full_restore(dto)

    ML_setup_CV_and_algo(controller, "GridSearchCV", split_start, split_end)
    SAVE_setups_and_results(controller, "pico_ml")

    end_time = datetime.now()
    logger.info(f"---> Duration of run : {end_time - start_time}")

###############################
#        Main function        #
###############################

@log_exceptions(logger)
def main():

    finish_an_experiment(3, 5)


if __name__ == "__main__":
    main()
