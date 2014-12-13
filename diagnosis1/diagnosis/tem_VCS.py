import os
import sys
import cdms2
import cdutil
import vcs
import numpy

# getting the absolute path of the previous directory
previousDir = os.path.abspath(os.path.join(os.getcwd(), '..'))
# adding the previous path to python path
sys.path.append(previousDir)
# importing xml_data_acces.py from previous directory diagnosisutils
import diagnosisutils.xml_data_access as xml_data_access
import cdutil.region as r
India = r.domain(longitude = (40, 120, 'cc'), latitude = (-10, 40, 'cc'))

o = xml_data_access.GribXmlAccess('/home/dileep/NCMRWF_XML')

levels=[850, 200]
hrs=[24, 48, 72, 96, 120]


date=('2010-6-10', '2010-9-30')
v = vcs.init()
print v.show('colormap')
v.mode=1
v.setcolormap("ASD")

tt=v.createtexttable('new', 'std')
tt.font=1
tt.priority=1

to=v.createtextorientation('new', 'centerup')
to.height=15
to.angle=0


l=v.createline('new', 'thick')
l.type=['solid']
l.width=3


new_iso_line=v.createisoline('new_iso_ln', 'ASD')
new_iso_line.line=['solid']
new_iso_line.linewidths =  [20.0]

tlp=v.createtemplate('AMIPDUD')

tlp.title.priority = 1
tlp.title.x=0.50
tlp.title.y = 0.95
tlp.title.texttable=tt
tlp.title.textorientation=to

tlp.mean.priority = 1
tlp.min.priority = 1
tlp.max.priority = 1


tlp.legend_type='VCS'
tlp.legend.line =l
tlp.legend.x1=0.07
tlp.legend.y1=0.15
tlp.legend.x2=0.93
tlp.legend.y2=0.11
tlp.legend.texttable=tt
tlp.legend.textorientation=to

tlp.scale(1)
tlp.scalefont(2.8)

new_iso=v.createisofill('new', 'ASD')


v.set('template', 'tlp')

for i in xrange(len(levels)):
    
    temp_anl = o.getData('rhprs', 'a', date ,level=levels[i], region= India, squeeze = 1)
 
    temp_anl_avg=cdutil.averager(temp_anl, axis='t', weight = 'equal')
    tem_anl_avg_numpy=numpy.array(temp_anl_avg)
    level_max=int(numpy.max(tem_anl_avg_numpy))+3
    level_min=int(numpy.min(tem_anl_avg_numpy))-3
    print 'temp_anl_avg.shape=', temp_anl_avg.shape
    print 'Anl_level_min=',level_min
    print 'Anl_level_max=', level_max
    
    scale = 2.0
    

    iso= v.getisoline('new_iso_ln')
    iso.line = ['solid']
    iso.linewidths =  [2.0, 2.0, 2.0, 2.0, 2.0, 2.0]

    mylevel =range(level_min, level_max, 5)
    
    
    iso.levels= mylevel
    iso.label='y'
    
    
    colorlist=[ 250, 244, 63, 75, 246, 90, 118, 141, 155, 5, 166, 190, 205, 224, 239, 241]#247, 10, 16, 25,
    #[ 250, 244, 63, 75, 90, 243, 126, 141, 245, 190, 205, 224, 239, 241]
    #
    iso.linecolors=colorlist
    a_unit="T254 ANLYSIS %shPa HUMIDITY JJAS 2010" %(str(levels[i]))

    
    v.plot(temp_anl_avg, iso,tlp, title=a_unit, continents=1)
    
    
    
    out_file_anl='/home/dileep/Desktop/Plots_/plots_anl/hum_avg_%s.png' %(str(levels[i]))
    v.png(out_file_anl)
    v.clear()
    
    for j in xrange(len(hrs)):
        
        
        forcast= o.getData('rhprs', 'f', date, str(hrs[j]), levels[i], region = India, squeeze = 1)
        fcst_error = (forcast-temp_anl)
        fcst_error_avg= cdutil.averager(fcst_error, axis='t', weight = 'equal')
        fcst_error_avg_numpy=numpy.array(fcst_error_avg)
        level_max_er=int(numpy.max(fcst_error_avg_numpy))+2
        level_min_er=int(numpy.min(fcst_error_avg_numpy))-2
        print level_max_er, level_min_er
        scale = 2.0
        
        iso= v.getisoline('new_iso_ln')
        
        mylevel = (range(-24, 24, 4))  #(range(level_min_er, level_max_er, 2))
        iso.levels= mylevel
        iso.label='y'
        iso.line = ['solid']
        iso.linewidths =[5.0]
        colorlist=[241]#, 242, 246, 244, 245, 243, 247, 248, 249, 250, 251]
        iso.linecolors=colorlist
        color_fill=[250, 244, 25, 246, 255, 252, 253, 243, 251, 108, 254, 248, 170,  242, 239, 249]
        #[250, 244, 25, 246, 253, 252, 254, 166, 248, 210, 239, 249]#243, 139, 245, 248, 210, 239, 249] # 251, 108, 254, 248, 170,  242, 239, 249]
        #
        #[ 250, 244, 246,  90, 243, 126, 141, 245, 190, 205, 224, 239, 241]
        # #243, 95,   146,  247, 242, 239]
        
       
        isofill= v.getisofill('quick')
        isofill.levels=mylevel
        isofill.level_1=-24 #level_min_er+1
        isofill.level_2=+24 #level_max_er-1
        isofill.ext_1='y'
        isofill.ext_2='y'
        #isofill.ext_1.set=-24
        #isofill.ext_2.set=+24
        isofill.fillareacolors=color_fill
        '''
        
        boxfill= v.getboxfill('quick')
        boxfill.levels=mylevel
        boxfill.level_1=-24 #level_min_er+1
        boxfill.level_2=+24 #level_max_er-1
        boxfill.ext_1='y'
        boxfill.ext_2='y'
        #boxfill.fillareacolors=color_fill
        '''
        b_unit="T254 %s hr FCST SYS ERR %shPa HUMIDITY JJAS 2010" %(str(hrs[j]), str(levels[i]))
        
        
        v.plot(fcst_error_avg,  tlp, isofill, continents=1, title=b_unit)
        v.plot(fcst_error_avg, iso, tlp, continents=1)
        out_file_fcst_error='/home/dileep/Desktop/Plots_/plots_fst_err/fcst_error_hum_avg_%s_%s.png' %(str(levels[i]), str(hrs[j]))
        v.png(out_file_fcst_error)
        v.clear()
        
        
        
    




