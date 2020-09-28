__author__='pier-luc'


from preprocessing.Utils import *
import numpy as np
from pymspec import Spectrum
from pymspec.spectrum import copy_spectrum_with_new_intensities


class Intensity_normalizer():
    """
    Will apply a ratio to the intensities of every spectrum so that the intensity of a reference m/z is identical
    in every spectrum
    This should help in making the spectrum comparable by correcting variations due to ionisation, spotting, ect.
    """
    def __init__(self, ref_mz = 406.1859, window=90):
        self.reference_mz = ref_mz
        self.average_intensity = 0
        self.window = window

    def fit(self, spectrum):
        #find ref mz and calculate average intensity. Will be the "intensity ref point".
        intensities = []
        for spect in spectrum:
            mz = self.find_ref_mass_in_spectra(spect)
            intensity = spect.peaks()[mz]
            intensities.append(intensity)
        average = np.average(np.array(intensities))
        self.average_intensity = average

    def transform(self, spectrum):
        for i, spect in enumerate(spectrum):
            #find ref mz in spect
            mz = self.find_ref_mass_in_spectra(spect)
            intensity = spect.peaks()[mz]
            #calculate intensity
            ratio = self.average_intensity/intensity
            #
            new_intensities = spect.intensity_values * ratio
            spectrum[i] = copy_spectrum_with_new_intensities(spect, new_intensities)

    def find_ref_mass_in_spectra(self, spectrum):
        """
        Search for the measured mz of the virtual lock-mass. Will return the most intense peaks in the window.
        :param window: the m/z area around each lock-mass. If peak is outside this window, it won't be found.
                       The window is in ppm.
        :param spectrum: The spectrum in which the measured m/z are searched
        :return:A list of measured m/z corresponding to the vlock-mass.
        :raises ValueError if a virtual lock mass is not found.
        """
        # TODO: Problem because there is a possibility we don't find the good peak because no threshold is applied.
        observed_mz = []
        num_of_skipped = 0
        peak = -1
        intensity = -1
        try:
            possible_matches = binary_search_find_values(spectrum.mz_values, self.reference_mz, self.window)
        except ValueError:
            raise ValueError("The reference mass was not found in the spectrum")
        if len(possible_matches) == 0:
            raise ValueError("The reference mass was not found in the spectrum")
        else:  # Will pick the most intense peak in the window
            intensities = []
            for i in possible_matches:
                intensities.append(spectrum.peaks()[i])
            intensities, possible_matches = (list(t) for t in zip(*sorted(zip(intensities, possible_matches))))
            peak = possible_matches[-1]
        observed_mz = (np.round(peak, 4))
        return observed_mz