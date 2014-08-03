import cdms2
import numpy
import trig
import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import processfilesPath, logpath
from diag_setup.logsetup import createLog
import diag_setup.netcdf_settings


# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def getMjoAmplitudePhases(pcs1, pcs2):
    """
    pcs1 - pcs1 or normalized pcs1. It must have timeAxis also.
    pcs2 - pcs2 or normalized pcs2.

    Updated Date : 11.06.2013

    """

    amp = numpy.ma.sqrt((pcs1 ** 2) + (pcs2 ** 2))
    phases = []

    for i in xrange(len(amp)):
        # get the actual half quadrant of the circle of the start x, y points
        # of pcs1, pcs2.
        hq = trig.getHalfQuadrantOfCircle(pcs1[i], pcs2[i])
        if hq == -1:
            phase = -1
        else:
            # adding 4 to make mjo phase.
            phase = (hq + 4) % 8
            if phase == 0: phase = 8
        # end of if hq == -1:
        phases.append(phase)
    # end of for i in xrange(len(amp)):

    timeAxis = pcs1.getTime()
    amp = amp.reshape((len(amp), 1))
    phases = numpy.array(phases)
    phases = phases.reshape((len(phases), 1))
    amp_pha = numpy.concatenate((amp, phases), axis=1)

    # making memmory free
    del amp, phases, pcs1, pcs2

    amp_pha = cdms2.createVariable(amp_pha, id='amppha')
    amp_pha.long_name = 'amplitude phases'
    amp_pha.comments = 'see axis comment also'
    apAxis = cdms2.createAxis([0, 1], id='amp_pha')
    apAxis.comments = """amplitudes and its phases.
    We can access amplitudes or phases alone by specifying either 0 or 1.
    eg: >>> data(amp_pha=0) # it will extract only amplitudes
        >>> data(amp_pha=1) # it will extract only phases
    By default it will extract both amplitudes and phases.
    Along with this you can sepcify time axis also. """
    amp_pha.setAxisList([timeAxis, apAxis])

    return amp_pha
# end of def getMjoAmplitudePhases(pcs1, pcs2):


def genMjoAmplitudePhases(infile, outfile, pcs1VarName='pcs1',
                          pcs2VarName='pcs2', pcs2Sign=-1, **kwarg):
    """

    Date : 11.06.2013
    """
    arglog = kwarg.get('log', None)
    if arglog is not None:
        log = arglog
    # end of if arglog is not None:

    f = cdms2.open(infile)
    pcs1 = f(pcs1VarName)
    pcs2 = f(pcs2VarName) * pcs2Sign
    f.close()

    amp_pha = getMjoAmplitudePhases(pcs1, pcs2)
    amp_pha.comments = 'see axis comment also'
    out = cdms2.open(outfile, 'w')
    out.write(amp_pha)
    out.close()
    log.info("Written amp_pha into nc file %s", outfile)
# end of def genMjoAmplitudePhases(infile, ...):


def makeMjoAmplitudePhases(rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                            year=None, seasons=['all']):
    """
    seasons : By default it takes ['all'] only. For the 'all' season only
              we might have calculated pcs1, pcs2 and norm_pcs1, norm_pcs2.
              If you calculated the pcs for some other seasons, then pass
              that also in this arg list.

    Written By : Arulalan.T

    Date : 22.07.2013

    """

    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    inpath = os.path.join(processfilesPath, 'Level2', 'Ceof',
                         rawOrAnomaly, filteredOrNot, yearDir)
    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        for season in os.listdir(anopath):
            sea = season.lower()[:3]
            if not sea in seasons:
                print "Though '%s' Season is available, skipping it without \
                    creating amplitude_phases_*.nc file, because in the arg \
                    seasons list it is not available. So enable it by passing \
                    this '%s' season to seasons list " % (season, sea)
                continue
            # end of if not sea in seasons:
            outpath = os.path.join(anopath, season)
            infile = 'ceof_vars_%s_%s_%s_%s_%s.nc' % (season, yearDir,
                                   rawOrAnomaly, filteredOrNot, subName)
            ceof_file = os.path.join(outpath, infile)
            if not os.path.isfile(ceof_file):
                print "The ceof_file doesnt exists ", ceof_file
                print "So cant perform amplitute phase. Skipping it"
                continue
            # end of if not os.path.isfile(ceof_file):
            outfile = 'amppha_of_pcs_1_2_of_ceof_%s_%s_%s_%s_%s.nc' % (season,
                             yearDir, rawOrAnomaly, filteredOrNot, subName)
            amppha_file = os.path.join(outpath, outfile)
            print "Calculating amp_pha for", season, yearDir, rawOrAnomaly,
            print filteredOrNot, subName
            genMjoAmplitudePhases(infile=ceof_file, outfile=amppha_file,
              pcs1VarName='pcs1', pcs2VarName='pcs2', pcs2Sign=-1)
         # end of for season in os.listdir(anopath):
    # end of for subName in os.listdir(inpath):
# end of def makeMjoAmplitudePhases(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    year = (1979, 2005)
    makeMjoAmplitudePhases('Anomaly', 'Filtered',  year)

    year = 2005
    makeMjoAmplitudePhases('Anomaly', 'Filtered',  year)

# end of if __name__ == '__main__':

