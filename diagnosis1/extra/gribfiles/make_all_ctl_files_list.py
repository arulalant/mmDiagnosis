''' Collecting all the anl,f24,f48,...,f168 ctl files and put into 
    seperate file lists as text files. So that using the output text files
    we can create xml file by passing that as input file to cdscan cmd.
'''

import os

datadir = '/NCMRWF/ncmrwf-data-2010'

os.chdir(datadir)
fanl = open('all_anl_ctl_list.txt', 'w')
f24 = open('all_fcst_24hr_ctl_list.txt', 'w')
f48 = open('all_fcst_48hr_ctl_list.txt', 'w')
f72 = open('all_fcst_72hr_ctl_list.txt', 'w')
f96 = open('all_fcst_96hr_ctl_list.txt', 'w')
f120 = open('all_fcst_120hr_ctl_list.txt', 'w')
f144 = open('all_fcst_144hr_ctl_list.txt', 'w')
f168 = open('all_fcst_168hr_ctl_list.txt', 'w')

for root, sub, files in os.walk('.'):
    print root
    for ctl in files:
        if ctl.endswith('grbanl.ctl'):
            # anl ctl file 
            fanl.write(root + '/' + ctl + '\n')
        
        elif ctl.endswith('grbf24.ctl'):
            # fcst 24 hout file
            f24.write(root + '/' + ctl + '\n')
            
        elif ctl.endswith('grbf48.ctl'):
            # fcst 48 hour files
            f48.write(root + '/' + ctl + '\n')            
           
        elif ctl.endswith('grbf72.ctl'):
            # fcst 72 hour files
            f72.write(root + '/' + ctl + '\n')            
           
        elif ctl.endswith('grbf96.ctl'):
            # fcst 96 hour files
            f96.write(root + '/' + ctl + '\n')            
           
        elif ctl.endswith('grbf120.ctl'):
            # fcst 120 hour files
            f120.write(root + '/' + ctl + '\n')            
           
        elif ctl.endswith('grbf144.ctl'):
            # fcst 144 hour files
            f144.write(root + '/' + ctl + '\n')            
           
        elif ctl.endswith('grbf168.ctl'):
            # fcst 168 hour files
            f168.write(root + '/' + ctl + '\n')
            
        else:
            pass
            
        # end of if
    # end of for ctl in files:
# end of for root,sub,files in os.walk(datadir): 
