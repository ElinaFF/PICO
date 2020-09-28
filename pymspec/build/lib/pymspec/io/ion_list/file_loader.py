#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author = Francis Brochu

import logging
import numpy as np
from ...spectrum import Spectrum

def load_ion_list(files, mz_precision=3, verbose=False):
    """
    Loads multiple ion list files

    Parameters:
    -----------
    files: list of str
           A list of ion list file names

    Returns:
    --------
    spectra: list of Spectrum objects
            A list of mass spectra extracted from the ion list files
    """

    logging.debug("Loading %d spectra"%len(files))

    #load ion list files into list
    #list of spectra, each a list of points, each a tuple [mz, i]
    spectrum_list = []
    for file in files:
        mz = []
        intensity = []

        f = open(file, "r")

        # Skip the header (6 lines)
        for i in range(6):
            f.readline()

        line = f.readline()
        #to end when it hits the end of the spectrum
        end_of_spec = False
        while((line != "") and (end_of_spec == False)):
            if(line[0] != "["):
                line = line.replace(" ", "\t")
                sline = line.split("\t")
                mz.append(float(sline[1]))
                intensity.append(float(sline[2]))
            else:
                end_of_spec = True
            line = f.readline()

        f.close()
        metadata = {}
        metadata["file"] = file
        spectrum_list.append(Spectrum(mz_values=np.array(mz, dtype=np.float),
                                     intensity_values=np.array(intensity, dtype=np.float),
                                     mz_precision=mz_precision, metadata=metadata))
        
        logging.debug("%.2f %% loaded"%(float(len(spectrum_list)) / len(files) * 100.0))
        
    return spectrum_list
