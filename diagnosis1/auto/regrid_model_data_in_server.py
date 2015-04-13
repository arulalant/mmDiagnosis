import os
import sys, time
import paramiko
from paramiko.common import INFO
# setting the absolute path of the previous directory
# getting the this py module path by __file__ variable
# pass that __file__ to the os.path.dirname, returns the path of this module
__curDir__ = os.path.abspath(os.path.dirname(__file__))
previousDir = os.path.abspath(os.path.join(__curDir__, '..'))
# adding the previous path to python path
sys.path.append(previousDir)
from diag_setup.globalconfig import logpath
from ping import pinghost
from ping import sleepIfPingHostDown


# create log object to written into logfile
logfile = os.path.join(logpath, __file__.split('.py')[0] + '.log')
# set the logfile path to the paramiko module
paramiko.util.log_to_file(logfile)


def regridOf(date, sshuser='kuldeep', sshserver='ncmr0102', sshpass=None,
            privatekey='/home/kuldeep/.ssh/id_rsa',
            cmdpath='/gpfs1/home/exp/gfs/nwprod/util/exec/',
            wgribpath='/gpfs1/software/openg/wgrib',
            frompath='/gpfs1/home/exp/gfs/nwdata/post/',
            topath='/scratch/ncmrtmp/kuldeep/2014/GFS/data/1p0/',
            regridcmd='copygb', dprefix='gdas.', fprefix='gdas1.t00z.grb',
        files=['anl', 'f24', 'f48', 'f72', 'f96', 'f120', 'f144', 'f168'], **kwarg):

    # sleep at most 100 min. check every 10 min interval ping host.
    # if host is down for 100 min, then quit the program
    sleepIfPingHostDown(sshserver)
    
    wgrib = kwarg.get('wgrib', False)
    varname = kwarg.get('varname', 'ULWRF')
    wpath = kwarg.get('wpath', None)

    year = date[:4]
    date_dir = dprefix + date
    frompath = os.path.join(frompath, date_dir)
    topath = os.path.join(topath, date_dir)    

    print "Login to ssh %s@%s" % (sshuser, sshserver)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if sshpass:
        ssh.connect(sshserver, username=sshuser, password=sshpass)
    else:
        ssh.connect(sshserver, username=sshuser, key_filename=privatekey)
    
    # login to the remote server machine/user.
    transport = ssh.get_transport()
    print "created path", topath
    transport._log(INFO, "Executing bash")
    stdin, stdout, stderr = ssh.exec_command("bash")
    # create directory path of topath
    cmd_make_topath = "mkdir -p %s " % topath
    transport._log(INFO, "Create path %s" % cmd_make_topath)
    stdin, stdout, stderr = ssh.exec_command(cmd_make_topath)
    cmdpath = os.path.join(cmdpath, regridcmd)
    
    if wpath:
        # create directory path of wpath
        wpath = os.path.join(wpath, date_dir)
        print "created path", wpath
        cmd_make_wpath = "mkdir -p %s " % wpath
        transport._log(INFO, "Create path %s" % cmd_make_wpath)
        stdin, stdout, stderr = ssh.exec_command(cmd_make_wpath)
        time.sleep(5)
    # end of if wpath:    

    for gribfile in files:
        gribfile = fprefix + gribfile
        infilepath = os.path.join(frompath, gribfile)
        outfilepath = os.path.join(topath, gribfile)
        if wgrib:
            wgribfilepath = os.path.join(wpath, gribfile)
            wgrib_cmd = "%s -s %s | grep '%s' | %s -i %s -grib -o %s" % (wgribpath, infilepath,
                                                    varname, wgribpath, infilepath, wgribfilepath)
            transport._log(INFO, "Executing Extraction '%s' variable alone by cmd '%s'" % (varname, wgrib_cmd))
            transport._log(INFO, wgrib_cmd)
            stdin, stdout, stderr = ssh.exec_command(wgrib_cmd)
            # lets wait 2 min to complete the above cmd
            time.sleep(120)
            # check the output file size is > 0 byte. Otherwise wait 2 min 
            # inside (10 times) loop until file size is > 0 byte.
            count = 0
            flag = True
            while (count < 20):
                getsize = "du %s" % wgribfilepath
                stdin, stdout, stderr = ssh.exec_command(getsize)                
                filesizeinfo = stdout.readlines()
                if len(filesizeinfo) == 0:
                    # i.e. du fpath returns none, because no such file exists till now!
                    if pinghost(sshserver):
                        pingstatus = "'%s' ping is up!" % sshserver                          
                    else:
                        pingstatus = "'%s' ping is down!!! Oops !" % sshserver                        
                    # end of if pinghost(sshserver):
                    transport._log(INFO, "%s file couldn't create. %s. 2 min sleep initiated, count=%d" % (outfilepath, pingstatus, count)) 
                    time.sleep(120)
                    count += 1
                    if (count % 5 == 0):
                        # some times the first regrid cmd may not execute properly 
                        # if actual file is in residence mode or in migrate mode.
                        # so lets redo it few more times.
                        transport._log(INFO, "Executing Regrid %s again" % wgrib_cmd)
                        stdin, stdout, stderr = ssh.exec_command(wgrib_cmd)
                    # end of if (count % 5 == 0):
                    continue    
                else:
                    filesizeinfo = filesizeinfo[0]
                # end of if len(filesizeinfo) == 0:
                if not filesizeinfo:
                    transport._log(INFO, "%s file 'du' command returns None like filesizeinfo '%s'" % (outfilepath, filesizeinfo))  
                filesize = int(filesizeinfo.split('\t')[0])
                if not filesize > 0:
                    # We need to give 2 min sleep (to fetch data from ibm tab),
                    # till it finishes wgrib cmd (then only it can extract olr
                    # variable alone, otherwise 0 byte error will occur).    
                    count += 1
                    transport._log(INFO, "%s file has 0 byte. So 0.5 min sleep initiated. Count=%d" % (wgribfilepath, count))        
                    time.sleep(30)                    
                else:      
                    msg = "%s has %d byte. " % (wgribfilepath, filesize)      
                    transport._log(INFO, msg+"(i.e. File written properly). So lets continue next task.")      
                    flag = False    
                    break
            # end of while (count < 10):
            
            # Since olr variable alone extracted and saved in outfilepath,
            # we need to give this outfilepath as infilepath to do regrid.
            infilepath = wgribfilepath
        # end of if wgrib:
        
        # regrid command from model resolution into 1x1 grid
        regrid_cmd = "%s -g3 -x %s %s" % (cmdpath, infilepath, outfilepath)
        transport._log(INFO, "Executing Regrid %s" % regrid_cmd)
        stdin, stdout, stderr = ssh.exec_command(regrid_cmd)
        # lets wait 2 min to complete the above cmd
        time.sleep(120)
        # check the output file size is > 0 byte. Otherwise wait 2 min 
        # inside (10 times) loop until file size is > 0 byte.
        count = 0
        flag = True
        while (count < 20):
            getsize = "du %s" % outfilepath
            stdin, stdout, stderr = ssh.exec_command(getsize)            
            filesizeinfo = stdout.readlines()
            if len(filesizeinfo) == 0:
                # i.e. du fpath returns none, because no such file exists till now!
                if pinghost(sshserver):
                    pingstatus = "'%s' ping is up!" % sshserver                          
                else:
                    pingstatus = "'%s' ping is down!!! Oops !" % sshserver                        
                # end of if pinghost(sshserver):
                transport._log(INFO, "%s file couldn't create. %s. 2 min sleep initiated.count=%d" % (outfilepath, pingstatus, count)) 
                time.sleep(120)
                count += 1
                if (count % 5 == 0):
                    # some times the first regrid cmd may not execute properly 
                    # if actual file is in residence mode or in migrate mode.
                    # so lets redo it few more times.
                    transport._log(INFO, "Executing Regrid %s again" % regrid_cmd)
                    stdin, stdout, stderr = ssh.exec_command(regrid_cmd)
                # end of if (count % 5 == 0):
                continue    
            else:
                filesizeinfo = filesizeinfo[0]
            # end of if len(filesizeinfo) == 0:
                
            if not filesizeinfo:
                transport._log(INFO, "%s file 'du' command returns None like filesizeinfo '%s'" % (outfilepath, filesizeinfo))  
            filesize = int(filesizeinfo.split('\t')[0])
            if not filesize > 0:
                # We need to give 2 min sleep (to fetch data from ibm tab),
                # till it finishes copygb regrid cmd (then only it contains
                # variables, otherwise 0 byte error will occur).   
                count += 1
                transport._log(INFO, "%s file has 0 byte. So 0.5 min sleep initiated. Count=%d" % (outfilepath, count))  
                time.sleep(30)                
            else:            
                msg = "%s has %d byte. " % (outfilepath, filesize)      
                transport._log(INFO, msg+"(i.e. File written properly). So lets continue next task.")  
                flag = False    
                break
        # end of while (count < 10):
    # end of for gribfile in files:
    # logout from the ssh user
    ssh.close()
    transport._log(INFO, "ssh session has closed")
    print "Logout from %s@%s" % (sshuser, sshserver)
# end of def regridOf(date, ...):


def regridOlrOf(date, frompath='/gpfs1/home/exp/gfs/nwdata/fcst/',
                topath='/scratch/ncmrtmp/kuldeep/2014/GFS/olr/1p0/',
                wpath='/scratch/ncmrtmp/kuldeep/2014/GFS/olr/data/',
                fprefix='gdas1.t00z.sfluxgrb', files=['f01'], wgrib=True):

    regridOf(date, frompath=frompath, topath=topath,
                       fprefix=fprefix, files=files, wpath=wpath, wgrib=wgrib)
# end of def regridOlrOf(date,...):








