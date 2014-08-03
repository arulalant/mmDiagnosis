import cdms2
import cdutil
from math import pi, cos
from eof2 import Eof
import pickle
import os, sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility
from diag_setup.globalconfig import processfilesPath
import diag_setup.netcdf_settings


timeobj = TimeUtility()


def _coslat_weights(latitude):
    """Square-root of cosine of latitude weights.

    *latdim*
       Latitude dimension values.

    """
    return [cos(lat * pi / 180.) for lat in latitude]
# end of def _coslat_weights(latitude):


def genEofVars(infiles, outfile, eobjf=True, latitude=(-30, 30, 'cob'),
                          NEOF=4, season='all', year=None, **kwarg):

    """

    """
    eofobj_endname = kwarg.get('eofobj_endname', None)

    for name, varName, infile in infiles:
        if season == 'all':
            f = cdms2.open(infile)
            if year:
                # add the time axis year statements here in future.
                data = f(varName, time=year, latitude=latitude)
            else:
                data = f(varName, latitude=latitude)
            # end of if year:
        elif season == 'sum':
            data = timeobj.getSummerData(varName, infile, latitude=latitude,
                                                                 year=year)
        elif season == 'win':
            data = timeobj.getWinterData(varName, infile, latitude=latitude,
                                                 year=year, cyclic=True)
        else:
            raise ValueError("arg 'season' must be either 'all/sum/win' only")
        # end of if season == 'all':

        data = data(squeeze=1)
        cdutil.setSlabTimeBoundsDaily(data)

        print "Multiplying coslat with data of %s for %s" % (name, season)
        lat = data.getLatitude()
        coslat = _coslat_weights(lat)
        for l in range(len(lat)):
            data[:, l] *= coslat[l]
        # end of for l in range(len(lat)):
        print "Doing EOF of %s for %s" % (name, season)
        eofobj = Eof(data, weights=None)

        if eobjf:
            # generate the eofobj binary file name and its path
            path = os.path.dirname(outfile)
            eofobj_filename = ['eofobj', 'level1', name, season]
            eofobj_filename = '_'.join(eofobj_filename)
            if eofobj_endname: eofobj_filename += '_' + eofobj_endname
            eofobj_filename += '.pkl'
            # end of if not eofobj_filename:
            eofobj_fpath = os.path.join(path, eofobj_filename)
            # store the eofobj into binary file using pickle module
            objf = open(eofobj_fpath, 'wb')
            pickle.dump(eofobj, objf, 2)
            comment = ''
            pickle.dump(comment, objf, 2)
            objf.close()
            print "Saved the eofobj in", eofobj_fpath
        # end of if eobjf:

        pcts = eofobj.pcs(pcscaling=0, npcs=2)
        eof_data = eofobj.eofs(neofs=NEOF, eofscaling=2)
        per_exp = eofobj.varianceFraction(neigs=NEOF) * 100

        pcts.id = '_'.join(['pcs', name, season])
        pcts.comment = ''
        per_exp.id = '_'.join(['per_exp', name, season])
        per_exp.comment = ''
        eof_data.id = '_'.join(['eof', name, season])
        eof_data.comment = ''

        out = cdms2.open(outfile, 'a')
        out.write(pcts)
        out.write(per_exp)
        out.write(eof_data)
        out.close()

        # make memory free
        del data, pcts, per_exp, eof_data, lat
    # for name, varName, infile in infiles:
    print "Saved the eof_vars_*.nc file in", outfile
# end of def genEofVars(infiles, outfile, ...):


def makeGenEofVars(rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                                 seasons=['sum', 'win'], year=None):

    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    seasondic = {'sum': 'Summer', 'win': 'Winter', 'all': 'All'}

    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    opath = os.path.join(processfilesPath, 'Level1', 'Eof', rawOrAnomaly,
                                         filteredOrNot, yearDir)
    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        anofiles_5x5 = [anofile for anofile in os.listdir(anopath)
                                    if anofile.endswith('5x5.nc')]
        file_input = []
        for afile in anofiles_5x5:
            varName = afile.split('_')[0]
            apath = os.path.join(anopath, afile)
            file_input.append((varName, varName, apath))
         #end of for afile in anofiles_5x5:
        eofobj_fileendname = '%s_%s_%s_%s' % (yearDir, rawOrAnomaly,
                                             filteredOrNot, subName)

        for sea in seasons:
            seasonName = seasondic.get(sea, 'season')
            outpath = os.path.join(opath, subName, seasonName)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "The path has created ", outpath
            # end of if not os.path.isdir(outpath):

            # creating individula nc files for each season, since
            # we cant overwrite the timeaxis in same nc file.
            outfile = 'eof_vars_%s_%s_%s_%s_%s.nc' % (seasonName,
                   yearDir, rawOrAnomaly, filteredOrNot, subName)
            file_output = os.path.join(outpath, outfile)
            genEofVars(file_input, file_output, season=sea,
                        year=year, eofobj_endname=eofobj_fileendname)
        # end of for sea in seasons:
    # end of for subName in os.listdir(inpath):
# end of def makeGenEofVars(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    year = (1979, 2005)
    makeGenEofVars('Anomaly', 'Filtered',  year=year)

    year = 2005
    makeGenEofVars('Anomaly', 'Filtered',  year=year)

# end of if __name__ == '__main__':


