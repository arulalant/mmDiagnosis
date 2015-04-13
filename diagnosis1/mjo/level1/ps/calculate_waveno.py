import os
import sys
import cdms2
from psutils import  summerWaveNumber, winterWaveNumber, annualWaveNumber
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import processfilesPath
import diag_setup.netcdf_settings


seasondic = {'sum': 'Summer', 'win': 'Winter', 'all': 'All'}


def calWaveNumber(rawOrAnomaly, filteredOrNot, year,
                             seasons=['sum', 'win', 'all']):

    if isinstance(year, int):
        yearDir = str(year)
    elif isinstance(year, tuple):
        yearDir = str(year[0]) + '_' + str(year[1])

    inpath = os.path.join(processfilesPath, 'Average', 'Zonal',
                                    rawOrAnomaly, filteredOrNot)
    opath = os.path.join(processfilesPath, 'Level1', 'WaveNumber',
                          rawOrAnomaly, filteredOrNot, yearDir)

    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        for anofile in os.listdir(anopath):
            anofilename = anofile.split('.')[0]
            varName = anofilename.split('_')[0]
            anoFilePath = os.path.join(anopath, anofile)
            for season in seasons:
                wavefile = anofilename + '_' + season + '_waveno' + '.nc'
                seasonName = seasondic.get(season, 'season')
                outpath = os.path.join(opath, subName, seasonName)
                if not os.path.isdir(outpath):
                    os.makedirs(outpath)
                    print "Path has created ", outpath
                # end of if not os.path.isdir(outpath):
                outfile = os.path.join(outpath, wavefile)
                if os.path.isfile(outfile):
                    print "The waveno nc file is already exists ", outfile
                    print "So Skipping the waveno"
                    continue
                # end of if os.path.isfile(outfile):

                if season in ['sum']:
                    waveno = summerWaveNumber(varName, anoFilePath, year=year)
                elif season in ['win'] and not isinstance(year, int):
                    # For single year it has only 2 months (Nov, Dec). So skipping now
                    waveno = winterWaveNumber(varName, anoFilePath, year=year)  ## iglimit ?
                elif season in ['all']:
                    waveno = annualWaveNumber(varName, anoFilePath, iglimit=220, year=year) ##?
                else:
                    print "Add season here. Now skipping"
                    continue
                # end of if season in ['sum']:

                f = cdms2.open(outfile, 'w')
                f.write(waveno)
                f.close()
                print "The waveno nc file has created ", outfile
                # make memory free
                del waveno
            # end of for season in seasons:
        # end of for anofile in os.listdir(anopath):
    # end of for subName in os.listdir(inpath):
# end of def calWaveNumber(rawOrAnomaly='Anomaly', filteredOrNot='Unfiltered',...):

if __name__ == '__main__':

    year = (1979, 2005)
    calWaveNumber('Anomaly', 'Unfiltered', year)
    year = 2005
    calWaveNumber('Anomaly', 'Unfiltered', year)

# end of if __name__ == '__main__':


