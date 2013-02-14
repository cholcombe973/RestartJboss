    #
    #Restarts the running jboss process
    #
__author__="cjh66"
__date__ ="$Apr 15, 2010 11:12:00 AM$"


import os
import signal
import subprocess
from subprocess import PIPE
import sys
import time

'''
    Returns the pid if 1 pid is found.  If none or multiple are returned
    this function will return None.
'''
def get_pid(name):
    cmd = subprocess.Popen("pgrep %s" % name, shell=True, stdout=PIPE).stdout
    pid = cmd.read()
    if len(pid) is 0:
        return None
    else:
        #check for multiple values
        if len(pid.split('\n')) > 2:
            return None
        else:
            # 1 pid value found and returned
            return pid.strip('\n')

if __name__ == "__main__":
    
    pid = get_pid("java")
    if pid is None:
        print "Pid not found, exiting"
        sys.exit(0)
    else:
        #watch the process until it's shut down and then restart the jboss
        print "killing process"
        os.kill(int(pid),signal.SIGKILL)
        #check if process is done

        while get_pid("java") is not None:
            time.sleep(5) #hold until process stops

        print "Restarting jboss"
        os.chdir("/app/jboss/bin")
        subprocess.Popen("su jboss -c /app/jboss/bin/startupJboss.sh", shell=True)
        print "Jboss process kicked off, exiting"
        sys.exit(0)