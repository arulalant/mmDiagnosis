import os
import sys
import cdms2
import vcs
from eeof_make_template_array import make_template_array
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__curDir__, '../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath

__vcsSlow__ = True


def plotEEof(infile, outpath, variables, season, NEEOF=2, **kwarg):
    """
    season - string not a list. string also should be 'jjas'/'all'.
    KWargs :
        ofileEndName - This string will be added to the end of the
                        outfile/plotfile name.

        pdf - By default takes True
        png - Optional.
        bg - 0 for this eof 4 template plots. option 1 is not working
        x - vcs.init() obj. By default it will create it own vcs init obj.

    """

    ofileEndName = kwarg.get('ofileEndName', None)
    titleEndName = kwarg.get('titleEndName', None)
    pdf = kwarg.get('pdf', 1)
    png = kwarg.get('png', 0)
    bg = kwarg.get('bg', 0)
    x = kwarg.get('x', None)
    if x is None:
        x = vcs.init()
        print "x init"
    # end of if x is None:
    x.clear()
    x.landscape()
    x.mode = 1
    
    dic={-4:'-4', -3:'-3', -2:'-2', -1:'-1', 0:'0', 1:'1', 2:'2', 3:'3', 4:'4'}
    lags = [0, 2, 4, 6, 8, 10, 12, 15]  

    my_template = make_template_array(v, Nrows=4, Ncols=2, xgap=0.03, 
                     ygap=-0.04, Left_Margin=0.09, Right_Margin=0.16, 
                               Top_Margin= 0.1, Bot_Margin=0.01, x=x)

    f = cdms2.open(infile)
    for name in variables:
        per_exp_var = '_'.join(['per_exp', name, season])
        per_exp = f(per_exp_var)

        eeof_var = '_'.join(['eof', name, season])

        if season in ['jjas']:
            seatxt = "JJAS (Jun-Sep)"        
        elif season in ['all']:
            seatxt = "All (Jan-Dec)"
        # end of  if season in ['jjas']:

        tit = "%s, EEOFs 1-%d, %s " % (name.upper(), NEOF, seatxt)
        if titleEndName: tit += titleEndName
        for i in xrange(8):
            line_number = 'new_%s' %(str(i))
            yx = x.createyxvsx(line_number,'default')
            yx.linewidth = 3
            yx.marker = 0
            yx.yticlabels1 = dic
            tlp = my_template[i]
            # for lag 0,  EEOF
            # In the Observation section the EEOF's/PC's were multiplied
            # by -1 if necessary. So that the results depict a consistent
            # picture of eastward propagation of enhanced convection,
            # wind and rainfall/olr anomalies
            if (i==0):        
                eeof1 = f(eeof_var, eeof=0, lag=0)(squeeze=1)
                eeof2 = f(eeof_var, eeof=1, lag=0)(squeeze=1)*(-1)
                
            elif (i==1):
                eeof1 = f(eeof_var, eeof=0, lag=2)(squeeze=1)
                eeof2 = f(eeof_var, eeof=0, lag=2)(squeeze=1)*(-1)

            elif (i==2):
                eeof1 = f(eeof_var, eeof=0, lag=4)(squeeze=1)
                eeof2 = f(eeof_var, eeof=0, lag=4)(squeeze=1)*(-1)

            elif (i==3):
                eeof1 = f(eeof_var, eeof=0, lag=6)(squeeze=1)
                eeof2 = f(eeof_var, eeof=0, lag=6)(squeeze=1)*(-1)

            elif (i==4):
                eeof1 = f(eeof_var, eeof=0, lag=8)(squeeze=1)
                eeof2 = f(eeof_var, eeof=0, lag=8)(squeeze=1)*(-1)

            elif (i==5):
                eeof1 = f(eeof_var, eeof=0, lag=10)(squeeze=1)
                eeof2 = f(eeof_var, eeof=0, lag=10)(squeeze=1)*(-1)

            elif (i==6):
                eeof1 = f(eeof_var, eeof=0, lag=12)(squeeze=1)*(-1)
                eeof2 = f(eeof_var, eeof=0, lag=12)(squeeze=1)*(-1)

            elif (i==7):
                eeof1 = f(eeof_var, eeof=0, lag=15)(squeeze=1)*(-1)
                eeof2 = f(eeof_var, eeof=0, lag=15)(squeeze=1)*(-1)       
            # end of if (i==0):          
            
            yx.datawc_y1 = min(eeof1.min(), eeof2.min())
            yx.datawc_y2 = max(eeof1.max(), eeof2.max())
            tlp.yticlabels1 = dic
            yx.yticlabels1 = dic
            comment_1 = 'Lag %s' %str(lags[i])
            eeof1.getAxisList()[0].id = 'Latitude (Deg)'
            eeof2.getAxisList()[0].id = 'Latitude (Deg)'
            # plot EEOF1 with solid line 
            yx.line = 'solid'
            x.flush()
            eeof1.long_name = ''
            eeof1.id = ''
            x.plot(eeof1, yx, tlp, comment1=comment_1, comment2='Amplitude', bg=bg)
            x.flush()
            
            # plot EEOF2 with dot line 
            yx.line = 'dot' 
            eeof2.long_name = ''
            eeof2.id = ''
            if i == 0:
                x.plot(eeof2, yx, tlp, title=tit, bg=bg)    
            else:
                x.plot(eeof2, yx, tlp, bg=bg)
            x.flush()         
        # end of for i in xrange(8):        
        x.update()
        if ofileEndName:
            out_file = eof_var + '_' + ofileEndName
        else:
            out_file = eof_var
        # end of if ofileEndName:
        outfile = os.path.join(outpath, out_file)
        print "Plot saved in", outfile,
        if pdf:
            x.pdf(outfile + '.pdf')
            print ".pdf"
        if png:
            x.png(outfile + '.png')
            print ".png"
        x.clear()
    # end of for name in variables:
    f.close()
