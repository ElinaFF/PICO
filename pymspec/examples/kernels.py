__author__ = 'Alexandre Drouin'

raise RuntimeError("This example is deprecated and must be updated.")

import numpy as np
from pymspec.spectrum import Spectrum
from pymspec.io.mzxml.file import MzXMLFile
from pymspec.compare.kernels import LinearKernel, XCorrKernel
from pymspec.preprocessing.raw import IntensityValueNormalization

#f = MzXMLFile("/Users/Alexandre/Downloads/Mix_1-1/QSTAR/mzXML/QS20051103_S_18mix_01.mzXML")
f = MzXMLFile("./example.mzXML")


f._open()

mz_precision = 0

spectra = []
for s in f.get_spectra():
    if s[2]['msLevel'] == 2 and s[2]['peaksCount'] > 0: # MS/MS scans only
        spectrum = Spectrum(s[0], s[1], mz_precision, s[2], preprocessing_steps=[IntensityValueNormalization()])
        spectra.append(spectrum)
        print spectrum
        print "-" * 200
        print

    if len(spectra) == 50:
        break

f.close()

print len(spectra), " get_spectra loaded."

print np.round(LinearKernel(normalize=True)(spectra, spectra), 2)
print
print np.round(XCorrKernel(shift_span=75, normalize=True)(spectra, spectra), 2)
print
