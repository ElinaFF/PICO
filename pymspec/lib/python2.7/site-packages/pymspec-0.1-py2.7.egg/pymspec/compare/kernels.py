__author__ = 'Alexandre Drouin'

import numpy as np
import pyximport; pyximport.install(setup_args={"include_dirs":np.get_include()},
                  reload_support=True)

from pymspec.compare.kernels_cython import __xcorr__, __spectral_dot__

#TODO: Known issue. Lorsqu'on arrondis pas les mz au plus proche entier, on a parfois des 0 sur la diag, ce qui
#      doit etre au fait que 2.34 peut parfois devenir 2.3400001 en memoire

class LinearKernel():
    def __init__(self, normalize=True):
        self.normalize = normalize

    def __call__(self, X, Y):
        K = np.zeros(shape=(len(X), len(Y)))

        normalize_fast = self.normalize and np.all(X==Y)

        for i in xrange(len(X)):
            for j in xrange(len(Y)):

                K[i,j] = __spectral_dot__(X[i].mz_values(), X[i].intensity_values(), Y[j].mz_values(), Y[j].intensity_values())

                if not normalize_fast and self.normalize:
                    K[i,j] /= (__spectral_dot__(X[i].mz_values(), X[i].intensity_values(), X[i].mz_values(), X[i].intensity_values()) * __spectral_dot__(Y[j].mz_values(), Y[j].intensity_values(), Y[j].mz_values(), Y[j].intensity_values()))**0.5

        if normalize_fast:
            norm = np.sqrt(np.diagonal(K))
            K = ((K/norm).T/norm).T

        return K

class XCorrKernel():
    def __init__(self, shift_span=75, normalize=True):
        self.shift_span = shift_span
        self.normalize = normalize

    def __call__(self, X, Y):
        K = np.zeros(shape=(len(X), len(Y)))

        normalize_fast = self.normalize and np.all(X==Y)

        for i in xrange(len(X)):
            for j in xrange(len(Y)):
                K[i,j] = __xcorr__(X[i], Y[j], self.shift_span)

                if not normalize_fast and self.normalize:
                    K[i,j] /= (__xcorr__(X[i], X[i], self.shift_span) * __xcorr__(Y[j], Y[j], self.shift_span))**0.5

        if normalize_fast:
            norm= np.sqrt(np.diagonal(K))
            K = ((K/norm).T/norm).T

        return K
