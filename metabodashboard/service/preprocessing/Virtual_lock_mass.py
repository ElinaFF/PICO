__author__ = 'pier-luc'

import copy
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import complete, fcluster, linkage
import logging

#from matplotlib.pyplot import cm
from metabodashboard.service.pymspec import Spectrum
import fastcluster as fc
from preprocessing.Utils import *

class Point():
    """
    Point class to be used only in the VLM algorithm (because of log). TODO: Change implementation
    """
    def __init__(self, mz, intensity, sample=None):
        self.mz = mz
        self.intensity = np.log10(intensity)
        self.sample = sample


class virtual_lock_mass_corrector():
    # TODO: Explain each option and make sure values are ok.
    def __init__(self, min_mz=50, max_mz=1200, vlm_intensity_threshold=1000, clusters_ppm_allowed=50,
                 max_delta_log_intensity=1, application_window=40, max_skipped_points=999, dist_matrix_dim=1,
                 overlaping_window=15):
        self.min_mz = min_mz
        self.max_mz = max_mz
        self.vlm_intensity_threshold = vlm_intensity_threshold
        self.clusters_ppm_allowed = clusters_ppm_allowed
        self.delta_log_intensity_allowed = max_delta_log_intensity
        self.apply_virtual_lock_mass_window = application_window
        self.allowed_skipped_points = max_skipped_points
        self.matrix_dimension = dist_matrix_dim
        self.overlaping_window = overlaping_window
        self.vlm_points = []


    def autoOptimize(self, spectrum, clusters_ppm_allowed=(10,20,30,40,50,60,70,80,90,100,110,120,130)):
        optimization_results = []
        for v in clusters_ppm_allowed:
             try:
                test_vlm = virtual_lock_mass_corrector(min_mz=self.min_mz, max_mz=self.max_mz,
                                                           vlm_intensity_threshold=self.vlm_intensity_threshold,
                                                           clusters_ppm_allowed=v,
                                                           max_delta_log_intensity=self.delta_log_intensity_allowed,
                                                           application_window=v,
                                                           max_skipped_points=self.allowed_skipped_points,
                                                           dist_matrix_dim=self.matrix_dimension,
                                                           overlaping_window=v/2)

                test_vlm.train(spectrum)
                optimization_results.append(len(test_vlm.vlm_points))
                logging.debug("Found %s peaks for clusters_ppm_allowed of %s ppm" %(len(test_vlm.vlm_points), v))
                #Something to stop early. If entry has more clusters thant the 2 next we select it.
                if len(optimization_results) > 3:
                    if optimization_results[-1] < optimization_results[-3] > optimization_results[-2]:
                        logging.debug("Stopping early!")
                        break
             except MemoryError:
                print("Could not run at %s ppm due to a surprisingly high number of peaks" %v) # TODO: Someting a bit harder than print
        best_results = max(optimization_results)
        logging.debug("Best value is %s ppm with %s clusters" %(
            clusters_ppm_allowed[optimization_results.index(best_results)], best_results))
        logging.debug("Distance values tried: %s" % str(clusters_ppm_allowed))
        logging.debug("Number of clusters found: %s" %str(optimization_results))
        index = optimization_results.index(best_results)
        self.clusters_ppm_allowed = clusters_ppm_allowed[index]
        self.overlaping_window = self.clusters_ppm_allowed/2


    def train(self, train_set):
        """
        Fill the vlm_points list based on the training set. Will overwrite its content if it is not empty.
        """
        ppm_overlap = self.overlaping_window/10**6
        self.vlm_points = []
        for i in range(self.min_mz, self.max_mz, self.matrix_dimension):
            points, clusters = self._find_candidates_vlm_points(train_set, [i-(i*ppm_overlap), i+self.matrix_dimension],
                                                                plot_points=False, plot_dendogram=False)
            if len(points) == 0:
                continue
            uniq_clusters = np.unique(clusters)
            for cluster_id in uniq_clusters:
                cluster_grouper = np.where(clusters == cluster_id)[0]
                points_in_cluster = points[cluster_grouper]
                logging.debug("Num pt in cluster: %s\nNum pts in train: %s" %(len(points_in_cluster), len(train_set)))
                samples_in_cluster = set(s.sample for s in points_in_cluster) # quick way to unique. Faster than numpy!
                if len(points_in_cluster) == len(samples_in_cluster) and len(samples_in_cluster) == len(train_set):
                    sorted_mz = [p.mz for p in points_in_cluster]
                    sorted_mz.sort()
                    logging.debug("Adding a VLM point: %s\n" % np.round(np.average([p.mz for p in points_in_cluster]), decimals=4))
                    logging.debug("Using: %s\nFrom: %s" %(sorted_mz, samples_in_cluster))
                    self.vlm_points.append(np.round(np.average([p.mz for p in points_in_cluster]), decimals=4))
                else:
                    logging.debug("Cluster is not a VLM.")
                    sorted_mz = [p.mz for p in points_in_cluster]
                    sorted_mz.sort()
                    logging.debug("Refused points: %s\nFrom: %s" %(sorted_mz, samples_in_cluster))
        self.vlm_points.sort()
        return

    def apply(self, data):
        for i, spect in enumerate(data):
            data[i] = self._apply_virtual_lock_mass(spect)

    def load(self, file_name):
        fi = open(file_name, 'r')
        self.min_mz = float(fi.readline())
        self.max_mz = float(fi.readline())
        self.vlm_intensity_threshold = int(fi.readline())
        self.clusters_ppm_allowed = int(fi.readline())
        self.delta_log_intensity_allowed = int(fi.readline())
        self.apply_virtual_lock_mass_window = int(fi.readline())
        self.allowed_skipped_points = int(fi.readline())
        self.matrix_dimension = int(fi.readline())
        self.overlaping_window = int(fi.readline())
        i = fi.readline()
        while 1:
            if i == "":
                break
            self.vlm_points.append(i)
            i = fi.readline()

    def save(self, file_name):
        fo = open(file_name, 'w')
        fo.write(str(self.min_mz)+"\n")
        fo.write(str(self.max_mz)+"\n")
        fo.write(str(self.vlm_intensity_threshold)+"\n")
        fo.write(str(self.clusters_ppm_allowed)+"\n")
        fo.write(str(self.delta_log_intensity_allowed)+"\n")
        fo.write(str(self.apply_virtual_lock_mass_window)+"\n")
        fo.write(str(self.allowed_skipped_points)+"\n")
        fo.write(str(self.matrix_dimension)+"\n")
        fo.write(str(self.overlaping_window)+"\n")
        for i in self.vlm_points:
            fo.write(str(i)+"\n")
        fo.close()

    #@staticmethod
    #def _generate_distance_matrix(points, w):
    #    r = np.array([(p.mz, p.intensity) for p in points])
    #    m = pdist(r, 'wminkowski', p=2, w=w)
    #    return m

    @staticmethod
    def _generate_distance_matrix(points):
        r = np.array([[p.mz] for p in points])
        m = pdist(r, 'euclidean')
        return m

    def _find_candidates_vlm_points(self, spectrum, window, show_warnings=False, plot_points=False, plot_dendogram=False):
        """
        Find a series of candidate VLM points for a specific window.
        The delta_log_intensity and ppm variables are not combined in the distance calculation.
        :param spectrum: A list of Spectrum
        :param window: A array of 2 float [mz1, mz2]
        :return: An array of candidates vlm points for this window using these spectrum.
        """
        window = [float(window[0]), float(window[1])]
        try:
            preprocessing_pipeline = common.Pipeline([discrete.MassRangeSelection(lower_range=window[0],
                                                                                  upper_range=window[1]),
                                                      discrete.ThresholdedPeakFiltering(self.vlm_intensity_threshold)])

            subspectrum = preprocessing_pipeline.fit_transform(spectrum)
        except ValueError:
            if show_warnings:
                print("Not a sufficient amount of points in region %s - %s" % (window[0], window[1]))
            return [], []

        points_list = []
        for i, spect in enumerate(subspectrum):
            for mz in spect.peaks():
                points_list.append(Point(mz, spect.peaks()[mz], i))


        if len(points_list) < len(subspectrum):
            if show_warnings:
                print("Not a sufficient amount of points in region %s - %s" % (window[0], window[1]))
            return [], []

        #w = self._find_w(window)

        #distance_matrix = self._generate_distance_matrix(points_list, w)
        distance_matrix = self._generate_distance_matrix(points_list)
        clusters_limit = window[1] * self.clusters_ppm_allowed / 10**6    # previously used self.overlaping_window
        clusters = fcluster(fc.linkage(distance_matrix, method="complete"), clusters_limit, 'distance')
        if plot_points:
            num_of_colors = len(np.unique(clusters))*2
            color_list = cm.rainbow(np.linspace(0,1,num_of_colors))
            for i, p in enumerate(points_list):
                plt.plot(p.mz, p.intensity, color=color_list[((clusters[i]-1)*2)], marker='o',
                         markerfacecolor=color_list[((clusters[i]-1) * 2)])
                plt.annotate(clusters[i], xy=(p.mz, p.intensity), xytext=(-5, 5), textcoords='offset points',
                             ha='right', va='bottom', arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
                print("P: %s;%s and cluster: %s" % (p.mz, p.intensity, clusters[i]))
            plt.grid(True)
            plt.xlabel("M/z")
            plt.ylabel("log(intensity)")
            plt.title("Points distribution colored by clusters")
            plt.show()
        if plot_dendogram:
            self._plot_dendrogram(spectrum, window)
        return np.array(points_list), np.array(clusters)

    #def _find_w(self, window):
    #    w2 = ((window[1] * self.overlaping_window/float(10**6))**2)/(self.delta_log_intensity_allowed**2)
    #    w = [1, w2]
    #    return w

    def _plot_dendrogram(self, spectrum, window):
        window = [float(window[0]), float(window[1])]

        preprocessing_pipeline = common.Pipeline([discrete.MassRangeSelection(lower_range=window[0],
                                                                              upper_range=window[1]),
                                                  discrete.ThresholdedPeakFiltering(self.vlm_intensity_threshold)])
        subspectrum = preprocessing_pipeline.fit_transform(spectrum)
        points_list = []
        for i, spect in enumerate(subspectrum):
            for mz in spect.peaks():
                points_list.append(Point(mz, spect.peaks()[mz], spect.metadata["file"]))

        labels = []
        for i in points_list:
            labels.append(i.sample.split('/')[-1]+"_"+str(i.mz)+"_"+str(i.intensity))
        w = self._find_w(window)
        distance_matrix = self._generate_distance_matrix(points_list, w)
        clusters_limit = window[1]*self.clusters_ppm_allowed/10**6
        clusters = fcluster(linkage(distance_matrix, method="complete"), clusters_limit, 'distance')

        clustering = complete(distance_matrix)
        ddata = plot_augmented_dendrogram(clustering, color_threshold=clusters_limit, p=len(points_list),
                                          truncate_mode="lastp", show_leaf_counts=False, labels=labels,
                                          leaf_rotation=90, leaf_font_size=10)
        plt.show()

    def _apply_virtual_lock_mass(self, spectrum, mode="flat"):
        """
        :param spectrum: the spectrum to correct
        :param mode: "flat" methode.
        :param window: The window size to search the vlock-mass in the spectrum. In ppm.
        :return: A corrected spectrum.
        """
        window =self.apply_virtual_lock_mass_window
        if len(self.vlm_points) <= 2:
            raise ValueError("There must be at least 3 points to use virtual lock-mass")
        spect_copy = copy.copy(spectrum)

        v_lockmass, observed_mz = self.find_vlock_mass_in_spectra(spect_copy, window)
        correction_ratios = self._calculate_correction_ratios(observed_mz, v_lockmass)
        corrected_mz = self._correct_points_smaller_than(spectrum, observed_mz[0], correction_ratios[0], mode=mode)
        index = 0
        while index < len(correction_ratios)-1:
            corrected_mz += self._correct_point_between(spectrum, observed_mz[index], observed_mz[index+1],
                                                        correction_ratios[index], correction_ratios[index+1])
            index += 1
        corrected_mz += self._correct_points_greater_than(spectrum, observed_mz[-1], correction_ratios[-1], mode=mode)
        if len(corrected_mz) != len(spectrum.mz_values):
            raise ValueError("There should be the same number of mz than in the initial spectrum:" +
                             str(len(corrected_mz)) + " vs " + str(len(spectrum.mz_values)))

        spectrum = Spectrum(np.array(corrected_mz), spectrum.intensity_values, spectrum.mz_precision, spectrum.metadata)
        return spectrum

    def find_vlock_mass_in_spectra(self, spectrum, window):
        """
        Search for the measured mz of the virtual lock-mass. Will return the most intense peaks in the window.
        :param window: the m/z area around each lock-mass. If peak is outside this window, it won't be found.
                       The window is in ppm.
        :param spectrum: The spectrum in which the measured m/z are searched
        :return:A list of measured m/z corresponding to the vlock-mass.
        :raises ValueError if a virtual lock mass is not found.
        """

        #TODO: Problem because there is a possibility we don't find the good peak because no threshold is applied.
        observed_mz = []
        num_of_skipped = 0
        v_lock_mass_found = []
        for v_mz in self.vlm_points:
            peak = -1
            intensity = -1
            try:
                possible_matches = binary_search_find_values(spectrum.mz_values, v_mz, window)
            except ValueError:

                if num_of_skipped < self.allowed_skipped_points:
                    print("Skipped mz %s" % v_mz)
                    num_of_skipped += 1
                    continue
                else:
                    raise ValueError("A virtual lock mass was not found in this spectrum: " + str(v_mz))
            if len(possible_matches) == 0:
                if num_of_skipped < self.allowed_skipped_points:
                    num_of_skipped += 1
                    print("Skipped mz %s" % v_mz)
                    continue
                else:
                    raise ValueError("A virtual lock mass was not found in this spectrum: " + str(v_mz))
            else:  # Will pick the most intense peak in the window
                intensities = []
                for i in possible_matches:
                    intensities.append(spectrum.peaks()[i])
                intensities, possible_matches = (list(t) for t in zip(*sorted(zip(intensities, possible_matches))))
                peak = possible_matches[-1]
            observed_mz.append(np.round(peak, 4))
            v_lock_mass_found.append(v_mz)
        observed_mz = np.array(observed_mz)
        v_lock_mass_found = np.array(v_lock_mass_found)
        np.around(observed_mz, decimals=4)
        return v_lock_mass_found, observed_mz

    def _calculate_correction_ratios(self, observed_mz, v_lock_mass):
        """
        Calculate the correction ratios for the virtual lock-mass and the corresponding observed mz
        :param observed_mz: A list of mz (array)
        :param v_lock_mass: The lock-mass reference values (array)
        :return: A list of correction ratio
        :raises: ValueError if one the list is empty, if list length is not equal or if there is a null or negative
        value
        """
        if len(observed_mz) <= 0 or len(v_lock_mass) <= 0:
            raise ValueError("There is no value in vlock_mass or observed_mz")
        if len(observed_mz) != len(v_lock_mass):
            raise ValueError("v_lock_mass and observed_mz have not the same amount of values")

        correction_ratios = []
        for i, v_mz in enumerate(v_lock_mass):
            o_mz = observed_mz[i]
            if v_mz <= 0 or o_mz <= 0:
                raise ValueError("Cannot calculate ratio for a null or nagative mz")
            ratio = np.float(v_mz / o_mz)
            correction_ratios.append(ratio)
        return correction_ratios

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
    def _correct_points_smaller_than(spectrum, mz, ratio, mode="flat"):
        """
        Will apply the correction ratio to every points <mz.
        No modification to correction ratio
        :param spectrum: the spectrum to correct
        :param mz: the observed mz of the first virtual lock mass
        :param ratio: the correction ratio of the first virtual lock mass
        :param mode: string. Flat for no change in ratio.
        :return: the corrected mz values of the spectrum, only those inferior to the first virtual lock mass
        """
        logging.debug("Length of mz before smaller: %s" % len(spectrum.mz_values))
        if mz <= 0 or ratio <= 0:
            raise ValueError("Mz and ration cannot be null or negative")
        mz_list = spectrum.mz_values.tolist()
        corrected_mz = []
        if mode == 'flat':
            right = binary_search_for_right_range(mz_list, mz)
            index = 0
            logging.debug("mz for smaller: %s" % mz)
            logging.debug("left: %s and value: %s" % (0, mz_list[0]))
            logging.debug("right: %s and value: %s" % (right, mz_list[right]))
            while index < right:
                corrected_mz.append(np.round(mz_list[index] * ratio, 4))
                index += 1
            if mz_list[index] < mz:
                # used to correct blanks correctly. Otherwise some values are missed because of the binary search.
                corrected_mz.append(np.round(mz_list[index] * ratio, 4))
        return corrected_mz

    @staticmethod
    def _correct_points_greater_than(spectrum, mz, ratio, mode="flat"):
        """
        :param spectrum: the spectrim to correct
        :param mz: the observed mz of the last virtual lock mass
        :param ratio: the correction ratio of the last virtual lock mass
        :param mode: flat, linear or 3rd degree
        :return: the corrected mz values of the spectrum, only those superior to the last virtual lock mass
        """
        corrected_mz = []
        if mz <= 0 or ratio <= 0:
            raise ValueError("Mz and ration cannot be null or negative")
        mz_list = spectrum.mz_values.tolist()
        if mode == 'flat':
            left = binary_search_for_right_range(mz_list, mz)
            index = left
            if mz_list[index] < mz:
                # adjust index for particular cases
                index += 1
            while index < len(mz_list):
                corrected_mz.append(np.round(mz_list[index] * ratio, 4))
                index += 1
        return corrected_mz

    def _correct_point_between(self, spectrum, mz1, mz2, ratio1, ratio2):
        """
        :param spectrum: the spectrum to correct
        :param mz1: an observed mz of a virtual lock mass (smaller than the 2nd)
        :param mz2: an observed mz of a virtual lock mass (greater than the first)
        :param ratio1: correction ratio of mz1
        :param ratio2: correction ratio of mz2
        :return: the corrected mz values from the spectrum that are between mz1 and mz2
        """
        if mz1 <= 0 or mz2 <= 0 or ratio1 <= 0 or ratio2 <= 0:
            raise ValueError("Mz and ratios cannot be null or negative")
        m, c = self._create_correction_function(mz1, mz2, ratio1, ratio2)
        # which method is the fastest? dict, list?
        mz_list = spectrum.mz_values.tolist()
        right = binary_search_for_right_range(mz_list, mz2)
        left = binary_search_for_left_range(mz_list, mz1)
        index = left
        corrected_mz = []
        while index < right:
            corrected_mz.append(np.round(mz_list[index]*(m*(mz_list[index])+c), 4))
            index += 1
        if mz_list[index] < mz2:
            # used to correct blanks correctly. Otherwise some values are missed because of the binary search.
            corrected_mz.append(np.round(mz_list[index]*(m*(mz_list[index])+c), 4))
        return corrected_mz

    def confirm_points_are_in_all_spectra(self, spect_list):
        vlms_real_positions = {}
        index = 0
        for spect in spect_list:
            vlm_founds, vlms_real_positions[index] = self.find_vlock_mass_in_spectra(spect, window=15.0)
            if len(vlm_founds) != len(vlms_real_positions[index]):
                raise ValueError("A point is missing in the train set")
            index += 1
        vlms_real_values = {}
        index = 0
        while index < len(vlms_real_positions[0]):
            vlms_real_values[index] = []
            index += 1

        for vlm in vlms_real_positions:
            index = 0
            for i in vlms_real_positions[vlm]:
                vlms_real_values[index].append(i)
                index += 1

        for i in vlms_real_values:
            l = np.array(vlms_real_values[i])
            l = np.sort(l)
            print("Average: %s +/- %s ppm" %(np.average(l), (l[-1]-l[0])/np.average(l)*(10**6)))