# This scipt will generate the ctl and idx files of the grib2 data of
# Models 2010 data

import os

walk = os.walk('/mnt/MODEL_DATA/CMC')
for root, sub, files in walk:
    print root
    os.chdir(root)
    for f in files:        
        if f.endswith('_anl.grib') and not f.endswith('.idx') \
                  and not f.endswith('.ctl') and not f.endswith('.pdef'):
            # Do need full to create ctl,idx files for the analysis files
            # -ts1dy is for setting 1day time stamp in ctl file
            # if timeaxis has day wise and stepday is 1 means, use ts1dy
            # option while create ctl file. Then only cdscan will works.
            # mn - minutes
            # hr - hour
            # dy - day
            # mo - month
            # yr - year
            os.system("g2ctl.pl -0 %s -ts1dy > %s.ctl " % (f, f))
            os.system("/usr/local/bin/grads-2.0.a8/gribmap -0 -i %s.ctl" % (f))
            #print os.system("ls")
        else:
            try:
                if (f.split('_')[3]).startswith('f') and \
                    not f.endswith('.idx') and not f.endswith('.ctl') \
                                            and not f.endswith('.pdef'):
                    # Do need full to create ctl,idx
                    # files for the fcst files
                    # -ts1dy is for setting 1day time stamp in ctl file
                    os.system("g2ctl.pl %s -ts1dy > %s.ctl " % (f, f))
                    os.system("/usr/local/bin/grads-2.0.a8/gribmap -i %s.ctl " % (f))

            except:
                #continue
                pass

    print os.system("ls")

print "Done"
