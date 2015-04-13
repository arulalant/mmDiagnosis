import cdms2
import cdutil
import numpy
import numpy.ma
import vcs
import os
import sys
import por_template_2x3_landscape as por_lanscape_2x3

x = por_lanscape_2x3.x

iso=x.createisofill('new1', 'ASD')

iso.levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

#([1, 5, 10, 15, 20, 25, 35, 45, 55, 60, 65, 70, 80])
#iso.levels=vcs.mkscale(0.,80.)
iso.fillareacolors = (246, 255, 252, 253, 254, 251, 140, 5, 171,
                                                 248, 249, 242, 239)
#iso.fillareacolors=vcs.getcolors(iso.levels)
iso.ext_1='y'
iso.ext_2='y'
iso.level_1=0
iso.level_2=1
hours=[24, 48, 72, 96, 120]
score_name= ['ts', 'pod', 'pofd', 'hr', 'far']
th_list=[0.1,  0.6,  1. ,  3. ,  5. ,  7.]

file_name='/NCMRWF/Process_Files/T254/StatiScore/2010/Season/jjas/24/stati_spatial_distribution_score_24hr_jjas_2010_T254.nc'

f=cdms2.open(file_name)

for j in xrange(len(score_name)):  
    # plotting different statistical scores
    score_name_capital = score_name[j].upper()
    for k in range(6):
        score=TS=f(score_name[j], threshold = th_list[k]) 
        title_plot='T254 D-01 %s %s THRESHOLD JJAS 2010' %(score_name_capital, str(th_list[k])) 
        # plotting different thresholds 
        if (k == 0):            
            x.plot(score, por_lanscape_2x3.leftOfTop_lscp, iso, title=title_plot,  continents=1, bg=1)
            
        elif (k == 1):            
            x.plot(score, por_lanscape_2x3.midOfTop_lscp, iso, title=title_plot,  continents=1, bg=1)
           
        elif (k == 2):            
            x.plot(score, por_lanscape_2x3.rightOfTop_lscp, iso, title=title_plot,  continents=1, bg=1)
            
        elif(k==3):            
            x.plot(score, por_lanscape_2x3.leftOfBot_lscp, iso, title=title_plot,  continents=1, bg=1)
            
        elif(k==4):            
            x.plot(score, por_lanscape_2x3.midOfBot_lscp, iso, title=title_plot,  continents=1, bg=1)
            
        elif(k==5):            
            x.plot(score, por_lanscape_2x3.rightOfBot_lscp, iso, title=title_plot,  continents=1, bg=1)
            
        else:
            pass
            
    out_f_name='/home/arulalan/Desktop/demo/%s_2010_obs.png' %(score_name_capital)
          
    x.png(out_f_name)     
    x.clear()
