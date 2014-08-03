import os, sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__autoDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__autoDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import uvcdat, logpath

# It contains only model projected scripts
level1 = {1: {'variance': {1: 'make_model_anomaly.py',
              2: 'do_model_lfilter.py',
              3: 'do_merge_model_anl_fcst_apply_lfilter.py'}}
        }

level2 = {1: {'ceof': {1: 'compute_model_projected_pcts.py',
             2: 'plot_model_projected_pcts.py'}},

        2: {'phase3d': {1: 'model_projected_pcts_amplitude_phase.py',
                        2: 'plot_model_projected_pcts_phase3d.py'}},
        }

mjoPath = os.path.join(previousDir, 'mjo')
# do both level1 and leve2
choice = '3'

if choice == '1':
    user_level = [('level1', level1)]
elif choice == '2':
    user_level = [('level2', level2)]
elif choice == '3':
    user_level = [('level1', level1), ('level2', level2)]
else:
    sys.exit(0)


thisDir = os.getcwd()
for level, levelDic in user_level:
    for i in range(1, len(levelDic)+1):
        processDic = levelDic.get(i)
        for processName in processDic:
            processScripts = processDic[processName]
            for j in range(1, len(processScripts)+1):
                script = processScripts[j]
                scriptPath = os.path.join(mjoPath, level, processName)
                os.chdir(scriptPath)
                logfile = os.path.join(logpath, 'mjo_model_run_log.txt')
                cmd = uvcdat + '  ' + script + '  >> ' + logfile
                print "Executing ", cmd
                os.system(cmd)
            # end of for j in range(1, len(processScripts)+1):
        # end of for processName in processDic:
    # end of  for i in range(1, len(levelDic)+1):
# end of for level, levelDic in user_level:

os.chdir(thisDir)


