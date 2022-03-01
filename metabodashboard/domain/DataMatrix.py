import pandas as pd


class DataMatrix:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def getData(self) -> pd.DataFrame:
        return self.data
