import unittest

import numpy as np

from pymspec.spectrum import Spectrum


class TestSpectrumArithmetic(unittest.TestCase):
    def test_addition_with_spectrum(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 2, 3, 4, 5], mz_precision=2,
                  metadata={"name": "test1"})
        s2 = Spectrum(mz_values=np.arange(5.0), intensity_values=[0, 1, 0, 1, 0], mz_precision=2,
                      metadata={"name": "test2"})

        self.assertEquals(s1 + s2, Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 3, 3, 5, 5], mz_precision=2, metadata=[{"name": "test1"}, {"name": "test2"}]))

        s3 = s1.copy()
        s3.mz_precision = 4
        self.assertRaises(ValueError, s1.__add__, s3)

    def test_addition_with_constant(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 2, 3, 4, 5], mz_precision=2, metadata={"name": "test1"})

        self.assertEquals(s1 + 5.0, Spectrum(mz_values=np.arange(5.0), intensity_values=[6, 7, 8, 9, 10], mz_precision=2, metadata={"name": "test1"}))

    def test_addition_with_vector(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 2, 3, 4, 5], mz_precision=2, metadata={"name": "test1"})
        v1 = np.array([1, 1, 1, 1, 1])
        v2 = [1, 1, 1, 1, 1]

        self.assertEquals(s1 + v1, Spectrum(mz_values=np.arange(5.0), intensity_values=[2, 3, 4, 5, 6], mz_precision=2, metadata={"name": "test1"}))
        self.assertEquals(s1 + v1, s1 + v2)

    def test_subtraction_with_spectrum(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 2, 3, 4, 5], mz_precision=2,
                  metadata={"name": "test1"})
        s2 = Spectrum(mz_values=np.arange(5.0), intensity_values=[0, 1, 0, 1, 0], mz_precision=2,
                      metadata={"name": "test2"})

        self.assertEquals(s1 - s2, Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 1, 3, 3, 5], mz_precision=2,
                                   metadata=[{"name": "test1"}, {"name": "test2"}]))

        s3 = s1.copy()
        s3.mz_precision = 4
        self.assertRaises(ValueError, s1.__sub__, s3)

    def test_subtraction_with_constant(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[5, 6, 7, 8, 9], mz_precision=2,
                  metadata={"name": "test1"})

        self.assertEquals(s1 - 5.0, Spectrum(mz_values=np.arange(5.0), intensity_values=[0, 1, 2, 3, 4], mz_precision=2,
                                  metadata={"name": "test1"}))

    def test_subtraction_with_vector(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[2, 3, 4, 5, 6], mz_precision=2,
                  metadata={"name": "test1"})
        v1 = np.array([1, 1, 1, 1, 1])
        v2 = [1, 1, 1, 1, 1]

        self.assertEquals(s1 - v1, Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 2, 3, 4, 5], mz_precision=2,
                                   metadata={"name": "test1"}))
        self.assertEquals(s1 - v1, s1 - v2)

    def test_multiplication_by_spectrum(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 2, 3, 4, 5], mz_precision=2,
                  metadata={"name": "test1"})
        s2 = Spectrum(mz_values=np.arange(5.0), intensity_values=[0, 1, 0, 1, 0], mz_precision=2,
                      metadata={"name": "test2"})

        self.assertEquals(s1 * s2, Spectrum(mz_values=np.arange(5.0), intensity_values=[0, 2, 0, 4, 0], mz_precision=2,
                                   metadata=[{"name": "test1"}, {"name": "test2"}]))

        s3 = s1.copy()
        s3.mz_precision = 4
        self.assertRaises(ValueError, s1.__mul__, s3)

    def test_multiplication_by_scalar(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[5, 6, 7, 8, 9], mz_precision=2,
                  metadata={"name": "test1"})

        self.assertEquals(s1 * 2.0, Spectrum(mz_values=np.arange(5.0), intensity_values=[10.0, 12.0, 14.0, 16.0, 18.0], mz_precision=2,
                                  metadata={"name": "test1"}))

    def test_multiplication_by_vector(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[2, 3, 4, 5, 6], mz_precision=2,
                  metadata={"name": "test1"})
        v1 = np.array([2, 2, 2, 2, 2])
        v2 = [2, 2, 2, 2, 2]

        self.assertEquals(s1 * v1, Spectrum(mz_values=np.arange(5.0), intensity_values=[4, 6, 8, 10, 12], mz_precision=2,
                                   metadata={"name": "test1"}))
        self.assertEquals(s1 * v1, s1 * v2)

    def test_division_by_spectrum(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 2, 1, 2, 1], mz_precision=2,
                  metadata={"name": "test1"})
        s2 = Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 2, 1, 2, 1], mz_precision=2,
                      metadata={"name": "test2"})

        self.assertEquals(s1/s2, Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 1, 1, 1, 1], mz_precision=2,
                                   metadata=[{"name": "test1"}, {"name": "test2"}]))

        s3 = s1.copy()
        s3.mz_precision = 4
        self.assertRaises(ValueError, s1.__div__, s3)

    def test_division_by_scalar(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[5, 6, 7, 8, 9], mz_precision=2,
                  metadata={"name": "test1"})
        self.assertEquals(s1/2.0, Spectrum(mz_values=np.arange(5.0), intensity_values=[2.5, 3.0, 3.5, 4.0, 4.5], mz_precision=2,
                                  metadata={"name": "test1"}))

    def test_division_by_vector(self):
        s1 = Spectrum(mz_values=np.arange(5.0), intensity_values=[2, 3, 4, 5, 6], mz_precision=2,
                  metadata={"name": "test1"})
        v1 = np.array([2, 2, 2, 2, 2])
        v2 = [2, 2, 2, 2, 2]

        self.assertEquals(s1/v1, Spectrum(mz_values=np.arange(5.0), intensity_values=[1, 1.5, 2.0, 2.5, 3.0], mz_precision=2,
                                   metadata={"name": "test1"}))
        self.assertEquals(s1/v1, s1/v2)