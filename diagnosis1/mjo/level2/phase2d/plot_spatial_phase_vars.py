import cdms2
import numpy
import vcs
import os
import sys
from make_template_array_spatial import make_template_array
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath

__vcsSlow__ =  True


def plotSpatialPhase2d(infile, outpath, variables, season,
                        title="Life Cycle Composite", **kwarg):
    """
    variables : variable generic names not an actual variable name.
                This variable generic name will complete the actual variable
                name by using season name also. It must be a list.
                eg : [olr, u200, u850]. It will complete the actual variable
                name like for eg: cc_olr_sum, cc_u200_win, n_days_olr_all
    seasons : It could be sum/win/all, not a list.

    title : It is partial title.

    Written By : Dileep.K

    Updated By : Arulalan.T [11.06.2013]

    """

    ofileEndName = kwarg.get('ofileEndName', None)
    titleEndName = kwarg.get('titleEndName', None)
    pdf = kwarg.get('pdf', 1)
    png = kwarg.get('png', 0)
    bg = kwarg.get('bg', 0)
    x = kwarg.get('x', None)

    if x is None:
        print "vcs init from eof_make_template_array"
        x = vcs.init()
    # end of if x is None:
    x.portrait()
    x.mode = 1
    dic = {-15: '15S', 0: 'Eq', 15: '15N'}

    my_cmap = x.createcolormap('my_cmap', 'default')
    #- Compute RGB values and fill the my_cmap.index dictionary for
    #  color indices 16 to 239:  blue is indices 16-127, red is
    #  indices 128-239:

    for icell in range(6, 100):
        rvalue = int(float(icell-6.)/(100.-6.) * 100.)
        gvalue = rvalue
        bvalue = 100
        my_cmap.index[icell] = [rvalue, gvalue, bvalue]
    for icell in range(100, 124):
        my_cmap.index[icell] = [100, 100, 100]

    for icell in range(125, 240):
        rvalue = 100
        gvalue = 75 - int(float(icell-131.)/(239.-131.) * 75.)
        bvalue = gvalue
        my_cmap.index[icell] = [rvalue, gvalue, bvalue]

    #- Set my color map to the active color map:

    x.setcolormap('my_cmap')
    x.setcolorcell(10, 100, 0, 0)

    if 'ph2dIsoLine' in x.listelements('isoline'):
        isolinetemp = x.getisoline('ph2dIsoLine')
    else:
        isolinetemp = x.createisoline('ph2dIsoLine', 'ASD')
    isolinetemp.linewidths = [1.0]
    isolinetemp.label = 'y'
    isolinetemp.yticlabels1 = dic
    isofill = x.getisofill('quick')
    isofill.yticlabels1 = dic

    my_template = make_template_array(Nrows=8, Ncols=1, xgap=0.5,
                        ygap=-0.04, Left_Margin=0.01, Right_Margin=0.01,
                        Top_Margin=-0.01, Bot_Margin=0.06, x=x)

    f = cdms2.open(infile)
    season_long_name = {'all': 'All', 'win': 'Winter', 'sum': 'Summer'}
    for name in variables:
        var_cc = 'cc_%s_%s' % (name, season)
        var_ndays = 'n_days_%s_%s' % (name, season)
        if (name == 'olr'):
            colorlist = range(6, 239, 12)
            plot_range = range(-24, 27, 3)
            isofill.level_1 = -24
            isofill.level_2 = 24
            isofill.levels = plot_range
            unit = "Wm!U-2"
        elif (name == 'u200'):
            colorlist = range(6, 239, 12)
            plot_range = range(-8, 9, 1)
            isofill.level_1 = -8
            isofill.level_2 = 8
            isofill.levels = plot_range
            unit = "ms!U-1"
        elif (name == 'u850'):
            colorlist = range(6, 239, 14)
            plot_range = (numpy.array(range(-35, 40, 5))/10.0).tolist()
            isofill.level_1 = -3.5
            isofill.level_2 = 3.5
            isofill.levels = plot_range
            unit = "ms!U-1"
        else:
            unit = ""
        # end of if (name == 'olr'):

        isofill.fillareacolors = colorlist
        isofill.ext_1 = 'y'
        isofill.ext_2 = 'y'

        titl = "%s (%s) %s " % (title, name.upper(), season_long_name[season])
        if titleEndName: titl += titleEndName
        for pha in range(1, 9):
            cc = f(var_cc, phase=pha)(squeeze=1)
            n_days = f(var_ndays, phase=pha)[0]
            cc.long_name = ''
            cc.id = ''
            comment_s = "Phase %s" % (str(pha))
            comment_2 = "%s days" % (str(n_days))
            comment_3 = season
            if season in ['sum']:
                comment_3 += " (May-Oct)"
            elif season in ['win']:
                comment_3 += " (Nov-Apr)"
            # end of if season in ['sum']:
            comment_4 = "Unit: " + unit
            tlp = my_template[pha-1]
            if (pha == 1):
                x.plot(cc, tlp, isofill, title=titl, comment1=comment_s,
                                       long_name='', comment2=comment_2,
                                comment4=comment_4, continents=1, bg=bg)
            else:
                x.plot(cc, tlp, isofill, long_name='', comment1=comment_s,
                                   comment2=comment_2, comment3=comment_3,
                                   continents=1, bg=bg)
            # end of if (pha == 1):
            x.flush()
        # end of for pha in range(1, 9):

        out_file = 'cc_%s_%s' % (name, season)
        if ofileEndName: out_file += '_' + ofileEndName
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
# end of def plotSpatialPhase2d(infile, outpath, variables, seasons):


