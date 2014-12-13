import cdms2, cdutil, numpy
cdms2.setNetcdfShuffleFlag(0)
cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)
def _generateBounds(data, samelen=True, cyclic=False):
    """ creating bounds array and return it
    We need to pass the data as list which consists of the bound's weights
    values. Then it should create return bounds as numpy array with
    proper shape.
    
    samelen : If it is True, then it should return bounds with same length 
              of the data. And in the last bound will be repeated if 
              cyclic is False, otherwise first value will be kept at the 
              last index of the bounds (make it as cyclic bound).
                
    example 1:
         boundlist = [0, 1, 2, 3, 4]
         bounds = _generateBounds(boundlist)
         bounds
        array([[ 0.,  1.],
               [ 1.,  2.],
               [ 2.,  3.],
               [ 3.,  4.]])

    example 2:
         boundlist = [0, 30, 58, 89, 119]
         bounds = _generateBounds(boundlist)
         bounds
        array([[   0.,   30.],
               [  30.,   58.],
               [  58.,   89.],
               [  89.,  119.]])

    example 3:
         boundlist = [0, 30, 58, 89, 119]
         bounds = _generateBounds(boundlist, samelen=True)
         bounds
        array([[   0.,   30.],
               [  30.,   58.],
               [  58.,   89.],
               [  89.,  119.],
               [ 119.,  119.]])
   
   example 4:
         boundlist = [0, 30, 58, 89, 119]
         bounds = _generateBounds(boundlist, samelen=True, cyclic=True)
         bounds
        array([[   0.,   30.],
               [  30.,   58.],
               [  58.,   89.],
               [  89.,  119.],
               [ 119.,  0.]])
               
    Written By : Arulalan.T
    
    """
    
    data_length = len(data)
    if not samelen:
        data_length -= 1
    # end of if not samelen:
    bounds = numpy.zeros((data_length, 2))
    for i in range(data_length):
        bounds[i][0] = data[i]        
        if i == data_length-1 and samelen:
            bounds[i][0] = data[i]
            if cyclic:                
                bounds[i][1] = data[0]
            else:
                bounds[i][1] = data[i]
            # end of if cyclic:
        else:
            bounds[i][1] = data[i+ 1]
        # end of if i == data_length-1 and samelen:        
    # end of for i in range(data_length):
    return bounds
# end of def _generateBounds(data):


def _rootcoslat_weights(latdim):
    """Square-root of cosine of latitude weights.

    *latdim*
       Latitude dimension values.

    """
    from math import pi, cos 
    coslat = [ ]
    for la in latdim:
        lat_new=cos(la*pi/180.)
        coslat.append(lat_new)
    return coslat   


f=cdms2.open('/media/dileep/B62675902675527B/GPCP_Rainfall/GPCP_precip_APDRC/V1.2/GPCP_precip_v1.2_1997_2008_HARMONIC_ANOMALY_JJAS.nc')
#('/media/dileep/B62675902675527B/GPCP_Rainfall/GPCP_Daily_rainfal_anomaly_for_jjas_1998_2008_60.5E_95.5E.nc')
#

#'/home/dileep/WORK/Research_wind/EEOF_experiments/Harmonic/JJAS_anomaly_from_climatology_and_first_three_harmonic.nc')


#'/home/dileep/WORK/Research_wind/EEOF_experiments/Harmonic/JJAS_anomaly_from_climatology_plus_mean_and_first_three_harmonic.nc')


#'/home/dileep/WORK/Research_wind/EEOF_experiments/GPCP_Rainfall/GPCP_Daily_rainfal_anomaly_for_jjas_1998_2008_60.5E_95.5E.nc')
#('/home/dileep/WORK/Research_wind/EEOF_experiments/norm_olr.nc')
#
ddof=1
#'/home/dileep/WORK/Research_wind/EEOF_experiments/GPCP_Rainfall/GPCP_Daily_rainfal_FILTERED_anomaly_for_jjas_1998_2008_60.5E_95.5E.nc'

#('/home/dileep/WORK/Research_wind/EEOF_experiments/GPCP_Rainfall/GPCP_Daily_rainfal_anomaly_for_jjas_1998_2008_60.5E_95.5E.nc')

var = 'rain' # 'precip'
data = f(var, longitude=(60.5, 95.5, 'ccb'), latitude=(-12.5, 30.5, 'ccb'))
# latitude=(10.5, 25.5, 'ccb'), longitude=(70.5, 85.5, 'ccb'))
#
data.id = 'precip'

#
#


