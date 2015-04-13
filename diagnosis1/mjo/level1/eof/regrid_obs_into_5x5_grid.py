import os
import sys
import cdms2
from regrid2 import Horizontal  # need to use BilinearGrid. But dont know about the args.
from genutil import statusbar
__curDir__ = os.path.dirname(__file__)
diagDir = os.path.abspath(os.path.join(__curDir__, '../../..'))
# adding the previous diagnosisutils path to python path
sys.path.append(diagDir)
from diag_setup.globalconfig import processfilesPath
import diag_setup.netcdf_settings


__Debug__ = False
__showStatusBar = True
_5x5_ncfilename = 'olr.sample.5x5.grid.nc'


def regrid_5by5(rawOrAnomaly='Anomaly', filteredOrNot='Unfiltered'):
    """
    Written By : Arulalan.T

    Date : 22.07.2013

    """

    inpath = os.path.join(processfilesPath, rawOrAnomaly, filteredOrNot)

    for subName in os.listdir(inpath):
        anopath = os.path.join(inpath, subName)
        for anofile in os.listdir(anopath):
            anofilename = anofile.split('.')[0]
            varName = anofilename.split('_')[0]
            if not anofilename.endswith('_5x5'):
                anofilename += '_5x5'
            # end of if not anofilename.endswith('_5x5'):
            anoFilePath = os.path.join(anopath, anofile)
            outfile = anofilename + '.nc'
            outpath = os.path.join(anopath, outfile)
            if os.path.isfile(outpath):
                print "5x5 regridded file already exists for", outpath
                continue
            # end of if os.path.isfile(outpath):

            grid5x5file = os.path.join(__curDir__, _5x5_ncfilename)
            varName5x5 = _5x5_ncfilename.split('.')[0]
            f = cdms2.open(grid5x5file)
            grid5x5 = f[varName5x5].getGrid()

            inf = cdms2.open(anoFilePath)
            grid_infile = inf[varName].getGrid()

            # Regridding the anomaly data
            # Creating the horizontal lat,lon regrid
            # Note that 'grid_infile' is the source and 'grid5x5' is the target
            regridfunc = Horizontal(grid_infile, grid5x5)
            anomalytime = inf[varName].getTime().asComponentTime()
            print "The out path is ", outpath
            loopCount = len(anomalytime)
            preview = 0
            for day in anomalytime:
                if __Debug__:
                    print "The Date : ", day
                data_5x5_regridded = regridfunc(inf(varName, time=day))
                outf = cdms2.open(outpath, 'a')
                outf.write(data_5x5_regridded)
                outf.close()
                # make memory free
                del data_5x5_regridded
                if __showStatusBar:
                    preview = statusbar(anomalytime.index(day), total=loopCount,
                               title='Regridding', prev=preview)
                 # end of if __showStatusBar:
            # end of for day in anomalytime:
            print
            print "The 5x5 regrid for the variable '%s' is stored %s" % (varName, outpath)
            inf.close()
            f.close()
        # end of for anofile in os.listdir(anopath):
    # end of for subName in os.listdir(inpath):
# end of def regrid_5by5(rawOrAnomaly='Anomaly', filteredOrNot='Unfiltered'):


if __name__ == '__main__':

    # see here we passed Filterd to do 5x5 regid
    regrid_5by5('Anomaly', 'Filtered')
# end of if __name__ == '__main__':



