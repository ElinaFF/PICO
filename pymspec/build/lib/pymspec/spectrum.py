__author__ = 'Alexandre Drouin'

import numpy as np
from copy import deepcopy
try:
    from itertools import izip as zip  #izip is not for python 3.X
except ImportError:
    pass
from .utils import _is_mz_precision_equal, binary_search_find_values, binary_search_for_left_range, \
    binary_search_for_right_range, take_closest

# TODO: Crop, arithmetic unsupported type raise exception, division and multiplication by another spectrum is sketchy
class Spectrum(object):
    def __init__(self, mz_values, intensity_values, mz_precision=3, metadata=None):
        self._peaks_mz = np.array([])
        self._peaks_intensity = np.array([])
        self._peaks = {}
        self.metadata = metadata
        self._mz_precision = mz_precision  # in decimals e.g.: mz_precision=3 => 5.342

        if len(mz_values) != len(intensity_values):
            raise ValueError("The number of mz values must be equal to the number of intensity values.")

        self.set_peaks(mz_values, intensity_values)

    def peaks(self):
        """
        Note: Peaks are not necessarily sorted here because of dict
        """
        return self._peaks

    @property
    def mz_values(self):
        """
        Note: Returned values are always sorted
        """
        return self._peaks_mz

    @property
    def mz_precision(self):
        return self._mz_precision

    @mz_precision.setter
    def mz_precision(self, new_precision):
        self._mz_precision = new_precision
        self.set_peaks(self.mz_values, self.intensity_values)

    @property
    def intensity_values(self):
        return self._peaks_intensity

    def intensity_at(self, mz):
        mz = round(mz, self._mz_precision)
        try:
            intensity = self._peaks[mz]
        except:
            intensity = 0.0
        return intensity

    def set_peaks(self, mz_values, intensity_values):
        # XXX: This function must create a copy of mz_values and intensity_values to prevent the modification of
        # referenced arrays. This is assumed by other functions. Be careful!

        # Sort the peaks by mz
        sort_mz = np.argsort(mz_values)
        mz_values = np.asarray(mz_values)[sort_mz]
        intensity_values = np.asarray(intensity_values)[sort_mz]

        # Round the mz values based on the mz precision
        mz_values = np.asarray(np.round(mz_values, self._mz_precision), dtype=np.float)

        # Contiguous mz values might now be equivalent. Combine their intensity values by taking the sum.
        unique_mz = np.unique(mz_values)
        unique_mz_intensities = np.zeros(unique_mz.shape)

        # Note: This assumes that mz_values and unique_mz are sorted
        if len(mz_values) != len(unique_mz):
            acc = 0
            current_unique_mz_idx = 0
            current_unique_mz = unique_mz[0]
            for i, mz in enumerate(mz_values):
                if mz != current_unique_mz:
                    unique_mz_intensities[current_unique_mz_idx] = acc  # Flush the accumulator
                    acc = 0  # Reset the accumulator
                    current_unique_mz_idx += 1  # Go to the next unique mz value
                    current_unique_mz = unique_mz[current_unique_mz_idx]  # Get the unique mz value
                acc += intensity_values[i]  # Increment the accumulator
            unique_mz_intensities[current_unique_mz_idx] = acc  # Flush the accumulator
        else:
            unique_mz_intensities = intensity_values

        self._peaks_mz = unique_mz
        self._peaks_mz.flags.writeable = False

        self._peaks_intensity.flags.writeable = False
        self._peaks_intensity = unique_mz_intensities

        self._peaks = dict([(round(self._peaks_mz[i], self._mz_precision), self._peaks_intensity[i]) for i in
                            range(len(self._peaks_mz))])

        self._check_peaks_integrity()


    def copy(self):
        return copy_spectrum(self)

    def __iter__(self):
        """
        Returns an iterator on the peaks of the spectrum.

        Returns:
        --------
        peak_iterator: iterator
            An iterator that yields tuples of (mz, int) for each peaks in the spectrum.
        """
        return zip(self._peaks_mz, self._peaks_intensity)

    def __eq__(self, other):
        # TODO: allclose and precision :S
        return self.metadata == other.metadata \
               and np.allclose(self._peaks_mz, other.mz_values) \
               and np.allclose(self._peaks_intensity, other.intensity_values) \
               and self._mz_precision == other.mz_precision

    def __add__(self, other):
        if isinstance(other, Spectrum):
            # Spectrum/Spectrum
            if other._mz_precision != self._mz_precision:
                raise ValueError("Spectrum/Spectrum arithmetic requires the use of identical mz_precisions.")

            mz_values = np.unique(np.hstack((self.mz_values, other.mz_values)))
            intensity_values = np.zeros(mz_values.shape[0])

            for i, mz in enumerate(mz_values):
                intensity_values[i] = self.intensity_at(mz) + other.intensity_at(mz)

            return Spectrum(mz_values=mz_values, intensity_values=intensity_values, mz_precision=self._mz_precision,
                            metadata=[self.metadata, other.metadata])

        elif isinstance(other, (int, long, float, complex)):
            # Spectrum/constant
            return Spectrum(mz_values=self.mz_values, intensity_values=self.intensity_values + float(other),
                            mz_precision=self._mz_precision, metadata=self.metadata)

        elif isinstance(other, (np.ndarray, list)):
            if len(other) != self.mz_values.shape[0]:
                raise ValueError(
                    "Spectrum/Vector arithmetic requires that the number of peaks and vector elements match.")

            return Spectrum(mz_values=self.mz_values, intensity_values=self.intensity_values + np.asarray(other),
                            mz_precision=self._mz_precision, metadata=self.metadata)

    def __sub__(self, other):
        if isinstance(other, Spectrum):
            # Spectrum/Spectrum
            if other._mz_precision != self._mz_precision:
                raise ValueError("Spectrum/Spectrum arithmetic requires the use of identical mz_precisions.")

            mz_values = np.unique(np.hstack((self.mz_values, other.mz_values)))
            intensity_values = np.zeros(mz_values.shape[0])

            for i, mz in enumerate(mz_values):
                intensity_values[i] = self.intensity_at(mz) - other.intensity_at(mz)

            return Spectrum(mz_values=mz_values, intensity_values=intensity_values, mz_precision=self._mz_precision,
                            metadata=[self.metadata, other.metadata])

        elif isinstance(other, (int, long, float, complex)):
            # Spectrum/Constant
            return Spectrum(mz_values=self.mz_values, intensity_values=self.intensity_values - float(other),
                            mz_precision=self._mz_precision, metadata=self.metadata)

        elif isinstance(other, (np.ndarray, list)):
            # Spectrum/Vector
            if len(other) != self.mz_values.shape[0]:
                raise ValueError(
                    "Spectrum/Vector arithmetic requires that the number of peaks and vector elements match.")

            return Spectrum(mz_values=self.mz_values, intensity_values=self.intensity_values - np.asarray(other),
                            mz_precision=self._mz_precision, metadata=self.metadata)

    def __mul__(self, other):
        if isinstance(other, Spectrum):
            # Spectrum/Spectrum
            if other._mz_precision != self._mz_precision:
                raise ValueError("Spectrum/Spectrum arithmetic requires the use of identical mz_precisions.")

            mz_values = np.unique(np.hstack((self.mz_values, other.mz_values)))
            intensity_values = np.zeros(mz_values.shape[0])

            for i, mz in enumerate(mz_values):
                intensity_values[i] = self.intensity_at(mz) * other.intensity_at(mz)

            return Spectrum(mz_values=mz_values, intensity_values=intensity_values, mz_precision=self._mz_precision,
                            metadata=[self.metadata, other.metadata])

        elif isinstance(other, (int, long, float, complex)):
            # Spectrum/Constant
            return Spectrum(mz_values=self.mz_values, intensity_values=self.intensity_values * float(other),
                            mz_precision=self._mz_precision, metadata=self.metadata)

        elif isinstance(other, (np.ndarray, list)):
            # Spectrum/Vector
            if len(other) != self.mz_values.shape[0]:
                raise ValueError(
                    "Spectrum/Vector arithmetic requires that the number of peaks and vector elements match.")

            return Spectrum(mz_values=self.mz_values, intensity_values=self.intensity_values * np.asarray(other),
                            mz_precision=self._mz_precision, metadata=self.metadata)

    def __div__(self, other):
        if isinstance(other, Spectrum):
            # Spectrum/Spectrum
            if other._mz_precision != self._mz_precision:
                raise ValueError("Spectrum/Spectrum arithmetic requires the use of identical mz_precisions.")

            mz_values = np.unique(np.hstack((self.mz_values, other.mz_values)))
            intensity_values = np.zeros(mz_values.shape[0])

            for i, mz in enumerate(mz_values):
                intensity_values[i] = self.intensity_at(mz) / other.intensity_at(mz)

            return Spectrum(mz_values=mz_values, intensity_values=intensity_values, mz_precision=self._mz_precision,
                            metadata=[self.metadata, other.metadata])

        elif isinstance(other, (int, long, float, complex)):
            # Spectrum/Constant
            return Spectrum(mz_values=self.mz_values, intensity_values=self.intensity_values / float(other),
                            mz_precision=self._mz_precision, metadata=self.metadata)

        elif isinstance(other, (np.ndarray, list)):
            # Spectrum/Vector
            if len(other) != self.mz_values.shape[0]:
                raise ValueError(
                    "Spectrum/Vector arithmetic requires that the number of peaks and vector elements match.")

            return Spectrum(mz_values=self.mz_values, intensity_values=self.intensity_values / np.asarray(other),
                            mz_precision=self._mz_precision, metadata=self.metadata)

    def __len__(self):
        return self._peaks_mz.shape[0]

    def __str__(self):
        me = "Metadata: " + str(self.metadata) + "\n"
        me += "Peaks: " + ', '.join(map(str, sorted(list(self.peaks().items()))))
        return me

    def _check_peaks_integrity(self):
        if not len(self._peaks_mz) == len(self._peaks_intensity):
            raise ValueError("The number of mz values must be equal to the number of intensity values.")
        if not all(self._peaks_mz[i] <= self._peaks_mz[i + 1] for i in range(len(self._peaks_mz) - 1)):
            raise ValueError("Mz values must be sorted.")
        if len(np.unique(self._peaks_mz)) != len(self._peaks_mz):
            raise ValueError("Mz value list contains duplicate values.")

