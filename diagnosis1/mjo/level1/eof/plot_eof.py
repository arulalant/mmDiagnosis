import os
import sys
import cdms2
import vcs
#import template
from eof_make_template_array import make_template_array
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath


__vcsSlow__ = True


def plotEof(infile, outpath, variables, season, NEOF=4, **kwarg):
    """
    season - string not a list. string also should be 'sum'/'win'/'all'.
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
    dic = {-30: '30S', -20: '20S', -10: '10S',
            0: 'Eq', 10: '10N', 20: '20N', 30: '30N'}

    my_cmap = x.createcolormap('my_cmap', 'default')
    #- Compute RGB values and fill the my_cmap.index dictionary for
    #  color indices 16 to 239:  blue is indices 16-127, red is
    #  indices 128-239:

    for icell in range(16, 110):
        rvalue = int(float(icell-16)/(122.-16.) * 100.)
        gvalue = rvalue
        bvalue = 100
        my_cmap.index[icell] = [rvalue, gvalue, bvalue]
    # end of for icell in range(16, 110):
    for icell in range(110, 131):
        my_cmap.index[icell] = [100, 100, 100]
    # end of for icell in range(110, 131):
    for icell in range(131, 240):
        rvalue = 100
        gvalue = 75 - int(float(icell-131)/(239.-131.) * 75.)
        #print "gvalue", gvalue
        bvalue = gvalue
        my_cmap.index[icell] = [rvalue, gvalue, bvalue]
    # end of for icell in range(131, 240):

    x.setcolormap('my_cmap')
    x.setcolorcell(10, 100, 0, 0)
    isoLineTempName = 'eofIsoLineTemp'

    if isoLineTempName in x.listelements('isoline'):
        # get the 'eofIsoLineTemplate' template object from temporary
        # memory of vcs template
        isolinetemp = x.getisoline(isoLineTempName)
    else:
        line_range = range(-18, 20, 2)
        line_range.remove(0)
        # create 'eofIsoLineTemp' template
        isolinetemp = x.createisoline(isoLineTempName, 'ASD')
        isolinetemp.linewidths = [1.0]
        isolinetemp.label = 'y'
        isolinetemp.yticlabels1 = dic
        isolinetemp.level = line_range
        isolinetemp.line = ['dash', 'dash', 'dash', 'dash', 'dash', 'dash',
                             'dash', 'dash', 'solid', 'solid', 'solid',
                           'solid', 'solid', 'solid', 'solid', 'solid']
        # saving the template into temporary python memory
        x.set('isoline', isoLineTempName)
    # end of if 'eofIsoLineTemplate' in x.listelements('template'):
    isoFillTempName = 'eofIsoFillTemp'
    if isoFillTempName in x.listelements('isofill'):
        # get the 'eofIsoLineTemp' template object from temporary
        # memory of vcs template
        isofill = x.getisofill(isoFillTempName)
    else:
        fill_range = range(-18, 20, 2)
        colorlist = range(6, 239, 12)
        # create 'eofIsoFillTemp' template
        isofill = x.createisofill(isoFillTempName, 'quick')
        isofill.levels = fill_range
        isofill.yticlabels1 = dic
        isofill.level_1 = -18
        isofill.level_2 = 18
        isofill.ext_1 = 'y'
        isofill.ext_2 = 'y'
        isofill.fillareacolors = colorlist
        # saving the template into temporary python memory
        x.set('isofill', isoFillTempName)
    # end of if 'eofIsoFillTemplate' in x.listelements('template'):

    my_template = make_template_array(Nrows=NEOF, Ncols=1, xgap=-0.1,
             ygap=-0.1, Left_Margin=0.01, Right_Margin=0.01,
       Top_Margin=0.01, Bot_Margin=0.06, x=x)

    f = cdms2.open(infile)
    for name in variables:
        per_exp_var = '_'.join(['per_exp', name, season])
        per_exp = f(per_exp_var)

        eof_var = '_'.join(['eof', name, season])

        if season in ['sum']:
            seatxt = "Summer (May-Oct)"
        elif season in ['win']:
            seatxt = "Winter (Nov-Apr)"
        elif season in ['all']:
            seatxt = "All (Jan-Dec)"
        # end of  if season in ['sum']:

        tit = "%s, EOFs 1-%d, %s " % (name.upper(), NEOF, seatxt)
        if titleEndName: tit += titleEndName
        for i in range(NEOF):
            # In the Observation section the EOF's/PC's were multiplied
            # by -1 if necessary. So that the results depict a consistent
            # picture of eastward propagation of enhanced convection,
            # wind and rainfall/olr anomalies
            data = -1 * f(eof_var, eof=i)
            data.long_name = ''
            data.id = ''
            comment = "Pecentage Explained(EOF-%s)=%s" % (str(i+1),
                                         str(round(per_exp[i], 3)))

            tlp = my_template[i]
            if (i == 0):
                x.plot(data, tlp, isofill, title=tit, comment1=comment,
                                      long_name='', continents=1, bg=bg)
            else:
                x.plot(data, tlp, isofill, comment1=comment,
                                      long_name='', continents=1, bg=bg)
            # end of if (i == 0):
            x.flush()
            x.plot(data, tlp, isolinetemp, bg=bg)
            x.flush()
        # end of for i in range(NEOF):
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


def doPlotEof(rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                             variables=['olr', 'u200', 'u850'],
                         seasons=['sum', 'win'], year=None, v=None):

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

    inpath = os.path.join(processfilesPath, 'Level1', 'Eof', rawOrAnomaly,
                                                filteredOrNot, yearDir)
    opath = os.path.join(plotsgraphsPath, 'Level1', 'Eof', rawOrAnomaly,
                                                filteredOrNot, yearDir)
    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        for season in os.listdir(anopath):
            sea = season.lower()[:3]
            if not sea in seasons:
                print "Though '%s' Season is available, skipping it without \
                plotting because in the arg seasons list it is not available.\
                So enable it by passing this '%s' season to seasons list " % \
                 (season, sea)
                continue
            # end of if not sea in seasons:
            eofncpath = os.path.join(anopath, season)
            outpath = os.path.join(opath, subName, season)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "The path has created ", outpath
            # end of if not os.path.isdir(outpath):

            infile = 'eof_vars_%s_%s_%s_%s_%s.nc' % (season, yearDir, rawOrAnomaly,
                                                   filteredOrNot, subName)
            file_input = os.path.join(eofncpath, infile)
            endname = [yearDir, rawOrAnomaly, filteredOrNot, subName]
            plotfile_endname = '_'.join(endname)
            plotttitle_endname = ' '.join(endname)
            plotEof(file_input, outpath, variables, season=sea, NEOF=4,
                    ofileEndName=plotfile_endname,
                    titleEndName=plotttitle_endname, pdf=1, x=v)
        # end of for season in os.listdir(seasonPath):
    # end of for subName in os.listdir(inpath):
# end of def doPlotEof(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    year = (1979, 2005)
    doPlotEof('Anomaly', 'Filtered',  year=year)

    year = 2005
    doPlotEof('Anomaly', 'Filtered',  year=year)

# end of if __name__ == '__main__':