lat=data.getLatitude()
coslat = _rootcoslat_weights(lat)
for l in range(len(lat)):
        data[:,l] *= coslat[l]

data = cdutil.averager(data, axis='x')#, weight='equal')
data = data(squeeze=1)


lon=data.getLongitude()
time_ax=data.getTime()
data=data.copy()
# Missing Value  we are replacing into 'nan'
missing=1e+20
if missing is not None:
    data[numpy.where(data == missing)]=numpy.NaN
records=data.shape[0]
originalshape=data.shape[1:]
channels = numpy.multiply.reduce(originalshape)
# We have to reshape the data into two dimention 
data = data.reshape([records, channels])
nonMissingIndex = numpy.where(numpy.isnan(data[0])==False)[0]
dataNoMissing = data[:, nonMissingIndex]
#numpy.savetxt('dataNoMissing.txt',dataNoMissing, delimiter=',')


#dic={-4:'-4', -3:'-3', -2:'-2', -1:'-1', 0:'0', 1:'1', 2:'2', 3:'3', 4:'4'}

from embedding import _embed_dimension

#g=cdms2.open('all_eeof_lags_from_harmonic_JJAS.nc', 'a')
lags=[15]
eofscaling = 2
per_explained = []
for i in xrange(len(lags)):
#    lag_ax.append(lag)
#    lag_ax = cdms2.createAxis(lag_ax)
#    lag_ax.id ='lag'
#    tlp = my_template[i]
    window = lags[i]+1###########################
    
    # here plen = lat x lon
    plen = dataNoMissing.shape[1]
    cov_matrix_eeof=_embed_dimension(dataNoMissing, window)
    #numpy.savetxt('cov_matrix_eeof.txt', cov_matrix_eeof, delimiter=',')
    A, Lh, E = numpy.linalg.svd(cov_matrix_eeof, full_matrices=False)
    
    print E.shape
    normfactor = float(records-window+1 - ddof)
    L= Lh*Lh/normfactor
    per_exp = [(L[:(lags[i]+1)]/L.sum())*100, (L[(lags[i]+1):][:(lags[i]+1)]/L.sum())*100]
    per_exp = list(per_exp)
    per_explained.append(per_exp)
    neofs = len(L)
    lag_axis = cdms2.createAxis(range(window))
    lag_axis.id='lag'  #_%s' %str(lags[i])
    lag_axis.setBounds(_generateBounds(lag_axis))    

    paxis =  lat #cdms2.createAxis(range(plen))
#    paxis.id='plen'
#    paxis.setBounds(_generateBounds(paxis))
    lat.setBounds(_generateBounds(lat))

    neeof = cdms2.createAxis(range(1, len(Lh)+1))
    neeof.id='neeof'#_%s' %str(lag)
    neeof.setBounds(_generateBounds(neeof))
    neeof.long_name = 'number of eeofs for lag %s' %str(lags[i])
    
    new_time_axis = time_ax[:-lags[i]]
    new_time_axis = cdms2.createAxis(new_time_axis)
    new_time_axis.units = time_ax.units
    new_time_axis.id = time_ax.id
    
    P = A*Lh
    pct1= P[:, 0]
    pct2= P[:, 1]
    pct1= cdms2.createVariable(pct1, id = 'pct1')
    pct2= cdms2.createVariable(pct2, id = 'pct2')
    pct1.setAxis(0, new_time_axis)
    pct2.setAxis(0, new_time_axis)
    h=cdms2.open('PC-Time-Series-I_and_II_Rainfall_jjas_V1.2.nc', 'a')
    h.write(pct1)
    h.write(pct2)
    h.close()
    
    if eofscaling == 0:
        E = E
    elif eofscaling == 1:
        for k in xrange(neofs):            
            E[k]=E[k]/ numpy.sqrt(L[k])
    elif eofscaling == 2:
        for l in xrange(neofs):            
            E[l]=E[l]* numpy.sqrt(L[l])
   
    eeof1 = E[:,0] # Extracting first column
    eeof1 = numpy.reshape(E[0], (window, len(lat)))
    eeof1 = cdms2.createVariable(eeof1, id = 'eeof1')
    eeof1.setAxisList([lag_axis, lat])
    g=cdms2.open('EEOF1_for_all_LAG_upto_15_rainfal_harmonic_anom_ncl_v1.2.nc', 'w')
    g.write(eeof1)
    g.close()
    
    eeof2 = E[:,1]
    eeof2 = numpy.reshape(E[1], (window, len(lat)))
    eeof2 = cdms2.createVariable(eeof2, id = 'eeof2')
    eeof2.setAxisList([lag_axis, lat])
    h=cdms2.open('EEOF2_for_all_LAG_upto_15_rainfal_harmonic_anom_ncl_v1.2.nc', 'w')
    h.write(eeof2)
    h.close()
    
    