def copy_spectrum(spectrum):
    """
    Copies a spectrum.

    Parameters:
    -----------
    spectrum: Spectrum
        The spectrum to copy

    Note:
    -----
    * This ensures that the metadata is deepcopied
    """
    metadata = deepcopy(spectrum.metadata)
    # XXX: The mz_values and intensity_values are copied in the constructor. No need to copy here.
    return Spectrum(mz_values=spectrum.mz_values, intensity_values=spectrum.intensity_values,
                    mz_precision=int(spectrum.mz_precision), metadata=metadata)

def copy_spectrum_with_new_intensities(spectrum, new_intensity_values):
    """
    Copies a spectrum and replaces its intensity values.

    Parameters:
    -----------
    spectrum: Spectrum
        The spectrum to copy
    new_intensity_values: array_like, dtype=float, shape=n_peaks
        The new intensity values

    Note:
    -----
    * This is more efficient than deepcopying the spectrum and modifying its intensity values.
    * This ensures that the metadata is deepcopied
    """
    metadata = deepcopy(spectrum.metadata)
    # XXX: The mz_values and intensity_values are copied in the constructor. No need to copy here.
    return Spectrum(mz_values=spectrum.mz_values, intensity_values=new_intensity_values,
                    mz_precision=int(spectrum.mz_precision), metadata=metadata)

