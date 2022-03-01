from sklearn.model_selection import train_test_split


class Splits:
    def __init__(self, labels: list, samples_id: list, train_test_proportion: float, number_of_splits: int):
        self.labels = labels
        self.samples_id = samples_id
        self.train_test_proportion = train_test_proportion
        self.number_of_splits = number_of_splits
        self.splits = []
        self._computeSplits()

    def _computeSplits(self):
        X = []
        y = []
        for label_index, sample_id in enumerate(self.samples_id):  # itère sur chq id unique
            X.append(sample_id)
            y.append(self.labels[label_index])

        for split_index in range(self.number_of_splits):
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.train_test_proportion,
                                                                random_state=split_index)

            self.splits.append([X_train, X_test, y_train, y_test])

    def getSplitsWithIndex(self, split_index: int) -> list:
        return self.splits[split_index]

