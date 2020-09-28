# -*- coding: utf8 -*-
__author__ = 'Alexandre Drouin'

import cPickle as c
from pymspec.preprocessing.common import *
from pymspec.preprocessing.raw import *
from pymspec.visualization.plot import SpectrumPlot

f = open("example_spectra_5_patients.pkl")
#f = open("example_spectra_5_replica.pkl")
spectra = c.load(f)
f.close()

# If we did not wish to obtain the baseline corrected spectra before normalizing them, we could have used a pipeline
spectra_baseline_and_normalized = \
    Pipeline([TopHatBaselineCorrection(structural_element_size=0.01),
             TotalIonCurrentNormalization(local=True, use_median=True, window_size=0.65)]).fit_transform(spectra)

print "Baseline Correction"
spectra_baseline = TopHatBaselineCorrection(structural_element_size=0.01).fit_transform(spectra)

print "Normalization"
spectra_normalized = TotalIonCurrentNormalization(local=False, use_median=True, window_size=0.25).fit_transform(
    spectra_baseline)

SpectrumPlot(title="Raw Spectra", spectra=spectra,
             spectra_labels=[s.metadata["sample_name"] + " Raw" for s in spectra]).show()
SpectrumPlot(title="Baseline Corrected Spectra", spectra=spectra_baseline,
             spectra_labels=[s.metadata["sample_name"] + " Baseline Corrected" for s in spectra]).show()
SpectrumPlot(title="Baseline Corrected and TIC Normalized Spectra", spectra=spectra_normalized,
             spectra_labels=[s.metadata["sample_name"] + " Baseline Corrected + Local TIC Normalization" for s in
                             spectra]).show()

SpectrumPlot(title="Baseline Corrected and TIC Normalized Spectra", spectra=spectra_baseline_and_normalized,
             spectra_labels=[s.metadata["sample_name"] + " Baseline Corrected + Local TIC Normalization" for s in
                             spectra]).show()
