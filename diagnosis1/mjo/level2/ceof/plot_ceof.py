import os
import sys
import cdms2, numpy
import vcs
from ceof_make_template_array import make_template_array
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath

__vcsSlow__ = True


def plotLineCEOF(infile, outpath, variables, season, **kwarg):
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
    x.portrait()
    x.mode = 1
    
    if 'ceof_yx' in x.listelements('yxvsx'):
        yx = x.getyxvsx('ceof_yx')
    else:
        to_l = x.createtextorientation('new_1', 'default')
        to_l.height = 25
        to_l.angle = 45
        dic1 = {0: '0', 60: '60E', 120: '120E', 180: '180',
                    240: '120W', 300: '60W', 360: '0'}
        dic2 = {-1.4: '-1.4', -1.2: '-1.2', -1: '-1', -0.8: '-0.8', -0.6: '-0.6',
                -0.4: '-0.4', -0.2: '-0.2', 0: '0', 0.2: '0.2', 0.4: '0.4',
                 0.6: '0.6', 0.8: '0.8', 1: '1', 1.2: '1.2', 1.4: '1.4'}
        yx = x.createyxvsx('ceof_yx', 'default')
        yx.linewidth = 2
        yx.xticlabels1 = dic1
        yx.yticlabels1 = dic2
        yx.textorientation = to_l
        yx.datawc_x1 = min(dic1)
        yx.datawc_x2 = max(dic1)
        yx.datawc_y1 = -1.65
        yx.datawc_y2 = 1.65
    # end of if 'ceof_yx' in x.listelements('yxvsx'):
    # marker off should be outside of creating yx.
    yx.marker = 0

    text1 = x.createtext()
    text1.height = 7
    text1.color = 1
    text1.x = [0.27, 0.48, 0.68]
    text1.y = [0.13, 0.13, 0.13]

    text2 = x.createtext()
    text2.height = 5
    text2.color = 1
    text2.x = [0.20, 0.42, 0.62]
    text2.y = [0.10, 0.10, 0.10]

    if 'ceof_line1' in x.listelements('line'):
        legend1 = x.getline('ceof_line1')
    else:
        legend1 = x.createline('ceof_line1')
        legend1.width = 3
        legend1.type = 'solid'
        legend1.color = 1
        legend1.x = [0.20, 0.26]
        legend1.y = [0.13, 0.13]
    # end of if 'ceof_line1' in x.listelements('line'):
    if 'ceof_line2' in x.listelements('line'):
        legend2 = x.getline('ceof_line2')
    else:
        legend2 = x.createline('ceof_line2')
        legend2.width = 3
        legend2.type = 'solid'
        legend2.color = 242
        legend2.x = [0.42, 0.47]
        legend2.y = [0.13, 0.13]
    # end of if 'ceof_line2' in x.listelements('line'):
    if 'ceof_line3' in x.listelements('line'):
        legend3 = x.getline('ceof_line3')
    else:
        legend3 = x.createline('ceof_line3')
        legend3.width = 3
        legend3.type = 'solid'
        legend3.color = 80
        legend3.x = [0.62, 0.67]
        legend3.y = [0.13, 0.13]
    # end of if 'ceof_line3' in x.listelements('line'):

    text2Strings = []
    season_long_name = {'all': 'All', 'win': 'Winter', 'sum': 'Summer'}
    varianceVars = {}
    stdVars = {}
    for var in variables:
        varianceVars[var] = '_'.join(['var_acc', var, season])
        stdVars[var] = '_'.join(['std', var, season])
    # end of for var in variables:

    tit = "Combined EOF, %s Season " % season_long_name[season]
    if titleEndName: tit += titleEndName
    f = cdms2.open(infile)

    my_template = make_template_array(Nrows=2, Ncols=1, xgap=-0.01,
                     ygap=-0.04, Left_Margin=0.1, Right_Margin=0.1,
                             Top_Margin=0.13, Bot_Margin=0.09, x=x)

    for i in range(2):  # mode 1, mode 2 loop
        for var in variables:  # olr, u200 & u850 variables loop
            tlp = my_template[i]
            tlp.legend.priority = 0
            com_eof_var = '_'.join(['eof', var, season])
            # extract the eof var with mode (=1, 2, ... NEOF)
            com_eof = f(com_eof_var)[i]

            per_exp_var = '_'.join(['per_exp', 'ceof', season])
            per_exp = f(per_exp_var)[i]
            zero_array = numpy.zeros(360, float)

            if (i == 0):
                comment_1 = "a) 1st mode %s%s" % (str(round(per_exp, 2)), '%')
                if season in ['sum']:
                    com_eof = com_eof * (-1)
                # end of if season in ['sum', 'all']:
            elif (i == 1):
                com_eof = com_eof * (-1)
                comment_1 = "b) 2nd mode %s%s" % (str(round(per_exp, 2)), '%')
            # end if (i == 0):

            if var in ['olr']:
                yx.linecolor = 1  # Black
                comment_2 = "Variance accounted for: "
                for variable in variables:
                    comment_2 += "%s=%s%s; " % (variable.upper(),
                        str(round(f(varianceVars[variable])[i], 2)), '%')
                # end of for variable in variables:

                if (i == 0):
                    tlp.xname.y = 0.60
                    tlp.yname.y = 0.75
                    tlp.yname.x = 0.09
                    x_name = "Longitude (Deg)"
                    y_name = "Normalized Amplitude"
                    text2Strings.append("STD: %s Wm!U-2" %
                                str(round(f(stdVars[var]), 2)))
                else:
                    tit = ""
                    tlp.xname.y = 0.23
                    x_name = "Longitude (Deg)"
                    tlp.yname.x = 0.09
                    tlp.yname.y = 0.38
                    y_name = "Normalized Amplitude"
                # end of if (i == 0):
                com_eof.id = y_name
                x.plot(com_eof, yx, tlp, long_name='', title=tit,
                         comment1=comment_1, comment2=comment_2,
                         comment3=x_name, yname=y_name, bg=bg)
                x.flush()
                x.plot(legend1, bg=bg)
            elif var in ['u200']:
                yx.linecolor = 80  # Green
                x.plot(com_eof, yx, tlp, long_name='', xname='', bg=bg)
                x.flush()
                x.plot(legend2, bg=bg)
                if (i == 0):
                    text2Strings.append("STD: %s ms!U-1" %
                            str(round(f(stdVars[var]), 2)))
                # end of if (i == 0):
            elif var in ['u850']:
                yx.linecolor = 242  # Red
                x.plot(com_eof, yx, tlp, long_name='', xname='', bg=bg)
                x.flush()
                x.plot(legend3, bg=bg)
                if (i == 0):
                    text2Strings.append("STD: %s ms!U-1" %
                              str(round(f(stdVars[var]), 2)))
                # end of if (i == 0):
            # end of if (var == 'olr'):
        # end of for var in variables:
        yx.linecolor = 1
        x.plot(zero_array, yx, tlp, bg=bg)
        x.flush()
    # end of for i in range(2):
    text1.string = [name.upper() for name in variables]
    text2.string = text2Strings
    x.plot(text1, bg=bg)
    x.plot(text2, bg=bg)
    x.update()
    out_file = 'ceof_' + season
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
    f.close()
    del x
