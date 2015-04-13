                                 #def harmonic_ts(climatology_data, no_harmonic, time):
import cdms2

cdms2.setNetcdfShuffleFlag(0)
cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)



def harmonic(climatology_data, no_harmonic, time_type):
    """ 
    Earth science data consists of a strong seasonality component as indicated by the
    cycles of repeated patterns in climate variables such as air pressure, temperature 
    and precipitation. The seasonality forms the strongest signals in this data and in 
    order to find other patterns, the seasonality is removed by subtracting the monthly 
    mean values of the raw data for each month. However since the raw data like air 
    temperature, pressure, etc. are constantly being generated with the help of satell-
    ite observations, the climate scientists usually use a moving reference base interval 
    of some years of raw data to calculate the mean in order to generate the anomaly time
    series and study the changes with respect to that. 
    
    Fourier series analysis decomposes a signal into an infinite series of harmonic compon-
    ents. Each of these components is comprised initially of a sine wave and a cosine wave 
    of equal integer frequency. These two waves are then combined into a single cosine wave,
    which has characteristic amplitude (size of the wave) and phase angle (offset of the wave). 
    Convergence has been established for bounded piecewise continuous functions on a closed 
    interval, with special conditions at points of discontinuity. Its convergence has been 
    established for other conditions as well, but these are not relevant to the analysis at
    hand.
    
    Reference: Daniel S Wilks,  'Statistical Methods in the Atmospheric Sciences' second Edition, page no(372-378)
    
    """
    
    import numpy, math
    if (time_type == 'year'):
        n = 365.0
    elif (time_type == 'month'):
        n = 12.0
    elif (time_type == 'daily'):
        n = 365.0
    elif (time_type == 'full'):
        n = len(climatology_data.getTime())
        n= float(n)
        P = n
    a, b, c = climatology_data.shape
    lat = climatology_data.getLatitude()
    lon = climatology_data.getLongitude()
    tim = climatology_data.getTime()
    sum_harmonic = numpy.zeros((a, b, c), dtype = numpy.float)
    sum_harmonic = cdms2.createVariable(sum_harmonic)
    sum_harmonic.setAxisList([tim, lat, lon])
    for la in xrange(len(lat)):            
        for lo in xrange(len(lon)):   

            t = numpy.arange(1, n+1)#numpy.arange(0, n)
            K_new = numpy.arange(1, (n/2.0)+1)
    #        cos = numpy.cos((2*math.pi*K_new*n)/P)#numpy.cos((2*math.pi*k*t)/n)
    #        sin = numpy.sin((2*math.pi*K_new*n)/P)#numpy.sin((2*math.pi*k*t)/n)
            
            dummy = numpy.zeros((a, b, c), dtype = numpy.float)
            dummy1 = numpy.zeros((a, b, c), dtype = numpy.float)
            Kth_harmonic = numpy.zeros((a, b, c), dtype = numpy.float)
            Ak = numpy.zeros((b, c), dtype = numpy.float)
            Bk = numpy.zeros((b, c), dtype = numpy.float)
            Ck = numpy.zeros((b, c), dtype = numpy.float)
            Qk = numpy.zeros((b, c), dtype = numpy.float)
            data_mean = numpy.zeros((b, c), dtype = numpy.float)       
            for k in range(1, no_harmonic + 1):
                data = climatology_data(lataitude =lat[la], longitude= lon[lo])
                data = data(squeeze = 1)
                data_mean[la, lo] = data.mean()
                Bk_elem = data*cos*(2/n)
                
                Bk_elem = data*sin*(2/n)
                dummy[:, la, lo] = Ak_elem
                dummy1[:, la, lo] = Bk_elem
                Ak[la, lo] = Ak_elem.sum()
                Bk[la, lo] = Bk_elem.sum()
                if (Ak[la, lo] > 0):
                    Qk_elm = math.atan(Bk[la, lo]/Ak[la, lo])
                elif (Ak[la, lo] < 0):
                    if (math.atan(Bk[la, lo]/Ak[la, lo]) - math.pi)<0:
                        Qk_elm = math.atan(Bk[la, lo]/Ak[la, lo]) + math.pi
                    elif (math.atan(Bk[la, lo]/Ak[la, lo]) - math.pi)>0:
                        Qk_elm = math.atan(Bk[la, lo]/Ak[la, lo])-math.pi
                elif (Ak[la, lo] == 0):
                    Qk_elm = (math.pi)/2.0
                Qk[la, lo] = Qk_elm
                t_k = (P/360*k)*(180/math.pi)*Qk[la, lo]+float(P/k)
                Ck[la, lo] = ((Ak[la, lo]**2) + (Bk[la, lo]**2))**(0.5)
                K_harmonic = Ck[la, lo]*numpy.cos((2*math.pi*n*(t-t_k)/2*P))
                
                Kth_harmonic[:, la, lo] = K_harmonic
        del dummy, dummy1, Ak, Bk, Ck 
               
        Kth_harmonic = cdms2.createVariable(Kth_harmonic)
        i_d = 'harmonic_%d' %(k)
        Kth_harmonic.id = i_d
        
        Kth_harmonic.setAxisList([tim, lat, lon])
        i_d_new= 'GPCP'+i_d+'.nc'
        h=cdms2.open(i_d_new, 'w')
        h.write(Kth_harmonic)
        h.close()
        sum_harmonic = Kth_harmonic + sum_harmonic
    sum_harmonic = sum_harmonic + data_mean
    return sum_harmonic
    
