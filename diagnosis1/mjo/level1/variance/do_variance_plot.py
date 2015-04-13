import os
import sys
import cdms2
import vcs
from variance_utils import plotVariance, summerVariance, winterVariance, calculateVariance
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath


seasondic = {'sum': 'Summer', 'win': 'Winter', 'all': 'All'}


def doPlotVariance(rawOrAnomaly, filteredOrNot, year,
                    seasons=['all', 'sum', 'win'], pdf=1, png=0):

    """
    filteredOrNot - It takes either 'Unfiltered' or 'Filtered'.
                    This is used to complete the path of the
                    anomaly files and to complete the plot title.

    rawOrAnomaly - Have to set proper path of the raw data to enable it.

    seasons : It takes list. By default ['all', 'sum', 'win']

    year - used to extract the needed data from anomaly and then
           it will be plotted. It could be even tuple to indicate
           range of years. By default it takes None. i.e. It will do
           plotVariance for the whole available years.

    Date : 06.07.2013
    """
    v = vcs.init()
    rawOrAnomaly = 'Anomaly'
    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)

        imgyearpath = os.path.join(plotsgraphsPath, 'Level1', 'Variance',
                            rawOrAnomaly, filteredOrNot, yearDir)
        ncyearpath = os.path.join(processfilesPath, 'Level1', 'Variance',
                          subName, rawOrAnomaly, filteredOrNot, yearDir)
        for anofile in os.listdir(anopath):
            varName = anofile.split('_')[0]
            anoFilePath = os.path.join(anopath, anofile)
            for season in seasons:
                seasonName = seasondic.get(season, 'season')
                # summer
                outpath = os.path.join(imgyearpath, subName, seasonName)
                if not os.path.isdir(outpath):
                    os.makedirs(outpath)
                    print "Path has created ", outpath
                # end of if not os.path.isdir(outpath):
                ncpath = os.path.join(ncyearpath, seasonName)
                if not os.path.isdir(ncpath):
                    os.makedirs(ncpath)
                    print "Path has created ", ncpath
                # end of if not os.path.isdir(ncpath):

                title = '%s %s %s %s %s' % (seasonName, subName, yearDir,
                                         varName.upper(), filteredOrNot)
                outfile = '%s_%s_%s_%s_%s_%s_variance' % (varName, seasonName,
                              subName, yearDir, filteredOrNot, rawOrAnomaly)
                imgpath = os.path.join(outpath, outfile)
                if pdf:
                    imgpath_ext = imgpath + '.pdf'
                else:
                    imgpath_ext = imgpath + '.png'
                # end of if pdf:
                if os.path.isfile(imgpath_ext):
                    print "The image file already exists in the path ", imgpath
                    print "So skipping summerVariance"
                else:
                    if season in ['sum']:
                        varianceData = summerVariance(varName, anoFilePath, year=year)
                    elif season in ['win']:
                        varianceData = winterVariance(varName, anoFilePath,
                                                cyclic=True, year=year)
                    elif season in ['all']:
                        varianceData = calculateVariance(varName, anoFilePath,
                                                    speed=False, year=year)
                    # end of if season in ['sum']:

                    plotVariance(varianceData, outfile=imgpath,
                               season=season, title=title, x=v,
                                               pdf=pdf, png=png)
                    # write into nc file.
                    ncfile = os.path.join(ncpath, outfile)
                    f = cdms2.open(ncfile + '.nc', 'w')
                    f.write(varianceData)
                    f.close()
                    # make memory free
                    del varianceData
                # end of if os.path.isfile(imgpath_ext):
            # end of for season in seasons:
        # end of for anofile in os.listdir(anopath):
    # end of for subName in os.listdir(inpath):
    # make memory free
    del v
# end of def doPlotVariance(filteredOrNot, year, ...):


if __name__ == '__main__':

    year = (1979, 2005)
    doPlotVariance('Anomaly', 'Unfiltered', year)
    doPlotVariance('Anomaly', 'Filtered',  year)

    year = 2005
    doPlotVariance('Anomaly', 'Unfiltered', year, seasons=['sum', 'win'])
    doPlotVariance('Anomaly', 'Filtered', year, seasons=['sum', 'win'])
# end of if __name__ == '__main__':



