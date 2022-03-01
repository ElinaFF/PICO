import pandas as pd


class MetaData:
    def __init__(self, meta_data: pd.DataFrame):
        self.meta_data = meta_data

    def getMetaData(self) -> pd.DataFrame:
        return self.meta_data