def copy_spectrum_with_new_mz_and_intensities(spectrum, new_mz_values, new_intensity_values):
    """
    Copies a spectrum and replaces its mz and intensity values.

    Parameters:
    -----------
    spectrum: Spectrum
        The spectrum to copy
    new_mz_values: array_like, dtype=float, shape=n_peaks
        The new mz values
    new_intensity_values: array_like, dtype=float, shape=n_peaks
        The new intensity values

    Note:
    -----
    * This is more efficient than deepcopying the spectrum and modifying its mz and intensity values.
    * This ensures that the metadata is deepcopied
    """
    metadata = deepcopy(spectrum.metadata)
    # XXX: The mz_values and intensity_values are copied in the constructor. No need to copy here.
    return Spectrum(mz_values=new_mz_values, intensity_values=new_intensity_values,
                    mz_precision=int(spectrum.mz_precision), metadata=metadata)

def mean_spectrum(spectra, return_std=True):
    """
    Compute the mean spectrum

    Parameters:
    -----------
    spectra : list of Spectrum
              A list of spectra.

    return_std : bool, default=True
              If True, the standard deviation at each m/z value is returned.

    Returns:
    --------
    mean_spectrum : Spectrum
                    The mean spectrum.

    intensity_std_by_mz : ndarray, dtype=np.float
                    The standard deviation at each m/z value.
    """
    mz_values = np.array(sorted(set(mz for spectra in spectra for mz in spectra.mz_values)))
    mean_intensity_values = np.zeros(mz_values.shape)

    if return_std:
        intensity_values_std = np.zeros(mz_values.shape)

    for i in xrange(len(mean_intensity_values)):
        spectra_intensities = np.array([s.intensity_at(mz_values[i]) for s in spectra])
        mean_intensity_values[i] = np.mean(spectra_intensities)

        if return_std:
            intensity_values_std[i] = np.std(spectra_intensities)

    mean = Spectrum(mz_values=mz_values, intensity_values=mean_intensity_values)

    if return_std:
        return mean, intensity_values_std
    else:
        return mean

