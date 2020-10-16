import json

class SplitProcessing():
    def __init__(self, file):
        with open(file, "r") as conf_file:
            dict = json.load(conf_file)

        self.type_process = dict["Type_of_processing"]
        self.opts_process = dict["Options_of_processing"]
        self.nbr_splits = dict["Nbr_splits"]
        self.nbr_processes = dict["Nbr_processes"]
        self.prop_in_test = dict["Proportion_in_test"]
        self.peakT = dict["Peak_threshold"]
        self.autoOpt = dict["AutoOptimize_nbr"]
        self.exp_designs = dict["Experimental_designs"]
        self.pairing = {"pn": dict["Pairing_pos_neg"], "other": dict["Pairing_other"]}
        self.Splits = dict["Splits"]
        self.metadata = dict["Metadata"]

    def get_list_all_files(self):
        return self.Splits["split0"][0] + self.Splits["split0"][1]

    def process_files(self):
        # determiner quel type de donnees/processing
        # loader files avec une fct
        # faire appel à la fonction adequate de processing
        # repartir data dans splits, si besoin
        return ""

    def _load_data_from_files(self, list_of_files):
        return ""

    def _process_pre_spliting(self):
        # if type of processing is LCMS or LDTD1
        return ""

    def _process_post_spliting(self):
        # if type of processing is LDTD2
        return ""

    def _build_splits_with_data_corresponding_to_file(self):
        return ""