# end of def plotEof(infile, outpath, variables, seasons, NEOF=4):


def doPlotEEof(rawOrAnomaly='Anomaly', filteredOrNot='Unfiltered',
                             variables=['precip'],
                         seasons=['jjas'], year=None, v=None):

    """
    Written By : Arulalan.T

    Date : 22.07.2013

    """

    v = vcs.init()
    if __vcsSlow__:
        v.pause_time = 1
    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    inpath = os.path.join(processfilesPath, 'miso', 'EEof', rawOrAnomaly,
                                                filteredOrNot, yearDir)
    opath = os.path.join(plotsgraphsPath, 'miso', 'EEof', rawOrAnomaly,
                                                filteredOrNot, yearDir)
    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        for season in os.listdir(anopath):
            sea = season.lower()[:4]
            if not sea in seasons:
                print "Though '%s' Season is available, skipping it without \
                plotting because in the arg seasons list it is not available.\
                So enable it by passing this '%s' season to seasons list " % \
                 (season, sea)

                continue
            # end of if not sea in seasons:
            eeofncpath = os.path.join(anopath, season)
            outpath = os.path.join(opath, subName, season)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "The path has created ", outpath
            # end of if not os.path.isdir(outpath):

            infile = 'eeof_vars_%s_%s_%s_%s_%s.nc' % (season, yearDir, rawOrAnomaly,
                                                   filteredOrNot, subName)
            file_input = os.path.join(eeofncpath, infile)
            endname = [yearDir, rawOrAnomaly, filteredOrNot, subName]
            plotfile_endname = '_'.join(endname)
            plotttitle_endname = ' '.join(endname)
            plotEEof(file_input, outpath, variables, season=sea, NEOF=2,
                    ofileEndName=plotfile_endname,
                    titleEndName=plotttitle_endname, pdf=1, x=v)
        # end of for season in os.listdir(seasonPath):
    # end of for subName in os.listdir(inpath):
# end of def doPlotEof(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    year = (1997, 2008)
    doPlotEEof('Anomaly', 'Filtered',  year=year)

    year = 2014
    doPlotEEof('Anomaly', 'Filtered',  year=year)

# end of if __name__ == '__main__':
  
        
