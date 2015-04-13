import numpy as np
import numpy.ma as ma
from numpy.lib.stride_tricks import as_strided


def _embed_dimension(array, window):
    """
    Embed a given length window from the leading dimension of an array.

    **Arguments:**

    *array*
        A 2-dimensional (nxm) `numpy.ndarray` or `numpy.ma.MaskedArray`.

    *window*
        An integer specifying the length of the embedding window.

    **Returns:**

        A 2-dimenensional (nx(m*window)) `numpy.ndarray` or
        `numpy.ma.MaskedArray` which is a view on the input *array*.
        
    **Example:**
    
        data = np.arange(4*3).reshape(4, 3)
        >>> data
        array([[ 0,  1,  2],
               [ 3,  4,  5],
               [ 6,  7,  8],
               [ 9, 10, 11]])
               
        >>> _embed_dimension(data, window=2)
        array([[ 0,  1,  2,  3,  4,  5],
               [ 3,  4,  5,  6,  7,  8],
               [ 6,  7,  8,  9, 10, 11]])
               
        >>> _embed_dimension(data, window=3)
        array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8],
               [ 3,  4,  5,  6,  7,  8,  9, 10, 11]])               
        
    Author: Dr Andrew Dawson
    Date: 18-11-2013
    
    """
    if array.ndim != 2:
        raise ValueError('array must have exactly 2 dimensions')
    if window >= array.shape[0]:
        raise ValueError('embedding window must be shorter than the '
                         'first dimension of the array')
    n, m = array.shape
    nwin = n - window + 1
    shape = (nwin, window) + array.shape[1:]

    strides = (array.strides[0], array.strides[0]) + array.strides[1:]
    windowed = as_strided(array, shape=shape, strides=strides)
    if ma.isMaskedArray(array):
        if array.mask is ma.nomask:
            windowed_mask = array.mask            
        else:
            strides = ((array.mask.strides[0], array.mask.strides[0]) +
                       array.mask.strides[1:])
            windowed_mask = as_strided(array.mask, shape=shape,
                                       strides=strides)
        # end of if array.mask is ma.nomask:
        windowed = ma.array(windowed, mask=windowed_mask)   
    # end of if ma.isMaskedArray(array):     
    out_shape = (nwin, window * array.shape[1])
    
    return windowed.reshape(out_shape)
