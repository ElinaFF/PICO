#!/usr/bin/env python
__author__ = 'Alexandre Drouin'

import os

import numpy as np
import xlrd

from ...spectrum import Spectrum


class PhytronixExcelFile:
    """
    Loads Phytronix excel MS data files.
    """

    def __init__(self, file_name):
        """
        Parameters:
        -----------
        file_name: string
            The name of the data file to load.
        """
        self.filename = file_name
        self.workbook = None

        if not os.path.exists(self.filename):
            raise RuntimeError("Filename %s does not exist." % (self.filename,))

        self.workbook = xlrd.open_workbook(self.filename)

    def get_mean_spectra(self, mz_precision=20):
        """
        Loads the mean spectrum for each sample with multiple scans in a data file.

        Parameters:
        ----------
        mz_precision: int, default=20
            The maximum number of decimals for the mz_values. Values be rounded to this precision.


        Returns:
        --------
        spectra: list, shape=[n_samples]
            The mean spectrum loaded from the data file for each sample.
        """
        return self._load_spectra(mean=True, mz_precision=mz_precision)

    def get_spectra(self, mz_precision=20):
        """
        Loads all spectra for each sample in a PhytronixExcelFile

        Parameters:
        ----------
        mz_precision: int, default=20
            The maximum number of decimals for the mz_values. Values be rounded to this precision.


        Returns:
        --------
        spectra: list, shape=[n_samples, n_spectra_per_sample] *** Note: n_spectra_per_sample can vary by sample
            Every spectrum for each sample in the data file.

        XXX:
        -----
        If we decide to return a numpy array of objects here, we must make sure that all samples have the same
        number of spectra. This is why a list is returned.

        """
        return self._load_spectra(mean=False, mz_precision=mz_precision)

    def _load_spectra(self, mean=True, mz_precision=20):
        """
        XXX:
        -----
        If we decide to return a numpy array of objects here, we must make sure that all samples have the same
        number of spectra if mean=False. This is why a list is returned.
        """
        spectrum_sheets = [sheet for sheet in self.workbook.sheets() if sheet.ncols > 2 and sheet.nrows > 2 and "SPECTRUM" in sheet.cell(1, 1).value]

        spectra = []
        for sheet in spectrum_sheets:
            metadata = {}
            intensity_values = []
            mz_values = []

            spectrum_col_idx = [i for i in xrange(sheet.ncols) if sheet.cell(1, i).value != ""]

            # Load metadata from header
            # NOTE: The metadata is loaded for each spectrum for the sample, although the avg masses are returned
            metadata["title"] = [sheet.cell(0, i).value for i in spectrum_col_idx]
            metadata["spectrum_type"] = [1 if sheet.cell(1, i).value == "SPECTRUM - MS" else -1 for i in
                                         spectrum_col_idx] #-1 = Unknown
            metadata["raw_files"] = [sheet.cell(2, i).value for i in spectrum_col_idx]
            metadata["mz_range"] = [
                (float(sheet.cell(3, i).value[sheet.cell(3, i).value.find("["): -1].replace("[", "").split("-")[0]),
                 float(sheet.cell(3, i).value[sheet.cell(3, i).value.find("["): -1].replace("[", "").split("-")[1]))
                for i in spectrum_col_idx]
            metadata["scan_range"] = [(int(sheet.cell(4, i).value.replace("Scan #: ", "").split("-")[0]),
                                       int(sheet.cell(4, i).value.replace("Scan #: ", "").split("-")[1]))
                                      for i in spectrum_col_idx]
            metadata["retention_time"] = [(float(sheet.cell(5, i).value.replace("RT: ", "").split("-")[0]),
                                           float(sheet.cell(5, i).value.replace("RT: ", "").split("-")[1]))
                                          for i in spectrum_col_idx]
            metadata["av"] = [int(sheet.cell(6, i).value.replace("AV: ", "")) for i in spectrum_col_idx]
            metadata["n_peaks"] = [int(sheet.cell(7, i).value.replace("Data points: ", "")) for i in spectrum_col_idx]
            metadata["sample_name"] = sheet.name
            metadata["n_scans"] = len(spectrum_col_idx)

            # Check file sanity
            assert sheet.cell(8, spectrum_col_idx[0]).value == "Mass"
            assert sheet.cell(8, spectrum_col_idx[0] + 1).value == "Intensity"

            spectrum_row_idx = range(9, sheet.nrows)

            # Sanity check the number of peaks
            assert len(spectrum_row_idx) == metadata["n_peaks"][0]

            for i in spectrum_row_idx:
                # Spectrum peaks are stored in 2 cells: mz_value and intensity_value
                row_mz_value = [float(sheet.cell(i, j).value) for j in spectrum_col_idx]
                row_intensity_value = [float(sheet.cell(i, j + 1).value) for j in spectrum_col_idx]

                # Sanity check mz_values before computing the mean
                assert np.allclose(row_mz_value, row_mz_value[0])

                mz_values.append(row_mz_value[0])
                intensity_values.append(row_intensity_value)

            if mean:
                spectra.append(Spectrum(mz_values=np.array(mz_values),
                                        mz_precision=mz_precision,
                                        intensity_values=np.mean(intensity_values, axis=1),
                                        metadata=metadata))
            else:
                sample_spectra = []
                for i in xrange(len(spectrum_col_idx)):
                    spectrum_metadata = {}
                    for key, value in metadata.iteritems():
                        if type(value) is list and len(value) == len(spectrum_col_idx):
                            spectrum_metadata[key] = value[i]
                        else:
                            spectrum_metadata[key] = value

                    sample_spectra.append(Spectrum(mz_values=np.array(mz_values),
                                                   mz_precision=mz_precision,
                                                   intensity_values=np.array(intensity_values)[:, i],
                                                   metadata=spectrum_metadata))
                spectra.append(sample_spectra)

        return spectra
