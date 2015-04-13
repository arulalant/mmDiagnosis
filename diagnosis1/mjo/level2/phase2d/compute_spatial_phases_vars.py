import cdms2
import numpy as np
import os, sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diagnosisutils.timeutils import TimeUtility
from diag_setup.globalconfig import processfilesPath
import diag_setup.netcdf_settings


timeobj = TimeUtility()


def getLifeCycleCompositeVars(data, amplitudes, phases, name='',
                                    season='', returnNDays=True):
    """

    data : Seasonal Variable data eg : olr or u200 or u850

    Updated Date : 10.06.2013
    """

    data = data(squeeze=1)
    lat = data.getLatitude()
    lon = data.getLongitude()
    timeAxis = data.getTime()
    time_range = timeAxis[:]

    com = np.zeros((len(lat), len(lon), 8), dtype=np.float32)
    n_com = np.zeros((len(lat), len(lon), 8), dtype=np.float32)
    ndays = np.zeros(8, dtype=np.float32)

    print "Computing no_days in each phases"
    for t in time_range:
        if (amplitudes(time=t)[0] > 1):
            phase_no = phases(time=t)[0]
            ndays[phase_no - 1] = ndays[phase_no - 1] + 1
            com[:, :, phase_no - 1] = com[:, :, phase_no - 1] + data(time=t)
            n_com[:, :, phase_no - 1] = n_com[:, :, phase_no - 1] + 1
        # end of if (amplitudes(time=t)[0] > 1):
    # end of for t in time_range:

    # make memory free
    del data, amplitudes, phases

    for ph in range(8):
        com[:, :, ph] = com[:, :, ph] / n_com[:, :, ph]
    # end of for ph in range(8):

    # generate phase axis
    phase_axis = np.array(range(1, 9), dtype=np.float32)
    phase_axis = cdms2.createAxis(phase_axis, id='phase')

    # generate the life cycle composite variable
    com = cdms2.createVariable(com, dtype=np.float32)
    com.id = '_'.join(['cc', name, season])
    com.long_name = "cycle_composite_%s_%s" % (name, season)
    com.setAxisList([lat, lon, phase_axis])
    com.comment = "Life Cycle Composite of %s %s complete" % (name, season)

    if not returnNDays:
        return com
    else:
        ndays = cdms2.createVariable(ndays)
        ndays.id = '_'.join(['n', 'days', name, season])
        ndays.long_name = "number of days in each phase in %s" % season
        ndays.comment = ''
        ndays.setAxisList([phase_axis])
        return com, ndays
    # end of if not returnNDay:
# end of def getLifeCycleCompositeVars(data, amplitudes, phases,...):


def genSpatialPhaseVars(infiles, amppha, outfile, lat=(-15, 15, 'cob'),
                                               season='all', **kwarg):
    """

    Updated Date : 10.06.2013

    """
    cyclic = kwarg.get('cyclic', True)
    year = kwarg.get('year', None)

    ampPhaVar, ampPhaFile = amppha
    out = cdms2.open(outfile, 'a')

    for name, varName, infile in infiles:
        print "Collecting %s data for season %s" % (name, season)
        if season == 'all':
            f = cdms2.open(infile)
            f1 = cdms2.open(ampPhaFile)
            if year:
                period = timeobj._getYearFirstLast(year)
                data = f(varName, time=period, latitude=lat)
                amphaData = f1(ampPhaVar, time=period)
            else:
                data = f(varName, latitude=lat)
                amphaData = f1(ampPhaVar)
            # end of if year:
            #f.close()
            f1.close()
        elif season == 'sum':
            print "Sumer"
            data = timeobj.getSummerData(varName, infile, latitude=lat, **kwarg)
            amphaData = timeobj.getSummerData(ampPhaVar, ampPhaFile, **kwarg)
        elif season == 'win':
            print "Winter"
            data = timeobj.getWinterData(varName, infile, latitude=lat,
                                                cyclic=cyclic, **kwarg)
            amphaData = timeobj.getWinterData(ampPhaVar, ampPhaFile,
                                                cyclic=cyclic, **kwarg)
        else:
            raise ValueError("arg 'season' must be either 'all/sum/win' only")

        amplitudes = amphaData[:, 0]
        phases = amphaData[:, 1]

        # make memory free
        del amphaData
        # get the life cycle composite and no of days in each phases variables
        ccom, ndays = getLifeCycleCompositeVars(data, amplitudes, phases,
                                            name, season, returnNDays=True)

        # make memory free
        del data

        # write into nc file
        out.write(ndays)
        out.write(ccom)

        # make memory free
        del ndays, ccom
        finish_comment = "Life cycle Composite of %s %s complete" % (season, name)
        print finish_comment
    # end of for name, varName, infile in infiles:
    out.close()
    print "Written Life cycle Composite vars into nc file", outfile
# end of def genSpatialPhaseVars(infiles, amppha, outfile, ...):


def makeSpatialPhaseVars(rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                         seasons=['sum', 'win'], seasonDir='All', **kwarg):
    """
    Written By : Arulalan.T

    Date : 22.07.2013

    """

    year = kwarg.get('year', None)
    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    seasondic = {'sum': 'Summer', 'win': 'Winter', 'all': 'All'}
    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    opath = os.path.join(processfilesPath, 'Level2', 'Ceof', rawOrAnomaly,
                                                  filteredOrNot, yearDir)

    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        anofiles = [anofile for anofile in os.listdir(anopath)
                             if not anofile.endswith('5x5.nc')]
        file_input = []
        for afile in anofiles:
            varName = afile.split('_')[0]
            apath = os.path.join(anopath, afile)
            file_input.append((varName, varName, apath))
        # end of for afile in anofiles:

        for sea in seasons:
            seasonName = seasondic.get(sea, 'season')
            amppath = os.path.join(opath, subName, seasonDir)
            outpath = os.path.join(opath, subName, seasonName)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "The path has created ", outpath
            # end of if not os.path.isdir(outpath):
            print "Doing Life Cycle Composite For", seasonName, yearDir

            ampfile = 'amppha_of_pcs_1_2_of_ceof_%s_%s_%s_%s_%s.nc' % (
                 seasonDir, yearDir, rawOrAnomaly, filteredOrNot, subName)
            ampfilepath = os.path.join(amppath, ampfile)
            ampvar = ampfile.split('_')[0]
            amppha_input = (ampvar, ampfilepath)
            if not os.path.isfile(ampfilepath):
                print "The ampfilepath is not exists ", ampfilepath
                print "So skipping creating cycle_composite files..."
                continue
            # end of if not os.path.isdir(outpath):
            # creating individual nc files for each season, since
            # we cant overwrite the timeaxis in same nc file.
            outfile = 'cycle_composite_%s_%s_%s_%s_%s.nc' % (seasonName,
                          yearDir, rawOrAnomaly, filteredOrNot, subName)
            file_output = os.path.join(outpath, outfile)
            if os.path.isfile(file_output):
                os.remove(file_output)
                print "The file already exists, so removed it. Lets recreate it", file_output
            # end of if os.path.isfile(file_output):
            genSpatialPhaseVars(file_input, amppha_input, file_output,
                                                  season=sea, **kwarg)
        # end of for sea in seasons:
    # end of for subName in os.listdir(inpath):
# end of def makeSpatialPhaseVars(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    year = (1979, 2005)
    makeSpatialPhaseVars('Anomaly', 'Filtered',  year=year)

    year = 2005
    makeSpatialPhaseVars('Anomaly', 'Filtered',  year=year)
# end of if __name__ == '__main__':


