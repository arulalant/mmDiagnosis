import os
import re
from collections import namedtuple

# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__setupDir__ = os.path.dirname(__file__)
# define the namedtuple for 'vars'
_varslist = namedtuple('vars', 'model_var, model_level, clim_var, obs_var, long_name, anl_hour')
# initializing the _varslist
_var = _varslist(None, None, None, None, None, None)

if __setupDir__ == '':
    __setupDir__ = '.'
pathfile = open(__setupDir__ + '/' + 'vars.txt')

variables = {}
for line in pathfile.readlines():
    if line.startswith('#'):
        # comment line in the text file. skip this line
        continue
    if line.find('#') != -1:
        # comment inline. removing commented parts inline
        line = line.split('#')[0]
    # removing whitespace fully
    linecopy = re.sub(r'\s', '', line)
    if linecopy.startswith('modelname') or linecopy.startswith('model_name') \
        or linecopy.startswith('obsname') or linecopy.startswith('obs_name') \
                                              or linecopy.startswith('name'):
        modelname = linecopy.split('=')[1]
        variables[modelname] = {}
    elif linecopy.startswith('short_var'):
        if not variables:
            raise ValueError("First set the model_name or modelname in the \
                              vars.txt file at the begining of the file.")
        textcopy = linecopy.split(',')
        text = line.split(',')
        varid = textcopy[0]
        if varid:
            shortvar, modelvar, model_level, climvar, obsvar = '', '', None, '', ''
            name, analysis_hour = '', None
            collections = {}
            for string, txt in zip(textcopy, text):
                value = string.split('=')[1]
                if string.startswith('short'):
                    shortvar = value
                    if not shortvar:
                        print "short is empty string. So skipping %s while \
                              collecting global variables name " % varid
                        continue
                    # end of if not modelvar:
                elif string.startswith('model') and not string.startswith('model_level'):
                    modelvar = value
                    if not modelvar:
                        print "model is empty string. So skipping %s while \
                              collecting global variables name " % varid
                        continue
                    # end of if not modelvar:
                elif string.startswith('model_level'):
                    model_level = value
                    if model_level:
                        model_level = float(model_level)
                elif string.startswith('clim'):
                    climvar = value
                elif string.startswith('obs'):
                    obsvar = value
                elif string.startswith('long_name'):
                    name = txt.split('=')[1].strip()
                elif string.startswith('anl_hour'):
                    analysis_hour = txt.split('=')[1].strip()
                else:
                    pass
                    # unneccessary text
            # end of for string, txt in zip(textcopy, text):
            # make copy of _var namedtuple with assigned values in dict
            collections[shortvar] = _var._replace(model_var=modelvar,
                                                  model_level=model_level,  
                                                  clim_var=climvar,
                                                  obs_var=obsvar,
                                                  long_name=name, 
                                                  anl_hour=analysis_hour)
            # update the global variables dictionary
            variables[modelname].update(collections)
        # end of if varid:
    elif linecopy.startswith('isovars'):
        isovars = linecopy.split('=')[1].split(',')
    else:
        # unneccessary contents
        pass
    # end of if linecopy.startswith('modelname'):
# end of for line in pathfile.readlines():
