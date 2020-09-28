__author__ = 'Alexandre Drouin'

import numpy as np
from bisect import bisect_left

def _is_mz_equal(reference_mz, spectra_list):
    mz_range = reference_mz

    for spectrum in spectra_list:
        if np.all(spectrum.mz_values != mz_range):
            return False

    return True

def _is_mz_precision_equal(reference_precision, spectra_list):
    for spectrum in spectra_list:
        if spectrum.mz_precision != reference_precision:
            return False

    return True


def _is_mz_step_constant(spectrum):
    previous_step = None

    mz_values = spectrum.mz_values
    for i in xrange(len(mz_values) - 1):
        step = round(mz_values[i + 1] - mz_values[i], spectrum.mz_precision)

        if step != previous_step and previous_step != None:
            print previous_step, step
            return False
        elif previous_step == -1.0:
            previous_step = step

    return True


def _is_metadata_type_dict(spectra):
    for spectrum in spectra:
        if not (isinstance(spectrum.metadata, dict) or spectrum.metadata is None):
            return False
    return True


def binary_search_for_left_range(mz_values, left_range):
    """
    Return the index in the sorted array where the value is larger or equal than left_range
    :param mz_values:
    :param left_range:
    :return:
    """
    l = len(mz_values)
    if mz_values[l-1] < left_range :
        raise ValueError("No value bigger than %s" % left_range)
    low = 0
    high = l -1
    while low <= high:
        mid = low +((high-low)/2)
        if mz_values[mid] >= left_range:
            high = mid - 1
        else:
            low = mid + 1
    return high+1


def binary_search_for_right_range(mz_values, right_range):
    """
    Return the index in the sorted array where the value is smaller or equal than right_range
    :param mz_values:
    :param right_range:
    :return:
    """
    l = len(mz_values)
    if mz_values[0] > right_range :
        raise ValueError("No value smaller than %s" % right_range)
    low = 0
    high = l - 1
    while low <= high:
        mid = low +((high-low)/2)
        if mz_values[mid] > right_range:
            high = mid - 1
        else:
            low = mid + 1
    return low-1

def binary_search_find_values(mz_values, left, right):
    return mz_values[left:right+1]

def take_closest(myList, myNumber):
    #http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before