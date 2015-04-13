import os
import sys
import time
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import models, climatologies, \
                 processfilesPath, logpath, plotexcludehour
from diag_setup.logsetup import createLog
from amplitude_phase import genMjoAmplitudePhases

_overWrite = True
# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def makeProjectedPctsAmplitudePhases(rawOrAnomaly='Anomaly',
             filteredOrNot='Filtered', seasons=['mjjas'], **kwarg):

    """
    
    KWarg:
        exclude : exclude hours. If some hours list has passed then those 
              model hours will be omitted. eg : 01 hour.
              Note : it will omit those exclude model hours directory.
              So for the remaining model anl, fcst hours only calculated the
              projected pcts amplitudes phases.
              
    12.08.2013
    """
    seasondic = {'sum': 'Summer', 'win': 'Winter', 'all': 'All', 'mjjas': 'MJJAS'}
    suffixPath = kwarg.get('suffixpath', None)
    exclude = kwarg.get('exclude', [])
    year = kwarg.get('year', '')
    overwrite = kwarg.get('overwrite', False)
    if overwrite: _overWrite = True
    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    if suffixPath:
        if isinstance(suffixPath, list):
            suffixPath = '/'.join(suffixPath)
        inpath = os.path.join(inpath, suffixPath)
        if not os.path.isdir(inpath):
            raise ValueError("The path doesnot exists '%s'" % inpath)
    # end of if suffixPath:
    
    fcstdirs = os.listdir(inpath)
    # remove the unwanted directories to be plotted
    for ex in exclude:
        if ex in fcstdirs:
            print "Omitted directory '%s' without doing projected pcts amplitude phase", ex
            fcstdirs.remove(ex)
        # end of if ex in fcstdirs:
    # end of for ex in exclude:
    for anl_fcst in fcstdirs:
        for sea in seasons:
            seasonName = seasondic.get(sea, 'season')
            # creating individual nc files for each season, since
            # we cant overwrite the timeaxis in same nc file.
            infile = 'projected_pcts_%s_%s_%s_%s.nc' % (seasonName,
                               rawOrAnomaly, filteredOrNot, anl_fcst)
            file_input = os.path.join(inpath, anl_fcst, infile)
            if os.path.isfile(file_input) and not _overWrite:
                log.warning("The file %s is exist already. \
                       So skipping computation of amplitude & phases of the \
                       projected pcts to this", file_input)
                continue
            # end of if os.path.isfile(file_output) ...:
            outfile = 'amppha_of_projected_pcs_1_2_of_ceof_%s_%s_%s_%s_%s.nc' % (seasonName,
                             year, rawOrAnomaly, filteredOrNot, anl_fcst)
            amppha_file = os.path.join(inpath, anl_fcst, outfile)
            if os.path.isfile(amppha_file) and not _overWrite:
                log.warning("The file %s is exist already. \
                   So skipping amp_pha of projected pcts to this", amppha_file)
                continue
            # end of if os.path.isfile(file_output) ...:

            log.info("Calculating projected amp_pha for %s %s %s %s %s", seasonName, 
                                         year, rawOrAnomaly, filteredOrNot, anl_fcst)
            genMjoAmplitudePhases(infile=file_input, outfile=amppha_file,
                     pcs1VarName='pcs1', pcs2VarName='pcs2', pcs2Sign=-1, log=log)
            log.info("amp_pha Finished") 
        # end of for sea in seasons:
    # end of for anl_fcst in fcstdirs:
# end of def makeProjectedPctsAmplitudePhases(...):


if __name__ == '__main__':

    # Creating the amplitude_phases of projected pcts nc files for the
    # models anomaly and its forecast hours datasets.
    # To reach that path, , we need to pass the suffixpath as
    # [modelName, ClimatologyName, Year, 'Daily'] in the kwarg.

    # get the current year
    cyear = str(time.localtime().tm_year)
    print "It will try to compute projected pcts amplitude phase  \
           only to the current year %s. \
           If you need to loop through all the available years in the \
           models anomaly path means, insert your code here." % cyear

    for climatology in climatologies:
        for model in models:
            modelPathList = [model.name, climatology.name, cyear, 'Daily']
            makeProjectedPctsAmplitudePhases('Anomaly', 'Filtered',
                  suffixpath=modelPathList, year=cyear,
                  seasons=['mjjas'], exclude=plotexcludehour, overwrite=True)
        # end of for model in models:
    # end of for climatology in climatologies:
# end of if __name__ == '__main__':



