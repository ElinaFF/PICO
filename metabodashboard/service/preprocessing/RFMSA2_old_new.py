__author__='pier-luc'


from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import complete, fcluster, linkage
import fastcluster as fc
from itertools import chain
import preprocessing.Utils
import numpy as np
import logging
from metabodashboard.service.pymspec.spectrum import *
import time

try:
    from itertools import izip as zip
except ImportError:  # will give error if python 3.X is used, so builtin function zip is used
    pass

class Reference_free_aligner2():

    def __init__(self, min_mz=50, max_mz=1200, max_distance=15):
        self.min_mz = min_mz
        self.max_mz = max_mz
        self.max_distance = max_distance
        self.reference_mz = []

    def train(self, train_set):
        self._train(train_set)


    def _train(self, train_set, auto_optimizer=False):
        """
        Fill the reference_mz attribute with possible m/z values.
        :param train_set: A set of pymspec object.
        :return: Nothing
        """
        possible_mz = list(chain(mz for spect in train_set for mz in spect.mz_values))
        possible_mz = np.sort(possible_mz)

        # Took some code generated during ATP by Alex Drouin
        # Split the list of unique m/z values into blocks
        # Note: if a peak is too far from its neighbor to possibly cluster with it, there is no need to consider them in
        #       the same clustering. The same applies for all peaks after the neighbor, as they are sorted.
        ppm_at_mz = possible_mz * float(self.max_distance*1) / 10**6  # 1x themax distance allowed in a cluster.
        d_next = np.hstack((np.abs(possible_mz[:-1] - possible_mz[1:]), [0]))  # The distance to the next peak
        tmp = np.where(d_next > ppm_at_mz)[0]
        block_ends = np.hstack((tmp, [len(possible_mz) - 1]))
        block_starts = np.hstack(([0], tmp + 1))

        # For each block, perform a hierarchical clustering
        logging.debug("There are %d peak blocks" % len(block_starts))
        mz_cluster_idx = np.zeros(possible_mz.shape[0], dtype=np.uint)
        if auto_optimizer:
            small= []
            ok = []
            big= []
        for start_idx, stop_idx in zip(block_starts, block_ends):
            block_mz_values = possible_mz[start_idx:stop_idx+1]
            block_start_mz = possible_mz[start_idx]
            block_stop_mz = possible_mz[stop_idx]
            logging.debug("There are %d peaks in the block" % len(block_mz_values))
            logging.debug("The block spans the interval [%.6f, %.6f]" % (block_start_mz, block_stop_mz))

            if start_idx == stop_idx:
                logging.debug("Cluster contained only 1 peak. Trivial clustering produced 1 cluster.")
                if not auto_optimizer:
                    self.reference_mz.append(block_start_mz)
                continue

            # Compute the distance between each m/z value
            if len(block_mz_values)<100000:
                logging.debug("Computing the distance between each pair of peaks using the m/z values")
                D = pdist(block_mz_values.reshape(-1, 1), metric="euclidean")

                # Compute the clustering distance threshold
                block_cluster_threshold = np.mean(block_mz_values * self.max_distance/10**6)  # Use mean window size
                logging.debug("A %d ppm interval roughly corresponds to %.6f m/z" % (self.max_distance,
                                                                                     block_cluster_threshold))

                logging.debug("Clustering the peaks")
                # Clustering using fastcluster. (it is very fast!)
                clusters = fcluster(fc.linkage(D, method='complete'), criterion="distance",
                                    t=block_cluster_threshold)
                uniq_clusters = np.unique(clusters)
                for cluster_id in uniq_clusters:
                    cluster_grouper = np.where(clusters == cluster_id)[0]
                    points_in_cluster = block_mz_values[cluster_grouper]
                    if auto_optimizer:
                        if len(points_in_cluster) == len(train_set):
                           ok.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                           self.reference_mz.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                        elif len(points_in_cluster) > len(train_set):
                           big.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                        elif len(points_in_cluster) < len(train_set):
                           small.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                        #self.reference_mz.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                    elif not auto_optimizer:
                        self.reference_mz.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
            else:
                logging.debug("Splitting in sub-blocks and computing the distance between each pair of peaks using the m/z values")
                print("Splitting in sub-blocks and computing the distance between each pair of peaks using the m/z values")
                blocks = [block_mz_values]
                sub_blocks = []
                has_big_block = True
                while has_big_block:
                    has_big_block=False
                    for b in blocks:
                        if len(b) > 100000:
                            sub_blocks.append(b[0:len(b)/2])
                            sub_blocks.append(b[len(b)/2:])
                            has_big_block = True
                    if has_big_block:
                        blocks  = sub_blocks
                        sub_blocks = []
                for b in blocks:
                    D = pdist(b.reshape(-1, 1), metric="euclidean")

                    # Compute the clustering distance threshold
                    block_cluster_threshold = np.mean(b * self.max_distance/10**6)  # Use mean window size
                    logging.debug("A %d ppm interval roughly corresponds to %.6f m/z" % (self.max_distance,
                                                                                         block_cluster_threshold))
                    logging.debug("Clustering the peaks")
                    # Clustering using fastcluster. (it is very fast!)
                    clusters = fcluster(fc.linkage(D, method='complete'), criterion="distance",
                                        t=block_cluster_threshold)
                    uniq_clusters = np.unique(clusters)
                    for cluster_id in uniq_clusters:
                        cluster_grouper = np.where(clusters == cluster_id)[0]
                        points_in_cluster = b[cluster_grouper]
                        if auto_optimizer:
                            if len(points_in_cluster) == len(train_set):
                               ok.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                               self.reference_mz.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                            elif len(points_in_cluster) > len(train_set):
                               big.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                            elif len(points_in_cluster) < len(train_set):
                               small.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                            #self.reference_mz.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
                        elif not auto_optimizer:
                            self.reference_mz.append(np.round(np.average([mz for mz in points_in_cluster]), decimals=4))
        if auto_optimizer:
            return small, ok, big
        else:
            self.reference_mz.sort()


    def apply(self, data_set):
        for i, spect in enumerate(data_set):
            data_set[i] = self._apply(spect)


    def _apply(self, spectrum):
        # Find closest point that is not outside possible window
        # If point: change mz
        # Else: keep or discard m/z?
        aligned_mz = []
        aligned_intensities = []
        not_found_mz = []
        not_found_intensities = []
        for mz in spectrum.mz_values:
            possible_matches = []
            try:
                possible_matches = preprocessing.Utils.binary_search_find_values(self.reference_mz, mz,
                                                                                 float(self.max_distance))
            except ValueError:
                not_found_mz.append(mz)
                not_found_intensities.append(spectrum.peaks()[mz])
                continue
            if len(possible_matches) > 1:
                possible_matches = [preprocessing.Utils.take_closest(possible_matches, mz)]

            if len(possible_matches) == 1:
                aligned_mz.append(possible_matches[0])
                aligned_intensities.append(spectrum.peaks()[mz])
            else:
                aligned_mz.append(mz)
                aligned_intensities.append(spectrum.peaks()[mz])
                not_found_mz.append(mz)
                not_found_intensities.append(spectrum.peaks()[mz])
                logging.debug("Length of possible_matches: %s\n" %(len(possible_matches)))
                # raise ValueError("Wut!")
        logging.debug("Did not found %s peaks in spect.\n" % (len(not_found_mz)))
        return Spectrum(aligned_mz, aligned_intensities, spectrum.mz_precision, spectrum.metadata)


    def autoOptimize(self, spectrum, max_distance_values=(10,20,30,40,50,60,70,80,90,100,110,120,130)):
        # This should maximize the number of cluster and keep errors to a minimum
        # We tolerate errors on some peaks if it provides a better a alignment on
        opt_results = []
        for v in max_distance_values:
            try:
                test_aligner = Reference_free_aligner2(min_mz=self.min_mz, max_mz=self.max_mz, max_distance=v)
                test_aligner._train(spectrum, auto_optimizer=True)
                opt_results.append(len(test_aligner.reference_mz))
                logging.debug("Found %s peaks for a max_distance of %s ppm" %(len(test_aligner.reference_mz), v))
                #Something to stop early. If entry has more clusters thant the 2 next we select it.
                if len(opt_results) > 3:
                    if opt_results[-1] < opt_results[-3] > opt_results[-2]:
                        logging.debug("Stopping early!")
                        break
            except MemoryError:
                print("Could not run at %s ppm due to a suprisingly high number of peaks" %v) # TODO: Someting a bit harder than print
        best_results = max(opt_results)
        logging.debug("Best value is %s ppm with %s clusters" %( max_distance_values[opt_results.index(best_results)], best_results))
        logging.debug("Distance values tried: %s" % str(max_distance_values))
        logging.debug("Number of clusters found: %s" %str(opt_results))
        index = opt_results.index(best_results)
        self.max_distance = max_distance_values[index]
        print("Max distance selected is : %s" %self.max_distance)


    def load(self, file_name):
        fi = open(file_name, 'r')
        self.min_mz = float(fi.readline())
        self.max_mz = float(fi.readline())
        self.max_distance = float(fi.readline())
        i = fi.readline()
        while 1:
            if i == "":
                break
            self.reference_mz.append(i)
            i = fi.readline()


    def save(self, file_name):
        fo = open(file_name, 'w')
        fo.write(str(self.min_mz)+"\n")
        fo.write(str(self.max_mz)+"\n")
        fo.write(str(self.max_distance)+"\n")
        for i in self.vlm_points:
            fo.write(str(i)+"\n")
        fo.close()


