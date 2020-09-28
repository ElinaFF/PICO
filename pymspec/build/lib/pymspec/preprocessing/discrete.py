__author__ = 'Alexandre Drouin'

import copy
import numpy as np
from ..base import PreprocessorMixin
from ..spectrum import unify_mz
from ..spectrum import Spectrum, copy_spectrum_with_new_intensities, copy_spectrum_with_new_mz_and_intensities
from ..utils import binary_search_for_left_range, binary_search_for_right_range

class IntensityBinarization(PreprocessorMixin):
    """
    A pre-processor for converting all peak intensities to binary values.
    """
    def transform(self, spectra_list):
        """
        Make peaks binary for a list of spectra.

        Parameters
        ----------
        spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of spectra to transform.

        Returns
        -------
        transformed_spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of transformed spectra.
        """
        spectra_list = np.array(spectra_list)
        for i, spectrum in enumerate(spectra_list):
            intensity_values = spectrum.intensity_values
            binary_values = np.array(intensity_values > 0, dtype=int)
            spectra_list[i] = copy_spectrum_with_new_intensities(spectrum, binary_values)

        return spectra_list

class MostIntensePeakFiltering(PreprocessorMixin):
    """
    A pre-processor for removing the less intense peaks.
    """
    def __init__(self, frac_of_peaks=0.5):
        """
        Constructor.

        Parameters
        ----------
        frac_of_peaks: float, default=0.5
            The fraction of most intense peaks to keep.
        """
        self.frac_of_peaks = frac_of_peaks

    def transform(self, spectra_list):
        """
        Filter peaks for a list of spectra.

        Parameters
        ----------
        spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of spectra to transform.

        Returns
        -------
        transformed_spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of transformed spectra.
        """

        spectra_list = np.array(spectra_list)
        for i, spectrum in enumerate(spectra_list):
            intensity_sort = np.argsort(spectrum.intensity_values * -1)

            max_peaks = len(spectrum)*self.frac_of_peaks
            if(max_peaks < 1):
                max_peaks = 1
            spectra_list[i] = copy_spectrum_with_new_mz_and_intensities(spectrum,
                                                                        spectrum.mz_values[intensity_sort][ :max_peaks],
                                                                        spectrum.intensity_values[intensity_sort][ :max_peaks])

        return spectra_list

class ThresholdedPeakFiltering(PreprocessorMixin):
    """
    A pre-processor for removing the peaks that are less intense than a given threshold.
    """
    def __init__(self, threshold=1.0, remove_mz_values=True):
        """
        Constructor.

        Parameters
        ----------
        threshold: float, default=1.0
                   The intensity threshold. All peaks that have an intensity value less or equal to this threshold will
                   be discarded.

        remove_mz_values : bool, default=True
                   Specifies if the m/z values where the intensity was below the threshold should be removed.
        """
        self.threshold = threshold
        self.remove_mz_values = remove_mz_values

    def transform(self, spectra_list):
        """
        Filter peaks for a list of spectra.

        Parameters
        ----------
        spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of spectra to transform.

        Returns
        -------
        transformed_spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of transformed spectra.
        """

        spectra_list = np.array(spectra_list)
        for i, spectrum in enumerate(spectra_list):
            if not self.remove_mz_values:
                intensity_values = copy.deepcopy(spectra_list[i].intensity_values)
                intensity_values[intensity_values <= self.threshold] = 0.0
                spectra_list[i] = copy_spectrum_with_new_intensities(spectrum, intensity_values)
            else:
                keep_mask = spectra_list[i].intensity_values > self.threshold
                spectra_list[i] = copy_spectrum_with_new_mz_and_intensities(spectrum,
                                                                            spectra_list[i].mz_values[keep_mask],
                                                                            spectra_list[i].intensity_values[keep_mask])
        return spectra_list