def unify_mz(spectra):
    """
    Unifies the m/z values for a list of spectra

    Parameters:
    -----------
    spectra: list of Spectrum
        A list of spectra.

    Note:
    -----
    * The operation is performed in-place
    """
    if not _is_mz_precision_equal(spectra[0].mz_precision, spectra):
        raise ValueError("The m/z precision of the spectra must be equal in order to unify the m/z values.")

    mz_values = np.array(sorted(set(mz for spectra in spectra for mz in spectra.mz_values)))

    for spectrum in spectra:
        spectrum.set_peaks(mz_values=mz_values,
                           intensity_values=np.array([spectrum.intensity_at(mz) for mz in mz_values]))

def unify_precision(spectra, new_precision):
    """
    Unifies the m/z precision for a list of spectra

    Parameters:
    -----------
    spectra: list of Spectrum
        A list of spectra.

    new_precision: int
        The number of decimals for the new precision

    Note:
    -----
    * The operation is performed in-place
    * If multiple m/z values are equal after adjusting the precision, their intensity values are summed.
    """
    for spectrum in spectra:
        spectrum.mz_precision = new_precision

def remove_noise_spectra(spectra, noiseSpectra, ppm_tolerance=5, intensity_tolerance=100):
    """
    :param spectra: array of the spectra to correct
    :param noiseSpectra: array of the background spectra, used to correct
    :param ppm_tolerance: int, default = 5, the number of ppm on which to tolerate m/z offset
    :param intensity_tolerance: int, default = 100, the factor by which the intensity of the spectrum
                                must be compared to the background
    :return: array of the corrected spectra
    """
    #must have the same number of spectra and background spectra
    correctedSpectra = []
    for i, noise_spec in enumerate(noiseSpectra):
        noise_mz_values = np.array(noise_spec.mz_values)
        noise_intensity_values = np.array(noise_spec.intensity_values)
        mz_values = np.array(spectra[i].mz_values)

        #Added a sort before correction. Could be removed if already sorted. Data need to be sorted for binary search
        sorter = np.argsort(mz_values)
        sorted_mz_values = mz_values[sorter]

        intensity_values = np.array(spectra[i].intensity_values)
        mz_to_cut = []
        for j, mz in enumerate(noise_mz_values):
            noise_int = noise_intensity_values[j]
            up_limit = round(mz + (mz * ppm_tolerance / 1000000), ndigits=4)
            down_limit = round(mz - (mz * ppm_tolerance / 1000000), ndigits=4)

            if((sorted_mz_values[0] < up_limit) and (sorted_mz_values[len(sorted_mz_values) - 1] > down_limit)):
                right = binary_search_for_right_range(sorted_mz_values, up_limit)
                left = binary_search_for_left_range(sorted_mz_values, down_limit)
                possible_matches = binary_search_find_values(sorted_mz_values, left, right)
            else:
                possible_matches = []
            if(len(possible_matches) == 1):
                idx = np.where(mz_values==possible_matches[0])
                mz_idx = idx[0][0]
                if(noise_int * intensity_tolerance >= intensity_values[mz_idx]):
                    mz_to_cut.append(possible_matches[0])
            elif(len(possible_matches) > 1):
                best_match = take_closest(possible_matches, mz)
                idx = np.where(mz_values==best_match)
                mz_idx = idx[0][0]
                if(noise_int * intensity_tolerance >= intensity_values[mz_idx]):
                    mz_to_cut.append(best_match)
        mz_to_cut = set(mz_to_cut)
        mz = []
        intensity = []
        for j, mz_val in enumerate(mz_values):
            if(mz_val not in mz_to_cut):
                mz.append(mz_val)
                intensity.append(intensity_values[j])
        correctedSpectra.append(Spectrum(np.array(mz), np.array(intensity), mz_precision=spectra[i].mz_precision))
    return correctedSpectra