if __name__ == '__main__':
    import glob
    import Virtual_lock_mass
    from metabodashboard.service.pymspec.spectrum import *
    from metabodashboard.service.pymspec.io.ion_list.file_loader import *
    import time
    from metabodashboard.service.pymspec.preprocessing.common import *
    from metabodashboard.service.pymspec.preprocessing.discrete import *

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s")

    t = time.time

    t1 =t()

    path = "/home/pier-luc/PycharmProjects/Mass_spectrometry/Data" \
           "/Metabolomic_soil_preliminary/Data_fct1/*.lcs"
    file_list = glob.glob(path)
    print("Loading")
    spect = load_ion_list(file_list, mz_precision=4)
    spect = ThresholdedPeakFiltering(threshold=100, remove_mz_values=True).fit_transform(spect)
    print("Loaded")

    vlm = Virtual_lock_mass.virtual_lock_mass_corrector(min_mz=100, max_mz=1000,
                                                        vlm_intensity_threshold=1000,
                                                        clusters_ppm_allowed=90,
                                                        max_delta_log_intensity=1,
                                                        application_window=15,
                                                        max_skipped_points=999,
                                                        dist_matrix_dim=1,
                                                        overlaping_window=30)
    t1 = t()
    print("Training VLM")
    #vlm.train(spect)
    print("Training done in %s" %(t()-t1))
    t1=t()
    print("Applying VLM")
    #vlm.apply(spect)
    print("Applying VLM done in %s" %(t()-t1))

    aligner = Reference_free_aligner2(min_mz=50, max_mz=1200, max_distance=15)
    print("Training aligner")
    t1 = t()
    aligner.train(spect)
    print("Training aligner done in %s" %(t()-t1))

    print("Applying aligner")
    t1 = t()
    aligner.apply(spect)
    print("Applying aligner done in %s" %(t()-t1))
    print(len(spect[0].mz_values))
    unify_mz(spect)
    print(len(spect[0].mz_values))
