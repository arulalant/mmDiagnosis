import cdms2
from eofs import EEof
import os, sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../'))
# adding the previous path to python path
sys.path.append(previousDir)
from diagnosisutils.timeutils import TimeUtility
from diag_setup.globalconfig import processfilesPath
import diag_setup.netcdf_settings


timeobj = TimeUtility()


def genEEofVars(infiles, outfile, latitude=(-12.5, 30.5, 'ccb'), 
                                  longitude=(60.5, 95.5, 'ccb'), 
                          NEEOF=2, season='JJAS', year=None, **kwarg):

    """
    Written By : Arulalan.T
    Date : 26.10.2014
    """

    for name, varName, infile in infiles:
        if season == 'all':
            f = cdms2.open(infile)
            if year:
                # add the time axis year statements here in future.
                data = f(varName, time=year, latitude=latitude)
            else:
                data = f(varName, latitude=latitude)
            # end of if year:
        elif season.upper() == 'JJAS':
            data = timeobj.getSeasonalData(varName, infpath, sday=1, smon=6, 
                                        eday=30, emon=9, latitude=latitude, 
                                        longitude=longitude, year=year)
            
        else:
            raise ValueError("arg 'season' must be either 'all/jjas' only")
        # end of if season == 'all':

        data = data(squeeze=1)
        cdutil.setSlabTimeBoundsDaily(data)

        print "Doing EEOF of %s for %s" % (name, season)
        eeofobj = EEof(data, lag=15, weights=None, center=False, ddof=1)

       
        pcts = eeofobj.pcs(pcscaling=0, npcs=2)
        eeof_data = eeofobj.eeofs(neeofs=NEEOF, eeofscaling=2)
        per_exp = eeofobj.varianceFraction(neigs=NEEOF) * 100

        pcts.id = '_'.join(['pcs', name, season])
        pcts.comment = ''
        per_exp.id = '_'.join(['per_exp', name, season])
        per_exp.comment = ''
        eeof_data.id = '_'.join(['eeof', name, season])
        eeof_data.comment = ''

        out = cdms2.open(outfile, 'a')
        out.write(pcts)
        out.write(per_exp)
        out.write(eeof_data)
        out.close()

        # make memory free
        del data, pcts, per_exp, eeof_data
    # for name, varName, infile in infiles:
    print "Saved the eeof_vars_*.nc file in", outfile
# end of def genEEofVars(infiles, outfile, ...):


def makeGenEEofVars(rawOrAnomaly='Anomaly', filteredOrNot='Unfiltered',
                                 seasons=['jjas'], year=None):

    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    seasondic = {'jjas': 'JJAS', 'all': 'All'}

    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    opath = os.path.join(processfilesPath, 'miso', 'EEof', rawOrAnomaly,
                                         filteredOrNot, yearDir)
    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        anofiles = [anofile for anofile in os.listdir(anopath)
                                    if anofile.endswith('.nc')]
        file_input = []
        for afile in anofiles:
            varName = afile.split('_')[0]
            apath = os.path.join(anopath, afile)
            file_input.append((varName, varName, apath))
         #end of for afile in anofiles:

        for sea in seasons:
            seasonName = seasondic.get(sea, 'season')
            outpath = os.path.join(opath, subName, seasonName)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "The path has created ", outpath
            # end of if not os.path.isdir(outpath):

            # creating individula nc files for each season, since
            # we cant overwrite the timeaxis in same nc file.
            outfile = 'eeof_vars_%s_%s_%s_%s_%s.nc' % (seasonName,
                   yearDir, rawOrAnomaly, filteredOrNot, subName)
            file_output = os.path.join(outpath, outfile)
            genEofVars(file_input, file_output, season=sea, year=year)
        # end of for sea in seasons:
    # end of for subName in os.listdir(inpath):
# end of def makeGenEofVars(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    year = (1979, 2005)
    makeGenEEofVars('Anomaly', 'Unfiltered',  year=year)

    year = 2005
    makeGenEEofVars('Anomaly', 'Unfiltered',  year=year)

# end of if __name__ == '__main__':


