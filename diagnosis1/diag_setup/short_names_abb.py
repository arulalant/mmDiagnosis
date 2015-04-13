"""
    short_names_abb.py : Loads the `short_names_abbreviation.json` file and make it as
               python dictionary variable.
    
    Written By : Arulalan.T
    
    Date : 09.02.2012
    
"""

import os
import json
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__setupDir__ = os.path.dirname(__file__)

if __setupDir__ == '':
    __setupDir__ = '.'

_pathfile = open(__setupDir__ + '/short_names_abbreviation .json')

shortNamesAbb = json.loads(_pathfile.read())
