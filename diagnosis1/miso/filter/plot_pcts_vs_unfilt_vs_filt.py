import cdms2, cdutil, numpy, vcs
years = [2000, 2002, 2005, 2008]


from template_4years_pcts_vs_filt_vs_unfilt import make_template_array

v=vcs.init()
#v.portrait()
v.mode=1


yx=v.createyxvsx('new_','default')    
yx.marker=0

my_template = make_template_array(v, Nrows=2, Ncols=2, xgap=0.01, ygap=-0.1,
 Left_Margin=0.01, Right_Margin=0.03, Top_Margin= 0.28, Bot_Margin=-0.3 )

months = ['JUN', 'JUL', 'AUG', 'SEP', '']

dic_y ={-4:'-4', -3:'-3', -2:'-2', -1:'-1', 0:'0', 1:'1', 2:'2', 3:'3', 4:'4'}

dic_x={0:'JUN', 29:'JUL', 60:'AUG', 91:'SEP', 121:'OCT'}
for i in xrange(4):    
    time_bound_1 = '%s-6-1' %str(years[i])
    time_bound_2 = '%s-9-30' %str(years[i])
    
    f = cdms2.open('/home/dileep/WORK/Research_wind/EEOF_experiments/PC-Time-Series-I_and_II_Rainfall_only_JJAS_for_all_years.nc')
    #('/home/dileep/WORK/Research_wind/EEOF_experiments/pcts_for_lags_15_eeof_10_25N_and_70.5_85.5E.nc')    
    pct1 = f('pct1')#, neeof=1)(squeeze=1)
    pct1 = pct1(time= (time_bound_1, time_bound_2))
    pct1 = (pct1-pct1.mean())/ pct1.std()
    
    dummy_time_axis = range(len(pct1))
    
    
    pct1=numpy.array(pct1)
    pct1=cdms2.createVariable(pct1, id='pct1')
    dummy_time_axis = cdms2.createAxis(dummy_time_axis, id= 't')
    pct1.setAxis(0, dummy_time_axis)
    
#    dic_x ={}
#    date_m = [0, 30, 61, 92, 121]
#    for j in xrange(len(date_m)):
#        print pct1.getTime()[date_m[j]]
#        dic_x[pct1.getTime()[date_m[j]]] = months[j]
    
        
#    print dic_x, pct1.getTime().asComponentTime()
    
    f_filterd = cdms2.open('/media/dileep/B62675902675527B/GPCP_Rainfall/GPCP_Daily_rainfal_FILTERED_anomaly_for_jjas_1998_2008_60.5E_95.5E.nc')
    filt_data = f_filterd('precip', latitude=(10.5, 25.5, 'cob'), longitude=(70.5, 85.5, 'cob'))
    filt_data = cdutil.averager(filt_data, axis='xy')
    filt_data = filt_data(time = (time_bound_1, time_bound_2))(squeeze=1)
    filt_data = (filt_data-filt_data.mean())/filt_data.std()
    
    filt_data = numpy.array(filt_data)
    filt_data = cdms2.createVariable(filt_data, id='filt')
    filt_data.setAxis(0, dummy_time_axis)
    
    f_unfil = cdms2.open('/home/dileep/WORK/Research_wind/EEOF_experiments/To_Suhas/gpcp_1dd_v1.2_p1d_10.5N_25.5N_70.5E_85.5E_anomaly.nc')
    #f_unfil = cdms2.open('/media/dileep/B62675902675527B/GPCP_Rainfall/JJAS_ANOMALY_GPCP_precipitaion_using_1997_2008_with_weight_option_default_in climatology_calculation.nc')
    #('/media/dileep/B62675902675527B/GPCP_Rainfall/GPCP_Daily_rainfal_anomaly_for_jjas_1998_2008_60.5E_95.5E.nc')
    #('/home/dileep/WORK/Research_wind/EEOF_experiments/Harmonic/JJAS_Anomaly_Harmonic.nc')
  
    unfil_data = f_unfil('precip' , latitude=(10.5, 25.5, 'cob'), longitude=(70.5, 85.5, 'cob'))
    unfil_data = cdutil.averager(unfil_data, axis='xy')
    unfil_data = unfil_data(time = (time_bound_1, time_bound_2))(squeeze=1)
    unfil_data = (unfil_data-unfil_data.mean())/unfil_data.std()    
    
    unfil_data = numpy.array(unfil_data)
    unfil_data = cdms2.createVariable(unfil_data, id='unfil')
    unfil_data.setAxis(0, dummy_time_axis)
    
    
    d = dic_x.keys()
    
    print min(d), max(d)
    yx.datawc_x1= min(d)
    yx.datawc_x2= max(d)
    yx.datawc_y1= -4
    yx.datawc_y2= 4
    yx.xticlabels1 = dic_x
    yx.yticlabels1 = dic_y
    
    tlp=my_template[i]
    if (i==0):
        titl='PC1 of EEOF Analysis Compared with Filtered and Unfiltered Rainfall Anomalies'
        #Averaged over the ISM Domain (10.5N-25.5N, 70.5E-85.5E) for Four Different JJAS Seasons'
    else:
        titl = ' '
        
    yx.linecolor ='red'
    yx.line = 'dot' 
    yx.linewidth=4
    v.plot(pct1,  yx, tlp, title=titl, comment1 = str(years[i]))
    yx.linecolor ='blue'
    yx.line = 'dot'
    tlp.xlabel1.priority=0
    v.plot(filt_data, tlp, yx)
    yx.linecolor =1
    yx.line = 'solid'
    yx.linewidth=2
    v.plot(unfil_data, tlp, yx)
    
    
ln1 = v.createline('new__1')
ln1.width = 4 
ln1.type = 'dot' 
ln1.color=242
ln1.x = [0.24, 0.30]       # x line positions
ln1.y = [0.05, 0.05]

ln2 = v.createline('new__2')
ln2.width = 4 
ln2.type = 'dot' 
ln2.color=244
ln2.x=[0.42, 0.48] 
ln2.y = [0.05, 0.05]

ln3 = v.createline('new__3')
ln3.width = 2 
ln3.type = 'solid' 
ln3.color=1
ln3.x=[0.60, 0.66] 
ln3.y = [0.05, 0.05]
v.plot(ln1)
v.plot(ln2)
v.plot(ln3)
text_legend = v.createtext('text_legend')
text_legend.x=[0.31, 0.49, 0.67]
text_legend.y=[0.05, 0.05, 0.05]
text_legend.string=['PC1 of EEOF', '25-90 Day', 'Anomaly']#'SSI2: Southerly Shear'
text_legend.color=1
text_legend.height = 15
text_legend.font=1
v.plot(text_legend)
    
#v.pdf('PCTS1_of_EEOF_filterd_unfilted_with_default_weight_option_in_climatology.pdf') 
v.pdf('/home/dileep/WORK/Research_wind/EEOF_experiments/To_Suhas/PCTS1_of_EEOF_filterd_unfilted_harmonic_climatology.pdf')     
