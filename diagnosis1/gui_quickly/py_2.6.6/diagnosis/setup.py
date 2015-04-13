#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 <Arulalan.T> <arulalant@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys
# the below path purpose is while creating $ quickly package, it should do the 
# import cdms2. For that purpose only, here we are setting the uvcdat/cdat path.
# later we must remove the below statement, by installing cdat in system python.
# so import cdms2 should work. 
sys.path.insert(0,'/home/arulalan/GIT/uvcdat_source/install/lib/python2.7/site-packages')
try:
    import DistUtilsExtra.auto
except ImportError:
    print >> sys.stderr, 'To build diagnosis you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

def update_data_path(prefix, oldvalue=None):

    try:
        fin = file('diagnosis/diagnosisconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:            
            fields = line.split(' = ') # Separate variable from value
            if fields[0] == '__diagnosis_data_directory__':
                # update to prefix, store oldvalue
                if not oldvalue:
                    oldvalue = fields[1]
                    line = "%s = '%s'\n" % (fields[0], prefix)
                else: # restore oldvalue
                    line = "%s = %s" % (fields[0], oldvalue)
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find diagnosis/diagnosisconfig.py")
        sys.exit(1)
    return oldvalue


def update_desktop_file(datadir):

    try:
        fin = file('diagnosis.desktop.in', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:            
            if 'Icon=' in line:
                line = "Icon=%s\n" % (datadir + 'media/icon.png')
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find diagnosis.desktop.in")
        sys.exit(1)


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        previous_value = update_data_path(self.prefix + '/share/diagnosis/')
        update_desktop_file(self.prefix + '/share/diagnosis/')
        DistUtilsExtra.auto.install_auto.run(self)
        update_data_path(self.prefix, previous_value)


        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
## In below string lines, we should not use triple single quotes or triple double
## quotes. If we used, while creating $ quickly package, it should throws error.
## So we have to use \ (back slash) to write multiple lines.
##################################################################################

DistUtilsExtra.auto.setup(
    name='diagnosis',
    version='0.1',
    license='GPL-3',
    author='Arulalan.T',
    author_email='arulalant@gmail.com',
    description='UI for managing diagnosis …',
    long_description='We can register model, observartion, climatology dataset. \
                      After that make cf standard name pair with the model variables \
                      name. Also can register the regular routine process. ',
    #url='https://launchpad.net/diagnosis',
    cmdclass={'install': InstallAndUpdateDataDirectory}
    )

