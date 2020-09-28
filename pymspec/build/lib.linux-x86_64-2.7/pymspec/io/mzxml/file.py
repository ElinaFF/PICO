__author__ = 'Alexandre Drouin'

#!/usr/bin/env python

'''
Based on PyMsXML (http://edwardslab.bmcb.georgetown.edu/software/PyMsXML.html)
'''
#########################################################################################
#                                                                                       #
# iQmerge software tool for merging CID and HCD scans for iTRAQ/TMT type experiments    #                                                                            #
# Written by Ashoka D. Polpitiya                                                        #
# for the Translational Genomics Research Institute (TGen), Phoenix, AZ                 #
#                                                                                       #
# Copyright 2011, Translational Genomics Research Institute                             #
# E-mail: ashoka@tgen.org                                                               #
# Website: http://iqmerge.googlecode.com                                                #
# --------------------------------------------------------------------------------------#
#                                                                                       #
# Licensed under the Apache License, Version 2.0 (the "License");                       #
# you may not use this file except in compliance with the License.                      #
# You may obtain a copy of the License at                                               #
#                                                                                       #
#       http://www.apache.org/licenses/LICENSE-2.0                                      #
#                                                                                       #
# Unless required by applicable law or agreed to in writing, software                   #
# distributed under the License is distributed on an "AS IS" BASIS,                     #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.              #
# See the License for the specific language governing permissions and                   #
# limitations under the License.                                                        #
#                                                                                       #
#########################################################################################

import numpy as np
import os
from ...spectrum import Spectrum
from mzXMLmdsax import mzXMLmdsax
from mzXMLspecsax import mzXMLspecsax
from xml.sax import *

class MzXMLFile:
    '''
    Read scans to a mzXML file
    '''
    def __init__(self,filename):
        self.filename = filename
        self.parser = None

        if not os.path.exists(self.filename):
            raise RuntimeError("Filename %s does not exist."%(self.filename,))

    def __del__(self):
        self.close()

    def _open(self):
        '''
        Open an mzXML file to read. Set the handlers.
        '''
        if self.parser == None:
            self.parser = make_parser()
            self.handler = mzXMLmdsax()
            self.parser.setContentHandler(self.handler)
            try:
                self.parser.parse(self.filename)
            except SAXException:
                pass

            self.md = self.handler.md

            self.parser = make_parser()
            self.handler = mzXMLspecsax()
            self.parser.setContentHandler(self.handler)

    def close(self):
        pass

    def get_spectra(self, mz_precision=20):
        '''
        Return the all spectra contained in the file
        '''
        self._open()
        spectra = []
        while True:
            try:
                self.parser.parse(self.filename)
            except SAXException:
                pass
            for (mz_values, intensities, d) in self.handler.spectra:
                spectra.append(Spectrum(mz_values=mz_values,
                                        mz_precision=mz_precision,
                                        intensity_values=intensities,
                                        metadata=d))
            if self.handler.done:
                break

        return np.asarray(spectra)

    def getMsRunMetaData(self):
        '''
        Tes method to get some meta data
        '''
        self._open()
        d = {}
        if self.md.has_key('startTime'):
            d.update({'startTime:PT%fS':self.md['startTime']})
        if self.md.has_key('endTime'):
            d.update({'endTime:PT%fS':self.md['endTime']})
        return d

    def getFilenames(self):
        return self.md['parentFile']

    def msManufacturer(self):
        return self.md.get('msManufacturer','')

    def msModel(self):
        return self.md.get('msModel','')

    def msIonisation(self):
        return self.md.get('msIonisation','')

    def msMassAnalyzer(self):
        return self.md.get('msMassAnalyzer','')

    def msDetector(self):
        return self.md.get('msDetector','')

    def acquisitionSoftware(self):
        return self.md.get('acquisitionSoftware','')

    def acquisitionSoftwareVersion(self):
        return self.md.get('acquisitionSoftwareVersion','')
