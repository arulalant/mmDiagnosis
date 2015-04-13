import os
import sys
import paramiko
from scp import SCPClient
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__diagnosisDir__ = os.path.dirname(__file__)
previousDir = os.path.abspath(os.path.join(__diagnosisDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import ftppath, archivepath
from ping import sleepIfPingHostDown


def push2server(sshuser='kuldeep', sshserver='192.168.1.102',
             sshpass='kuldeep123', privatekey=None,
             topath='/home/ftp/pub/outgoing/kuldeep/MJO_at_NCMRWF'):
    
    # sleep at most 100 min. check every 10 min interval ping host.
    # if host is down for 100 min, then quit the program
    sleepIfPingHostDown(sshserver)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if sshpass:
        ssh.connect(sshserver, username=sshuser, password=sshpass)
    else:
        ssh.connect(sshserver, username=sshuser, key_filename=privatekey)

    scp = SCPClient(ssh.get_transport())

    currentDir = os.getcwd()
    os.chdir(archivepath)
    files = os.listdir(archivepath)
    for fname in files:
        scp.put(fname, topath)
    # end of for fname in files:
    ssh.close()  # close ssh
    os.chdir(currentDir)
# end of def push2server(...):


if __name__ == '__main__':    
    
    push2server(sshserver=ftppath)
# end of if __name__ == '__main__':





