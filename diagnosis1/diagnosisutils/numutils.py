"""
.. module:: numutis.py
   :synopsis: Few simple extension of numpy will be added in this module

.. moduleauthor:: Arulalan.T <arulalant@gmail.com>

"""

import numpy


def nextmax(x, val=None):
    """
    :func:`nextmax`: Returns the max value next to the top max value of the
                     numpy x. If val doesnot passed by user, it returns the
                     second most max value.
    Inputs : x, numpy array
             val, any value. If value passed, then it should return the max
             value of the next to the passed value.

    Usage :

        >>> x = numpy.array([[10, 1], [100, 1000]])
        >>> x
        array([[  10,    1],
               [ 100, 1000]])
        >>> nextmax(x)
        100
            we didnt pass any val, so it should return 2nd max value

        >>> nextmax(x,99)
        10
            we passed 99 as the val. So it should return the next max value
            to the 99 is 10.

        >>> nextmax(x,1000)
        100
            we passed 1000 as the val. So it should return the next max value
            to the 1000 is 100.

        >>> nextmax(x,1)

            we passed 1 as the val. i.e. the least number in the x (or least
            number which is not even present in the x). So there is no next
            max number to 1. It should return None.

        we can find out 3rd most max value by just calling this function two
        times.
        >>> n = nextmax(x)
        >>> nextmax(x, n)
        >>> 10

        10 is the 3rd most number in x.

    Written By : Arulalan.T

    Date : 27.09.2011

    """

    if not val:
        val = x.max()
    nmax = numpy.ma.masked_greater_equal(x, val).max()
    if nmax:
        return nmax
    else:
        return None
# end of def nextmax(x, val=None):


def nextmin(x, val=None):
    """
    :func:`nextmin`: Returns the min value next to the least min value of the
                     numpy x. If val doesnot passed by user, it returns the
                     second lease min value.
    Inputs : x, numpy array
             val, any value. If value passed, then it should return the min
             value of the next to the passed value.

    Usage :

        >>> x = numpy.array([[10, 1], [100, 1000]])
        >>> x
        array([[  10,    1],
               [ 100, 1000]])
        >>> nextmin(x)
        10
            we didnt pass any val, so it should return 2nd min value

        >>> nextmin(x, 11)
        100

            we passed 11 as the val. So it should return the next min value
            to the 11 is 100.

        >>> nextmin(x, 101)
        1000

            we passed 101 as the val. So it should return the next min value
            to the 101 is 1000.

        >>> nextmin(x, 1000)

            we passed 1000 as the val. i.e. the most number in the x (or most
            number which is not even present in the x). So there is no next
            min number to 1000. It should return None.

        we can find out 3rd least min value by just calling this function two
        times.
        >>> n = nextmin(x)
        >>> nextmin(x, n)
        >>> 100

        100 is the 3rd least number in x.

    Written By : Arulalan.T

    Date : 27.09.2011

    """

    if not val:
        val = x.min()
    nmin = numpy.ma.masked_less_equal(x, val).min()
    if nmin:
        return nmin
    else:
        return None
# end of def nextmin(x, val=None):


def permanent(data):
    """
    permanent: Square Matrix permanent

    It would be numpy data or list data.

    Matrix permanent is just same as determinant of the matrix but change -ve
    sign into +ve sign through out its calculation of determinant.

    eg 1:
        >>> a = numpy.ones(9).reshape((3,3))
        >>> z = permanent(a)
        >>> print z
        >>> 6.0

    eg 2:
        >>> a = numpy.ones(16).reshape((4,4))
        >>> z = permanent(a)
        >>> print z
        >>> 24.0

    Written By : Arulalan.T

    Date : 01.08.2012

    """
    # initialize the local variables everytime when the function call by
    # itself.

    # initialize the result variable & row index as zero.
    res = 0
    rowIdx = 0
    data = numpy.array(data)
    dshape = data.shape
    if dshape[0] != dshape[1]:
        print "The data shape, ", dshape
        raise ValueError("The passed data is not square matrix")

    for colIdx in range(dshape[1]):
        # loop through the column index of the first row of data

        if dshape == (2, 2):
            # data shape is (2,2). So calculate the 2x2 matrix permanent
            # and return it. (return is import for routine call)
            return (data[0][0] * data[1][1]) + (data[0][1] * data[1][0])
        else:
            # get the value of the data(rowIdx, colIdx)
            rowVal = data[rowIdx][colIdx]
            # matrix shape is higher than the (2,2). So remove the current
            # row and column elements from the data and do calculate the
            # permanent for the rest of the matrix data.

            # multiply with the rowVal and add to the result.
            res += rowVal * permanent(remove_nxm(data, rowIdx, colIdx))
    # end of for colIdx in range(dshape[1]):
    return res
# end of def permanent(data):


def remove_nxm(data, n, m):
    """
    remove_nxm : Remove n-th row and m-th column from the matrix/numpy data.
    zero is the starting index for the row and column.
    To remove first row & column, we need to pass 0 as args.

    eg:
        >>> a = numpy.arange(20).reshape((4,5))
        >>> print a
        >>> [[ 0  1  2  3  4]
             [ 5  6  7  8  9]
             [10 11 12 13 14]
             [15 16 17 18 19]]
        >>> b = remove_nxm(a, 2, 2)
        >>> print b
        >>> [[ 0  1  3  4]
             [ 5  6  8  9]
             [15 16 18 19]]
        >>>
          ..note:: removed 2-nd row and 2-column from the matrix a.

        >>> c = remove_nxm(a, 0, 4)
        >>> print c
        >>> [[ 5,  6,  7,  8],
             [10, 11, 12, 13],
             [15, 16, 17, 18]]
        >>>
         ..note:: removed 0-th row and 4-th column from the matrix a.

    Written By : Arulalan.T

    Date : 01.08.2012

    """

    # vertical split the data w.r.t row (n wise)
    pdata = numpy.vsplit(data, [n, n + 1])

    # remove the n-th row of the data
    if n == 0:
        pdata = pdata[-1]
    elif n > 0:
        if pdata[-1].any():
            # concatenate the splited rowwise data (i.e removed the n-th row)
            pdata = numpy.concatenate((pdata[0], pdata[-1]), axis=0)
        else:
            pdata = pdata[0]
    # end of remove the n-th row of the data

    # horizontal split the data w.r.t column (m wise)
    pdata = numpy.hsplit(numpy.array(pdata), [m, m + 1])

    # remove the m-th column of the data
    if m == 0:
        pdata = pdata[-1]
    elif m > 0:
        if pdata[-1].any():
            # concatenate the splited column wise data
            # (i.e removed the mth column)
            pdata = numpy.concatenate((pdata[0], pdata[-1]), axis=1)
        else:
            pdata = pdata[0]
    # end of # remove the m-th column of the data

    return numpy.array(pdata)
# end of def remove_nxm(data, n, m):
