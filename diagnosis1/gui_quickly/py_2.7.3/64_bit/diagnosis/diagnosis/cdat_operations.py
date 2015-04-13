import sys 
#sys.path.append('/home/arulalan/GIT/uvcdat_source/install/bin/')
sys.path.insert(0,'/home/arulalan/GIT/uvcdat_source/install/lib/python2.7/site-packages')


def cdfile_check(filePath):
    import cdms2
    try:
        f = cdms2.open(filePath, 'r')
        f.close()
        del f
        return True
    except cdms2.error.CDMSError, AttributeError:
        #print "Error Handling"
        return False
    except:
        return False
        
def get_year(filePath):
    import cdms2
    try:
        f = cdms2.open(filePath, 'r')
        variables = f.listvariables()
        
        for var in variables:            
            if not var.startswith('_'):
                # get the time of the variable 
                time = f[var].getTime()
                # get the units 
                units = time.units                
                # do the string operation to get the year from the units
                year = units.split('-')[0].split()[-1]
                f.close()
                return year                 
                # we can get the year as follows. But it loads all the time 
                # objects into list.
                #year = time.asComponentTime()[0].year        
                
    except cdms2.error.CDMSError, AttributeError:
        #print "Error Handling"
        return None
    except:
        return None
    
        
