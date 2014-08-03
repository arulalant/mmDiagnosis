"""
.. module:: generate_statistical_score_bars.py
   :synopsis: This script do plotting the bargraphs of the various statistical
              score versus threshold in XMGRACE.
.. moduleauthor:: Dileepkumar R <dileepkunjaai@gmail.com>,
                  Arulalan.T <arulalant@gmail.com>

Date : 04.08.2011

Updated on : 28.09.2011

"""

import os
import sys
import numpy
import numpy.ma
import cdms2
from genutil import xmgrace
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__diagnosisDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__diagnosisDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
# importing plot.py, xml_data_acces.py, TimeUtility from previous directory
# uv_cdat_code.diagnosisutils
import uv_cdat_code.diagnosisutils.xml_data_access as xml_data_access
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility
from uv_cdat_code.diagnosisutils import numutils
from diag_setup.globalconfig import  threshold, processfilesPath, \
                               plotsgraphsPath, seasons
from diag_setup.varsdict import variables
from diag_setup.gendir import createDirsIfNotExists

# create time utility object
timobj = TimeUtility()

regions = {'CIndia': 'Central India [73-90E, 22-28N]',
            'PenIndia': 'Peninsular India [74-85E, 7-21N]',
            'WcstIndia': 'West Coast [70-78E, 10-20N]',
            'AIR': 'All India [67-100 E, 7-37N]'}