# end of def plotLineCEOF(infile, outpath, variables, seasons):


def doPlotLineCEOF(rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                                  variables=['olr', 'u850', 'u200'],
                    seasons=['sum', 'win', 'all'], year=None, **kwarg):

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
    opath = os.path.join(plotsgraphsPath, 'Level2', 'Ceof',
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
            outpath = os.path.join(opath, subName, season)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "The path has created ", outpath
            # end of if not os.path.isdir(outpath):

            infile = 'ceof_vars_%s_%s_%s_%s_%s.nc' % (season, yearDir,
                                 rawOrAnomaly, filteredOrNot, subName)
            file_input = os.path.join(ceofncpath, infile)
            endname = [yearDir, rawOrAnomaly, filteredOrNot, subName]
            plotfile_endname = '_'.join(endname)
            plotttitle_endname = ' '.join(endname)
            plotLineCEOF(file_input, outpath, variables, season=sea,
                    ofileEndName=plotfile_endname,
                    titleEndName=plotttitle_endname, pdf=1, x=x)
        # end of for season in os.listdir(seasonPath):
    # end of for subName in os.listdir(inpath):
# end of def doPlotLineCEOF(rawOrAnomaly='Anomaly', ...):

if __name__ == '__main__':

    v = vcs.init()
    year = (1979, 2005)
    doPlotLineCEOF('Anomaly', 'Filtered',  year=year, x=v)

    year = 2005
    doPlotLineCEOF('Anomaly', 'Filtered',  year=year, x=v)

# end of if __name__ == '__main__':




