import cdms2
import vcs
# under the rainfall directory
f=cdms2.open('rainfall.xml')
data = f('pobs')

import numpy.ma as MA
data_lessthan_0 = MA.masked_where(data>=0, data)
data_lessthan_0


data_lessthan_0.setAxis(0, data.getTime())
data_lessthan_0.setAxis(1, data.getLatitude())
data_lessthan_0.setAxis(2, data.getLongitude())

x = vcs.init()                                               
for i in range(0,len(data_lessthan_0)):                      
    x.plot( data_lessthan_0( time=slice(i,i+1) ),continents = 6, bg = 0)
    x.gif('outfile.gif',merge='a')                                     
    x.clear()  