#    var='eeof_%s' %str(lags[i])
#    eeof1=E(neeof=1)(squeeze=1)
#    
#    eeof1=eeof1*(-1)
#    eeof2=E(neeof=2)(squeeze=1)
   


#g=cdms2.open('all_eeof_lags.nc')
#for lag in lags:
#    
#    var='eeof_%s' %str(lag)
#    neeof='neeof_%s' %str(lag)
#    
##    yx.datawc_x1=-12
##    yx.datawc_x2= max(d)
#    
#    print g(var).min(), g(var).max()
#    
#    eeof1=g(var, neeof=1)(squeeze=1)
#    eeof2=g(var, neeof=2)(squeeze=1)
#    yx.datawc_y1= min(eeof1.min(), eeof2.min())
#    yx.datawc_y2= max(eeof1.max(), eeof2.max())
#    eeof1=eeof1*(-1)
#    v.plot(eeof1, yx)
#    yx.line = 'dot' 
#    v.plot(eeof2, yx)
#    out_fnme='%s.pdf' %var
#    v.pdf(out_fnme)
#    yx.line = 'solid'
#    v.clear()
#    

#eof = E #cdms2.createVariable(E)
#x_axis=cdms2.createAxis(range(len(E)/window))
#y_axis=cdms2.createAxis(range(len(E)/window))

### Block D
#eof_D = eof[44:][:, 44:]
##eof_D_1 = eof_D[:, 0]
##eof_D_1 = cdms2.createVariable(eof_D_1)
##eof_D_1.setAxis(0, x_axis)

##eof_D_2 = eof_D[0]
##eof_D_2 = cdms2.createVariable(eof_D_2)
##eof_D_2.setAxis(0, x_axis)
### BLOCK B
#eof_B = eof[:44][:, 44:]

### BLOCk C
#eof_C = eof[44:][:, :44]
##eeof1==E[0, :][44:]

###Block A
#eof_A=eof[:44][:, :44]
#block_string=['A', 'B', 'C', 'D']
#block=[eof_A, eof_B, eof_C, eof_D]
#import vcs
#v=vcs.init()
#for i in xrange(len(block)):
#    block[i] = cdms2.createVariable(block[i])
#    block[i].id = block_string[i]
#    block[i].setAxis(0, x_axis)
#    block[i].setAxis(0, y_axis)
#    column = block[i][:, 0]
#    column.id='%s_column' %block_string[i]
#    plot_name_colum='/home/dileep/WORK/Research_wind/EEOF_experiments/test_plots/%s_column.pdf' %block_string[i]
#    
#    row = block[i][0]
#    row.id = '%s_row' %block_string[i]
#    plot_name_row = '/home/dileep/WORK/Research_wind/EEOF_experiments/test_plots/%s_row.pdf' %block_string[i]    
#    v.plot(column)        
#    v.pdf(plot_name_colum)
#    v.clear()
#    v.plot(row)
#    v.pdf(plot_name_row)
#    v.clear()


#dof=1
#normfactor = float(records - dof)
#L = Lh * Lh / normfactor
#neofs = len(L)
#flatE = numpy.ones([neofs, channels], dtype=data.dtype)*numpy.NaN
#flatE[:, nonMissingIndex] = E
#P = A * Lh
#slicer = slice(0, neofs)
#rval = flatE[slicer].copy()
#eof=rval.reshape((neofs,) + originalshape)

#g=cdms2.open('CDAT_eof_new.nc', 'w')
#eof=cdms2.createVariable(eof)
#eof.id='eof'
#eof=eof(squeeze=1)
#neof=range(1, neofs+1)
#neof=cdms2.createAxis(neof)
#neof.id='neof'
#neof.long_name='number of eofs'
#eof.setAxisList([neof, lat, lon])
#g.write(eof)
#g.close()




#### Testing & Experimenting ###
#xax=numpy.arange(144)
#xax=cdms2.createAxis(xax)
#xax.id='dummy_axis'
#eef1=E[:, 0][:144]
#eef1=cdms2.createVariable(eef1, id='testing_eeof1')
#eef1.setAxis(0, xax)
#import vcs
#v=vcs.init()
#v.plot(eef1)
#v.pdf('eef1_first_44.pdf')
#v.clear()
# t=numpy.reshape(numpy.arange(5*6), (5, 6))
