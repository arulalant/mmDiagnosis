import cdms2, numpy, math, MV2, cdutil
#from climatology_utils import dailyClimatology


def harmonic(data, k=3):
    
    data = data.reorder('t...')
    cdutil.setAxisTimeBoundsDaily(data.getTime())
    axislist = data.getAxisList()
    dataid = data.id 
    
    daily = True 
    monthly = False
    
    timeAxis = axislist[0]
    N = 365. #len(timeAxis)
#    P = 10. # 10 year, yearly harmonic oscilation
#    P = 10*12 # 10 year, monthly harmonic oscilation
#    P = 10*365 # 10 year, daily harmonic oscilation 
#    if P > N:
#        raise ValueError("P('%d') value should not exceed N(%d)" % (P,N))
        
    if k > N/2:
        raise ValueError("k value should not exceed (%d) i.e. N/2 value" % (N/2))
    
    if len(timeAxis) > 366:
        print 'found more than 1 year data.'
#        y_t = dailyClimatology(data, action='sum')
    else:
        y_t = data 
    # end of if len(timeAxis) > 366:
    
    Y_0 = cdutil.averager(data, axis='t', action='average', weights='equal')

    # make memory free
    del data 
        
    t = numpy.arange(1, N+1, dtype='float')
    
    otheraxis = list(Y_0.shape)
    ax_product = 1
    for ax in otheraxis:
        ax_product *= ax
    otheraxis.insert(0,N)
    t = t.repeat(ax_product).reshape(otheraxis)    
    angle = 2 * math.pi * t/N
    Y_k = 0.
    
    for i in range(1,k+1):
    
        kangle = angle*i
       
        A_k = (2./N) * cdutil.averager(y_t * numpy.cos(kangle), axis='t', action='sum')
        B_k = (2./N) * cdutil.averager(y_t * numpy.sin(kangle), axis='t', action='sum')   
        C_k = MV2.sqrt((A_k*A_k) + (B_k*B_k))
        
        # if A_k is positiv, then retain this phase_angle as it is.
        # phase_angle should be in degrees
        phase_angle = phase_arc_angle = MV2.arctan(B_k/A_k) 
        
        # if A_k is zero, then replace phase_angle with pi/2 else retain same
        phase_angle = MV2.where(MV2.equal(A_k, 0.), math.pi/2.0, phase_arc_angle)
               
        # if A_k is negative, then add pi with phase_angle (if it is <= pi ) 
        condition1 = MV2.logical_and(MV2.less(A_k, 0.), MV2.less_equal(phase_arc_angle, math.pi))
        phase_angle = MV2.where(condition1, phase_arc_angle+math.pi, phase_arc_angle)
        # if A_k is negative, then subtract pi from phase_angle (if it is > pi ) 
        condition2 = MV2.logical_and(MV2.less(A_k, 0.), MV2.greater(phase_arc_angle, math.pi)) 
        condition3 = MV2.logical_or(condition1, condition2)
        phase_angle = MV2.where(condition3, phase_arc_angle-math.pi, phase_arc_angle)
    
        # make memory free 
        del phase_arc_angle
        
        if daily and not monthly:
            # subtract 15 days lag to adjust phase_angle w.r.t daily
            print "Daily Subtraction"
            phase_angle -= (15.*2*math.pi)/N
        # end of if daily and not monthly:

        phase_angle = numpy.array(phase_angle)
#        phase_angle = numpy.tile(phase_angle, N).reshape(kangle.shape)         
        kangle = numpy.array(kangle)
        Y_k += C_k * MV2.cos(kangle - phase_angle)
    # end of for i in range(1,k+1):
    
    # add mean to the sum of first k-th harmonic of data 
    Y_k += Y_0
    
    # make memory free
    del y_t, Y_0
    
    sumOfMean_and_first_k_harmonic = cdms2.createVariable(Y_k, id=dataid)
    sumOfMean_and_first_k_harmonic.setAxisList(axislist)
    sumOfMean_and_first_k_harmonic.comments = 'sumOfMean_and_first_%d_harmonic' % k
    
    # make memory free
    del Y_k
    
    # return result
    return sumOfMean_and_first_k_harmonic
# end of def harmonic(data, k=3):
        



cdms2.setNetcdfShuffleFlag(0)
cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)

        
        
f = cdms2.open('/media/dileep/B62675902675527B/GPCP_Rainfall/GPCP_precipitaion_climatology_using_1997_2008.nc')
#data = f('precip',latitude=(10.5), longitude=(76.5),squeeze=1)
data = f('precip')#,latitude=(10.5,12.5), longitude=(76.5,77.5)) 
#, time=('1997-10-1', '1997-10-20'), longitude=(71,85))
hclim = harmonic(data)

hclim = hclim(latitude=(10.5,25.5,'ccb'), longitude=(70.5,85.5,'ccb'))

hclim.comment = 'Climatology - calculated from 1997-1-1 to 2008-12-31 and then applied harmonic analysis over that Climatology. This data contains sum of mean and first three harmonics over Climatology'

g=cdms2.open('ToSuhasgpcp_1dd_v1.2_p1d_10.5N_25.5N_70.5E_85.5E_sum_of_mean_and_first_3_harmonics.nc', 'w')
g.write(hclim)
g.close()

d1= data(latitude=10.5, longitude=76.5,squeeze=1)
h1= hclim(latitude=10.5, longitude=76.5,squeeze=1)
import vcs
v=vcs.init()
v.plot(h1)
v.plot(d1)

   
        
        
        
        
        
        
