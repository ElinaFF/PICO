__author__='pier-luc'
__version__=3

import logging
import ast
from bisect import bisect_left
from collections import defaultdict

import numpy as np
from metabodashboard.service.pymspec.spectrum import *


"""
Objective is to test multiple algorithme to
find the best one to aligne multiple mass spectrum
"""


class Mass_spect_aligner():
    def __init__(self, correction_search_window=10, alignment_window=5, low_count_approximation=7/8, mz_precision=4,
                 ppm_search_window=10, find_peaks_ppm_window=5):
        self.correction_search_window = correction_search_window
        self.ppm_search_window = ppm_search_window # Not used
        self.alignment_window = alignment_window    # Not used
        self.minimal_spectrum = None
        self.find_peaks_ppm_window = find_peaks_ppm_window
        self.low_count_approximation = low_count_approximation
        self.mz_precision = mz_precision

    def train(self, spectrum_list):
        temp_spect = defaultdict(int)
        for spectrum in spectrum_list:
            for mz in spectrum.mz_values:
                temp_spect[mz] += 1

        mz = np.array(temp_spect.keys())
        sorter = np.argsort(mz)
        mz = mz[sorter]
        counts = np.array(temp_spect.values())[sorter]
        minimal_spectrum = self._find_peaks(mz, counts)
        minimal_spectrum = np.array(minimal_spectrum, dtype=np.float)
        sorter = np.argsort(minimal_spectrum)
        self.minimal_spectrum = minimal_spectrum[sorter]

    def apply(self, spectrum_list, allow_unseen_peaks=True, unify=True):
        """ TODO: add a unssen_peak_error?
        Perform alignment on place.
        :param spectrum_list: This list of spectrum must have passed the same transformation procedure than the
         data used for the aligned_spectra
         alignment.
        :return: The spectrum_list after alignement.
        """
        counter = 0
        for (num, spectrum) in enumerate(spectrum_list):
            new_mz = []
            corresponding_intensity = []
            for mz in spectrum.mz_values:
                up_limit = round(mz + (mz * self.correction_search_window / 10**6), ndigits=4)
                bot_limit = round(mz - (mz * self.correction_search_window / 10**6), ndigits=4)
                try:
                    right = binary_search_for_right_range(self.minimal_spectrum, up_limit)
                    left = binary_search_for_left_range(self.minimal_spectrum, bot_limit)
                    possible_matches = binary_search_find_values(self.minimal_spectrum, left, right)
                except ValueError as e:
                    if allow_unseen_peaks:
                        continue
                    else:
                        print("Warning: %s" %e)
                        continue
                if len(possible_matches) == 1:
                    new_mz.append(possible_matches[0])
                    corresponding_intensity.append(spectrum.peaks()[mz])
                elif len(possible_matches) > 1:
                    possible_matches.sort()
                    best_match = take_closest(possible_matches, mz)
                    new_mz.append(best_match)
                    corresponding_intensity.append(spectrum.peaks()[mz])
                else:
                    if allow_unseen_peaks:
                        print("There is no value for corresponding mz: %s" % mz)
                        new_mz.append(mz)
                        corresponding_intensity.append(spectrum.peaks()[mz])
                    else:
                        pass
                        # raise ValueError("There is no value for corresponding mz: %s" % mz)
            spectrum.set_peaks(np.array(new_mz, dtype=float), np.array(corresponding_intensity, dtype=float))
            counter += 1
            logging.debug("%.2f %% aligned" % (float(counter) / len(spectrum_list) * 100.0))
        return spectrum_list

    def apply2(self, spectrum_list, allow_unseen_peaks=True, unify=True):
        """ TODO: add a unssen_peak_error?
        Perform alignment on place.
        :param spectrum_list: This list of spectrum must have passed the same transformation procedure than the
         data used for the aligned_spectra
         alignment.
        :return: The spectrum_list after alignement.
        """
        for (num, spectrum) in enumerate(spectrum_list):
            counter = 0
            new_mz = []
            corresponding_intensity = []
            before_alignement = len(spectrum.mz_values)
            for mz in self.minimal_spectrum:
                up_limit = round(mz + (mz * self.correction_search_window / 10**6), ndigits=4)
                bot_limit = round(mz - (mz * self.correction_search_window / 10**6), ndigits=4)
                try:
                    right = binary_search_for_right_range(spectrum.mz_values, up_limit)
                    left = binary_search_for_left_range(spectrum.mz_values, bot_limit)
                    possible_matches = binary_search_find_values(spectrum.mz_values, left, right)
                except ValueError as e:
                    if unify:
                        print("Warning: %s" %e)
                        counter += 1
                        new_mz.append(mz)
                        corresponding_intensity.append(0)
                        continue
                    else: # not sure if we should allow it anymore.
                        print("Warning failing: %s" %e)
                        continue
                if len(possible_matches) == 1:
                    new_mz.append(mz)
                    corresponding_intensity.append(spectrum.peaks()[possible_matches[0]])
                elif len(possible_matches) > 1:
                    possible_matches = np.sort(possible_matches)
                    best_match = take_closest(possible_matches, mz)
                    new_mz.append(mz)
                    corresponding_intensity.append(spectrum.peaks()[best_match])
                else:
                    if unify:
                        counter+=1
                        new_mz.append(mz)
                        corresponding_intensity.append(0)
                    else:
                        pass
                        # raise ValueError("There is no value for corresponding mz: %s" % mz)
            spectrum.set_peaks(np.array(new_mz, dtype=float), np.array(corresponding_intensity, dtype=float))
            print("Did not found %s out of %s peaks and %s peaks" %(counter, len(self.minimal_spectrum), before_alignement))
        return spectrum_list

    def load(self, filename):
        fi = open(filename, "r")
        self.correction_search_window = int(fi.readline())
        self.ppm_search_window = int(fi.readline())
        self.alignment_window = int(fi.readline())
        self.find_peaks_ppm_window = int(fi.readline())
        self.low_count_approximation = int(fi.readline())
        self.mz_precision = int(fi.readline())
        i = fi.readline()
        while 1:
            if i == "":
                break
            self.minimal_spectrum.append(i)
            i = fi.readline()
        fi.close()

    def save(self, filename):
        fo = open(filename, 'w')
        fo.write(str(self.correction_search_window)+"\n")
        fo.write(str(self.ppm_search_window)+"\n")
        fo.write(str(self.alignment_window)+"\n")
        fo.write(str(self.find_peaks_ppm_window)+"\n")
        fo.write(str(self.low_count_approximation)+"\n")
        fo.write(str(self.mz_precision)+"\n")
        for i in self.minimal_spectrum:
            fo.write(str(i)+"\n")
        fo.close()

    def _find_peaks(self, mz_list, unit_intensity):
        """
        Will remove noise and define the peaks that will be kept for alignement.
        Need improvement: counts-weigth average, the 7/8 position when diversity is too high,
        double peaks identification,
        :param mz_list:
        :param unit_intensity:
        :return: A list of current_mz.
        """

        minimal_spectrum_mz = []
        mz_list, unit_intensity = (list(t) for t in zip(*sorted(zip(mz_list, unit_intensity))))
        mz_buffer = []

        current_index = 0
        while current_index < len(mz_list):
            first_mz = mz_list[current_index]
            max_possible_mz_to_search = round((float(10**6) / (10**6 - self.find_peaks_ppm_window)) * first_mz,
                                              ndigits=self.mz_precision)

            right = binary_search_for_right_range(mz_list, max_possible_mz_to_search)
            left = binary_search_for_left_range(mz_list, first_mz)
            mz_buffer = binary_search_find_values(mz_list, left, right)
            intensity_buffer = binary_search_find_values(unit_intensity, left, right)

            i = 0
            average_mz = 0
            number_of_spectrum = 0
            for j in mz_buffer:
                multiplicator = intensity_buffer[i]
                number_of_spectrum += multiplicator
                average_mz += (j * multiplicator)
            average_mz = round(average_mz/number_of_spectrum, ndigits=self.mz_precision)

            minimal_spectrum_mz.append(average_mz)

            current_index = right+1
            mz_buffer = []
        # Remove the last mz and add it to the minimal spectrum.
        if len(mz_buffer) > 1:
            raise ValueError("There is a problem in the find peaks algo")
        if len(mz_buffer) == 1:
            minimal_spectrum_mz.append(mz_buffer[0])
        return minimal_spectrum_mz

    def _find_peaks_with_CHC(self, mz_list):
        from scipy.spatial.distance import pdist
        from scipy.cluster.hierarchy import complete, fcluster, linkage
        minimal_spectrum_mz = []
        r = np.array([(p.mz, p.intensity) for p in mz_list])
        m = pdist(r, 'eucledian')
        distance_matrix = self._generate_distance_matrix(mz_list, w)
        clusters_limit = window[1] * self.clusters_ppm_allowed / 10**6    # previously used self.overlaping_window
        clusters = fcluster(linkage(distance_matrix, method="complete"), clusters_limit, 'distance')

    def make_matrix_for_all_spectrum(self, spectrum):
        matrix = {}
        for mz in self.minimal_spectrum:
            matrix[mz] = []
        current_spectrum = 0
        for spect in spectrum:
            for mz in spect.mz_values:
                current = matrix[mz]
                while len(current) < current_spectrum:
                    current.append(0)
                current.append(1)
                matrix[mz] = current
            for mz in matrix:
                while len(matrix[mz]) <= current_spectrum:
                    matrix[mz].append(0)
            current_spectrum += 1
            logging.debug("Done matrix for %s spectrum" % current_spectrum)
        return matrix

    @staticmethod
    def output_matrix(matrix, spectrum_list, file_name):
        fout = open(file_name, 'w')
        line = "MZ"
        for spectrum in spectrum_list:
            line = line + "\t" + str(spectrum.metadata)
        fout.write(line+"\n")

        for mz in matrix:
            line = str(mz)
            for values in matrix[mz]:
                line = line + "\t" + str(values)
            fout.write(line + "\n")
        fout.close()

    @staticmethod
    def _take_closest(my_list, my_number):
        # http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
        """
        Assumes myList is sorted. Returns closest value to myNumber.

        If two numbers are equally close, return the smallest number.
        """
        pos = bisect_left(my_list, my_number)
        if pos == 0:
            return my_list[0]
        if pos == len(my_list):
            return my_list[-1]
        before = my_list[pos - 1]
        after = my_list[pos]
        if after - my_number < my_number - before:
            return after
        else:
            return before

