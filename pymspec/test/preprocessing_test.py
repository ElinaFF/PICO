import unittest

from pymspec.preprocessing.common import *
from pymspec.preprocessing.raw import *
from pymspec.preprocessing.discrete import *


class TestPipeline(unittest.TestCase):
    #TODO: test with preprocessors that use fit
    def test_fit_transform(self):
        peak_filter = MostIntensePeakFiltering(frac_of_peaks=0.5)
        intensity_binarizer = IntensityBinarization()
        pipeline = Pipeline([peak_filter, intensity_binarizer])

        spectra = [Spectrum(mz_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            mz_precision=0,
                            intensity_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                   Spectrum(mz_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            mz_precision=0,
                            intensity_values=[1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])]

        self.assertTrue(np.all(pipeline.fit_transform(spectra) == \
                               [Spectrum(mz_values=[10, 9, 8, 7, 6], mz_precision=0, intensity_values=[1.0]*5),
                                Spectrum(mz_values=[1, 2, 3, 4, 5], mz_precision=0,
                                         intensity_values=[1.0]*5)]))

class TestTotalIonCurrentNormalization(unittest.TestCase):
    pass


class TestTopHatBaselineCorrection(unittest.TestCase):
    pass


class TestMostIntensePeakFiltering(unittest.TestCase):
    def test_preprocessor(self):
        spectra = [Spectrum(mz_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            mz_precision=0,
                            intensity_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                   Spectrum(mz_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            mz_precision=0,
                            intensity_values=[1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])]

        filter = MostIntensePeakFiltering(0.5)
        self.assertTrue(np.all(filter.fit_transform(spectra) == \
                               [Spectrum(mz_values=[10, 9, 8, 7, 6], mz_precision=0, intensity_values=[10, 9, 8, 7, 6]),
                                Spectrum(mz_values=[1, 2, 3, 4, 5], mz_precision=0,
                                         intensity_values=[1.0, 0.9, 0.8, 0.7, 0.6])]))


class TestIntensityBinarization(unittest.TestCase):
    def test_preprocessor(self):
        spectra = [Spectrum(mz_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            mz_precision=0,
                            intensity_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                   Spectrum(mz_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            mz_precision=0,
                            intensity_values=[1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])]

        preprocessor = IntensityBinarization()

        self.assertTrue(np.all(preprocessor.fit_transform(spectra_list=spectra) == [
            Spectrum(mz_values=range(1, 11), mz_precision=0, intensity_values=[1.0] * 10)] * 2))