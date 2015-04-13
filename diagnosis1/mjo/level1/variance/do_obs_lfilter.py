import os
import sys
import cdms2
import numpy
from variance_utils import lfilter
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import processfilesPath, logpath
from diag_setup.logsetup import createLog

_weightPath = os.path.join(__curDir__, 'lfilter_weights.dat')
lweights = numpy.loadtxt(_weightPath, dtype=float)

# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def applyLanczosFilter(rawOrAnomaly, filteredOrNot, weights=lweights, **kwarg):
    """
    Date : 08.07.2013

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
    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        # make the out path as Filtered
        outpath = os.path.join(processfilesPath, rawOrAnomaly, 'Filtered')
        if suffixPath:
            outpath = os.path.join(outpath, suffixPath, subName)
        else:
            outpath = os.path.join(outpath, subName)
        # end of if suffixPath:
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
            log.info("Path has created %s", outpath)
        # end of if not os.path.isdir(outpath):

        for anofile in os.listdir(anopath):
            anonamelist = anofile.split('.')[0].split('_')
            anoFilePath = os.path.join(anopath, anofile)

            varName = anonamelist[0]
            anonamelist.append('filtered')
            outfilename = '_'.join(anonamelist) + '.nc'

            outfile = os.path.join(outpath, outfilename)
            if os.path.isfile(outfile) and not _overWrite:
                log.warning("The file %s is exists already. \
                       So skipping lfilter to this",  outfile)
                continue
            # end of if os.path.isfile(outfile):
            inf = cdms2.open(anoFilePath, 'r')
            log.info("Extracting anomaly data of '%s' var from '%s'",
                                                varName, anoFilePath)
            anomaly = inf(varName)
            inf.close()
            log.info("Applying Lanczos Filter to the anomaly")
            filteredAnomaly = lfilter(anomaly, weights, cyclic=True)

            # make memory free
            del anomaly

            outf = cdms2.open(outfile, 'w')
            outf.write(filteredAnomaly)
            outf.close()
            
            sdate = filteredAnomaly.getTime().asComponentTime()[0]
            edate = filteredAnomaly.getTime().asComponentTime()[-1]
            
            log.info("Created lfiltered file '%s' for the season from '%s' to '%s'", outfile, str(sdate), str(edate))
            # make memory free
            del filteredAnomaly
        # end of for anofile in os.listdir(anopath):
    # end of for subName in os.listdir(inpath):
# end of def applyLanczosFilter():


if __name__ == '__main__':

    # this will create the filteredAnomaly only for the observations.
    # for the models anomaly, we need to pass the suffixpath as
    # [modelName, ClimatologyName, Year, 'Daily'] in the kwarg.
    applyLanczosFilter('Anomaly', 'Unfiltered')
# end of if __name__ == '__main__':

