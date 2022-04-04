import numpy as np
import pandas as pd
import os
from .Utils import *

class DataFormat:
    """
    Take data file(s) as input and output a matrix where columns are samples and lines features. With the matrix comes
    a list of the columns names to retrieve the samples properly.
    """
    def __init__(self, path_to_data, use_raw):
        self.use_raw = use_raw
        self.inpath = path_to_data

        #TODO : make sure to handle the situation where the data file/data matrix is not from progenesis
        if os.path.isfile(path_to_data):
            self.in_format = "LCMS"
        elif os.path.isdir(path_to_data):
            self.in_format = "LDTD"
        else:
            raise TypeError("The given path is not valid, it have to be a file or a directory.")

    def convert(self):
        if self.in_format == "LCMS":
            data = self._convert_from_LCMS()
        elif self.in_format == "LDTD":
            data = self._convert_from_LDTD()
        return data

    def _convert_from_LCMS(self):
        file_ext = self.inpath.split(".")[-1]
        if "csv" in file_ext:
            # TODO : beware of the sep (, or ;)
            header = pd.read_csv(self.inpath, header=None, sep=",", nrows=3, index_col=0).fillna('').to_numpy()
            datatable = pd.read_csv(self.inpath, header=[0, 1, 2], sep=",", index_col=0)
        elif "xls" in file_ext or "od" in file_ext:  #TODO : restrict the "od" condition, might be too large
            datatable = pd.read_excel(self.inpath, header=2, index_col=0)
            header = pd.read_excel(self.inpath, nrows=1, index_col=0)
        else:
            raise TypeError("The input file is not of the right type, must be excel, odt or csv.")
        return self._read_Progenesis_data_table(datatable, header)

    def _convert_from_LDTD(self):
        # TODO :  implement the handling of LDTD data format
        return ""

    def _read_Progenesis_data_table(self, datatable, header):
        """
        Assumes Raw data columns are written after Normalized data columns in the file.
        :param datatable:
        :return:
        """
        print(header)
        if not self.use_raw and "Normalised abundance" in header[0]:  #header.columns.tolist():
            start_data = list(header[0]).index("Normalised abundance")
        elif self.use_raw and "Raw abundance" in header[0]:  #header.columns.tolist():
            start_data = list(header[0]).index("Raw abundance")
        else:
            raise KeyError("There is no Raw or Normalized abundance detected in the header.")

        new_header = []
        for l in header:
            new_header.append(list_filler(l))

        datatable.columns = new_header
        datatable_compoundsInfo = datatable.iloc[:, 0:start_data]
        datatable_compoundsInfo.columns = datatable_compoundsInfo.columns.droplevel([0, 1])
        datatable_compoundsInfo = datatable_compoundsInfo.T

        if self.use_raw:
            datatable = datatable["Raw abundance"]
            labels, sample_names = list(zip(*datatable.columns))
        else:
            datatable = datatable["Normalised abundance"]
            labels, sample_names = list(zip(*datatable.columns))

        datatable.columns = datatable.columns.droplevel(0)
        datatable = datatable.T

        return datatable_compoundsInfo, datatable, labels, sample_names


        # start_normalized = header.columns.tolist().index("Normalised abundance")
        # labels_array = np.array(header.iloc[0].tolist())

        # if with_raw:
        #     start_raw = header.columns.tolist().index("Raw abundance")
        #     sample_names = datatable.iloc[:, start_normalized:start_raw].columns
        #     labels = labels_array.tolist()[start_normalized:start_raw]
        # else:
        #     sample_names = datatable.iloc[:, start_normalized:].columns
        #     labels = labels_array.tolist()[start_normalized:]
        #
        # current_label = ""
        # for idx, l in enumerate(labels):
        #     if l != "nan":
        #         current_label = l
        #     else:
        #         labels[idx] = current_label
        #
        # if with_raw:
        #     datatable_compoundsInfo = datatable.iloc[:, 0:start_normalized]
        #     datatable_normalized = datatable.iloc[:, start_normalized:start_raw]
        #     datatable_raw = datatable.iloc[:, start_raw:]
        #     datatable_raw.columns = [i.rstrip(".1") for i in datatable_raw.columns]  # Fix the columns names
        #
        #     datatable_normalized = datatable_normalized.T
        #     datatable_raw = datatable_raw.T
        #     datatable_compoundsInfo = datatable_compoundsInfo.T
        #     datatable_normalized.rename(columns={"Compound": "Sample"})
        #     datatable_raw.rename(columns={"Compound": "Sample"})
        #
        #     if self.use_raw:
        #         return datatable_compoundsInfo, datatable_raw, labels, sample_names
        #     else:
        #         return datatable_compoundsInfo, datatable_normalized, labels, sample_names
        # else:
        #     datatable_compoundsInfo = datatable.iloc[:, 0:start_normalized]
        #     datatable_normalized = datatable.iloc[:, start_normalized:]
        #     datatable_normalized = datatable_normalized.T
        #     datatable_compoundsInfo = datatable_compoundsInfo.T
        #     datatable_normalized.rename(columns={"Compound": "Sample"})
        #     return datatable_compoundsInfo, datatable_normalized, labels, sample_names