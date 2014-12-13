import cdms2, numpy, cdutil
from pyclimate.LanczosFilter import LanczosFilter


#from compute_daily_anomaly import genDailyAnomalyFile

#anomaly = genDailyAnomalyFile('olr', '/home/dileep/WORK/Research_wind/EEOF_experiments/Filtering_folder/NCEPolr.day.mean.nc', 'olr', '/home/dileep/WORK/Research_wind/EEOF_experiments/Filtering_folder/NCEP_climatology_olr.day.mean.nc', 4, '/home/dileep/WORK/Research_wind/EEOF_experiments/Filtering_folder/NCEP_anomaly_olr.day.mean.nc', year= (1979, 2009))


from variance_utils import lfilter
f=cdms2.open('/home/dileep/WORK/Research_wind/EEOF_experiments/Filtering_folder/NCEPolr.day.mean.nc')
#('/home/dileep/WORK/Research_wind/EEOF_experiments/Filtering_folder/NCEP_anomaly_olr.day.mean.nc')
#('/home/dileep/WORK/Research_wind/EEOF_experiments/GPCP_Rainfall/GPCP_Daily_rainfal_anomaly_for_jjas_1998_2008_60.5E_95.5E.nc')
data= f('olr', time = ('1979-1-1', '2009-12-31'))
### this filter weights n returns (2n+1) length weights.
l = LanczosFilter(filtertype='bp', fc1=(1.0/90.0), fc2=(1.0/25.0), n=69)
C=l. getcoefs()
# saving weights ito text
C=numpy.array(C)
# taking only last (n+1) weights. i.e. from half to till end points.
C=C[((len(C))/2):]

numpy.savetxt('LanczosFilter_weighs_25_90.txt', C)
# lfilter function takes only n+1 weights..,. Need to update in function itself to pass 2n+1 and/or n+1 weights.
fdata=lfilter(data , C, cyclic=True)
del data
g=cdms2.open('NCEP_filterd_25_to_90_with_139_weights_rowdata_OLR_1979_2009.nc', 'w')
g.write(fdata)
g.close()
del fdata
