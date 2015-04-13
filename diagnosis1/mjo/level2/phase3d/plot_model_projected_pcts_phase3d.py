import os
import sys
import xmgrace
import cdms2
from phase3d import mjo_phase3d
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diagnosisutils.timeutils import TimeUtility
from diagnosisutils.xml_data_access import GribXmlAccess
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath, models, \
                        climatologies, logpath, plotceofanlsince, plotexcludehour
from diag_setup.xml_status import getModelAnlFirstLastDate
from diag_setup.logsetup import createLog

timeobj = TimeUtility()
xmlobj = GribXmlAccess('.')
# create log object to written into logfile
logfile = __file__.split('.py')[0] + '.log'
log = createLog(__file__, os.path.join(logpath, logfile))


def makeProjectedPctsPhases3DPlots(pcs1VarName, pcs2VarName, pcs2Sign=-1,
                        rawOrAnomaly='Anomaly', filteredOrNot='Filtered',
                                              seasons=['mjjas'], **kwarg):

    """
    CAUTION : To plot the season time period will be calculated
            season time will be calculated using xmlobj.findPartners()
            method. By default it takes 'Analysis'.
            i.e. period from 01-05-yyyy to 30-9-yyyy for the 'mjjas' season.
            If dtype will be '24' means then period will be from 30-04-yyyy
            to 29-09-yyyy. Likewise user can pass fcst hour.

    KWarg:
        exclude : exclude hours. If some hours list has passed then those
              model hours will be omitted. eg : 01 hour.
              Note : it will omit those exclude model hours directory.
              So for the remaining model anl, fcst hours only plotted the
              projected pcts.

    12.08.2013
    """

    x = kwarg.get('x', None)
    if x is None:
        x = xmgrace.init()
        print "x init"
    # end of if x is None:

    seasondic = {'sum': 'Summer', 'win': 'Winter',
                  'all': 'All', 'mjjas': 'MJJAS'}
    suffixPath = kwarg.get('suffixpath', None)
    leastOutDir = kwarg.get('leastoutdir', None)
    modelname = kwarg.get('mname', '')
    year = kwarg.get('year', '')
    cyclic = kwarg.get('cyclic', False)
    timeOrder = kwarg.get('timeorder', None)
    exclude = kwarg.get('exclude', [])
    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)
    opath = os.path.join(plotsgraphsPath, 'Level2', 'Proj_Pcts', 'Phase3D',
                                         rawOrAnomaly, filteredOrNot)
    anl_season = ''
    if suffixPath:
        if isinstance(suffixPath, list):
            suffixPath = '/'.join(suffixPath)
        inpath = os.path.join(inpath, suffixPath)
        opath = os.path.join(opath, suffixPath)
        if not os.path.isdir(inpath):
            raise ValueError("The path doesnot exists '%s'" % inpath)
    # end of if suffixPath:

    if leastOutDir:
        # This option will help us to create daily date wise directory
        opath = os.path.join(opath, leastOutDir)
    # end of if leastOutDir:

    if not os.path.isdir(opath):
        os.makedirs(opath)
        print "The path has created", opath
    # end of if not os.path.isdir(opath):

    anl_fcst_hrs = os.listdir(inpath)
    # remove the unwanted directories to be used to do projected pcts
    for ex in exclude:
        if ex in anl_fcst_hrs:
            print "Omitted directory '%s' without doing projected pcts", ex
            anl_fcst_hrs.remove(ex)
        # end of if ex in anl_fcst_hrs:
    # end of for ex in exclude:
    anl_fcst_hrs = timeobj._sortFcstHours(anl_fcst_hrs)
    for anl_fcst in anl_fcst_hrs:
        inputpath = os.path.join(inpath, anl_fcst)
        # create the anl_fcst sub directory in case seasonal
        # plot files to be stored inside anl_fcst directory
        outpath = opath
