import cdms2
import numpy
import diagnosisutils.plot as plots
import por_template_2x2_portrait as por_2x2

x=por_2x2.x

#####----WIND-----####
f_U_wind_name='/NCMRWF/Process_Files/T254/Anomaly/2010/Month/ugrdprs_T254_2010_mean_anomaly.nc'
f_V_wind_name='/NCMRWF/Process_Files/T254/Anomaly/2010/Month/vgrdprs_T254_2010_mean_anomaly.nc'
f_U=cdms2.open(f_U_wind_name)
f_V=cdms2.open(f_V_wind_name)
U=f_U('ugrdprs', time= '2010-6-1',level = 850, latitude =(0,40), longitude = (60,100))
U= U[::10, ::10]
print U.shape
V=f_V('vgrdprs', time= '2010-6-1',level = 850, latitude =(0,40), longitude = (60,100))
V= V[::10, ::10]
print V.shape
title_wind = 'T254 WIND ANOMALY 850hPa JUNE 2010'
genvector = plots.genVector(40, 1)

###----ISO LINE(HUMIDITY MEAN ANALYSIS)----####

f_mean_hum_anl = cdms2.open('/NCMRWF/Process_Files/T254/Mean/2010/Season/jjas/Analysis/rhprs_T254_2010_jjas_mean_analysis.nc')

hum = f_mean_hum_anl('rhprs', level=850, latitude =(0,40), longitude = (60,100))
hum_array = numpy.array(hum)
hum_mx=int(numpy.amax(hum_array))
hum_mn=int(numpy.amin(hum_array))

diff= (hum_mx-hum_mn)/14
hum_level=range(hum_mn, hum_mx, diff)
# setting isoline
isolinetemp = x.createisoline('genIsoLine', 'ASD')
isolinetemp.line = ['solid']
isolinetemp.linewidths = [1.0]
isolinetemp.label = 'y'
isoColors = [250, 244, 25, 246, 255, 253, 251, 252, 254, 166, 248, 249, 210, 239]
isolinetemp.levels = hum_level
isolinetemp.linecolors = isoColors
title_hum= 'T254 M.A 850 hPa HUMIDITY JJAS 2010'

###---ISO LINE +FILL ----###
f=cdms2.open('/NCMRWF/all_xml/all_fcst_24hr_ctl.xml')
V=f('vgrdtrp', time='2010-6-6', level=850,latitude =(0,40), longitude = (60,100) )
U=f('ugrdtrp', time='2010-6-6', level=850, latitude =(0,40), longitude = (60,100))
# Calculating the wind speed (m/s)
R=(V**2 + U**2)**0.5
# Mean Sea Level Pressure
MSLP=f('prmslmsl', time='2010-6-6', latitude =(0,40), longitude = (60,100))#, level=850)
# Setiing the isoline level dynamicaly
msl=numpy.array(MSLP)
mx_msl=int(numpy.amax(msl))
mn_msl=int(numpy.amin(msl))

dif=(mx_msl-mn_msl)/15

level_isoline=range(mn_msl, mx_msl, 500)

# Title of plot
title_ECMWF='MSLP, WIND SPEED at 850 hPa'
# setting isoline
isoline_new=x.createisoline('genIsoLine_new', 'ASD')
isoline_new.line = ['solid']
isoline_new.linewidths = [1.0]
isoline_new.label = 'y'

colorlist=[1]#(0, 6,  16, 30, 158, 197, 216, 241,242, 243,246,250,248,249)
levels=level_isoline
if levels:
    # setting isoline levels if user passed
    isoline_new.levels = levels
if colorlist:
    # setting isoline colors if user passed
    isoline_new.linecolors = colorlist
# saving the 'genIsoLine' into temporary python memory

# make isotypelevels for checking purpose, i.e. check the already created
# template levels and user passed levels are same or not
isotypelevels = [[lev, 0] for lev in levels]

#Isofill setting
iso=x.getisofill('default')

new_temp = por_2x2.leftOfBot_prt
new_temp.legend.priority = 1
new_temp.legend.y1=0.03
new_temp.legend.x1=0.07
new_temp.legend.y2=0.04
new_temp.legend.x2=0.48

for k in range(3):
    if (k==0):
        # plotting wind vector
        x.plot(U, V,  por_2x2.leftOfTop_prt, genvector, title=title_wind,  continents=1, bg=0)

    elif (k == 1):
        # plotting iso line
        x.plot(hum, por_2x2.rightOfTop_prt, isolinetemp, title=title_hum, continents=1, bg = 0)
    
    elif (k==2):
        # plotting iso fill line
        x.plot(R, new_temp, iso,title=title_ECMWF, continents=1, bg=0)
        x.plot(MSLP, new_temp, isoline_new, title='')

x.png('/home/arulalan/Desktop/demo/CMA_2010_obs.png')
