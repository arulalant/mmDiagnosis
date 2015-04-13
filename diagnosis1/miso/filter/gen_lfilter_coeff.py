import numpy 
from pyclimate.LanczosFilter import LanczosFilter


### The filter weights n returns (2n+1) length weights.
l = LanczosFilter(filtertype='bp', fc1=(1.0/90.0), fc2=(1.0/25.0), n=69)
# get coefficients of 
C = l. getcoefs()
# saving weights ito text
C = numpy.array(C)
# taking only last (n+1) weights. i.e. from half to till end points.
C = C[((len(C))/2):]
# lfilter function takes only n+1 weights (i.e. 70 weights)... 
numpy.savetxt('LanczosFilter_weights_25_90_days.dat', C)
