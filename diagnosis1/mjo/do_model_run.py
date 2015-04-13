import os, sys
# It contains only model projected scripts
level1 = {1: {'variance': {1: 'make_model_anomaly.py',
              2: 'do_model_lfilter.py'}}
        }


level2 = {1: {'ceof': {1: 'compute_model_projected_pcts.py',
             2: 'plot_model_projected_pcts.py'}},

        2: {'phase3d': {1: 'model_projected_pcts_amplitude_phase.py',
                        2: 'plot_model_projected_pcts_phase3d.py'}},
        }

mjoPath = '.'
uvcdat = '/home/dileep/UV-CDAT_Versions/uv1_2/install/bin//python'

choice = raw_input("1. Level1 \n2. Level2 \n3. Both Level1 and Level2 \
                     \n0.quit \nEnter Your Choice : ").strip()

if choice == '1':
    user_level = [('level1', level1)]
elif choice == '2':
    user_level = [('level2', level2)]
elif choice == '3':
    user_level = [('level1', level1), ('level2', level2)]
else:
    sys.exit(0)

for level, levelDic in user_level:
    for i in range(1, len(levelDic)+1):
        processDic = levelDic.get(i)
        for processName in processDic:
            print processName
            processScripts = processDic[processName]

            for j in range(1, len(processScripts)+1):
                script = processScripts[j]
                scriptPath = os.path.join(mjoPath, level, processName, script)
                logfile = os.path.join(mjoPath, 'all_log.txt')
                cmd = uvcdat + '  ' + scriptPath #+ '  >> ' + logfile
                print "Executing ", cmd
                os.system(cmd)
            # end of for j in range(1, len(processScripts)+1):
        # end of for processName in processDic:
    # end of  for i in range(1, len(levelDic)+1):
# end of for level, levelDic in user_level:





















