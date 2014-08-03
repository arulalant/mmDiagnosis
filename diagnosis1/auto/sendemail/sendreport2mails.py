from mail import gmail
import os
import sys
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__curDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
prepreviousDir = os.path.abspath(os.path.join(__curDir__, '../..'))
# adding the previous path to python path
sys.path.append(prepreviousDir)
from diag_setup.globalconfig import archivepath
import datetime
from ping import sleepIfPingHostDown
import smtplib

'''
Written By : Arulalan.T
Date : 31.05.2014
'''

# sleep at most 100 min. check every 10 min interval ping host.
# if host is down for 100 min, then quit the program
sleepIfPingHostDown("smtp.gmail.com")

now = datetime.datetime.now()
curdate = now.strftime("%Y-%m-%d")

body=""
f1=open(os.path.join(__curDir__, 'body'))
for  bodylines in f1.readlines():
	body+=bodylines 
f1.close()


files = os.listdir(archivepath)
if len(files) > 0:
    attachment = os.path.join(archivepath, files[0])
    date = files[0].split('_')[1].split('.')[0]
    date = date[0:4]+'-'+date[4:6]+'-'+date[6:8]
else:
    attachment = None
    date = curdate
    
subject = "MJO @ NCMRWF - Auto Report on " + date

f = open(os.path.join(__curDir__, 'to_mails'))
try:
   for to_mail_id in f.readlines():
       if to_mail_id.startswith('#'): continue 
       to_mail_id=to_mail_id.strip()
       if not to_mail_id.endswith('>'):
           to_mail_id = '<' + to_mail_id + '>'
       # end of if not to_mail_id.endswith('>'):

       ### In NCMRWF, port 553 is closed.
       # 'nmap smtp.gmail.com' says port 25 only opens. 
       # So here we are using port as 25. But it throws some error at last.
       # Though email will be sent correctly. Tested.
       gmail(to_mail_id, subject, body, attachment, port=25)
       print "mail sent to :"+to_mail_id
except smtplib.SMTPRecipientsRefused, e:
    print "known error, need to fix it.\n %s" % str(e)
except Exception, e:
    print "what is this error,\n %s" % str(e)
finally:
    f.close()
# end of try: 

print "\nmail sent successfully to all\n"
