__author__='pier-luc'

from scipy.cluster.hierarchy import dendrogram
from .metabodashboard.service.pymspec.preprocessing import common, discrete
#import matplotlib.pyplot as plt
import numpy as np
from bisect import bisect_left


def binary_search_for_left_range(spectrum, left_range):
    """
    Return the index in the sorted array where the value is larger or equal than left_range
    :param spectrum:
    :param left_range:
    :return:
    """
    l = len(spectrum)
    if spectrum[l-1] < left_range :
        raise ValueError("No value bigger than %s" % left_range)
    low = 0
    high = l -1
    while low <= high:
        mid = low + ((high-low)//2)
        if spectrum[mid] >= left_range:
            high = mid - 1
        else:
            low = mid + 1
    return high+1


def binary_search_for_right_range(spectrum, right_range):
    """
    Return the index in the sorted array where the value is smaller or equal than right_range
    :param spectrum:
    :param right_range:
    :return:
    """
    l = len(spectrum)
    if spectrum[0] > right_range :
        raise ValueError("No value smaller than %s" % right_range)
    low = 0
    high = l - 1
    while low <= high:
        mid = low + ((high-low)//2)
        if spectrum[mid] > right_range:
            high = mid - 1
        else:
            low = mid + 1
    return low-1


def binary_search_find_values(spectrum, mz, window):
    """
    Find the values in an centered interval
    :param spectrum: A list of values
    :param mz: The centered points of the search
    :param window: The intervale
    :return: A list of values in the range mz +/- intervale
    """
    right = binary_search_for_right_range(spectrum, mz+(mz*window/1000000.0))
    left = binary_search_for_left_range(spectrum, mz-(mz*window/1000000.0))
    return spectrum[left:right+1]


def take_closest(my_list, my_number):
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



def plot_augmented_dendrogram(*args, **kwargs):
    ### http://stackoverflow.com/questions/11917779/how-to-plot-and-annotate-hierarchical-clustering-dendrograms-in-scipy-matplotlib
    ddata = dendrogram(*args, **kwargs)
    if not kwargs.get('no_plot', False):
        for i, d in zip(ddata['icoord'], ddata['dcoord']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            plt.plot(x, y, 'ro')
            plt.annotate("%.3g" % y, (x, y), xytext=(0, -8),
                         textcoords='offset points',
                         va='top', ha='center')
    return ddata


def plot_points_distribution(spectrum, window):
    preprocessing_pipeline = common.Pipeline([discrete.MassRangeSelection(lower_range=window[0], upper_range=window[1]),
                                              discrete.MostIntensePeakFiltering(frac_of_peaks=0.1)])
    subspectrum = preprocessing_pipeline.fit_transform(spectrum)
    x = []
    y = []
    colors = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
    for i, spect in enumerate(subspectrum):
        x = []
        y = []
        for mz in spect.peaks():
            x.append(mz)
            y.append(np.log10(spect.peaks()[mz]))
        plt.plot(x, y, colors[i])
    #plt.axis([95, 101, 8, 14])
    plt.grid(True)
    plt.xlabel("M/z")
    plt.ylabel("log(intensity)")
    plt.title("Points distribution for 8 samples (2 calibrations)")
    plt.show()


def measure_average_distance_between_two_spect(spect, reference, window, print_d = False):
    distance = 0
    num_of_peaks = 0
    d = []
    for mz in spect.mz_values:
        try:
            ref_values = binary_search_find_values(reference.mz_values, mz, window)
        except:
            continue
        if len(ref_values) == 1:
            ref_value = ref_values[0]
        elif len(ref_values) > 1:
            ref_value = take_closest(ref_values, mz)
        else:
            continue
        d.append(((abs(ref_value-mz))/ref_value)*1000000)
        distance += ((abs(ref_value-mz))/ref_value)*1000000 # in ppm because otherwise its uncomparable
        num_of_peaks += 1
    if print_d:
        print(d)
    return distance/num_of_peaks
