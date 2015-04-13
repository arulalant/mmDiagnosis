import os
import sys
import vcs
from plot_pcts_utils import plotPcts
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath, models, \
               climatologies, logpath, plotceofanlsince, plotceoftinterval, plotexcludehour
from diag_setup.logsetup import createLog
from diag_setup.xml_status import getModelAnlFirstLastDate
from diagnosisutils.timeutils import TimeUtility


__vcsSlow__ = True
timeobj = TimeUtility()
# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def makeProjectedPctsPlots(pcs1VarName, pcs2VarName,
            rawOrAnomaly='Anomaly', filteredOrNot='Filtered', **kwarg):

    """
    12.08.2013
    """

    x = kwarg.get('x', None)
    if x is None:
        print "before x init()"
        x = vcs.init()
        print "successfully x init done!"
    # end of if x is None:
    x.clear()
    x.portrait()
    if __vcsSlow__:
        x.pause_time = 1

    suffixPath = kwarg.get('suffixpath', None)
    leastOutDir = kwarg.get('leastoutdir', None)
    modelname = kwarg.get('mname', '')
    year = kwarg.get('year', '')
    sedate = kwarg.get('sedate', None)
    xinterval = kwarg.get('tinterval', 10)
    omit = kwarg.get('exclude', [])
    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    opath = os.path.join(plotsgraphsPath, 'Level2', 'Proj_Pcts', 'Ceof',
                                         rawOrAnomaly, filteredOrNot)
    if suffixPath:
        if isinstance(suffixPath, list):
            suffixPath = '/'.join(suffixPath)
        inpath = os.path.join(inpath, suffixPath)
        opath = os.path.join(opath, suffixPath)
        if not os.path.isdir(inpath):
            log.error("The path doesnot exists '%s'", inpath)
            raise ValueError("The path doesnot exists '%s'" % inpath)
    # end of if suffixPath:

    if leastOutDir:
        # This option will help us to create daily date wise directory
        opath = os.path.join(opath, leastOutDir)
    # end of if leastOutDir:
    if not os.path.isdir(opath):
        os.makedirs(opath)
        log.info("The path has created %s", opath)
    # end of if not os.path.isdir(opath):
    outfname = 'ceof_projected_pcts_%s_%s_%s' % (modelname,
                                rawOrAnomaly, filteredOrNot)
    outfpath = os.path.join(opath, outfname)
    comment2 = "%s Analysis Vs Fcst" % (modelname)
    log.info("Ceof Projected PCTS plotting has started")

    # Omit the Merged Directory "also" along with passed "exclude" list
    # while plotting Ceof of model anl, fcst hours.
    omit.append('Merged')

    plotPcts(pcs1VarName, pcs2VarName, inpath, outfpath, pcs2Sign=-1,
              title="Combined EOF Normalized Projected PC Time Series " + year,
              comment_1="Normalized Projected PCTS-",
              comment_2=comment2, stitle1="date",
              x_name="Days", y_name="Normalized PCTS-",
              sedate=sedate, tinterval=xinterval, exclude=omit, x=x)
    log.info("Ceof Projected PCTS plotting has finished")
# end of def makeProjectedPctsPlots(...):


if __name__ == '__main__':

    # plotting the projected pcts for the models anomaly and its
    # forecast hours datasets.
    # To reach that path, we need to pass the suffixpath as
    # [modelName, ClimatologyName, Year, 'Daily'] in the kwarg.
    v = vcs.init()

    # get the first and lastest date of xml analysis timeAxis
    anlFirstLastDate = getModelAnlFirstLastDate()

    if plotceofanlsince:
        # plot ceof anl since date has mentioned in the configure.txt file.
        # so analysis first date should be from plotceofanlsince
        analysisPeriod = (plotceofanlsince, anlFirstLastDate[-1])
    else:
        analysisPeriod = anlFirstLastDate
    # end of if plotceofanlsince:

    # conver the component time object into yyyymmdd string format
    currentDate = timeobj.comp2timestr(anlFirstLastDate[-1], returnHour='no')
    cyear = str(anlFirstLastDate[-1].year)

    print "It will try to plot projected pcts only to the current year %s. \
           If you need to loop through all the available years in the \
           models anomaly path means, insert your code here." % cyear
    for climatology in climatologies:
        for model in models:
            modelPathList = [model.name, climatology.name, cyear, 'Daily']
            makeProjectedPctsPlots('norm_pcs1', 'norm_pcs2',
                    suffixpath=modelPathList, mname=model.name, year=cyear,
                    leastoutdir=currentDate, sedate=analysisPeriod,
                    tinterval=plotceoftinterval, exclude=plotexcludehour, x=v)
        # end of for model in models:
    # end of for climatology in climatologies:
# end of if __name__ == '__main__':


