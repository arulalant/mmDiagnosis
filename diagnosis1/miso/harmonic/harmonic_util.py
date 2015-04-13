import cdms2, numpy, math, MV2, cdutil


def harmonic(data, k=3, time_type='daily', phase_shift=15):
    """     
    Inputs : 
        data : climatology data 
        k : Integer no to compute K th harmonic. By default it takes 3.
        time_type : daily | monthly | full (time type of input climatology)
                    'daily' -> it returns 365 days harmonic,
                    'monthly' -> it returns 12 month harmonic,
                    'full' -> it retuns harmonic for full length of 
                    input data. 
                    
        phase_shift : Used to subtract 'phase_shift' days lag to adjust
                      phase_angle w.r.t daily or monthly. By default it takes
                      15 days lag to adjust phase_angle w.r.t daily data.
                      User can pass None disable this option.
    
    Returns :
        Returns "sum mean of mean and first K th harmonic" of input 
        climatology data. 
    
    Concept :
    
    Earth science data consists of a strong seasonality component as 
    indicated by the cycles of repeated patterns in climate variables such 
    as air pressure, temperature and precipitation. The seasonality forms 
    the strongest signals in this data and in order to find other patterns,
    the seasonality is removed by subtracting the monthly mean values of the
    raw data for each month. However since the raw data like air temperature,
    pressure, etc. are constantly being generated with the help of satellite
    observations, the climate scientists usually use a moving reference base 
    interval of some years of raw data to calculate the mean in order to 
    generate the anomaly time series and study the changes with respect to
    that. 
    
    Fourier series analysis decomposes a signal into an infinite series of 
    harmonic components. Each of these components is comprised initially of 
    a sine wave and a cosine wave of equal integer frequency. These two waves
    are then combined into a single cosine wave, which has characteristic 
    amplitude (size of the wave) and phase angle (offset of the wave). 
    Convergence has been established for bounded piecewise continuous 
    functions on a closed interval, with special conditions at points of
    discontinuity. Its convergence has been established for other conditions
    as well, but these are not relevant to the analysis at hand.
    
    Reference: Daniel S Wilks, 'Statistical Methods in the Atmospheric 
               Sciences' second Edition, page no(372-378).
               
    Written By : Arulalan.T
    
    Date : 16.05.2014
    
    """
    
    data = data.reorder('t...')
    cdutil.setAxisTimeBoundsDaily(data.getTime())
    axislist = data.getAxisList()
    timeAxis = axislist[0]
    dataid = data.id     
    
    if time_type in ['daily']:
        N = 365.0   # must be float 
    elif time_type[:3] in ['mon']:
        N = 12.0    # must be float 
    elif time_type in ['full']:
        N = float(len(timeAxis))
        
    if k > N/2:
        raise ValueError("k value should not exceed (%d) i.e. N/2 value" % (N/2))
    
    if len(timeAxis) > 366:
        print 'found more than 1 year data.'
        raise ValueError("Kindly pass only climatology data")
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
        
        if phase_shift:
            # subtract 15 days lag to adjust phase_angle w.r.t daily
            phase_angle -= (phase_shift *2 * math.pi) / N
        # end of if daily and not monthly:

        phase_angle = numpy.array(phase_angle)
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
# end of def harmonic(cdata, k=3, time_type='daily', phase_shift=15):        
        
