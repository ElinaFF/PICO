from metabodashboard.domain import MetaboController

METADATA_PATH = 'metadata_test.csv'
DATAMATRIX_PATH = 'DataMatrix.csv'

def main():

    metabo_controller = MetaboController()

    if not metabo_controller.set_metadata_dataframe_from_path(METADATA_PATH):
        raise RuntimeError('Metadata file not setted')
    metabo_controller.set_data_matrix_from_path(DATAMATRIX_PATH, use_raw=False)
    print("Metadata and DataMatrix are set_from_path")

    metabo_controller.set_id_column('Sample')
    metabo_controller.set_target_column('diet')
    metabo_controller.add_experimental_design({"N-A": "NA", "MED": ["MED", "MED/w"]})
    print("Experimental design added")

    metabo_controller.set_splits_parameters(20, 0.8)
    metabo_controller.set_selected_models(['DecisionTree', 'RandomForest'])

    print("Learning starts...")
    metabo_controller.learn(5)
    print("finished")


if __name__ == '__main__':
    main()
