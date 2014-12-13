import os
import sys
import cdms2
import cdutil
from wk_utils import genWKVars, plotWK_Sym_ASym
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diagnosisutils.timeutils import TimeUtility
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath

timeobj = TimeUtility()


def makeWKPlots(rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                 seasons=['sum', 'win'], segment=96, overlap=60, **kwarg):
    """
    Written By : Arulalan.T

    Date : 22.07.2013

    """

    year = kwarg.get('year', None)
    seasondic = {'all': 'All', 'sum': 'Summer', 'win': 'Winter', 'jjas': 'JJAS'}

    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])
    # end of if isinstance(year, int):

    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    opath = os.path.join(processfilesPath, 'Level2', 'WK', rawOrAnomaly,
                                         filteredOrNot, yearDir)
    imgpath = os.path.join(plotsgraphsPath, 'Level2', 'WK', rawOrAnomaly,
                                         filteredOrNot, yearDir)
    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        anofiles = [anofile for anofile in os.listdir(anopath)
                                    if not anofile.endswith('5x5.nc')]
        for afile in anofiles:
            varName = afile.split('_')[0]
            infile = os.path.join(anopath, afile)
            for season in seasons:
                seasonName = seasondic.get(season, 'season')
                outncpath = os.path.join(opath, subName, seasonName)
                outimgpath = os.path.join(imgpath, subName, seasonName)
                if not os.path.isdir(outncpath):
                    os.makedirs(outncpath)
                    print "The path has created ", outncpath
                # end of if not os.path.isdir(outncpath):
                if not os.path.isdir(outimgpath):
                    os.makedirs(outimgpath)
                    print "The path has created ", outimgpath
                # end of if not os.path.isdir(outimgpath):

                print "Collecting data %s for season %s" % (varName, season)
                if season == 'all':
                    f = cdms2.open(infile)
                    if year:
                        period = timeobj._getYearFirstLast(year)
                        anomalyData = f(varName, time=period)
                    else:
                        anomalyData = f(varName)
                    # end of if year:
                    f.close()
                elif season == 'sum':
                    anomalyData = timeobj.getSummerData(varName, infile, **kwarg)
                elif season == 'win':
                    anomalyData = timeobj.getWinterData(varName, infile, **kwarg)
                else:
                    raise ValueError("arg 'season' must be either 'all/sum/win' only")
                # end of if season == 'all':
                # setting the timebounds daily
                cdutil.setSlabTimeBoundsDaily(anomalyData)
                
                wkfile = 'wk_vars_%s_%s_%s_%s_%s.nc' % (seasonName,
                      yearDir, rawOrAnomaly, filteredOrNot, subName)
                # In genWKVars function wkfile name has been changed
                # w.r.t segment & overlap. So it should return the new
                # filename path after written nc file.
                wkfile = genWKVars(anomalyData, outpath=outncpath,
                   outfile=wkfile, segment=segment, overlap=overlap)

                output = '%s_%s_%s_%s_WK_Sym_ASym' % (varName, subName, seasonName, yearDir)
                plottitile = '%s - Multi Scale Metrics - Wheeler Kiladis Diagram' % (subName)
                comment_2 = 'Variable (Data) : %s (%s), Period : %s %s' % (varName,
                                                     subName, seasonName, yearDir)

                plotWK_Sym_ASym(wkfile, outpath=outimgpath, outfile=output,
                                ptitle=plottitile, comment_2=comment_2)
            # end of for season in seasons:
        # end of for afile in anofiles:
    # end of for subName in os.listdir(inpath):
# end of def makeWKPlots(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

#    year = (1979, 2005)
#    makeWKPlots('Anomaly', 'Filtered',  year, seasons=['sum', 'win', 'jjas'])

    year = 2004
    makeWKPlots('Anomaly', 'Filtered',  seasons=['sum', 'win'], year=year, cyclic=False)
    
    year = 2005
    makeWKPlots('Anomaly', 'Filtered',  seasons=['sum', 'win'], year=year, cyclic=True)

# end of if __name__ == '__main__':







