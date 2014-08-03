#!/usr/local/uvcdat/1.3.1/bin/python
import datetime, os, sys, time
while True:
 now = datetime.datetime.now()
 today = now.strftime('%Y-%m-%d %H:%M')
 c_date = today.split(' ')[0]
 c_hour, c_min = today.split(' ')[1].split(':')
 #print c_min
 datefile = '/home/kuldeep/IITD/ncmrwf-replication/auto/auto_cron_date.txt'

 if os.path.isfile(datefile):
   f = open(datefile)
   file_date = f.readlines()[0].strip()
   if file_date == c_date:
       print "going to sleep for 1 hour"
       time.sleep(60*60)

 if c_hour == '14' and c_min == '00':
     print "Initiated"
     os.system("/usr/bin/xvfb-run export DISPLAY='localhost:213.0' & /usr/local/uvcdat/1.3.1/bin/python /home/kuldeep/IITD/ncmrwf-replication/auto/auto_run_all.py >> /home/kuldeep/IITD/ncmrwf-replication/auto/auto_run_all_cron.txt")

     f = open(datefile, 'w')
     f.write(c_date)
     f.close()
 time.sleep(30)
 
