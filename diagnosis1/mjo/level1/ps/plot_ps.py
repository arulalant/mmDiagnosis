import os
import sys
import xmgrace
from psutils import powerSpectrum, summerPowerSpectrum, winterPowerSpectrum
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath


seasondic = {'sum': 'Summer', 'win': 'Winter', 'all': 'All'}


def plotPowerSpectrum(xdata, ydata, outfile, xname='Frequency(cycles/day)',
              yname='Power X Frequency', title='WP WINTER', pdf=0, jpeg=1):
    """

    Written by : Alok Singh, Arulalan.T

    Date : 10.01.2013

    """

    x = xmgrace.init()
    x.landscape()
    # Set the area of graph
    x.Graph[0].vymin = .1
    x.Graph[0].vymax = .9
    x.Graph[0].vxmin = .1
    x.Graph[0].vxmax = .9
    # Set the title and lable the axis
    x.Graph[0].title = title
    x.Graph[0].xaxis.label = xname
    x.Graph[0].yaxis.label = yname
    # set the min ans max for the X and  Y axis
    x.Graph[0].yaxis.min = 0
    x.Graph[0].yaxis.max = 3.5
    x.Graph[0].xaxis.min = 0.005
    x.Graph[0].xaxis.max = .51
    x.Graph[0].xaxis.scale = 'logarithmic' # x-axis lograthmic scale
    # Adding sets tp graph 0
    x.add_set(0)
    x.add_set(0)
    x.add_set(0)
    # Setting line colour , style and weidth for all sets
    x.Graph[0].Set[0].line.color = 4
    x.Graph[0].Set[1].line.color = 'red'
    x.Graph[0].Set[2].line.color = 'red'
    x.Graph[0].Set[3].line.color = 4
    x.Graph[0].Set[0].line.linewidth = 1.5
    x.Graph[0].Set[1].line.linewidth = .5
    x.Graph[0].Set[2].line.linewidth = .5
    x.Graph[0].Set[3].line.linewidth = 1.5
    x.Graph[0].Set[0].legend = ''
    x.Graph[0].Set[0].line.linestyle = 'solid'
    x.Graph[0].Set[1].line.linestyle = 'dash'
    x.Graph[0].Set[2].line.linestyle = 'dash'
    x.Graph[0].Set[3].line.linestyle = 'solid'
    # Plotting Rednoise , Significance levels & power  Vs Frequency
    # Here ydata = power_freq, xdata = frequency.
    x.plot([ydata], xs=[xdata])

    if pdf: x.pdf(outfile + '.pdf')
    if jpeg: x.jpeg(outfile + '.jpeg')
# end of def plotPowerSpectrum(xdata, ydata, outfile, ...):


def doPlotPowerSpectrum(rawOrAnomaly, filteredOrNot, year,
                            seasons=['sum', 'win'], pdf=0, jpeg=1):

    """

    Written By : Arulalan.T

    Date : 22.07.2013

    """

    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    inpath = os.path.join(processfilesPath, 'Average', 'Area',
                                    rawOrAnomaly, filteredOrNot)

    for subName in os.listdir(inpath):
        varpath = os.path.join(inpath, subName)
        opath = os.path.join(plotsgraphsPath, 'Level1', 'PowerSpectrum',
                                rawOrAnomaly, filteredOrNot, yearDir)
        for varName in os.listdir(varpath):
            anopath = os.path.join(varpath, varName)
            for anofile in os.listdir(anopath):
                anofilelist = anofile.split('.')[0].split('_')
                regionName = anofilelist[-1]
                anoFilePath = os.path.join(anopath, anofile)
                for season in seasons:
                    seasonName = seasondic.get(season, 'season')
                    outpath = os.path.join(opath, subName, varName, seasonName)
                    if not os.path.isdir(outpath):
                        os.makedirs(outpath)
                        print "Path has created ", outpath
                    # end of if not os.path.isdir(outpath):
                    title = '%s %s %s %s %s %s' % (seasonName, subName, yearDir,
                                 varName.upper(), regionName, filteredOrNot)
                    outfile = '%s_%s_%s_%s_%s_%s_%s_ps' % (varName, seasonName, subName,
                            yearDir, filteredOrNot, rawOrAnomaly, regionName)
                    imgpath = os.path.join(outpath, outfile)
                    if pdf:
                        imgpath_ext = imgpath + '.pdf'
                    else:
                        imgpath_ext = imgpath + '.jpeg'
                    # end of if pdf:
                    if os.path.isfile(imgpath_ext):
                        print "The image file already exists in the path ", imgpath
                        print "So skipping summerVariance"
                    else:
                        if season in ['sum']:
                            # summer
                            power, frequency = summerPowerSpectrum(varName,
                                                        anoFilePath, year=year)
                        elif season in ['win']:
                            # winter
                            power, frequency = winterPowerSpectrum(varName,
                                                     anoFilePath, year=year)
                        # end of if season in ['sum']:
                        
                        power_freq = power * frequency
                        # plot frequency in x-axis Vs power_freq
                        # in y-axis of any 2-D plot
                        plotPowerSpectrum(xdata=frequency, ydata=power_freq,
                            outfile=imgpath, title=title, pdf=pdf, jpeg=jpeg)
                        # make memory free
                        del power_freq, power, frequency
                    # end of if os.path.isfile(imgpath_ext):
                # end of for season in seasons:    
            # end of for anofile in os.listdir(anopath):
        # end of for varName in os.listdir(varpath):
    # end of for subName in os.listdir(inpath):
# end of def doPlotPowerSpectrum(rawOrAnomaly, filteredOrNot, year):


if __name__ == '__main__':

    year = (1979, 2005)
    doPlotPowerSpectrum('Anomaly', 'Unfiltered', year)
    year = 2005
    doPlotPowerSpectrum('Anomaly', 'Unfiltered', year)

# end of if __name__ == '__main__':



