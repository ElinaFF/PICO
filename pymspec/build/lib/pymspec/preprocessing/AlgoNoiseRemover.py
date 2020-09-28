from pymspec.preprocessing.common import *
from pymspec.preprocessing.discrete import *
import scipy.stats as st
from collections import OrderedDict
from pymspec.io.ion_list.file_loader import *




class NoiseRemover(object):
    """
    TODO

    """

    def __init__(self, start=50, end=1200, alpha=0.6, jump_length=50, window_size=150):
        """
        Initiate a VirtualLockMassCorrector object.
        :param start: starting value of the computing in the spectrum 
        :param end: ending value of the computing in the spectrum 
        :param alpha: percentage of the ignored values to define a cutoff  
        :param jump_length: length of the shifting of the window_size
        :param window_size: length of the range
        :return:
        """
        self.start = start
        self.end = end
        self.alpha = alpha
        self.jump_length = jump_length
        self.window_size = window_size
        self.liste_params = []
        self.liste_thres = []
        self.moy = 0.0
        self.mod = 0.0
        self.thres_area = {}
        self.range_liste_start = []
        self.mean_area = []

    def fit_distribution(self, data, distribution=st.nct):
        """
        Find parameters of fit distribution to data
        :param data: sample of the spectrum to fit the distribution on
        :param distribution: probability density function which fit the most on this kind of data
        :return: parameters of the fitted function
        """

        params = distribution.fit(data)

        df = params[0]
        nc = params[1]
        loc = params[2]
        scale = params[3]

        return df, nc, loc, scale, distribution

    def find_list_of_range(self):
        """
        Create an appropriate list of range
        :return: list of tuples which represent the starting and ending values for each range
        """

        start = self.start
        end = self.end
        jump = self.jump_length
        window = self.window_size

        nbr_possible_range = ((end - start) - (window - jump)) // jump
        rest = (((end - start) - (window - jump)) % jump)

        range_list = []
        for i in range(nbr_possible_range):
            a = start + (i * jump)
            b = a + window
            w = (a, b)
            range_list.append(w)

        if rest != 0:
            b = end
            a = b - window
            w = (a, b)
            range_list.append(w)

        return range_list

    def find_threshold(self, spectrum, window):
        """
        Compute threshold for the given range
        :param spectrum: the spectrum of data to work on
        :param window: tuple of the limits of a specific range in the spectrum
        :return: a threshold value
        """

        pipeline = Pipeline([MassRangeSelection(*window)])
        cut_spect = pipeline.fit_transform([spectrum])
        data = cut_spect[0].intensity_values
        # ----------> Cut x1
        # data2 = []
        # for i, val in enumerate(data):
        #
        #     if i < 10:
        #         data2.append(val)
        #     elif i % 2 != 0:
        #         data2.append(val)
        # data = np.array(data2)

        # ----------> Cut x2 ------> selected for now
        data2 = []
        for i, val in enumerate(data):

            if i < 10:
                data2.append(val)
            elif 10 < i < 500 and i % 2 != 0:
                data2.append(val)
            elif i % 3 == 0:
                data2.append(val)
        data = np.array(data2)

        # -------> cutx1 modif
        #         data2 = []
        #         for i, val in enumerate(data):
        #             if i < 100:
        #                 data2.append(val)
        #             elif i % 3== 0:
        #                 data2.append(val)
        #         data = np.array(data2)

        df, nc, loc, scale, distribution = self.fit_distribution(data)
        self.liste_params.append((df, nc, loc, scale))

        self.moy = np.mean(data)
        self.mod = st.mode(data)

        threshold_value = distribution.interval(self.alpha, df, nc, loc, scale)[1]

        return threshold_value

    def find_all_threshold(self, spectrum):
        """
        Gather all threshold for the entire spectrum
        :param spectrum: the spectrum of data to work on
        :return: list of all the threshold
        """

        threshold_list = []

        list_of_range = self.find_list_of_range()
        self.range_liste_start = list_of_range

        for i in list_of_range:
            t = self.find_threshold(spectrum, i)
            threshold_list.append(t)

        self.liste_thres = threshold_list

        return threshold_list

    def threshold_per_area(self, spectrum):
        """
        Find the appropriate threshold for an area
        :param spectrum: the spectrum of data to work on
        :return: dictionary with the range of an area and corresponding threshold
        """

        threshold_list = self.find_all_threshold(spectrum)
        range_list = self.find_list_of_range()

        if len(range_list) == 0:
            raise ValueError("The list of range 'range_list' is empty")

        if len(threshold_list) == 0:
            raise ValueError("The list of threshold 'threshold_list' is empty")

        list_of_area = []
        mean_of_area = []
        decomp_range_list = []
        dico_range_threshold = {}
        dico_value_threshold = OrderedDict([])

        for i, j in enumerate(range_list):  # create dictionary of threshold corresponding to range
            dico_range_threshold[j] = threshold_list[i]

        for i in range_list:  # create list of all values for establishing range of area
            for value in i:
                decomp_range_list.append(value)

        decomp_range_list = set(decomp_range_list)
        decomp_range_list = list(decomp_range_list)
        decomp_range_list.sort()  # get values in order : smaller to greater

        for i in range(len(decomp_range_list) - 1):  # match values to create range of area
            area = (decomp_range_list[i], decomp_range_list[i + 1])
            list_of_area.append(area)
            mean = (decomp_range_list[i] + decomp_range_list[i + 1]) // 2
            mean_of_area.append(mean)
            start_threshold = 0
            for key in dico_range_threshold.keys():
                if mean >= key[0] and mean < key[1]:
                    if dico_range_threshold[key] > start_threshold:
                        start_threshold = dico_range_threshold[key]
                        dico_value_threshold[area] = dico_range_threshold[key]

        smaller_threshold = min(threshold_list)

        self.thres_area = dico_value_threshold
        self.mean_area = mean_of_area

        return dico_value_threshold, smaller_threshold

    def apply_threshold(self, spectrum):

        """
        Apply the appropriate threshold on the spectrum
        :param spectrum: the spectrum of data to work on
        :param area_threshold: dictionary with the range of an area and corresponding threshold
        :param smaller_t: value of the smaller threshold found
        :return: modify spectrum
        """
        area_threshold, smaller_t = self.threshold_per_area(spectrum)
        if len(area_threshold) == 0:
            raise ValueError("Dictionary of corresponding threshold for a given area is empty")

        mask_del_smaller = spectrum.intensity_values > smaller_t
        # Working with the arrays instead of the Spectrum in ordre to save time...
        copy_mz_values = spectrum.mz_values[mask_del_smaller]
        copy_intensities = spectrum.intensity_values[mask_del_smaller]

        for i in area_threshold.keys():
            mask_mz_inf = copy_mz_values < i[0]
            mask_mz_sup = copy_mz_values >= i[1]
            mask_mz = mask_mz_inf + mask_mz_sup
            mask_intensity = copy_intensities > area_threshold[i]
            mask_area = mask_mz + mask_intensity
            copy_mz_values = copy_mz_values[mask_area]
            copy_intensities = copy_intensities[mask_area]
        spectrum = copy_spectrum_with_new_mz_and_intensities(spectrum, copy_mz_values,
                                                             copy_intensities)
        return spectrum

    def apply_threshold_manual(self, spectrum, t):
        """
        Apply the appropriate threshold on the spectrum
        :param spectrum: the spectrum of data to work on
        :param t: setting manual value of threshold
        :return: modify spectrum
        """

        mask_t = spectrum.intensity_values > t
        spectrum = copy_spectrum_with_new_mz_and_intensities(spectrum, spectrum.mz_values[mask_t],
                                                             spectrum.intensity_values[mask_t])

        return spectrum

    def fit(self, spectra):

        """
        TODO
        """
        pass

    def transform(self, spectra):
        """
        Apply the transformation (create a copy)
        """
        modified_spect = []
        for spect in spectra:
            modified_spect.append(self.apply_threshold(spect))
        return modified_spect

    def fit_transform(self, spectra):
        """
        Apply the transformation (call transform...)
        :param spectra: List of spect
        :return:
        """
        return self.transform(spectra)