class AverageTotalIonCurrentNormalization(PreprocessorMixin):
    """
    A pre-processor for total ion current (TIC) normalization,
    that normalizes to the average TIC in the array of spectra.
    """
    def transform(self, spectra_list):
        """
        Correct baseline for a list of spectra.

        Parameters
        ----------
        spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of spectra to transform.

        Returns
        -------
        transformed_spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of transformed spectra.
        """

        TIC = np.zeros(shape=(spectra_list.shape[0]))
        for i in xrange(len(spectra_list)):
            TIC[i] = np.sum(spectra_list[i].intensity_values)
        avg_TIC = np.mean(TIC)

        spectra_list = np.array(spectra_list)
        for i, spectrum in enumerate(spectra_list):
            new_intensity_values = spectrum.intensity_values / avg_TIC
            spectra_list[i] = copy_spectrum_with_new_intensities(spectrum, new_intensity_values)

        return spectra_list

class SelectKBestFeatures(PreprocessorMixin):
    """
    A pre-processor to select the k best features, with the scoring function being
    the highest maximum peak intensity
    """
    def __init__(self, n_features=1000, use_x_max=10):
        """
        Constructor.

        Parameters
        ----------
        n_features: int, default=1000
                    The number of best scored features/peaks to keep.
        use_x_max: int, default=10
                   Number of maximum peaks to average to get the score
        """
        self.n_features = n_features
        self.use_x_max = use_x_max

    def transform(self, spectra_list):
        """
        Selects k best features in an array of spectra

        Parameters
        ----------
        spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of spectra to transform.
            Recommend to pass aligned spectra

        n_features: int, number of features to return/keep

        Returns
        -------
        transformed_spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of transformed spectra.
        """
        #copy the passed spectra, then unify_mz
        spec = []
        for s in spectra_list:
            spec.append(s.copy())

        spec = np.array(spec)
        unify_mz(spec)

        #get the mz_values
        mz_values = np.array(spec[0].mz_values)
        #store the score of each peak, with its mz
        score = []
        for mz in xrange(mz_values.shape[0]):
            temp = []
            for s in xrange(spec.shape[0]):
                temp.append(spec[s].intensity_values[mz])
            if(self.use_x_max == 1):
                score.append(mz_values[mz], max(temp))
            else:
                temp = np.sort(temp)
                temp = temp[:self.use_x_max]
                score.append((mz_values[mz], np.mean(temp)))

        #sort the score array by score, keep the [n_features] best
        sorted_score = sorted(score, key=lambda tup: tup[1])
        sorted_score = sorted_score[:self.n_features]
        keep_mz = []
        for mz in sorted_score:
            keep_mz.append(mz[0])

        #make the new spectra list and return it
        new_spec = []
        for i in xrange(len(spec)):
            tempInt = []
            for mz in keep_mz:
                tempInt.append(spec[i].intensity_at(mz))
            new_spec.append(Spectrum(keep_mz, tempInt, mz_precision=spec[i].mz_precision))

        new_spec = np.array(new_spec)

        return new_spec

class MassRangeSelection(PreprocessorMixin):
    """
    A pre-processor for removing the peaks that are outside a given window on the m/z range
    """
    def __init__(self, lower_range=50.0, upper_range =2000.0):
        """
        Constructor.

        Parameters
        ----------
        lower_range: float, default=50.0
                   The intensity threshold. All peaks that have an intensity value less or equal to this threshold will
                   be discarded.

        upper_range : float, default=2000.0
                   Specifies if the m/z values where the intensity was below the threshold should be removed.
        """
        self.lower_range = lower_range
        self.upper_range = upper_range

    def transform(self, spectra_list):
        """
        Filter peaks for a list of spectra.

        Parameters
        ----------
        spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of spectra to transform.

        Returns
        -------
        transformed_spectra_list: array-like, type=Spectrum, shape=[n_spectra]
            The list of transformed spectra.
        """


        spectra_list = np.array(spectra_list)
        for i, spectrum in enumerate(spectra_list):
            mz_values = spectra_list[i].mz_values
            intensity_values = spectra_list[i].intensity_values

            #mz_values is sorted and intensity values in the same order.
            #find the indices of the peaks are within the range and slice the arrays.
            lower_idx = binary_search_for_left_range(mz_values, self.lower_range)
            upper_idx = binary_search_for_right_range(mz_values, self.upper_range) + 1

            spectra_list[i] = copy_spectrum_with_new_mz_and_intensities(spectrum, mz_values[lower_idx:upper_idx],
                                                                        intensity_values[lower_idx:upper_idx])

        return spectra_list