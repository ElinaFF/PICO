
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

from urllib import unquote
from xml.sax import *

class mzXMLmdsax(handler.ContentHandler):

    def __init__(self):
        self.md = {}
        self.context = ''

    def startElement(self, name, attrs):
        self.context += ':%s'%(name,)
        # print >>sys.stderr, ">>",self.context
        # sys.stderr.flush()
        if self.context.endswith(':msRun'):
            if attrs.has_key('startTime'):
                self.md['startTime'] = float(attrs['startTime'][2:-1])
            if attrs.has_key('endTime'):
                self.md['endTime'] = float(attrs['endTime'][2:-1])
        elif self.context.endswith(':parentFile'):
            if not self.md.has_key('parentFile'):
                self.md['parentFile'] = []
            self.md['parentFile'].append((unquote(attrs['fileName']),attrs['fileType'],attrs['fileSha1']))
        elif self.context.endswith(':instrument'):
            self.md['msManufacturer'] = attrs.get('manufacturer', '')
            self.md['msModel'] = attrs.get('model', '')
            self.md['msIonisation'] = attrs.get('ionisation', '')
            self.md['msMassAnalyzer'] = attrs.get('msType', '')
        elif self.context.endswith(':msInstrument:msManufacturer'):
            self.md['msManufacturer'] = attrs['value']
        elif self.context.endswith(':msInstrument:msModel'):
            self.md['msModel'] = attrs['value']
        elif self.context.endswith(':msInstrument:msIonisation'):
            self.md['msIonisation'] = attrs['value']
        elif self.context.endswith(':msInstrument:msMassAnalyzer'):
            self.md['msMassAnalyzer'] = attrs['value']
        elif self.context.endswith(':msInstrument:msDetector'):
            self.md['msDetector'] = attrs['value']
        elif self.context.endswith(':msInstrument:software'):
            if attrs['type'] == 'acquisition':
                self.md['acquisitionSoftware'] = attrs['name']
                self.md['acquisitionSoftwareVersion'] = attrs['version']
        elif self.context.endswith(':instrument:software'):
            if attrs['type'] == 'acquisition':
                self.md['acquisitionSoftware'] = attrs['name']
                self.md['acquisitionSoftwareVersion'] = attrs['version']
        elif self.context.endswith(':scan'):
            raise SAXException("Early termination")

    def endElement(self, name):
        # print >>sys.stderr, "<<",self.context
        # sys.stderr.flush()
        self.context = self.context[0:-(len(name)+1)]
