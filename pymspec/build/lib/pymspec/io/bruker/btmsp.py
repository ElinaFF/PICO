#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__='pier-luc'

import logging
import numpy as np
from ...spectrum import Spectrum
import zipfile
import xml.etree.ElementTree as ET
import tempfile
import shutil


def load_btmsp(files, mz_precision=1, verbose=False):
    """
    Loads a list of Bruker btmsp files into Pymspec
    :param files: List of files
    :param mz_precision:
    :param verbose:
    :return:A list of Spectrum
    """

    spectra = []
    directory_name = tempfile.mkdtemp()
    logging.debug("Directory name: "+directory_name+'\n')
    for f in files:
        mz = []
        intensities = []
        massError = []
        relativeIntensitiesError = []
        zip_ref = zipfile.ZipFile(f, 'r')
        files_in_archive = zip_ref.namelist()
        if len(files_in_archive) != 2:
            raise IOError("Not a btmsp file")
        zip_ref.extractall(directory_name)
        zip_ref.close()
        for g in files_in_archive:
            if g == '[Content_Types].xml':  # Not an important file
                continue
            logging.debug("Filename:" + g + "\n")
            tree = ET.parse(directory_name + "/" + g)
            root = tree.getroot()
            for peak in root.findall("./mainSpectrum/mainSpectrumPeaklist/peaks/peak"):
                mz.append(float(peak.get("mass")))
                massError.append(float(peak.get("massError")))
                intensities.append(float(peak.get("relativeIntensity")))
                relativeIntensitiesError.append(float(peak.get("relativeIntensityError")))
        metadata = {"massError" : massError, "relativeIntensityError" : relativeIntensitiesError, "file" : f}
        spectra.append(Spectrum(np.array(mz), np.array(intensities), mz_precision=mz_precision, metadata=metadata))
    shutil.rmtree(directory_name, ignore_errors=True)
    return spectra