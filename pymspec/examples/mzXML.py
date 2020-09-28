__author__ = 'Alexandre Drouin'

raise RuntimeError("This example is deprecated and must be updated.")

from pprint import pprint

from pymspec.preprocessing.raw import NearestIntegerMzValues, IntensityValueNormalization
from pymspec.io.mzxml.file import MzXMLFile


f = MzXMLFile("./example.mzXML")

spectra = []
for s in f.get_spectra():

    if s.metadata['msLevel'] == 2 and len(s.peaks()) > 0: # MS/MS scans only
        spectra.append(s)
        print "-" * 200
        print s.metadata
        print pprint(s.peaks())
        print

f.close()

print len(spectra), " get_spectra loaded."
