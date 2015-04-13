#Reading Lat_Long file
#[ Actually this file contain two column only one is Lattitude(for X-axs) and
#other is Longitude( for Y-axis)

import numpy
# Reading the data file
lat_long = numpy.loadtxt("SAMPLE_COUPLEDATA.txt", dtype=float, comments='#',
    delimiter=None, converters=None, skiprows=1, usecols=None, unpack=False)
import math
import numpy as np
from numpy import matrix
#taking the first column
lat = lat_long[..., 0]
#taking the different element of first column only
lat= numpy.unique(lat)
# taking 2nd column
lon= lat_long[..., 1]
lon= numpy.unique(lon)
#############################################################################

def distance(x, y):
    """
    We are going to find the shortest distance. If  a paticular lat long
    location is given (say (x, y) ), then we are going to find the point
    nearest among the     set of lat-long location and find the distance
    between the that point to (x, y). Distance we measure in kilo meter.
    """
# h will give the nearest point to x
    h=lat[abs(x-lat).argsort()[0]]
# k will give the nearest point to y
    k=lon[(abs(y-lon)).argsort()[0]]

# d arc the shortest distance.
    xh=(x-h)*(math.pi/180)
    xr= x*(math.pi/180)
    yr= y*(math.pi/180)
    yk= (y-k)*(math.pi/180)
# r is the radious of earth in 'km' (approximate value from the web url--
# http://www.universetoday.com/26629/radius-of-the-earth/)
    r=6371
# We are actually calculating the arc length. 'ca' gives the angle difference
    ca= 2*np.arcsin(((math.sin(xh/2))**2)+(math.cos(xr))*(math.cos(yr))*
                                                  ((math.sin(yk/2))**2))**0.5
# d is the arc length
    d= ca*r
# Here we are going to find the diagonal length of given grid point. Since,
# we are using spherical  coordinate the diagonal distance are not uniform.

    x1= h*(math.pi/180)
    y1= k*(math.pi/180)
    y2= lon[(abs(y-lon)).argsort()[1]]*(math.pi/180)
    x2= lat[abs(x-lat).argsort()[1]]*(math.pi/180)

    d1 = 2*np.arcsin(((math.sin((x1-x2)/2))**2)+(math.cos(x1))*(math.cos(x2))*
                                              ((math.sin((y1-y2)/2))**2))**0.5
# 'dgn' is the diagonal distance.
    dgn= (d1*r)*0.25

    return numpy.array([d, dgn])
#############################################################################

def interpl(x, y, n):
    """
    Here we interpolate the data using Multiple Linear Regression(MLR)
    The general purpose of multiple linear regression is to seek for the
    linear relationship between a dependent variable and several independent
    variables.

    Methods:
        The least squares estimation of b for the multiple linear
        regression model y = Xb + e is b = (X'.X)-1.X'.y, assuming (X' X) is
        a non-singular matrix. Note that this is equivalent to assuming that
        the column vectors of X are independent.
    Reference:
        [Linear Regression Analysis Theory and Computing Authors:Xin Yan &
        Xiao Gang Su
        Page No: 41-71]
    Input:
        Here x and y are independent , (here lat & long)
        n----is the method for selection .For example if we need '9' point
        surrounding we choose n=3,
    """
    n= int(n)
    h=k=[]
# h & k are nearest 3 lat & long of our given location
    h=[lat[abs(x-lat).argsort()[i]] for i in xrange(n)]
    k=[lon[(abs(y-lon)).argsort()[i]] for i in xrange(n)]
    a=[]
    a=[numpy.argwhere(h[i]==lat_long[..., 0]) for i in xrange(len(h))]

    b=[]
    b=[numpy.argwhere(k[i]==lat_long[..., 1]) for i in xrange(len(k))]
    a= numpy.array(a)
    b=numpy.array(b)
# a & b gives the corresponding index array of points in lat & long column
    a= a.flatten()
    b= b.flatten()
#k denote the index of corresponding lat long of the 9 points
    k=[a[i] for i in xrange(len(a)) for j in xrange(len(b)) if (a[i]==b[j])]

#  HHH gives the data poins corresponding to the surrounding grid poins
    HHH=[]
    HHH=[lat_long[i] for i in xrange(len(k))]
    HHH=numpy.array(HHH)
# A is the matrix of independent variable
    A= HHH[:, 0:2]
    A= matrix(A)
# B is the matrix of dependent variable
    B=matrix(HHH[:, 2:3])

# C denote MLR coeffients
    C=(((A.T*(A)).I)*A.T)*B

    return (x*C[0]+y*C[1])
###########################################################################

def near(x, y):
    """
    Here we choose the nearest grid point data to the given location
    """
    # h will give the nearest point to x

    h=lat[abs(x-lat).argsort()[0]]

# k will give the nearest point to y

    k=lon[(abs(y-lon)).argsort()[0]]
    a=numpy.argwhere(h==lat_long[..., 0])

    b=numpy.argwhere(k==lat_long[..., 1])


    a= a.flatten()
    b= b.flatten()

#k denote the index of nearest point
    k=[a[i] for i in xrange(len(a)) for j in xrange(len(b)) if (a[i]==b[j])]

    return lat_long[k, 2]
#############################################################################

def best(x, y, n):
    n=int(n)
    """
    If the distance of the location from the nearest grid is
    less than one-fourth of the diagonal distance between any two grid points,
    then more importance is given to the nearest grid forecast values
    otherwise the interpolated value is considered
    """
    if (distance(x, y)[0]< distance(x, y)[1]):
        return near(x, y)
    else:
        return interpl(x, y, n)
#############################################################################
