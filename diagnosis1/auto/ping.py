import os, sys


def pinghost(hostname='www.google.com', wait='20'):
    '''
    hostname - either ip or hostname in str type
    wait - sec in str type
        
    Date : 29.05.2014
    '''
    response = os.system("ping -c 1 -t " + wait + ' ' + hostname + " > /dev/null 2>&1")
    #time.sleep(int(wait))
    if response == 0:
        print hostname, 'is up!'
        result = True
    else:
        print hostname, 'is down!'
        result = False
    return result
# end of def pinghost(hostname='google.com', wait='20'):

def sleepIfPingHostDown(hostname, sec=600, counter=10):
    '''
    sec - default it takes 10 min
    counter - 10
    So it will wait 10 min and reping again. If host is up, then it will 
    return, else again sleep. It will repeat the same for counter times 
    (by default 10 times, so total 100 min (1 hour, 40 min)
    
    Written By : Arulalan.T
    Date : 31.05.2014
    '''
    count = 0
    while (count < counter):
        if pinghost(hostname):
            return
        else:
            print "%s is down! so taking %d sec sleep. count=%d" % (hostname, sec, count)
            time.sleep(sec)
        # end of if pinghost(hostname):
        count += 1
    # end of while (count < counter):
    if pinghost(hostname):
        return
    else:
        sys.exit(0)
    # end of if pinghost(hostname):
# end of def sleepIfPingHostDown(hostname, sec):
    

### pure python ping - https://github.com/duanev/ping-python

#import subprocess
#hostname = "google.com"
#ping_response = subprocess.Popen(["/bin/ping", "-c1", "-w100", hostname], stdout=subprocess.PIPE).stdout.read()
#print ping_response
#if ping_response == 0:
#  print hostname, 'is up!'
#else:
#  print hostname, 'is down!'


