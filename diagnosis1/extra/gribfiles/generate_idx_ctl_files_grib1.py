# This scipt will generate the ctl and idx files of the grib1 (<2) data of
# NCMRWF 2010 data

import os


walk = os.walk('/NCMRWF/ncmrwf-data-2010/')
for root, sub, files in walk:
    print root
    os.chdir(root)
    for f in files:
        if f.endswith('anl'):
            # Do need full to create ctl,idx files for the analysis files
            # -ts1dy is for setting 1day time stamp in ctl file
            os.system("grib2ctl.pl %s -ts1dy > %s.ctl " % (f, f))
            os.system("gribmap -i %s.ctl" % (f))
            #print os.system("ls")
        else:
            try:
                if (f.split('.')[2]).startswith('grbf') and \
                    not f.endswith('.idx') and not f.endswith('.ctl'):
                    # Do need full to create ctl,idx
                    # files for the fcst files
                    # -ts1dy is for setting 1day time stamp in ctl file
                    # we no need to pass -verf option for fcst file, since
                    # it cdat cant read the data
                    os.system("grib2ctl.pl %s -ts1dy > %s.ctl " % (f, f))
                    os.system("gribmap -i %s.ctl -0 " % (f))

            except:
                #continue
                pass

    print os.system("ls")

print "Done"
