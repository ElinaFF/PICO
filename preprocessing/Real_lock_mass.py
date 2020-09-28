__author__='pier-luc'

import logging

from pymspec import Spectrum
from Utils import *


class Real_lock_mass_corrector():
    """
    This is a real lock-mass corrector. The objective is to correct the spectra from a plate to place masses closer to
    their real m/z. This step should be perform before VLM and RFMSA. It should help at reducing the number of error
    caused by the VLM and RFMSA. Almost mandatory for clustering.
    """
    def __init__(self,  exact_mass_values=[], mz_precision=4, search_window=500, select_most_intense_peak=True,
                 minimal_intensity=1000):
        self.exact_mass_values = exact_mass_values
        self.mz_precision = mz_precision
        self.search_window = search_window
        self.select_most_instense_peak = select_most_intense_peak

        if self.select_most_instense_peak and minimal_intensity != 1000:
            UserWarning("The minimal instensity is not used when select_most_intense_peak is True")

        self.minimal_instensity = minimal_intensity

        if not self.select_most_instense_peak:
            raise NotImplementedError("This option is not implemented yet")

        self.measured_mass = []
        self.correction_ratios = []
        self._trained = False

    def train(self, rlm_spectrum):
        """
        Will use the rlm_spectrum to set the measured mass and calcul the correction ratio.
        After execution de Real_lock_mass_corrector is ready to use.
        :param rlm_spectrum: The real lock-mass Pymspec spectrum
        :return: Nothing
        """
        for rlm in self.exact_mass_values:
            possible_points = binary_search_find_values(rlm_spectrum.mz_values, rlm, self.search_window)
            if len(possible_points) <= 0:
                raise ValueError("A point in the exact mass list is not found in the rlm_spectrum.\n"
                                 "Are you using the RLM spectrum? ")
            to_chose = []
            for i in possible_points:
                to_chose.append((i,rlm_spectrum.peaks()[i]))
            self.measured_mass.append(self._find_highest_point(to_chose)[0])
        self._calculate_correction_ratios()
        self._trained = True

    def apply(self, spectra):
        """
        Apply the trained
        :param spectra: A list of Pymspec spectrum to correct
        :return: A list of corrected spectrum
        """
        if not self._trained:
            raise ValueError("The real lock mass corrector is not trained yet.")

        corrected_spectra = []
        for spect in spectra:
            before = len(spect.mz_values)
            corrected_spectra.append(self._apply(spect))
            if before != len(corrected_spectra[-1].mz_values):
                logging.debug(str(before))
                logging.debug(str(len(corrected_spectra[-1].mz_values)))
                raise ValueError("There are points missing")
        return corrected_spectra


    def _apply(self, spectrum):
        corrected_mz = self._correct_points_smaller_than(spectrum)
        index = 0
        while index < len(self.correction_ratios)-1:
            corrected_mz += self._correct_points_between(spectrum, self.measured_mass[index], self.measured_mass[index+1],
                                                        self.correction_ratios[index], self.correction_ratios[index+1])
            index += 1
        corrected_mz += self._correct_points_greater_than(spectrum)
        if len(corrected_mz) != len(spectrum.mz_values):
            raise ValueError("There should be the same number of mz than in the initial spectrum:" +
                             str(len(corrected_mz)) + " vs " + str(len(spectrum.mz_values)))
        spectrum = Spectrum(np.array(corrected_mz), spectrum.intensity_values, spectrum.mz_precision, spectrum.metadata)
        return spectrum

    def _calculate_correction_ratios(self):
        """
        Calculate the correction ratios for the virtual lock-mass and the corresponding observed mz
        :return: Nothing
        :raises: ValueError if one the list is empty, if list length is not equal or if there is a null or negative
        value
        """
        if len(self.measured_mass) <= 0 or len(self.exact_mass_values) <= 0:
            raise ValueError("There is no value in vlock_mass or observed_mz")
        if len(self.measured_mass) != len(self.exact_mass_values):
            raise ValueError("v_lock_mass and observed_mz have not the same amount of values")

        correction_ratios = []
        for i, exact_mz in enumerate(self.exact_mass_values):
            measured_mz = self.measured_mass[i]
            if exact_mz <= 0 or measured_mz <= 0:
                raise ValueError("Cannot calculate ratio for a null or nagative mz")
            ratio = np.float(exact_mz / measured_mz)
            self.correction_ratios.append(ratio)

    def _correct_points_smaller_than(self, spectrum):
        """
        Will apply the correction ratio to all points that are smaller or equal to the lowest observed reference mass.
        Flat correction ratio.
        :param spectrum: The spectrum to correct
        :return: A section of mz that are corrected
        """
        logging.debug("Length of mz before correction with smaller: %s" % len(spectrum.mz_values))

        ratio = self.correction_ratios[0]
        right_limit_value = self.measured_mass[0]

        mz_list = spectrum.mz_values.tolist()
        corrected_mz = []
        right = binary_search_for_right_range(mz_list, right_limit_value)
        index = 0
        logging.debug("mz for smaller: %s" % right_limit_value)
        logging.debug("left: %s and value: %s" % (0, mz_list[0]))
        logging.debug("right: %s and value: %s" % (right, mz_list[right]))

        while index < right:
            corrected_mz.append(np.round(mz_list[index] * ratio, 4))
            index += 1
        if mz_list[index] < right_limit_value:
            # Some values are missed by the binary search in some cases
            corrected_mz.append(np.round(mz_list[index] * ratio, 4))
        return corrected_mz


    def _correct_points_greater_than(self, spectrum):
        """
        Will apply the correction ratio to all points that are greater or equal to the gratest observed reference mass.
        Flat correction ratio
        :param spectrum: The spectrum to correct.
        :return: A section of corrrected mz.
        """
        ratio = self.correction_ratios[-1]
        left_limit_value = self.measured_mass[-1]
        corrected_mz = []

        if left_limit_value <= 0 or ratio <= 0:
            raise ValueError("Mz and ration cannot be null or negative")

        mz_list = spectrum.mz_values.tolist()
        left = binary_search_for_right_range(mz_list, left_limit_value)
        index = left

        if mz_list[index] < left_limit_value:
            # adjust index for particular cases
            index += 1
        while index < len(mz_list):
            corrected_mz.append(np.round(mz_list[index] * ratio, 4))
            index += 1
        return corrected_mz


    def _correct_points_between(self, spectrum, left_bound, right_bound, ratio1, ratio2):
        if left_bound <= 0 or right_bound <= 0 or ratio1 <= 0 or ratio2 <= 0:
            raise ValueError("Mz and ratios cannot be null or negative")

        m, c = self._create_correction_function(left_bound, right_bound, ratio1, ratio2)

        mz_list = spectrum.mz_values.tolist()
        right = binary_search_for_right_range(mz_list, right_bound)
        left = binary_search_for_left_range(mz_list, left_bound)
        index = left
        corrected_mz = []

        while index < right:
            corrected_mz.append(np.round(mz_list[index]*(m*(mz_list[index])+c), 4))
            index += 1
        if mz_list[index] < right_bound:
            corrected_mz.append(np.round(mz_list[index]*(m*(mz_list[index])+c), 4))
        return corrected_mz


    @staticmethod
    def _create_correction_function(mz1, mz2, ratio1, ratio2):
        """
        Create the y = m*x + b function for the 2 points in parameter
        :param mz1: lowest mz
        :param mz2: highest mz
        :param ratio1: correction ratio at mz1
        :param ratio2: correction ratio at mz2
        :return: a numpy function that can correct the values between mz1 and mz2
        :raises: ValueError is an mz or ratio is <= 0
        """
        if mz1 <= 0 or mz2 <= 0 or ratio1 <= 0 or ratio2 <= 0:
            raise ValueError("Mz and ratios cannot be null or negative")

        x = np.array([mz1, mz2])
        y = np.array([ratio1, ratio2])
        x = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(x, y)[0]
        logging.debug("M: %s, C %s" % (m, c))
        return m, c

    @staticmethod
    def _find_highest_point(points):
        """
        Return the point with the highest intensity. Not fast but usable for small list of points
        :param points: A list of point (ex: (0,0)
        :return: A point
        """
        max = 0
        result = (0,0)
        for p in points:
            if p[1] > max:
                max = p[1]
                result = p
        return result


if __name__ == '__main__':
    import glob
    from pymspec.io.ion_list.file_loader import *

    logging.basicConfig(level=logging.ERROR)
    logging.debug("Welcome to the RLM test suit.\n")

    rlm_spect_file = "/home/pier-luc/plapie01_32/Mass_spectrometry/Data/Lupus_LDTD/Data_fct1/LOCK-MASS_ACN_MeOH_pos_S1_R2.lcs"
    path_to_spect_files = "/home/pier-luc/plapie01_32/Mass_spectrometry/Data/Lupus_LDTD/Data_fct1/SAIN*ACN_MeOH_pos*.lcs"
    files_to_correct = glob.glob(path_to_spect_files)

    rlm_spect = load_ion_list([rlm_spect_file], mz_precision=4)[0]

    ref_masses = [152.0706, 406.1932, 609.2807]
    rlm = Real_lock_mass_corrector(ref_masses)
    rlm.train(rlm_spect)

    spectra = load_ion_list(files_to_correct, mz_precision=4)
    corrected = rlm.apply(spectra)
    logging.debug("\nCompleted!\n")



































