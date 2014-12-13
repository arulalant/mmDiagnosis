import os
import sys
import time
import cdms2
import numpy
import vcs
from ceof_make_template_array import make_template_array
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diagnosisutils.timeutils import TimeUtility
from diagnosisutils.xml_data_access import GribXmlAccess

timeobj = TimeUtility()
xmlobj = GribXmlAccess('.')


def _getYXTemplate(x, timeAxis, tinterval=10, ymin=-2.5, ymax=2.5):

    xdic = {}
    time_list = timeAxis.asComponentTime()[:]
    l_time = len(time_list)
    # xaxis - generate timeAxis index and its corresponding date as label
    selected_index = range(0, l_time, tinterval)
    # Adjust first, last date should be present in the label.
    if (l_time - selected_index[-1]) > 3:
        selected_index.append(l_time - 1)
    else:
        selected_index[-1] = l_time - 1
    for i in range(len(selected_index)):
        sel_time = str(time_list[selected_index[i]])
        year_mon_day = sel_time.split(' ')[0]
        xdic[selected_index[i]] = year_mon_day
    # end of for i in range(len(selected_index)):

    # generate yaxis index and its corresponding values
    yvalues = numpy.arange(ymin, ymax+0.5, 0.5).tolist()
    ydic = {}
    for i in yvalues:
        ydic[i] = str(i)
    # end of for i in yvalues:

    if 'pcts_yx' in x.listelements('yxvsx'):
        yx = x.getyxvsx('pcts_yx')
    else:
        yx = x.createyxvsx('pcts_yxvsx', 'default')
        yx.linewidth = 2
        yx.xticlabels1 = xdic
        yx.yticlabels1 = ydic
        yx.datawc_x1 = min(xdic)
        yx.datawc_x2 = max(xdic)
        yx.datawc_y1 = ymin
        yx.datawc_y2 = ymax
        yx.marker = 0

    return yx
# end of def _getYXTemplate(x, timeAxis, tinterval):


