import os, sys
### It is having only facility to run observation data set.
## Todo :
# Not model dataset. Need to add those scripts path in this dictionaries..
level1 = {1: {'variance': {1: 'make_obs_anomaly.py',
              2: 'do_obs_lfilter.py',
              3: 'do_variance_plot.py'}},

        2: {'ps': {1: 'do_avg.py',
                   2: 'plot_ps.py',
                   3: 'calculate_waveno.py',
                   4: 'plot_ps_2d.py'}},

        3: {'eof': {1: 'regrid_obs_into_5x5_grid.py',
                    2: 'eof_diag.py',
                    3: 'plot_eof.py'}}
        }


level2 = {1: {'ceof': {1: 'ceof_diag.py',
             2: 'plot_ceof.py'}},

        2: {'phase3d': {1: 'amplitude_phase.py',
                        2: 'plot_phase3d.py'}},

        3: {'phase2d': {1: 'compute_spatial_phases_vars.py',
                        2: 'plot_spatial_phase_vars.py'}},

        4: {'wk': {1: 'plot_wk_figures.py'}}

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





