#        outpath = os.path.join(opath, anl_fcst)
#        if not os.path.isdir(outpath):
#            os.makedirs(outpath)
#            print "The path has created", outpath
#        # end of if not os.path.isdir(opath):
        for season in seasons:
            seasonName = seasondic.get(season, 'season')
            # creating individual nc files for each season, since
            # we cant overwrite the timeaxis in same nc file.
            infile = 'projected_pcts_%s_%s_%s_%s.nc' % (seasonName,
                               rawOrAnomaly, filteredOrNot, anl_fcst)
            infpath = os.path.join(inputpath, infile)

            ampfile = 'amppha_of_projected_pcs_1_2_of_ceof_%s_%s_%s_%s_%s.nc' % (seasonName,
                             year, rawOrAnomaly, filteredOrNot, anl_fcst)
            amppha_file = os.path.join(inputpath, ampfile)
            ampvar = ampfile.split('_')[0]
            if season == 'all':
                f = cdms2.open(infpath)
                if year:
                    # add the time axis year statements here in future.
                    npc1 = f(pcs1VarName, time=year)
                    npc2 = f(pcs2VarName, time=year)
                else:
                    npc1 = f(pcs1VarName)
                    npc2 = f(pcs2VarName)
                # end of if year:
            elif season == 'sum':
                npc1 = timeobj.getSummerData(pcs1VarName, infpath, year=year)
                npc2 = timeobj.getSummerData(pcs2VarName, infpath, year=year)
            elif season == 'win':
                npc1 = timeobj.getWinterData(pcs1VarName, infpath, year=year,
                                                              cyclic=cyclic)
                npc2 = timeobj.getWinterData(pcs2VarName, infpath, year=year,
                                                              cyclic=cyclic)
            elif season in 'mjjas':
                if anl_fcst in ['anl', 'Analysis']:

                    if plotceofanlsince:
                        sday = int(plotceofanlsince[4:6])
                        smon = int(plotceofanlsince[6:8])
                    else:
                        sday = 1
                        smon = 5
                    # end of if plotceofanlsince:
#                    eday = 30
#                    emon = 9
                    # get the latest comptime of analysis data.
                    f = cdms2.open(infpath)
                    anlLatestDate = f[pcs1VarName].getTime().asComponentTime()[-1]
                    eday = anlLatestDate.day
                    emon = anlLatestDate.month
                    anl_season = ''

                elif anl_fcst in ['Merged']:
                    # Merged analysis and fcst hours plot stuff
                    f = cdms2.open(infpath)
                    mergetime = f[pcs1VarName].getTime().asComponentTime()
                    mergeFirstDate = mergetime[0]
                    mergeLatestDate = mergetime[-1]
                    sday = mergeFirstDate.day
                    smon = mergeFirstDate.month
                    eday = mergeLatestDate.day
                    emon = mergeLatestDate.month
                    startday = str(mergeFirstDate).split(' ')[0]
                    anl_season = "%s's Merged Anl & Fcst HRs" % startday

                elif anl_fcst.isdigit():
                    # find fcst hour partner data w.r.t analysis date as 0001-05-01
                    # as start of the season
#                    #'0001-05-01'
                    pStartDate = xmlobj.findPartners('a', plotceofanlsince, int(anl_fcst))
                    sday = pStartDate.day
                    smon = pStartDate.month
                    # find fcst hour partner data w.r.t analysis date as 0001-09-30
                    # as end of the season
