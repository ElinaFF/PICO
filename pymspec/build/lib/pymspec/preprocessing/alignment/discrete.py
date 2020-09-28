from collections import defaultdict

import numpy as np

from ..common import PreprocessorMixin


def _binary_search_for_left_range(spectrum, left_range):
    """
    Return the index in the sorted array where the value is larger or equal than left_range
    :param spectrum:
    :param left_range:
    :return:
    """
    l = len(spectrum)
    if spectrum[l - 1] < left_range:
        raise ValueError("No value bigger than %s" % left_range)
    low = 0
    high = l - 1
    while low <= high:
        mid = low + ((high - low) / 2)
        if spectrum[mid] >= left_range:
            high = mid - 1
        else:
            low = mid + 1
    return high + 1


def _binary_search_for_right_range(spectrum, right_range):
    """
    Return the index in the sorted array where the value is smaller or equal than right_range
    :param spectrum:
    :param right_range:
    :return:
    """
    l = len(spectrum)
    if spectrum[0] > right_range:
        raise ValueError("No value smaller than %s" % right_range)
    low = 0
    high = l - 1
    while low <= high:
        mid = low + ((high - low) / 2)
        if spectrum[mid] > right_range:
            high = mid - 1
        else:
            low = mid + 1
    return low - 1


class MassAccuracyAlignment(PreprocessorMixin):
    def __init__(self, mz_precision=5, mz_tolerance=5):
        self.mz_precision = float(mz_precision)
        self.mz_tolerance = float(mz_tolerance)
        self.landmark_spectrum = None

    def fit(self, spectra_list):
        mz, n_occurences = self._mz_histogram(spectra_list)
        self.landmark_spectrum = self._find_landmarks(mz, n_occurences)

    def transform(self, spectra_list):
        if self.landmark_spectrum is None:
            raise RuntimeError("Preprocessor must be fitted before transforming.")
        return self._align_with_landmarks(spectra_list, self.mz_tolerance)

    def _mz_histogram(self, spectra):
        minimal_spectra = defaultdict(int)
        for i, spectrum in enumerate(spectra):
            for mz in spectrum.mz_values:
                minimal_spectra[mz] += 1
        mz = np.array(minimal_spectra.keys())
        sorter = np.argsort(mz)
        mz = mz[sorter]
        intensities = np.array(minimal_spectra.values())[sorter]
        return mz, intensities

    def _find_landmarks(self, mz_values, n_occurences):
        """
        Notes:
        ------
        * Assumes that the mz are sorted.
        """
        mz_landmarks = []
        mz_range_buffer = []
        intensity_range_buffer = []
        next_range_buffer = []
        next_intensity_buffer = []

        current_index = -1

        # There is a problem with current_index in this section. TODO: is it still true?
        while current_index + 1 < len(mz_values):
            if len(mz_range_buffer) == 0:
                current_index += 1
                mz_range_buffer.append(mz_values[current_index])
                intensity_range_buffer.append(n_occurences[current_index])
            mz = mz_range_buffer[0]

            max_mz_for_true_peak = 10 ** 6 / (10 ** 6 - self.mz_precision) * mz

            while mz < max_mz_for_true_peak and current_index + 1 < len(mz_values):
                current_index += 1
                mz = mz_values[current_index]
                intensity = n_occurences[current_index]
                #we check where to put the new values...
                if mz <= max_mz_for_true_peak:
                    mz_range_buffer.append(mz)
                    intensity_range_buffer.append(intensity)
                else:
                    next_range_buffer.append(mz)
                    next_intensity_buffer.append(intensity)

            # We use the m/z with the most occurences as an approximation of the middle point for this range.
            # If all m/z values have only 1 occurence, we use the maximum m/z value that is less than
            # max_mz_for_true_peak
            true_peak_idx = np.argmax(intensity_range_buffer)
            if intensity_range_buffer[true_peak_idx] == 1:
                true_peak_mz = mz_range_buffer[len(intensity_range_buffer) - 1]
            else:
                true_peak_mz = mz_range_buffer[true_peak_idx]

            # We append the true peak to the landmark spectrum
            mz_landmarks.append(true_peak_mz)

            max_mz_in_range = true_peak_mz + true_peak_mz * self.mz_precision / 1000000

            # If there is a value in next_range_buffer
            # * Check if it belongs in the current range
            # * Yes: Add it to the range and clear the buffer
            # * No: Leave it in the buffer, the next loop will be skipped and it will be handled right after.
            if len(next_range_buffer) > 0 and next_range_buffer[0] <= max_mz_in_range:
                mz_range_buffer.append(next_range_buffer[0])
                intensity_range_buffer.append(next_intensity_buffer[0])
                next_range_buffer = []
                next_intensity_buffer = []

            # Add the elements to the right of the true peak
            while mz <= max_mz_in_range and current_index + 1 < len(mz_values):
                current_index += 1
                mz = mz_values[current_index]
                intensity = n_occurences[current_index]
                #we check where to put the new values...
                if mz <= max_mz_in_range:
                    mz_range_buffer.append(mz)
                    intensity_range_buffer.append(intensity)
                else:
                    next_range_buffer.append(mz)
                    next_intensity_buffer.append(intensity)

            # Flush the values that were read ahead into the current mz buffer
            mz_range_buffer = next_range_buffer
            intensity_range_buffer = next_intensity_buffer
            next_range_buffer = []
            next_intensity_buffer = []

        #There might be a last value in there....
        if len(mz_range_buffer) == 1:
            mz_landmarks.append(mz_range_buffer[0])

        if len(mz_range_buffer) > 1:
            raise ValueError("There is a problem in the find peaks algo")

        return mz_landmarks

    def _align_with_landmarks(self, spectra, mz_tolerance):
        for spectrum in spectra:
            new_mz = []
            corresponding_intensity = []
            for i, mz in enumerate(spectrum.mz_values):
                up_limit = mz + mz * float(mz_tolerance) / 1000000
                bot_limit = mz - mz * float(mz_tolerance) / 1000000
                if((self.landmark_spectrum[0] < up_limit) and (self.landmark_spectrum[-1] > bot_limit)):
                    right = _binary_search_for_right_range(self.landmark_spectrum, up_limit)
                    left = _binary_search_for_left_range(self.landmark_spectrum, bot_limit)
                    possible_matches = self.landmark_spectrum[left:right + 1]
                else:
                    possible_matches = []

                # Match the observed peak to a landmark.
                # * If there are multiple possibilities, take the one that has the closest m/z value.
                # * If there is no match, leave the lonely peak where it is, since we only align based on our
                # landmarks. These peaks are not aligned, but they are preserved.
                if len(possible_matches) > 0:
                    new_mz.append(possible_matches[np.argmin(np.abs(possible_matches - mz))])
                else:
                    new_mz.append(mz)
                corresponding_intensity.append(spectrum.intensity_values[i])
            spectrum.set_peaks(new_mz, corresponding_intensity)
        return spectra

