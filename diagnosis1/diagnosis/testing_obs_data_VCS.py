'''
Usage:
    This programme is used for checking the observed data is correct or not,
    for that we plot the observed data in vcs, and analyse the plot.

Written by: Dileepkumar R
JRF- IIT DELHI

Date: 03.08.2011;
'''

import cdms2
import cdutil
import numpy
import numpy.ma
import vcs


#Opening the observed rainfall netcdf data file
f_rain=cdms2.open('/home/dileep/z/Model_data/CMA_China/Monsoon_2010/CMA_2010_August_f24.grib.ctl')

# Initialising VCS
v = vcs.init()

#vcs.pause(10)
print v.show('template')
print v.show('legend_type')
#print v.show('isofill')
#print v.show('isoline')
#print v.show('line')

#print v.show('colormap')
#print v.show('fillarea')
#v.setcolormap("white_to_green")
#v.update()
v.mode=1
l=v.createline('new', 'ASD1')
l.type=['solid']
l.width=2

tt=v.createtexttable('new', 'std')
tt.font=1
tt.expansion=150
#tt.color=241

tt.priority=1

to=v.createtextorientation('new', 'center')
to.height=20
to.angle=0
#to.path='right'
#tt.string="Observed Rainfall Data"
#tt.textorientation='center'


tlp=v.createtemplate('AMIPDUD')
tlp.units.priority = 1
tlp.units.x=0.47
tlp.units.y=0.90
tlp.units.texttable=tt
#tlp.units.string=
tlp.mean.priority = 0
tlp.min.priority = 0
tlp.max.priority = 0

tlp.units.textorientation=to

tlp.scale(0.9, axis='x')#, font=10)

tlp.scale(1.5, axis='y')
tlp.box1.x2 = 0.9

#tlp.xtic1.priority = 0
#tlp.xtic1.y1 = 2
#tlp.xtic1.y2 = 2


#tlp.xtic1.line = default
tlp.move(0.1, 'y')
tlp.move(0.02, 'y')
print tlp.list('legend')

#tlp.legend_type='VCS'

#tlp.legend.priority = 1
#tlp.legend.y1=0.06
##tlp.legend.x2=0.1
#tlp.legend.y2=0.1



#tlp.unitsfont(2.8)
#tlp.scale(1.3)

tlp.scalefont(2.8)

tlp.xlabel1.priority=1
#tlp.xlabel1.y=0.44
tlp.xlabel1.texttable=tt
tlp.ylabel1.texttable=tt
#tlp.xlabel1.textorientation=to
v.set('template', 'tlp')

#bbllx = 0.25
#bblly = 0.25
#bburx = 0.75
#bbury = 0.75
#title_fontht = 40
#xytitle_fontht = 30
#ticklabel_fontht = 30
#ticklength = 0.01
#ticklabel_font = 2
#titles_font = 2



tlp.legend.priority = 1


iso=v.createisofill('new', 'ASD')
#iso= v.getisofill('quick')
tlp.legend.line =l
tlp.legend_type='VCS'
iso.levels=([1, 5, 10, 15, 20, 25, 35, 45, 55])
iso.fillareacolors=(0, 6,  16, 30, 158, 197, 216, 241, 0)



tlp.legend.y1=0.09
tlp.legend.texttable=tt
#tlp.legend.x2=0.1
tlp.legend.y2=0.06
#tlp.legend.x2=0.1

iso.ext_1='y'
iso.ext_2='y'
iso.level_1=1
iso.level_2=40

#tlp.moveto(0.06, 0.22)
tlp.script('my_template', 'w')


obs=f_rain('rain_obs')
time = obs.getTime()
lat= obs.getLatitude()
lon= obs.getLongitude()

obs_masked=numpy.ma.array(obs)
# We are replacing all negative value  to 0
# We are giving the condition as 'obs_old>0' for replacing negative value by
# '0'----Why?---->{We are givig all value as 0 if it is 'false', if we give
# condition as 'obs_old<0' then the all value which are 'false' replaced by
#'0' thats why we givig the condition as 'obs_old>0'}
obs_masked =numpy.ma.where(obs_masked>0, obs_masked, 0)
obs_masked=numpy.array(obs_masked)

final_obs = cdms2.createVariable(obs_masked, axes = [time, lat, lon])

obs_avg=cdutil.averager(final_obs, axis='t', weight = 'equal')
a_units="Observed Rainfall Data"

v.plot(obs_avg, iso, tlp, units=a_units, continents=6)#, bg=1)
#v.showbg()
print v.canvasinfo()
v.canvasraised()
v.png('/home/dileep/Desktop/Obs_data.png')#, width=100, height=130, units='cm')
v.close()