def doPlotSpatialPhase2d(rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                                         varnames=['olr', 'u850', 'u200'],
                               seasons=['sum', 'win'], year=None, **kwarg):
    """
    Written By : Arulalan.T

    Date : 22.07.2013

    """

    x = kwarg.get('x', None)
    if x is None:
        x = vcs.init()
        print "x init"
    # end of if x is None:
    x.clear()
    x.portrait()
    if __vcsSlow__:
        x.pause_time = 1

    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    inpath = os.path.join(processfilesPath, 'Level2', 'Ceof',
                         rawOrAnomaly, filteredOrNot, yearDir)
    opath = os.path.join(plotsgraphsPath, 'Level2', 'CycleComposite',
                                rawOrAnomaly, filteredOrNot, yearDir)
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
            ceofncpath = os.path.join(anopath, season)

            ccfile = 'cycle_composite_%s_%s_%s_%s_%s.nc' % (season, yearDir,
                                 rawOrAnomaly, filteredOrNot, subName)
            file_input = os.path.join(ceofncpath, ccfile)

            if not os.path.isfile(file_input):
                print "The cycle_composite is not exists ", file_input
                print "So skipping plotting spatial cycle_composite images..."
                continue
            # end of if not os.path.isfile(ccpath):

            outpath = os.path.join(opath, subName, season)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "The path has created ", outpath
            # end of if not os.path.isdir(outpath):
            endname = [yearDir, rawOrAnomaly, filteredOrNot, subName]
            plotfile_endname = '_'.join(endname)
            plotttitle_endname = ' '.join(endname)
            plotSpatialPhase2d(file_input, outpath, varnames, season=sea,
                    ofileEndName=plotfile_endname,
                    titleEndName=plotttitle_endname, pdf=1, x=x)
    # end of for subName in os.listdir(inpath):
# end of def doPlotSpatialPhase2d(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    v = vcs.init()
    year = (1979, 2005)
    doPlotSpatialPhase2d('Anomaly', 'Filtered',
        varnames=['olr', 'u850', 'u200'], seasons=['sum', 'win'],  year=year, x=v)

    year = 2005
    doPlotSpatialPhase2d('Anomaly', 'Filtered',
        varnames=['olr', 'u850', 'u200'], seasons=['sum', 'win'],  year=year, x=v)