#                    #'0001-09-30'
                    # Use the analysis latest date to get its partner's latest date.
                    pEndDate = xmlobj.findPartners('a', anlLatestDate, int(anl_fcst))
                    eday = pEndDate.day
                    emon = pEndDate.month
                    # generate the subtitle1 string
                    anlStartDate = timeobj.timestr2comp(plotceofanlsince)
                    anlStartDate = str(anlStartDate).split(' ')[0]
                    anlEndDate = str(anlLatestDate).split(' ')[0]
                    anl_season = "Anl Season : " + anlStartDate + " to " + anlEndDate

                else:
                    pass
                # extract seasonal data
                npc1 = timeobj.getSeasonalData(pcs1VarName, infpath, sday,
                                               smon, eday, emon, year=year)
                npc2 = timeobj.getSeasonalData(pcs2VarName, infpath, sday,
                                               smon, eday, emon, year=year)
            else:
                raise ValueError("arg 'season' must be either \
                                    'all/sum/win/mjjas' only")
            # end of if season == 'all':
            ampf = cdms2.open(amppha_file)
            sdate = npc1.getTime().asComponentTime()[0]
            # get the phase alone for the sdate
            phase = ampf(ampvar, time=sdate, amp_pha=1, squeeze=1)
            phase = int(phase)
            # multiply npc2 with pcs2sign. By default it wil be
            # multiplied with -1
            npc2 = npc2 * pcs2Sign
            if pcs1VarName.startswith('norm'):
                npc1.id = 'Normalized Projected PC1'
            if pcs2VarName.startswith('norm'):
                npc2.id = 'Normalized Projected PC2'

            if anl_fcst.isdigit():
                anlfcst = anl_fcst + ' HR'
                anl_fcst = anl_fcst + '_HR'
            else:
                anlfcst = anl_fcst

            # Jut to make sure the analysis and fcst hours are in same colors
            # while plotting for its partners
            if anl_fcst in ['Analysis']:
                pcolors = ['magenta', 'blue', 'violet', 'orange', 'red', 'green']
            elif anl_fcst in ['Merged']:
                pcolors = ['red', 'magenta', 'blue', 'violet', 'orange', 'green']
            else:
                pcolors = ['magenta', 'blue', 'violet', 'orange', 'red', 'green']
            # end of if anl_fcst in ['Analysis']:

            ptitle = '%s %s %s %s %s' % (modelname, anlfcst, seasonName,
                                                rawOrAnomaly, filteredOrNot)
            outfname = 'phase3d_projected_norm_pcts_%s_%s_%s_%s_%s' % (modelname,
                          anl_fcst, seasonName, rawOrAnomaly, filteredOrNot)
            outfpath = os.path.join(outpath, outfname)
            # plotting
            x = mjo_phase3d(npc1, npc2, sxyphase=phase, colors=pcolors, pposition1=None,
                        plocation='in', mintick=4, pdirection='anticlock', title=ptitle,
                                stitle1=anl_season, stitle2='date', timeorder=timeOrder)
            # save plot
            x.ps(outfpath)
            log.info("phase3d plot saved for %s model %s in %s", modelname, anlfcst, outfpath)
            ampf.close()
        # end of for sea in seasons:
    # end of for subName in os.listdir(inpath):
# end of def makeProjectedPctsPhases3DPlots(...):


if __name__ == '__main__':

    # plotting the projected pcts for the models anomaly and its
    # forecast hours datasets.
    # To reach that path, we need to pass the suffixpath as
    # [modelName, ClimatologyName, Year, 'Daily'] in the kwarg.
    x = xmgrace.init()
    # get the first and lastest date of xml analysis timeAxis
    anlFirstLastDate = getModelAnlFirstLastDate()

    # conver the component time object into yyyymmdd string format
    currentDate = timeobj.comp2timestr(anlFirstLastDate[-1], returnHour='no')
    cyear = str(anlFirstLastDate[-1].year)

    print "It will try to plot phase3d projected pcts only to the current year %s. \
           If you need to loop through all the available years in the \
           models anomaly path means, insert your code here." % cyear
    for climatology in climatologies:
        for model in models:
            modelPathList = [model.name, climatology.name, cyear, 'Daily']
            makeProjectedPctsPhases3DPlots('norm_pcs1', 'norm_pcs2',
                        suffixpath=modelPathList, mname=model.name,
                        leastoutdir=currentDate, year=cyear, exclude=plotexcludehour, x=x)
        # end of for model in models:
    # end of for climatology in climatologies:
# end of if __name__ == '__main__':