def genBarDiagrams(var, multiData, hours, outpath=None, bargap=0.25, barwidth=1,
                                                             yticdiff=0.25):
    """
    :func:`genBarDiagrams`: It should generate the least directory hierarichy
        structure of season statiscore in the plotsgraphspath by score name.
        It will plots score values in xmgrace as bar diagram and save it
        inside the appropirate directory, by reading the nc file of the
        appropirate process season Region statiscore files path.

        It should plot for all the vars of that statiscore nc files.

    Inputs : var is the variable name. If var is 'all' means, then it should
             plot the bar diagram for all the available variables in the passed
             path nc or xml file.

             path is an absolute nc or xml file path.

             outpath is the path to store the images. If it is None means, it
             should create the least (plotname)directory in the current
             directory path itself and save it.

             bargap is the value of the gap ratio in between each bars of each
             threshold in xaxis of score bar diagram.

             barwidth is the width of the each bar in xaxis of the score
             bar diagram.

             yticdiff is the difference of the tic levels in y axis of the
             bar diagram.


    Written By : Dileep Kumar.R, Arulalan.T

    Updated on : 28.09.2011

    """

    

    # year
    year = '2010'
    # region
    regionName = 'AIR'
    seamon = 'JJAS'
    allvars = None
    if var == 'all':
        # var is all. So we have to take all the vars from passed ncpath.
        allvars = [var for var in f.listvariable() if not var.startswith('bounds')]
    else:
        if isinstance(var, list):
            allvars = var
        else:
            allvars = [var]

    if not outpath:
        # get the current workig directory
        outpath = os.getcwd()

    # setting some intelligent to set xaxis values and its labels depends on
    # no of threshold dynamically
    xdic = {}
    xval = []
    sno = 0
    i = 0
    while(i< len(hours)):
        if sno % 2:
            # set xaxis threshold string
            xdic[sno] = str(hours[i])
            i += 1
            xval.append(sno)
        else:
            # set xaxis empty string
            xdic[sno] = ''
        # end of if sno % 2:
        sno += 1
    # end of while(i< len(threshold)):
    # set final xaxis empty string
    xdic[sno] = ''
    # xaxis numpy value
    xval = numpy.array(xval)
    # xlist to set xaxis scales min, max value in xmgrace
    xlist = xdic.keys()
    xlist.sort()
    
    models = multiData.keys()
    models.sort()
    # make hours as int type and do sort
    #hours = [int(hr) for hr in hours]
    #hours.sort()
    # calculation and generating x axis shift alignments scales for
    # multiple hours bar for single threshold.
    # i.e. setting gap b/w each vertical bar for all the threshold(xaxis)bars
    rem = len(models) / 2
    leng = rem * bargap
    bar_shift_list = numpy.arange(-leng, leng + bargap, bargap)
    bar_shift_list = [round(shift, 3) for shift in bar_shift_list]
    if len(hours) < len(bar_shift_list):
        centerindex = len(bar_shift_list) / 2
        bar_shift_list.remove(bar_shift_list[centerindex])
    # end of if len(hours) < len(bar_shift_list):

    # make fcst hour name in legend
    legendNames = []
    for m in models:
        legendNames.append(m)
    # end of for hr in hours:

    # colorList is the list of colors of different bars corresponds
    # to forcast hours
    colorList = ['black', 'red', 'green', 'orange', 'maroon', 'blue', '	turquoise']
    org_yticdiff = yticdiff
    for varName in allvars:
        scoreName = varName.upper()
        # make reduce the yaxis tic lables for some scores
        if scoreName in ['ODR']:
            org_yticdiff = yticdiff
            yticdiff = yticdiff * 2
        else:
            # for other scores maintain the function definition value for
            # yticdiff variable
            yticdiff = org_yticdiff
        # create plot name directory if it is not exists
        scoreNamePath = createDirsIfNotExists(outpath, scoreName)
        # get the score data
        #score = f(varName)

        score = multiData['T254']

        title_string = 'Threat Score (3.0 Threshold)'

        for model in multiData:
            score = multiData[model]
            # for condition checking purpose we get the data alone.
            nscore = numpy.array(score)

            # setting y axis min and max values depends upon the min, max of score
            if (numpy.min(nscore) < 0):
                Y_axis_min = int(numpy.min(nscore)) - yticdiff
            else:
                Y_axis_min = 0
            # end of if (numpy.min(nscore) < 0):
            if (numpy.max(nscore) > 1):
                Y_axis_max = int(numpy.max(nscore)) + 1
            else:
                Y_axis_max = 1
            # end of if (numpy.max(nscore) > 1):

            # setting y axis lables dynamically by find round max of score
            if Y_axis_max >= 1e+20:
                Y_second_max = numutils.nextmax(nscore)
                ydicmax = round(Y_second_max, 2)
            else:
                # change the max level into next to make good view in y axis
                Y_axis_max = Y_axis_max + yticdiff
                ydicmax = Y_axis_max
            ydicmax = (ydicmax-(ydicmax % yticdiff)) + yticdiff
            # get the min value of score
            ydicmin = nscore.min()

            if ydicmin < 0:
                if ydicmin == -1e+20:
                    ydicmin = numutils.nextmin(nscore)
                # -ve value
                # adjust min value by rounding w.r.t yticdiff
                Y_axis_min = (ydicmin-(ydicmin % yticdiff)) - yticdiff
            else:
                Y_axis_min = 0
            Y_second_min = ydicmin
            # generate the ydic values
            ydicval = numpy.arange(Y_axis_min, ydicmax + yticdiff, yticdiff)

        ydic = {}
        for val in ydicval:
            ydic[val] = str(val)
        # setting some intelligent to set infinity in y axis label with
        # one interval after the second max of y axis
        if Y_axis_max >= (1e+20) or Y_axis_min <= (-1e+20):
            # setting infinity value
            ydicindex = ydic.keys()
            ydicindex.sort()
            for y in ydicindex:
                if y >= Y_second_max:
                    Y_axis_max = y + yticdiff
                    # add one more y axis label at next to next max val
                    # of yaxis scale
                    ydic[Y_axis_max] = str(Y_axis_max)
                    # set yaxis max val in yaxis lable for infinity case
                    Y_axis_max += yticdiff
                    # break
                # end of if y >= Y_second_max:
                if y <= Y_second_min:
                    Y_axis_min = y - yticdiff
                    # add one more y axis label at next to next max val
                    # of yaxis scale
                    ydic[Y_axis_min] = str(Y_axis_min)
                    # set yaxis max val in yaxis lable for infinity case
                    Y_axis_min -= yticdiff
                # end of if y >= Y_second_max:
            # end of for y in ydicindex:
            # change the y axis max val label by 'Infinity' for 1e+20 val in
            # score value
            ydic[Y_axis_max] = 'Infinity'
            ydic[Y_axis_min] = '-Infinity'
        # end of if Y_axis_max >= (1e+20):

        x = xmgrace.init()
        x.Graph[0].vymin = .20
        x.Graph[0].vymax = .90
        x.Graph[0].vxmin = .15
        x.Graph[0].vxmax = .88
        x.Graph[0].bar_hgap = 1
        x.Graph[0].status = 'on'

        x.Graph[0].title = title_string + ' ' + year
        x.Graph[0].stitle = regions.get(regionName) + ' ' + seamon
        # ymin for graph 0
        x.Graph[0].yaxis.min = Y_axis_min
        # ymax for graph 0
        x.Graph[0].yaxis.max = Y_axis_max
        # Main tick every unit
        x.Graph[0].yaxis.tick.inc = 1
        # 4 sub in between, 1 every .25 units
        x.Graph[0].yaxis.tick.minor_ticks = 1
        x.Graph[0].yaxis.bar.status = 'on'
        # setting min value of x axis
        x.Graph[0].xaxis.min = xlist[0]
        # setting max value of x axis
        x.Graph[0].xaxis.max = xlist[-1]

        x.Graph[0].xaxis.tick.spec.loc = xdic
        x.Graph[0].xaxis.tick.label.char_size = .6
        x.Graph[0].xaxis.tick.orientation = 'out'
        x.Graph[0].xaxis.label = 'Forecast Hours'
        x.Graph[0].yaxis.tick.spec.loc = ydic
        x.Graph[0].yaxis.tick.label.char_size = .6
        x.Graph[0].yaxis.tick.orientation = 'out'

        x.Graph[0].yaxis.label = 'Threat Score'
        x.Graph[0].legend.char_size = .7
        x.Graph[0].legend.x = .9  # Legend at 90% in x
        x.Graph[0].legend.y = .8  # Legend at 80% in y

        for setno in range(len(models)):
            if setno != 0:
                x.add_set(0)
            # set bar type
            x.Graph[0].Set[setno].type = 'bar'
            # Set width of bar
            #x.Graph[0].Set[setno].symbol.size = 1.03
            x.Graph[0].Set[setno].symbol.size = barwidth
            # Set Color
            x.Graph[0].Set[setno].fill.color = colorList[setno]
            # Switch offing the line which connected on all the bars top edge
            x.Graph[0].Set[setno].line.type = 0
            # Setting the legend
            x.Graph[0].Set[setno].legend = legendNames[setno]
            # add the bar_shift_list elements to all the element of threshold
            xshiftval = xval + bar_shift_list[setno]
            # x axis values
            xshiftval = numpy.ma.array(xshiftval)
            # y axis values
            score = multiData[models[setno]]
            yval = numpy.ma.array(score).squeeze()
            # Some statistical score takes values -1e+20, for plotting itmakes
            # some problem, threfore we are going to change -1e+20 as 0
            # (Theoriticaly it is not correct)
            # yval = numpy.ma.where(yval !=-1e+20, yval, 0)
            yval = numpy.ma.where(yval !=-1e+20, yval, Y_axis_min)
            # plot in xmgrace in the corresponding set of graph
            print yval, xshiftval
            x.plot(yval, xshiftval, G = 0, S = setno)
            x.update()
        # end of for setno in range(len(hours)):

        output_filename = "Test.jpg" 
        #output_filename = scoreNamePath + '/' + output_filename
        x.jpeg(output_filename, color = 'color', quality = 80, dpi = 300,
                                         smoothing = 0, baseline = 'off')
    # end of for var in allvars:
    f.close()
# end of def genBarDiagrams(var, path, hours, outpath=None):




path = '/home/dileep/myrepo1/multi_bar'

files = ['statistical_score_AIR_jjas_2010_CMA.nc',
'statistical_score_AIR_jjas_2010_CPTEC.nc',
'statistical_score_AIR_jjas_2010_ECMWF.nc',
'statistical_score_AIR_jjas_2010_KMA.nc',
'statistical_score_AIR_jjas_2010_T254.nc']



all_models = {}
for fi in files:
   f = cdms2.open(path + '/' + fi)
   data = f('ts', threshold = 3.0)
   modelname = fi.split('_')[-1].split('.')[0]
   all_models[modelname] = data
   f.close()
   
genBarDiagrams('ts', all_models, [24,48,72,96,120])
