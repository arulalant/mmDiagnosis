import cdms2
import os, sys
from harmonic_util import harmonic
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__curDir__, '../..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import processfilesPath, climatologies
import diag_setup.netcdf_settings


def createHarmonic(inpath, outpath, pfile):
    """
    createHarmonic : This function will create harmonic climatolgies
    
    inpath : absolute path of climatologies
    outpath : absolute path of harmonic climatolgies going to be store.
    pfile : climatology partial file name.
    
    Written By : Arulalan.T
    
    Date : 26.10.2014
    
    """
    
    ncfiles = [f for f in os.listdir(inpath) if f.endswith(pfile)]
    
    for fname in ncfiles:    
        # get varName
        varName = fname.split('.')[0]
        
        # get climatolgy data 
        infilepath = os.path.join(inpath, fname)
        inf = cdms2.open(infilepath)
        cdata = inf(varName)
        # apply harmonic over the above climatolgy data 
        # sum of mean and first three harmonic of climatolgy
        hdata = harmonic(cdata, k=3, time_type='daily', phase_shift=15)
        
        # make memory free 
        del cdata 
        
        # get outfile name 
        outfname = fname.split('.')
        outfname = '.'.join(outfname.insert(-1, 'harmonic'))
        outfpath = os.path.join(outpath, outfname)
        
        # write harmonic climatolgy data 
        outf = cdms2.open(outfpath)
        outf.write(hdata)
        outf.close()        
        inf.close()
        # make memory free
        del hdata
    # end of for fname in ncfiles:
# end of def createHarmonic(inpath, outpath, pfile):


if __name__ == '__main__':


    for climatology in climatologies:
        if climatology.dfile and climatolgy.name.lower() == 'miso':
            # daily climatolgy path
            climatologyPath = os.path.join(climatology.path, 'Daily')                       
            
            # calling below fn to create daily harmonic climatology
            createHarmonic(climatologyPath, climatologyPath,                                                
                                            climatology.dfile)            

        else:
            print "In configure.txt climatolgyname is not 'miso' or \
                   climpartialdayfile not mentioned. \
                   So can not compute daily harmonic climatolgies."
        # end of if climatology.dfile and ...:
    # end of for climatology in climatologies:

    print "Done! Creation of Daily harmonic climatolgies netCdf Files"
# end of if __name__ == '__main__':
