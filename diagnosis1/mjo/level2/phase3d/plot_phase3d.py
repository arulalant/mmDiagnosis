import cdms2
import os
import sys
from phase3d import mjo_phase3d
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__levelDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__levelDir__, '../../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diagnosisutils.timeutils import TimeUtility
from diag_setup.globalconfig import processfilesPath, plotsgraphsPath


timeobj = TimeUtility()
seasondic = {'all': 'All', 'sum': 'Summer', 'win': 'Winter'}


def makeMjoPhases3DPlots(rawOrAnomaly, filteredOrNot,
               year, yearDir=None, seasons=['sum', 'win'], seasonDir='All',
               pcs1VarName='norm_pcs1', pcs2VarName='norm_pcs2',
               pcs2Sign=-1, cyclic=False, **kwarg):
    """
    Written By : Arulalan.T

    Date : 22.07.2013

    """
    if not yearDir:
        if isinstance(year, int):
            yearDir = str(year)
        elif isinstance(year, tuple):
            yearDir = str(year[0]) + '_' + str(year[1])
    # end of if not yearDir:

    timeOrder = kwarg.get('timeorder', None)
    inpath = os.path.join(processfilesPath, 'Level2', 'Ceof', rawOrAnomaly,
                                         filteredOrNot, yearDir)
    opath = os.path.join(plotsgraphsPath, 'Level2', 'Phase3D', rawOrAnomaly,
                                        filteredOrNot, str(year)) ###???
    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        if seasonDir  not in os.listdir(anopath):
            print "The passed seasonDir '%s' is not available in the path '%s'\
                   So cant find the ceof_vars_*.nc file and amppha_*.nc file.\
                   So skipping plotting of amplitude phase3d " % (seasonDir, anopath)
            continue
        # end of if seasonDir  not in os.listdir(anopath):
        ceofpath = os.path.join(inpath, subName, seasonDir)
        infile = 'ceof_vars_%s_%s_%s_%s_%s.nc' % (seasonDir, yearDir,
                              rawOrAnomaly, filteredOrNot, subName)
        ceof_file = os.path.join(ceofpath, infile)
        if not os.path.isfile(ceof_file):
            print "The ceof_file doesnt exists ", ceof_file
            print "So cant perform amplitute phase. Skipping it"
            continue
        # end of if not os.path.isfile(ceof_file):
        ampfile = 'amppha_of_pcs_1_2_of_ceof_%s_%s_%s_%s_%s.nc' % (seasonDir,
                              yearDir, rawOrAnomaly, filteredOrNot, subName)
        amppha_file = os.path.join(ceofpath, ampfile)
        ampvar = ampfile.split('_')[0]
        for season in seasons:
            seasonName = seasondic.get(season, 'season')
            outpath = os.path.join(opath, subName, seasonName)
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
                print "The path has created ", outpath
            # end of if not os.path.isdir(outpath):

            if season == 'all':
                f = cdms2.open(ceof_file)
                if year:
                    # add the time axis year statements here in future.
                    npc1 = f(pcs1VarName, time=year)
                    npc2 = f(pcs2VarName, time=year)
                else:
                    npc1 = f(pcs1VarName)
                    npc2 = f(pcs2VarName)
                # end of if year:
            elif season == 'sum':
                npc1 = timeobj.getSummerData(pcs1VarName, ceof_file, year=year)
                npc2 = timeobj.getSummerData(pcs2VarName, ceof_file, year=year)
            elif season == 'win':
                npc1 = timeobj.getWinterData(pcs1VarName, ceof_file, year=year,
                                                              cyclic=cyclic)
                npc2 = timeobj.getWinterData(pcs2VarName, ceof_file, year=year,
                                                              cyclic=cyclic)
            else:
                raise ValueError("arg 'season' must be either 'all/sum/win' only")
            # end of if season == 'all':
            outfile = 'Phase3D_%s_%s_%s_%s_%s' % (seasonName, yearDir,
                                 rawOrAnomaly, filteredOrNot, subName)
            ptitle = 'Phase3D %s %s %s %s' % (subName, seasonName,
                                       rawOrAnomaly, filteredOrNot)
            out_file = os.path.join(outpath, outfile)
            ampf = cdms2.open(amppha_file)
            sdate = npc1.getTime().asComponentTime()[0]
            phase = ampf(ampvar, time=sdate, amp_pha=1, squeeze=1)
            phase = int(phase)
            # multiply npc2 with pcs2sign. By default it wil be
            # multiplied with -1
            npc2 = npc2 * pcs2Sign
            if pcs1VarName.startswith('norm'):
                npc1.id = 'Normalized PC1'
            if pcs2VarName.startswith('norm'):
                npc2.id = 'Normalized PC2'
            # plotting
            x = mjo_phase3d(npc1, npc2, sxyphase=phase, pposition1=None,
                      plocation='in', mintick=4, pdirection='anticlock',
                                      title=ptitle, timeorder=timeOrder)

            x.ps(out_file)
            print "phase3d plot saved in", outfile
            ampf.close()
        # end of for season in seasons:
    # end of for subName in os.listdir(inpath):
# end of def makeMjoPhases3DPlots(rawOrAnomaly='Anomaly', ...):


if __name__ == '__main__':

    yearDir = '1979_2005'
    year = 1979
    makeMjoPhases3DPlots('Anomaly', 'Filtered', year=year, yearDir=yearDir,
                                                     seasons=['sum', 'win'])


    year = 2005
    makeMjoPhases3DPlots('Anomaly', 'Filtered', year=year, seasons=['sum'])

    # for the single year winter season if we want to include JFMA season
    # with the same ND season for the same year.
    # To plot it in such a order, we have to provide the timeorder in nos.
    # Then only it will be plotted NDJFMA.
    # Otherwise it will plot as JFMAND & make looks like mess-up.
    makeMjoPhases3DPlots('Anomaly', 'Filtered', year=year, seasons=['win'],
                            cyclic=True, timeorder=[11, 12, 1, 2, 3, 4])


# end of if __name__ == '__main__':






