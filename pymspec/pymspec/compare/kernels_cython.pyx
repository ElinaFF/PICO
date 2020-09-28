__author__ = 'Alexandre'

import cython
import numpy as np
cimport numpy as np

np.import_array()

float_type = np.float64
ctypedef np.float64_t FLOAT_t

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef __xcorr__(x, y, FLOAT_t shift_span):
    cdef FLOAT_t alpha = __spectral_dot__(x.mz_values(), x.intensity_values(), y.mz_values(), y.intensity_values())
    cdef FLOAT_t beta = 0.0

    cdef np.ndarray[FLOAT_t, ndim=1] x_mz = x.mz_values()
    cdef np.ndarray[FLOAT_t, ndim=1] x_int = x.intensity_values()
    cdef np.ndarray[FLOAT_t, ndim=1] y_mz = y.mz_values()
    cdef np.ndarray[FLOAT_t, ndim=1] y_int = y.intensity_values()

    cdef FLOAT_t t
    for t in np.arange(-1*shift_span, shift_span, 1.0, dtype=float_type):
        beta += __spectral_dot__(x_mz+t, x_int, y_mz, y_int)

    return alpha - (beta/(2*shift_span) if shift_span else 0.0)

#@cython.boundscheck(False)
#cpdef __xcorr__(x, y, int shift_span):
#    cdef float alpha = 0.0
#    cdef np.ndarray[FLOAT_t, ndim=1] beta = np.zeros(shift_span*2)
#    cdef int i
#    cdef int t
#    cdef float mz
#    cdef float dot
#    cdef np.ndarray[FLOAT_t, ndim=1] x_mz_values = np.asarray(x.mz_values())
#    cdef np.ndarray[FLOAT_t, ndim=1] y_mz_values = np.asarray(y.mz_values())
#    cdef np.ndarray[FLOAT_t, ndim=1] common_mz
#
#    for i in xrange(shift_span*2):
#        t = i - shift_span
#
#        common_mz = np.intersect1d(x_mz_values, y_mz_values+t)
#
#        dot = 0.0
#        for mz in common_mz:
#            dot += x.intensity_at(mz) * y.intensity_at(mz-t)
#
#        beta[i] = dot
#
#        if t == 0:
#            alpha = dot
#
#    return alpha - np.mean(beta)

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef FLOAT_t __spectral_dot__(np.ndarray[FLOAT_t, ndim=1] x_mz, np.ndarray[FLOAT_t, ndim=1] x_int, np.ndarray[FLOAT_t, ndim=1] y_mz, np.ndarray[FLOAT_t, ndim=1] y_int):
    cdef float dot = 0.0
    cdef int i = 0
    cdef int j = 0
    while i < x_mz.shape[0] and j < y_mz.shape[0]:
        if x_mz[i] < y_mz[j]:
            i+=1
        elif x_mz[i] > y_mz[j]:
            j+=1
        else:
            dot += x_int[i]*y_int[j]
            i+=1
            j+= 1

    return dot

#cpdef __spectral_dot__(x, y):
#    # Observation: Ca sert a rien de considerer des m/z
#    # pour lesquels les deux spectres n'ont pas de peak,
#    # puisque le produit sera nul a cette position.
#    mz_values = set(x.mz_values())
#    mz_values.intersection_update(y.mz_values())
#
#    cdef float dot = 0.0
#    cdef float mz
#    for mz in mz_values:
#        dot += x.intensity_at(mz) * y.intensity_at(mz)
#
#    return dot