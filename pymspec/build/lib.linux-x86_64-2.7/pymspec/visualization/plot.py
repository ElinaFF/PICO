__author__ = 'Dany Vohl'

'''
Code by Dany Vohl
Started on November 5 2013.
-
File: plot.py
What?: Produce 2D spectral graphs.
'''

import numpy as np
from pylab import *
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from copy import deepcopy
from pymspec.preprocessing import discrete
from pymspec.spectrum import *

class SpectrumPlot:
    def __init__(self, spectra=[], spectra_labels=[], spectra_discrete=False, show_spectra=True, show_mean_spectrum=False, show_uncertainty=False, title="", x_label="m/z", y_label="Intensity", legend_label="", mz_range=None):
        self.spectra = spectra
        self.spectra_labels = spectra_labels

        if len(spectra_labels) != 0 and len(spectra) != len(spectra_labels):
            raise ValueError("If specified, the number of spectrum labels must match the number of spectra.")

        self.spectra_discrete = spectra_discrete
        self.show_spectra = show_spectra
        self.show_mean_spectrum = show_mean_spectrum
        self.show_uncertainty = show_uncertainty

        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.legend_label = legend_label
        self.mz_range = mz_range

    def _init_plot(self):
        clf()
        title(self.title)

        # Determine plot layout
        if self.show_mean_spectrum and self.show_uncertainty:
            spectra_plot = subplot(2,1,2)
            uncertainty_plot = subplot(2,1,1, sharex=spectra_plot)
            uncertainty_plot.set_ylabel("Relative Uncertainty")
            setp(uncertainty_plot.get_xticklabels(), visible=False)
        else:
            spectra_plot = subplot(1,1,1)

        spectra_plot.set_xlabel(self.x_label)
        spectra_plot.set_ylabel(self.y_label)


        if self.show_mean_spectrum:
            if(self.mz_range != None):
                selectedMz = []
                for spectra in self.spectra:
                    for mz in spectra.mz_values:
                        if((mz > self.mz_range[0]) and (mz < self.mz_range[1])):
                            selectedMz.append(mz)
                mz_values = np.array(sorted(set(selectedMz)))
            else:
                mz_values = np.array(sorted(set(mz for spectra in self.spectra for mz in spectra.mz_values)))

            mean_intensity_values = np.zeros(mz_values.shape)
            intensity_values_std = np.zeros(mz_values.shape)
            for i in xrange(len(mean_intensity_values)):
                spectra_intensities = np.array([s.intensity_at(mz_values[i]) for s in self.spectra])
                mean_intensity_values[i] = np.mean(spectra_intensities)
                intensity_values_std[i] = np.std(spectra_intensities)

            intensity_absolute_uncertainties = 2.0*intensity_values_std / (len(self.spectra)**0.5)
            intensity_relative_uncertainties = intensity_absolute_uncertainties / mean_intensity_values

            if self.spectra_discrete:
                _, stemlines, baseline = spectra_plot.stem(mz_values, mean_intensity_values, markerfmt=' ', label="Mean Spectrum")
                setp(stemlines, "color", "black")
                setp(baseline, "color", "black")
            else:
                spectra_plot.plot(mz_values, mean_intensity_values, lw=0.6, color="black", label="Mean Spectrum")

            if self.show_uncertainty:
                if self.spectra_discrete:
                    uncertainty_plot.stem(mz_values, intensity_relative_uncertainties, markerfmt=" ")
                else:
                    uncertainty_plot.plot(mz_values, intensity_relative_uncertainties)

        if self.show_spectra:
            colors = cm.rainbow(np.linspace(0, 1, len(self.spectra)))

            for i, spectrum in enumerate(self.spectra):
                if(self.mz_range != None):
                    selectedMz = []
                    for mz in spectrum.mz_values:
                        if((mz > self.mz_range[0]) and (mz < self.mz_range[1])):
                            selectedMz.append(mz)
                    if self.spectra_discrete:
                        spectra_plot.stem(selectedMz, spectrum.intensity_values, color=colors[i], markerfmt=' ', label=self.spectra_labels[i] if len(self.spectra_labels) > 0 else None)
                    else:
                        spectra_plot.plot(selectedMz, spectrum.intensity_values, color=colors[i], lw=0.5, label=self.spectra_labels[i] if len(self.spectra_labels) > 0 else None)

                else:
                    if self.spectra_discrete:
                        _, stemlines, baseline = spectra_plot.stem(spectrum.mz_values, spectrum.intensity_values, markerfmt=' ', label=self.spectra_labels[i] if len(self.spectra_labels) > 0 else None)
                        setp(stemlines, "color", colors[i])
                        setp(baseline, "color", colors[i])
                    else:
                        spectra_plot.plot(spectrum.mz_values, spectrum.intensity_values, color=colors[i], lw=0.5, label=self.spectra_labels[i] if len(self.spectra_labels) > 0 else None)

        spectra_plot.legend(loc="upper right", title=self.legend_label)

        tight_layout(h_pad=1.0)

    def show(self):
        self._init_plot()
        show()

    def save(self, file_name):
        self._init_plot()
        savefig(file_name)


class AlignmentPlot:
    def __init__(self, spectra, labels, title="", keep_most_intense_frac=1.0, concensus_frac=1.0,
                 colors=["Reds", "Blues"]):
        self.spectra = deepcopy(spectra)    #Is it necessary?
        self.labels = labels
        self.title = title

        if 0 > keep_most_intense_frac > 1:
            raise ValueError("The keep_most_intense_frac must be between 0.0 and 1.0")
        self.keep_most_intense_frac = keep_most_intense_frac

        if 0 > concensus_frac > 1:
            raise ValueError("The consensus_frac must be between 0.0 and 1.0")
        self.consensus_frac = concensus_frac

        if len(colors) != 2:
            raise ValueError("There must be 2 colors")
        self.colors = colors

    def _init_plot(self):

        spectra = discrete.MostIntensePeakFiltering(self.keep_most_intense_frac).fit_transform(self.spectra)
        unify_mz(spectra)

        fig, axes = plt.subplots(nrows=len(spectra) + 1, sharex=True, sharey=True)
        fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=10)

        all_values = np.zeros((len(spectra), len(spectra[0])))
        for i, spectrum in enumerate(spectra):
            all_values[i] = np.log(spectrum.intensity_values + 1)

        consensus = np.uint8(np.sum(np.uint8(all_values > 0), axis=0) >= self.consensus_frac * len(spectra))
        all_values = np.vstack((consensus, all_values))
        labels = ["Consensus (%d matches)"%np.sum(consensus)] + self.labels

        for ax, (spectrum_intensities, label) in zip(axes, zip(all_values, labels)):
            values = np.vstack((spectrum_intensities, spectrum_intensities))
            if "Consensus" in label:
                ax.imshow(values, aspect='auto', cmap=plt.get_cmap(self.colors[0]), interpolation="none")
            else:
                ax.imshow(values , aspect='auto', cmap=plt.get_cmap(self.colors[1]), interpolation="none")
            pos = list(ax.get_position().bounds)
            x_text = pos[0] - 0.01
            y_text = pos[1] + pos[3]/2.
            fig.text(x_text, y_text, label, va='center', ha='right', fontsize=10)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
        for ax in axes:
            ax.set_axis_off()

    def show(self):
        self._init_plot()
        show()

    def save(self, file_name):
        self._init_plot()
        savefig(file_name)
