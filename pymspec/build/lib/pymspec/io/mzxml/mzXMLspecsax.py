#!/usr/bin/env python
'''
mzXML parser
Based on PyMsXML (http://edwardslab.bmcb.georgetown.edu/software/PyMsXML.html)


'''
#########################################################################################
#                                                                                       #
# iQmerge software tool for merging CID and HCD scans for iTRAQ/TMT type experiments    #                                                                            #
# Written by Ashoka D. Polpitiya                                                        #
# for the Translational Genomics Research Institute (TGen), Phoenix, AZ                 #
#                                                                                       #
# E-mail: ashoka@tgen.org                                                               #
# Website: http://iqmerge.googlecode.com                                                #
#                                                                                       #
#########################################################################################

import sys
from array import array
from base64 import b64decode
from xml.sax import *

class mzXMLspecsax(handler.ContentHandler):

    def __init__(self):
        self.context = ''
        self.content = ''
        self.spectra = []
        self.instrument_md = {}
        self.done = False
        self.scancount = 0
        self.scanmax = 1000
        self.scanstart = 0
        
    def startElement(self, name, attrs):
        self.context += ':%s'%(name,)
        # print >>sys.stderr, ">>",self.context
        # sys.stderr.flush()
        self.content = ''

        if name == 'scan':
            self.scanmd = {}
            self.scanlevel = int(attrs['msLevel'])
            self.scannum = int(attrs['num'])
            if attrs.has_key('retentionTime'):
                self.rt = float(attrs['retentionTime'][2:-1])
            if attrs.has_key('endMz'):
                self.endMz = float(attrs['endMz'])
            if attrs.has_key('startMz'):
                self.startMz = float(attrs['startMz'])
            self.polarity = attrs.get('polarity',None)
            for (k,v) in attrs.items():
                self.scanmd[k] = v
            self.precursorMz = None
            self.scancount += 1
        elif name == 'msRun':
            self.scancount = 0
            self.spectra = []
            self.context = ':msRun'
        elif name == 'scanOrigin':
            self.scanmd['scanOrigin'] = attrs
        elif name == 'instrument':
            self.instrument_md = attrs._attrs
        elif self.context.endswith(':scan:nameValue'):
            self.scanmd['nameValue.%s:%%s'%attrs['name']] = attrs['value']
            
    def characters(self, content):
        if self.scancount >= self.scanstart:
            if self.context.endswith(':peaks') or \
                   self.context.endswith(':precursorMz'):
                self.content += content
            
    def endElementORG(self, name):
        if self.scancount >= self.scanstart:
            if self.context.endswith('scan:peaks'):
                
                self.spec = array('f')
                # print >>sys.stderr, len(self.content), len(b64decode(self.content)), self.content
                self.spec.fromstring(b64decode(self.content))
                if sys.byteorder != 'big':
                    self.spec.byteswap()
            elif self.context.endswith(':scan'):
                d = {'msLevel':self.scanlevel}
                # Optional ('scan.' and prefixformat spec. needed)
                if hasattr(self,'rt'):
                    d.update({'scan.retentionTime:PT%fS':self.rt})
                if hasattr(self,'startMz'):
                    d.update({'scan.startMz:%f':self.startMz})
                if hasattr(self,'endMz'):
                    d.update({'scan.endMz:%f':self.endMz})
                if self.polarity != None:
                    d.update({'scan.polarity:%s':self.polarity})
                if self.scanlevel == 1:
                    print 1
                if self.scanlevel == 2:
                    print 2
                    d.update({'precursorMz':self.precursorMz})
                if self.scanmd.has_key('scanOrigin'):
                    d.update({'scanOrigin.parentFileID:%s': self.scanmd['scanOrigin']['parentFileID'],
                              'scanOrigin.num:%d': int(self.scanmd['scanOrigin']['num'])})
                for (k,v) in self.scanmd.items():
                    if not d.has_key(k):
                        d[k] = v

                assert len(self.spec) % 2 == 0

                mz_values = []
                intensities = []
                for i in xrange(0, len(self.spec), 2):
                    mz_values.append(self.spec[i])
                    intensities.append(self.spec[i + 1])

                assert len(mz_values) == len(intensities)

                self.spectra.append((mz_values, intensities, d))
                if len(self.spectra) >= self.scanmax:
                    self.scanstart = self.scancount+1
                    raise SAXException("Early termination")
            elif self.context.endswith('scan:precursorMz'):
                self.precursorMz = float(self.content)
        if self.context.endswith('msRun'):
            self.done = True
        # print >>sys.stderr, "<<",self.context
        # sys.stderr.flush()
        self.context = self.context[0:-(len(name)+1)]

    def endElement(self, name):
        if self.scancount >= self.scanstart:
            if self.context.endswith('scan:peaks'):
                
                self.spec = array('f')
                # print >>sys.stderr, len(self.content), len(b64decode(self.content)), self.content
                
                self.spec.fromstring(b64decode(self.content))
                
                if sys.byteorder != 'big':
                    self.spec.byteswap()
                    
            #elif self.context.endswith(':scan'): ## This line will write only MS2 scans.
                d = {'msLevel':self.scanlevel}
                # Optional ('scan.' and prefixformat spec. needed)
                if hasattr(self,'rt'):
                    d.update({'scan.retentionTime:PT%fS':self.rt})
                if hasattr(self,'startMz'):
                    d.update({'scan.startMz:%f':self.startMz})
                if hasattr(self,'endMz'):
                    d.update({'scan.endMz:%f':self.endMz})
                if self.polarity != None:
                    d.update({'scan.polarity:%s':self.polarity})
                if self.scanlevel == 2:
                    d.update({'precursorMz':self.precursorMz})
                if self.scanmd.has_key('scanOrigin'):
                    d.update({'scanOrigin.parentFileID:%s': self.scanmd['scanOrigin']['parentFileID'],
                              'scanOrigin.num:%d': int(self.scanmd['scanOrigin']['num'])})
                for (k,v) in self.scanmd.items():
                    if not d.has_key(k):
                        d[k] = v

                assert len(self.spec) % 2 == 0

                mz_values = []
                intensities = []
                for i in xrange(0, len(self.spec), 2):
                    mz_values.append(self.spec[i])
                    intensities.append(self.spec[i + 1])

                assert len(mz_values) == len(intensities)

                self.spectra.append((mz_values, intensities, d))
                if len(self.spectra) >= self.scanmax:
                    self.scanstart = self.scancount+1
                    raise SAXException("Early termination")
            elif self.context.endswith('scan:precursorMz'):
                self.precursorMz = float(self.content)
        if self.context.endswith('msRun'):
            self.done = True
        # print >>sys.stderr, "<<",self.context
        # sys.stderr.flush()
        self.context = self.context[0:-(len(name)+1)]