#f=cdms2.open('/home/dileep/WORK/Research_wind/EEOF_experiments/Harmonic/HARMONIC_GPCP_FULL_ROW_Data_for_selected_region/gpcp_1dd_v1.2_p1d_selected_region_10._25.5N_70.5_85.5E.nc')

f = cdms2.open('/media/dileep/B62675902675527B/GPCP_Rainfall/GPCP_precipitaion_climatology_using_1997_2008.nc')

#('/media/dileep/B62675902675527B/GPCP_Rainfall/Daily_Precipitation/gpcp_1dd_v1.2_p1d.xml')
#('/media/dileep/B62675902675527B/GPCP_Rainfall/GPCP_precipitaion_climatology_using_1997_2008_with_weight_option_equal.nc')
#
#('/home/dileep/mnt/Obs/NCEP-NCAR_Reanalysis/air.surface.mon.mean_NCEP_NCAR_Climatology_1948-1-1_2011-3-1.nc')
#('air-----> '/home/dileep/mnt/Obs/NCEP-NCAR_Reanalysis/air.surface.mon.mean_NCEP_NCAR_Climatology_1948-1-1_2011-3-1.nc')
#
#'precip'----> ('/home/dileep/WORK/Research_wind/EEOF_experiments/GPCP_Rainfall/GPCP_Daily_rainfal_climatology_using_1997_to_2008.nc')
#
time_type = 'full'#'year'
no_harmonic = 3
climatology_data = f('precip', time = ('1997-1-1', '2008-12-31'), latitude=(10.5, 25.5, 'ccb'), longitude=(70.5, 85.5, 'ccb'))
#latitude=(-12.5, 30.5, 'ccb'), longitude=(60.5, 95.5, 'ccb'))
sum_harmonic = harmonic(climatology_data, no_harmonic, time_type)
sum_harmonic.id = 'mean_and_first_%d_harmonic_of_row_data_full' %(no_harmonic)
#g=cdms2.open('/home/dileep/WORK/Research_wind/EEOF_experiments/Harmonic/GPCP_HARMONIC_JJAS_full_row_data_selected_region_10._25.5N_70.5_85.5E.nc', 'w')
g=cdms2.open('dileep_gpcp_1dd_v1.2_p1d_10.5N_25.5N_70.5E_85.5E_sum_of_mean_and_first_3_harmonics.nc', 'w')
#('/media/dileep/B62675902675527B/NCEN_reanalysis_air_clim_sum_harmonic_of_mean_and_first_3.nc', 'w')
g.write(sum_harmonic)
g.close()

##        #(condition-I: If Ak_elm > 0, then Phase 'Qk_elm' calculated as )
##        Pos_Ak = numpy.ma.masked_where(Ak_elem <0, Ak_elem)
##        Qk_elm = numpy.arctan(Bk_elem/Pos_Ak)
##        #(condition-II: If Ak_elm < 0, then Phase 'Qk_elm' calculated as )
##        Neg_Ak = numpy.ma.masked_where(Ak_elem >0, Ak_elem)
##        Qk_elm_neg_cond = numpy.arctan(Bk_elem/Neg_Ak)
##        Qk_elm_neg_cond_I = Qk_elm_neg_cond + math.pi
##        Qk_elm_neg_cond_I = numpy.ma.masked_where(Qk_elm_neg_cond_I > 2*math.pi, Qk_elm_neg_cond_I)
##        Qk_elm_neg_cond_II = Qk_elm_neg_cond - math.pi
##        Qk_elm_neg_cond_II = numpy.ma.masked_where(Qk_elm_neg_cond_II <0, Qk_elm_neg_cond_II)
##        #(Condition III: If Ak_elem =0) 
##        Zero_Ak = numpy.ma.masked_where(Ak_elem != 0, Ak_elem)
##        Qk_elm_zero = Zero_Ak+(math.pi)*(0.5)
