from metabodashboard.domain import SplitGroup, MetaData


class ExperimentalDesign:
    def __init__(self, classes_design: dict, number_of_splits: int, train_test_proportion: float, metadata: MetaData):
        self.classes_design = classes_design
        self.name = ""
        self._computeName()

        self.split_group = SplitGroup(metadata, train_test_proportion, number_of_splits, self.name)

    def _computeName(self):
        class_list = self.classes_design.keys()
        for class_name in class_list:
            self.name += class_name + "_vs_"
        self.name = self.name[:-4]