def plotPcts(pcs1VarName, pcs2VarName, mpath, outfile, pcs2Sign=-1,
              title="Combined EOF Projected Normalized PC Time Series",
              comment_1="Projected Normalized PCTS-",
              comment_2="Analysis Vs Fcst",
              stitle1="date",
              x_name="Days", y_name="Normalized PCTS-", **kwarg):
    """
    stitle1 : If 'date' has passed then it will draw string as season of
                  available dates (from startdate to enddate).
    
    exclude : exclude hours. If some hours list has passed then those 
              model hours will be omitted. eg : 01 hour.
              Note : it will omit those exclude model hours directory.
    KWargs:
        sedate : start end date of analysis data to be plotted.
             Its corresponding partners fcst data also will be plotted
             using partnerDate.
    11.08.2013

    """
    pdf = kwarg.get('pdf', 1)
    png = kwarg.get('png', 0)
    tinterval = kwarg.get('tinterval', 10)
    exclude = kwarg.get('exclude', [])
    ncfile_begin = kwarg.get('ncfile_begin', 'projected')
    sedate = kwarg.get('sedate', None)
    credits = "Created by : IIT-Delhi Dr.Krishna AchutaRao, Arulalan.T"
    credits += "  Using UVCDAT 1.3.1.   Testing Version : 0.1a"
    bg = kwarg.get('bg', 0)
    x = kwarg.get('x', None)
    if x is None:
        print "x going to initiate in plot_pcts_utils.py"
        x = vcs.init()
        print "x inited successfully in plot_pcts_utils.py"
    # end of if x is None:
    x.clear()
    x.portrait()
    x.updateorientation()
    x.mode = 1

    my_template = make_template_array(Nrows=2, Ncols=1, xgap=-0.01,
                    ygap=-0.04, Left_Margin=0.1, Right_Margin=0.1,
                    Top_Margin=0.13, Bot_Margin=0.09, x=x)

    colordic = {'Analysis': 1,     # Black
                '24 hr': 242,      # Red
                '48 hr': 243,      # Green
                '72 hr': 244,      # Blue
                '96 hr': 247,      # Pink
                '120 hr': 246,     # Sea Blue
                '144 hr': 248,     # Orange
                '168 hr': 249,     # Brown
                '192 hr': 250,     # Dark Blue
                '216 hr': 245,     # Yellow
                '240 hr': 255      # Light Blue
                }

    to1 = x.gettextorientation('centerup')
    to1.height = 15
    to1.angle = 0

    tt = x.createtexttable('new', 'std')
    tt.font = 3
    tt.priority = 1

    txto = x.createtextorientation('new', 'centerup')
    txto.height = 5
    txto.angle = -45

    ln1 = x.createline()
    ln1.width = 3
    ln1.type = 'solid'
    ln1.color = colordic.get('Analysis', 1)
    ln1.x = [0.16, 0.209]   # x line positions
    ln1.y = [0.13, 0.13]    # y line positions
    text1x = []
    text1y = []
    pctypes = []

    fcstdirs = os.listdir(mpath)
    # remove the unwanted directories to be plotted
    for ex in exclude:
        if ex in fcstdirs:
            print "Omitted directory '%s' without doing plotting pcts" % ex
            fcstdirs.remove(ex)
        # end of if ex in fcstdirs:
    # end of for ex in exclude:
    # sort the directories of fcst hours in string
    fcstdirs = timeobj._sortFcstHours(fcstdirs)
    if sedate:
        fcstStartDates = xmlobj.findPartners('a', sedate[0], returnType='c')
        fcstEndDates = xmlobj.findPartners('a', sedate[-1], returnType='c')
        if fcstdirs[0].isalpha():
            fcstStartDates[fcstdirs[0]] = timeobj.timestr2comp(sedate[0])
            fcstEndDates[fcstdirs[0]] = sedate[-1]
        # end of if fcstdirs[0].isalpha():
    # end of if sedate:
    firstTimeAxis = None
    for i in [1, 2]:
        lnidx = 0
        lnx = 0.18
        lny = 0.13
        for dirname in fcstdirs:
            mtypepath = os.path.join(mpath, dirname)
            pc_ncfile = [fname for fname in os.listdir(mtypepath)
                if fname.endswith('.nc') and fname.startswith(ncfile_begin)]
            if not pc_ncfile:
                print "The path doesnt contain the nc file startswith('%s'). \
                       So skipping to extract pcts from '%s'" % (ncfile_begin, mtypepath)
                continue
            # end of if not pc_ncfile:
            f = cdms2.open(os.path.join(mtypepath, pc_ncfile[0]))

            # get the current fcst hour start end date w.r.t analysis start end date.
            if dirname.isdigit():
                # hours will be integer in the partners dates dictionary
                anl_fcst = int(dirname)
            else:
                anl_fcst = dirname
            # end of if dirname.isdigit():
            tperiod = (fcstStartDates[anl_fcst], fcstEndDates[anl_fcst])

            if i == 1:
                if sedate:
                    pcts = f(pcs1VarName, time=tperiod)
                else:
                    pcts = f(pcs1VarName)
                # end of if sedate:
            else:
                if sedate:
                    pcts = f(pcs2VarName, time=tperiod)
                else:
                    pcts = f(pcs2VarName)
                # end of if sedate:
                pcts = pcts * pcs2Sign
            # end of if i == 1:

            if not pctypes:
                firstTimeAxis = pcts.getTime()
                # pass the time axis to set the x label as dates.
                yx = _getYXTemplate(x, firstTimeAxis, tinterval)
                if stitle1 == 'date':
                    # get the start and end date of the analysis season
                    tcomp = firstTimeAxis.asComponentTime()
                    stime = str(tcomp[0]).split(' ')[0]
                    etime = str(tcomp[-1]).split(' ')[0]
                    stitle1 = 'Season : %s to %s' % (stime, etime)
                # end of if stitle1 == 'date':
            else:
                # resetting the timeAxis. So we can compare the pcts line plot.
                pcts.setAxis(0, firstTimeAxis)
            # end of if not pctypes:

            f.close()

            if i == 1:
                ypos = 0.605
            else:
                ypos = 0.235
            tlp = my_template[i-1]
            tlp.xlabel1.textorientation = txto
            tlp.xlabel1.texttable = tt
            tlp.xlabel1.y = ypos
            tlp.comment3.y = ypos - 0.03
            tlp.legend.priority = 0
            tlp.title.priority = 0
            tlp.yname.priority = 0
            if dirname == 'Analysis':
                name = 'Anl'
            elif dirname.isdigit():
                name = dirname + ' hr'
            else:
                name = dirname
            # end of if dirname == 'Analysis':

            pcts = numpy.ma.array(pcts.getValue())
            lncolor = colordic.get(name, 1)
            if (lnidx == 0):
                yx.linecolor = lncolor
                if (i == 1):
                    tlp.xname.y = 0.60
                    tlp.yname.y = 0.75
                    tlp.yname.x = 0.09
                    _y_name = y_name + str(i)
                    _comment_1 = 'a) ' + comment_1 + str(i)
                    pcts.id = _y_name
                    tlp.yname.priority = 0
                    tlp.comment2.x = 0.5
                    tlp.comment2.y = 0.97
                    tlp.comment2.textorientation = to1
                    tlp.comment2.texttable = tt
                    x.plot(pcts, yx, tlp, long_name='', title=title,
                            comment1=_comment_1, comment2=comment_2,
                            comment3=x_name, comment4='', yname=_y_name, bg=bg)
                    x.flush()
                else:
                    tlp.xname.y = 0.23
                    tlp.yname.x = 0.09
                    tlp.yname.y = 0.38
                    _y_name = y_name + str(i)
                    _comment_1 = 'b) ' + comment_1 + str(i)
                    pcts.id = _y_name
                    x.plot(pcts, yx, tlp, long_name='', title='',
                            comment1=_comment_1, comment2='',
                            comment3=x_name, yname=_y_name, bg=bg)
                    x.flush()
                # end of if (i == 1):
                x.plot(ln1, bg=bg)
                x.flush()
            else:
                pcts.id = ''
                yx.linecolor = lncolor
                tlp.yname.priority = 0
                x.plot(pcts, yx, tlp, long_name='', xname='', bg=bg)

                ln = x.createline()
                ln.width = 3
                ln.type = 'solid'
                ln.color = lncolor
                if lnidx == 6:
                    lny = 0.11
                    lnx = 0.30
                # end of if lnidx == 6:
                ln.x = [lnx, lnx + 0.04]
                ln.y = [lny, lny]
                x.plot(ln, bg=bg)
                x.flush()
            # end of if (lnidx == 0):
            del pcts
            lnidx = lnidx + 1
            if i == 1:
                pctypes.append(name)
                text1x.append(lnx + 0.05)
                text1y.append(lny)
            # end of if i == 1:
            lnx = lnx + 0.12
        # end of for dirname in xrange(len(variable_all)):
        zero_array = numpy.zeros(360, float)
        yx.linecolor = 1
        x.plot(zero_array, yx, tlp, bg=bg)
        x.flush()
    # end of for i in [1, 2]:

    text1 = x.createtext()
    text1.x = text1x
    text1.y = text1y
    text1.height = 7
    text1.color = 1
    text1.string = pctypes

    # draw the footer comment
    created_on = 'Created On : ' + time.strftime('%Y-%m-%d %H:%M:%S %Z')
    text2 = x.createtext()
    text2.x = [0.25, 0.45]
    text2.y = [0.04, 0.025]
    text2.height = 5
    text2.color = 1
    text2.string = [credits, created_on]
    text2.font = 6
    text2.spacing = 4

    # plot the sub title
    text3 = x.createtext()
    text3.x = [0.6]
    text3.y = [0.9]
    text3.height = 7
    text3.color = 1
    text3.string = [stitle1]
    text3.font = 4
    print "Going to plot text and all"
    x.plot(text1, bg=bg)
    x.plot(text2, bg=bg)
    x.plot(text3, bg=bg)
    x.flush()
    print "Let me save the plot"
    if pdf:        
        x.pdf(outfile + '.pdf')
        # Overwrite existing postscript file with a new postscript file
        #x.postscript(outfile + '.ps', 'r', 'p')
        #x.postscript_old(outfile + '.ps', 'r', 'p')
        #x.pdf(outfile + '.pdf', 'p')
        #x.gs(filename=outfile + '.pdf', device='pdfwrite', orientation='p', resolution='200x200')
    if png:
        x.png(outfile + '.png')
    x.clear()
    x.clean_auto_generated_objects()
# end of def plotPcts(...):



