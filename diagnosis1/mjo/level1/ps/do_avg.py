import os
import sys
import cdms2
from psutils import areaAvg, zonalAvg
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from uv_cdat_code.diagnosisutils.regions import regions
from diag_setup.globalconfig import processfilesPath
import diag_setup.netcdf_settings


def doAreaAvg(rawOrAnomaly='Anomaly', filteredOrNot='Unfiltered',
                            regionsList=['IO', 'WP', 'BB', 'MC']):

    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    opath = os.path.join(processfilesPath, 'Average', 'Area',
                                    rawOrAnomaly, filteredOrNot)

    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        for anofile in os.listdir(anopath):
            anofilename = anofile.split('.')[0] + '_avg_'
            varName = anofilename.split('_')[0]
            anoFilePath = os.path.join(anopath, anofile)
            outpath = os.path.join(opath, subName, varName)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "Path has created ", outpath
            # end of if not os.path.isdir(outpath):
            for regionName in regionsList:
                regionObj = regions.get(regionName, None)
                #print regionObj
                if not regionObj:
                    print "regionName '%s' is not available in regions dictionary" % regionName
                    print "So Skipping with out doing areaAvg for this region"
                    continue
                # end of if not regionObj:
                avgData = areaAvg(varName, anoFilePath, region=regionObj)
                avgfile = anofilename + regionName + '.nc'
                avgfilepath = os.path.join(outpath, avgfile)
                f = cdms2.open(avgfilepath, 'w')
                f.write(avgData)
                f.close()
                print "The areaAvg file has created in ", avgfilepath
                # make memory free
                del avgData
            # end of for regionName in regionsList:
        # end of for anofile in os.listdir(anopath):
    # end of for subName in os.listdir(inpath):
# end of def doAreaAvg(rawOrAnomaly='Anomaly', ...):


def doZonalAvg(rawOrAnomaly='Anomaly', filteredOrNot='Unfiltered', lat=(-10, 10)):

    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    opath = os.path.join(processfilesPath, 'Average', 'Zonal',
                                    rawOrAnomaly, filteredOrNot)

    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        outpath = os.path.join(opath, subName)
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
            print "Path has created ", outpath
        # end of if not os.path.isdir(outpath):
        for anofile in os.listdir(anopath):
            anofilename = anofile.split('.')[0] + '_10N_10S' # have to make it w.r.t input lat
            varName = anofilename.split('_')[0]
            anoFilePath = os.path.join(anopath, anofile)

            avgData = zonalAvg(varName, anoFilePath, latitude=lat)
            avgfile = anofilename + '_zm' + '.nc'
            avgfilepath = os.path.join(outpath, avgfile)
            f = cdms2.open(avgfilepath, 'w')
            f.write(avgData)
            f.close()
            print "The areaAvg file has created in ", avgfilepath
            # make memory free
            del avgData
        # end of for anofile in os.listdir(anopath):
    # end of for subName in os.listdir(inpath):
# end of def doZonalAvg(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    doAreaAvg()
    doZonalAvg()

# end of if __name__ == '__main__':




