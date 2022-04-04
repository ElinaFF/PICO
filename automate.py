from metabodashboard.domain import MetaboController

METADATA_PATH = 'meta.xlsx'
DATAMATRIX_PATH = 'data.csv'

def main():

    metabo_controller = MetaboController()

    metabo_controller.set_metadata_dataframe_from_path(METADATA_PATH)
    metabo_controller.set_data_matrix_from_path(DATAMATRIX_PATH, use_raw=False)

    metabo_controller.set_id_column('Sample')
    metabo_controller.set_target_column('diet')
    metabo_controller.add_experimental_design({"NA": "NA", "MED": ["MED", "MED/w"]})

    metabo_controller.set_splits_parameters(20, 0.8)
    metabo_controller.set_selected_models(['RandomForest', 'DecisionTree'])

    metabo_controller.learn(5)


if __name__ == '__main__':
    main()
