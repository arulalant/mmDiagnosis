import os

uvcdat = '/usr/local/uvcdat/1.2.0/bin//python'
anomaly_script = 'make_obs_anomaly.py'
filter_script = 'do_lfilter.py'

f = open('log.txt', 'w')
cmd1 = uvcdat + '  ' + anomaly_script + '  >> anolog.txt'
r1 = os.popen(cmd1)
#for line in r1.readlines():
#    f.write(line)

#del r1

cmd2 = uvcdat + '  ' + filter_script + '  >> fillog.txt'
r2 = os.popen(cmd2)
#for line in r2.readlines():
#    f.write(line)

#f.close()

#del r2
