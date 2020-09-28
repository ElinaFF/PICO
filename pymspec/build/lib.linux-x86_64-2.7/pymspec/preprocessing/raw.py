__author__ = 'Alexandre Drouin'

from math import ceil

import numpy as np
from scipy import ndimage

from ..spectrum import Spectrum, copy_spectrum_with_new_intensities
from ..base import PreprocessorMixin
from ..utils import _is_mz_step_constant


#TODO peak selection, denoizing
class TotalIonCurrentNormalization(PreprocessorMixin):
    """
    A pre-processor for total ion current (TIC) normalization.
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
        spectra_list = np.array(spectra_list)

        for i, spectrum in enumerate(spectra_list):
            total_ion_current = np.sum(spectrum.intensity_values)
            new_intensity_values = spectrum.intensity_values / total_ion_current
            spectra_list[i] = copy_spectrum_with_new_intensities(spectrum, new_intensity_values)
        return spectra_list


class QualityControl(PreprocessorMixin):
    """
    A pre-processor for quality control assesment.
    """
    def __init__(self, remove_spectrum=True, restriction_ratio=2.33):
        self.remove_spectrum = remove_spectrum
        self.restriction_ratio = restriction_ratio
        self.average_intensity = 0
        self.std = 0

    def fit(self, spectra_list):
        spectra_list = np.array(spectra_list)
        intensities_sum = [np.sum(i.intensity_values) for i in spectra_list]
        self.average_intensity = np.average(intensities_sum)
        self.std = np.std(intensities_sum)

    def transform(self, spectra_list):
        min = max(0, self.average_intensity - self.restriction_ratio * self.std)  # In some rare case the value was under 0
        max = self.average_intensity + self.restriction_ratio * self.std
        qc_passed = []
        for spectrum in spectra_list:
            intensity_sum = np.sum(spectrum.intensity_values)
            if min > self.intensities_sum or self.intensities_sum > max:  # Does not pass QC
                if not self.remove_spectrum:
                    spectrum.metadata["QC"] = False
                    qc_passed.append(spectrum)
            else:
                spectrum.metadata["QC"] = True
                qc_passed.append(spectrum)
        return qc_passed


# class TotalIonCurrentNormalization(PreprocessorMixin):
#     #TODO: This could be super optimized with cython
#     """
#     A pre-processor for total ion current (TIC) normalization.
#     """
#     def __init__(self, local=True, use_median=True, window_size=0.1):
#         """
#         Constructor.
#
#         Parameters
#         ----------
#         local: bool, default=True
#             Specifies if the normalization must be done locally or on the whole spectrum.
#         use_median: bool, default=True
#             Specifies if the median must be used instead of the mean. The median is known to be more robust to noise.
#         window_size: float, default=0.1
#             The size of the sliding window used for normalizing. If local=False, the window_size is set to 2.0.
#         """
#         if not local:
#             window_size = 2.0
#
#         self.window_size = window_size
#         self.use_median = use_median
#
#     def fit(self, spectra_list):
#         """
#         Fit the pre-processing algorithm based on a training sample of spectra.
#         This sets the mean/median TIC values for each m/z point.
#
#         Parameters
#         ----------
#         spectra_list: array-like, type=Spectrum, shape=[n_spectra]
#             The list of training spectra.
#
#         Pre-conditions
#         --------------
#         * For each spectrum, the step between the m/z values must be constant.
#         * Each spectrum must have the same m/z values.
#         """
#         if not _is_mz_step_constant(spectra_list[0]):
#             raise ValueError("The step between m/z values must be constant.")
#         if not _is_mz_equal(spectra_list[0].mz_values, spectra_list):
#             raise ValueError("The spectra must have the same m/z values.")
#
#         self.mz_values = spectra_list[0].mz_values
#         window_size = int(len(self.mz_values) * self.window_size)
#         spectra_intensities = np.array([s.intensity_values for s in spectra_list])
#         self.tic = np.zeros(len(self.mz_values))
#
#         if self.use_median:
#             aggregate_tic_values = np.median
#         else:
#             aggregate_tic_values = np.mean
#
#         half_window_size = ceil(float(window_size) / 2)
#
#         current_sum = np.sum(spectra_intensities[:, 0 : half_window_size + 1], axis=1)
#         sum_min = 0.0 - half_window_size
#         sum_max = half_window_size
#
#         for i in xrange(len(self.mz_values)):
#             if i > 0:
#                 if i > half_window_size:
#                     current_sum -= spectra_intensities[:, sum_min]
#                     sum_min += 1
#
#                 if sum_max < len(self.mz_values) - 1:
#                     sum_max += 1
#                     current_sum += spectra_intensities[:, sum_max]
#
#             self.tic[i] = aggregate_tic_values(current_sum)
#
#     def transform(self, spectra_list):
#         """
#         Transform a list of spectra based on the fitted TIC values.
#
#         Parameters
#         ----------
#         spectra_list: array-like, type=Spectrum, shape=[n_spectra]
#             The list of spectra to transform.
#
#         Returns
#         -------
#         transformed_spectra_list: array-like, type=Spectrum, shape=[n_spectra]
#             The list of transformed spectra.
#         """
#         spectra_list = np.array(spectra_list)
#
#         if not _is_mz_equal(self.mz_values, spectra_list):
#             raise ValueError("The spectra must have the same m/z values than the ones used to fit the preprocessor.")
#
#         for i, spectrum in enumerate(spectra_list):
#             spectra_list[i] = spectrum.copy() / self.tic
#
#         return spectra_list


class TopHatBaselineCorrection(PreprocessorMixin):
    """
    A pre-processor for spectrum baseline correction based on the Top-Hat filter.

    Dougherty, E. R., & Lotufo, R. A. (2003, September). Hands-on morphological image processing. Bellingham: Spie.

    """
    def __init__(self, structural_element_size=0.01):
        """
        Constructor.

        Parameters
        ----------
        structural_element_size: float, default=0.01
            The width of the structural element given as a fraction of the total number of m/z points.
        """
        self.structural_element_size = structural_element_size

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
        spectra_list = np.array(spectra_list)
        for i, spectrum in enumerate(spectra_list):
            if not _is_mz_step_constant(spectrum):
                raise ValueError("The step between m/z values must be constant.")

            structural_element = np.ones(int(round(len(spectrum) * self.structural_element_size)), dtype=np.int)
            new_intensity_values = ndimage.white_tophat(spectrum.intensity_values, None, structural_element)

            spectra_list[i] = spectrum.copy()
            spectra_list[i].set_peaks(mz_values=spectrum.mz_values, intensity_values=new_intensity_values)

        return spectra_list