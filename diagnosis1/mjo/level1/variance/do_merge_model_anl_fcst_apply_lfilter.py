"""
do_merge_model_anl_fcst_apply_lfilter script create filtered data only 
to the forecast index... i.e. todo
"""
import os
import sys
import time
import numpy
import cdms2
from variance_utils import lfilter
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from uv_cdat_code.diagnosisutils.timeutils import TimeUtility
from diag_setup.globalconfig import models, climatologies, logpath, processfilesPath
from diag_setup.logsetup import createLog


_weightPath = os.path.join(__curDir__, 'lfilter_weights.dat')
lweights = numpy.loadtxt(_weightPath, dtype=float)

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))
timeobj = TimeUtility()


def mergeAnlFcstApplyLanczosFilter(rawOrAnomaly, filteredOrNot='Unfiltered',
                                               weights=lweights, **kwarg):
    """
    mergeAnlFcstApplyLanczosFilter : first merge the full analysis with next
        7 or 10 or 15 days forecasts latest date (last time slice alone) data.
        Then apply LanczosFilter and get the last 7+1 or 10+1 or 15+1 or
        (1 anl + no of fcst hours) days lfiltered data alone.

    KWarg :
        suffixpath - pass the suffixPath either in list or string to do
                    lfilter for the models anomaly datasets.
                    It should followed the particular  directory structure
                    as follows.
                    "processfilesPath, Anomaly, Unfiltered/Filtered,
                    <Will be inserted your suffixpath here>,
                    Least Node Directories to loop through".

        overwrite - If it it true, then it will be overwrite
                    the existing lfiltered nc files.

    Written By : Arulalan.T

    Date : 02.10.2013

    """
    suffixPath = kwarg.get('suffixpath', None)
    overwrite = kwarg.get('overwrite', False)
    if overwrite:
        _overWrite = True
    else:
        _overWrite = False
    arglog = kwarg.get('log', None)
    if arglog is not None:
        log = arglog
    # end of if arglog is not None:
    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    if suffixPath:
        if isinstance(suffixPath, list):
            suffixPath = '/'.join(suffixPath)
        inpath = os.path.join(inpath, suffixPath)
        if not os.path.isdir(inpath):
            err = "The path doesnot exists '%s'" % inpath
            log.error(err)
            raise ValueError(err)
    # end of if suffixPath:

    # get the sorted fcst hour directories
    anlfcstdirs = timeobj._sortFcstHours(os.listdir(inpath))
    
    anlpath = os.path.join(inpath, anlfcstdirs[0])
    # get the nc files name of mean anomaly
    ncfiles = [f for f in os.listdir(anlpath) if f.endswith('.nc') \
                                    if not 'merged_anl_fcst' in f]
    # collect the varNames from the nc file itself
    variables = []
    for ncfile in ncfiles:
        vari = ncfile.split('_')
        if vari[1].isdigit():
            # for mjo works, variable_level_foo.nc has mentioned.
            varlev, varName, level = vari[:2], vari[0], vari[1]
        else:
            varlev, varName, level = [vari[0]], vari[0], None
        # end of if vari[1].isdigit():
        # combine var and level with '_'
        varlev = '_'.join(varlev)
        variables.append((varlev, varName, level))
    # end of for ncfile in ncfiles:

    for varlev, varName, level in variables:
        # variable intialize
        anlfcstData = numpy.array([])
        error = False
        # loop to extract the latest date anl and fcst hours data and merge
        for subName in anlfcstdirs:
            anopath = os.path.join(inpath, subName)
            ncfile = [f for f in os.listdir(anopath) if f.startswith(varlev) \
                                                        and f.endswith('.nc')]
            if not ncfile:
                log.debug("Cant find the ncfile for %s varName of %s",
                                                      varlev, subName)
                continue
            # end of if not ncfile:
            varncfile = os.path.join(anopath, ncfile[0])

            f = cdms2.open(varncfile)
            # extract the last / latest date data alone
            latestDayData = f(varName, time=slice(-1, 0))

            if anlfcstData.shape == (0,):
                # analysis latest data
                anlfcstData = latestDayData
                anllatestDate = latestDayData.getTime().asComponentTime()[0]
            else:
                fcstlatestDate = latestDayData.getTime().asComponentTime()[0]
                if anllatestDate != fcstlatestDate:
                    log.debug("Error : %s %s latestDate %s is not matching with \
                       %s's latestDate %s. So going to skip %s variable %s",
                        subName, varlev, str(fcstlatestDate),
                        anlfcstdirs[0], str(anllatestDate), subName, varlev)
                    # set error flag as true.
                    error = True
                    break
                # end of if anllatestDate != fcstlatestDate:

                # merging the latest analysis and latest date forecast hours
                anlfcstData = numpy.concatenate((anlfcstData, latestDayData))
            # end of if anlfcstData.shape == (0,):
            f.close()
        # end of for subName in anlfcstdirs:

        if error:
            # set flag as false
            error = False
            # skip this variable
            continue
        # end of if error:

        anlpath = os.path.join(inpath, anlfcstdirs[0])
        print varlev, anlpath
        # get the nc files name of mean anomaly
        ncfile = [f for f in os.listdir(anlpath) if f.startswith(varlev) \
                                                      and f.endswith('.nc')]
        if not ncfile:
            log.error("No Analysis file startswith('%s') in %s", varlev, anlpath)
            log.info("So Skipping variable %s with out merging & lfilter", varlev)
            continue
        # end of if not ncfile:
            
        varncfile = os.path.join(anlpath, ncfile[0])
        # analysis file
        f = cdms2.open(varncfile)
        log.info("Extracting anomaly data of '%s' var from '%s'",
                                              varName, varncfile)
        # extract the full data till before the last/latest date.
        # i.e. last / latest date data is omitted since already taken in that
        # in the anlfcstData. slice(-1) will do this job.
        analysisData = f(varName, time=slice(-1))
        levAxis = analysisData.getLevel()
        latAxis = analysisData.getLatitude()
        lonAxis = analysisData.getLongitude()
        # get the analysis start time
        anlStartDate = str(analysisData.getTime().asComponentTime()[0])
        # merge the avaliable analysis (full analysis) and latest/last date
        # of the forecast hours data (last date alone).
        mergedAnlFcstData = numpy.concatenate((analysisData, anlfcstData))

        # make memory free
        del analysisData, anlfcstData

        totaldays = len(mergedAnlFcstData)
        # genearate the timeAxis for the merged analysis & fcst dataset
        mergeTAxis = timeobj._generateTimeAxis(totaldays, anlStartDate)
        # create the merged analysis & fcst data as single cdms variable
        mergedAnlFcstData = cdms2.createVariable(mergedAnlFcstData, id=varName)
        # with proper time axis and other dimension axis informations
        axlist = [axis for axis in [mergeTAxis, levAxis, latAxis, lonAxis] if axis]
        mergedAnlFcstData.setAxisList(axlist)

        log.info("Applying Lanczos Filter to the anomaly")
        # apply the lfilter to the mergedAnlFcstData and get the last
        # len(anlfcstdirs) days filtered data alone. Here used kwarg
        # 'returntlen' with -ve to get the last no of days filtered data.
        filteredMergedAnomaly = lfilter(mergedAnlFcstData, weights,
                                 cyclic=True, returntlen=-1*len(anlfcstdirs))

        # make memory free
        del mergedAnlFcstData

        # make the out path as Filtered
        outpath = os.path.join(processfilesPath, rawOrAnomaly, 'Filtered')

        if suffixPath:
            outpath = os.path.join(outpath, suffixPath, 'Merged')
        else:
            outpath = os.path.join(outpath, 'Merged')
        # end of if suffixPath:

        if not os.path.isdir(outpath):
            os.makedirs(outpath)
            log.info("Path has created %s", outpath)
        # end of if not os.path.isdir(outpath):

        outfilename = ncfile[0].replace('anl', 'merged_anl_fcst')
        outfile = os.path.join(outpath, outfilename)
        
        if os.path.isfile(outfile) and not _overWrite:
            log.warning("The file %s is exist already. \
                   So skipping lfilter to this",  outfile)
            continue
        # end of if os.path.isfile(outfile):

        outf = cdms2.open(outfile, 'w')
        outf.write(filteredMergedAnomaly)
        outf.close()
        print outfile
        log.info("Created merged analysis & forecast lfiltered file '%s'", outfile)
        # make memory free
        del filteredMergedAnomaly
    # end of  for varlev, varName, level in variables:
# end of def mergeAnlFcstApplyLanczosFilter(...):


if __name__ == '__main__':

    # applying the lancoz filter to the models anomaly datasets.
    # for the models anomaly, we need to pass the suffixpath as
    # [modelName, ClimatologyName, Year, 'Daily'] in the kwarg.

    # get the current year
    year = time.localtime().tm_year
    log.info("It will try to apply lfilter only to the current year %d. \
           If you need to loop through all the available years in the \
           models anomaly path means, insert your code here.", year)

    for climatology in climatologies:
        for model in models:
            log.info("The Lanczos Filter has started for the model '%s' - \
                      merged analysis and forecast hours data ", model.name)
            modelPathList = [model.name, climatology.name, str(year), 'Daily']
            mergeAnlFcstApplyLanczosFilter('Anomaly', 'Unfiltered',
                    suffixpath=modelPathList, overwrite=True, log=log)
            log.info("The Lanczos Filter has finished for the model '%s' - \
                      merged analysis and forecast hours data ", model.name)
        # end of for model in models:
    # end of for climatology in climatologies:
# end of if __name__ == '__main__':



