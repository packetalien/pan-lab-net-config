#!/usr/bin/env python
# ========================================================================
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# ========================================================================
# [1] https://blog.shichao.io/2012/10/04/progress_speed_indicator_for_urlretrieve_in_python.html
# Functions reporthook and save adapted/copied from [1]
#

__author__ = "Richard Porter (@packetalien)"
__copyright__ = "Copyright 2018, Palo Alto Networks"
__version__ = "0.1"
__license__ = "Apache 2.0"
__status__ = "Beta"

import os
import sys
import time
import getpass
import urllib
import urllib2
import hashlib
import fnmatch
from os.path import expanduser
from subprocess import call
from sys import platform
import platform

#MacOS Fusion Variables
vmnetfile = "fusion-vmnet-config.txt"
fusionconf = 'https://raw.githubusercontent.com/packetalien/pan-lab-net-config/master/fusion-vmnet-config.txt'
funsioncfgfile = 'networking'

#Windows Workstation Variables
workstationconf = 'https://github.com/packetalien/pan-lab-net-config/blob/master/se-default-vmnet.cfg'
workstationcfgfile = 'se-default-vmnet.cfg'


def integritycheck(filename):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()

def savemacos(url, filename):
    user,home = getuser()
    basedir = "/Documents/Virtual Machines.localized/IT-Managed-VMs"
    savedir = home + basedir + "/" + filename
    urllib.urlretrieve(url, savedir, reporthook)

def savewin(url, filename):
    user,home = getuser()
    basedir = os.path.normpath("/Documents/Virtual Machines/IT-Managed-VMs")
    savedir = os.path.normpath(home + basedir + "/" + filename)
    urllib.urlretrieve(url, savedir, reporthook)

def getuser():
    localuser = getpass.getuser()
    home = expanduser("~")
    return localuser, home

def filesearchmacos(filename):
    user,home = getuser()
    basedir = "/Documents/Virtual Machines.localized/IT-Managed-VMs"
    searchdir = home + basedir
    for base, dirs, files, in os.walk(searchdir):
        if filename in files:
            return True

def filecheckmacos(filename):
    basedir = '/Library/Preferences/'
    searchdir = basedir
    for base, dirs, files, in os.walk(searchdir):
        if filename in files:
            return True

def filecheckwin(filename):
    user,home = getuser()
    basedir = os.path.normpath("/Documents/Virtual Machines/IT-Managed-VMs")
    searchdir = os.path.normpath(home + basedir)
    for base, dirs, files, in os.walk(searchdir):
        if filename in files:
            return True

def importcfgwin(cfgfile):
    try:
        user,home = getuser()
        basedir = os.path.normpath(home)
        cfgimport = os.path.normpath("\"" + home + "\\" + cfgfile + "\"")
        cmd = os.path.normpath("\"C:\Program Files (x86)\VMware\VMware Workstation\\vnetlib.exe\"")
        cmdtrue = os.path.normpath(cmd + " " + "--" + " " + "import" + " " +  cfgimport)
        call(cmdtrue,shell=True)
        print("\n")
        print 30 * "-" , "IMPORT" , 30 * "-"
        print("File %s Imported." % (cfgimport))
        print("For support goto https://goo.gl/cHtQ2B")
        print 30 * "-" , "IMPORT" , 30 * "-"
        print("\n")
    except:
        print ("\n")
        print 30 * "-" , "ERROR" , 30 * "-"
        print("An error occured during import.")
        print("For support goto https://goo.gl/cHtQ2B")
        print 30 * "-" , "ERROR" , 30 * "-"
        print ("\n")

def cfgbackwin(cfgfile):
    try:
        user,home = getuser()
        basedir = os.path.normpath(home)
        worknetbuild = os.path.normpath(home + "\\"+ cfgfile)
        workbak = os.path.normpath(worknetbuild + filetimestamp())
        cmd = os.path.normpath("\"C:\Program Files (x86)\VMware\VMware Workstation\\vnetlib.exe\"")
        cmdtrue = os.path.normpath(cmd + " " + "--" + " " + "export" + " " + workbak)
        call(cmdtrue, shell=True)
        print("\n")
        print 30 * "-" , "BACKUP" , 30 * "-"
        print("Netconfig backuped. Find it at %s." % (workbak))
        print("For support goto https://goo.gl/cHtQ2B")
        print 30 * "-" , "BACKUP" , 30 * "-"
        print("\n")
    except:
        print ("\n")
        print 30 * "-" , "ERROR" , 30 * "-"
        print("An error occured during backup.")
        print("For support goto https://goo.gl/cHtQ2B")
        print 30 * "-" , "ERROR" , 30 * "-"
        print ("\n")

def importcfgmacos(filename):
    try:
        print 30 * "-" , "IMPORT" , 30 * "-"
        print("You will need to enter credentials three times.")
        user,home = getuser()
        basedir = "/Documents/Virtual Machines.localized/IT-Managed-VMs"
        savedir = home + basedir + "/" + filename
        fusionnetdir = '/Library/Preferences/VMware Fusion/'
        fusionnetbuild = fusionnetdir + "networking"
        subprocess.call(["sudo","/Applications/VMware Fusion.app/Contents/Library/vmnet-cli","--stop"])
        call(["cp","-f",savedir,fusionnetbuild])
        subprocess.call(["sudo","/Applications/VMware Fusion.app/Contents/Library/vmnet-cli","--configure"])
        subprocess.call(["sudo","/Applications/VMware Fusion.app/Contents/Library/vmnet-cli","--start"])
        print("Netconfig imported. Find it at %s." % (savedir))
        print("For support goto https://goo.gl/cHtQ2B")
        print 30 * "-" , "IMPORT" , 30 * "-"
        print("\n")
    except:
        print ("\n")
        print 30 * "-" , "ERROR" , 30 * "-"
        print("An error occured during import.")
        print("For support goto https://goo.gl/cHtQ2B")
        print 30 * "-" , "ERROR" , 30 * "-"
        print ("\n")

def cfgbackmacos(filename):
    try:
        fusionnetdir = '/Library/Preferences/VMware Fusion/'
        fusionnetbuild = fusionnetdir + "networking"
        if filecheckmacos(filename):
            print("\n")
            print 30 * "-" , "BACKUP" , 30 * "-"
            print("You will need to enter credentials to backup.")
            fusionbak = fusionnetbuild + filetimestamp()
            subprocess.call(["sudo","cp","-f",fusionnetbuild,fusionbak])
            print("Netconfig backuped. Find it at %s." % (fusionbak))
            print("For support goto https://goo.gl/cHtQ2B")
            print 30 * "-" , "BACKUP" , 30 * "-"
            print("\n")
        else:
            print ("\n")
            print 30 * "-" , "ERROR" , 30 * "-"
            print("Network config not present.")
            print("Start VMWare Fusion and try again.")
            print("For support goto https://goo.gl/cHtQ2B")
            print 30 * "-" , "ERROR" , 30 * "-"
            print ("\n")
    except:
        print ("\n")
        print 30 * "-" , "ERROR" , 30 * "-"
        print("An error occured during backup.")
        print("For support goto https://goo.gl/cHtQ2B")
        print 30 * "-" , "ERROR" , 30 * "-"
        print ("\n")

def filetimestamp():
    filetimestamp = time.strftime("%Y%m%d-%H%M%S")
    tagstamp = filetimestamp + ".bak"
    return tagstamp

def main():
    username,homedir = getuser()
    oscheck = platform.system()
    if oscheck == "Darwin":
        try:
            if filesearchmacos(vmnetfile):
                print("\n")
                print 30 * "=" , "CONFIGURING" , 30 * "="
                cfgbackmacos(funsioncfgfile)
                importcfgmacos(vmnetfile)
                print("Successful import and backup.")
                print("For support goto https://goo.gl/cHtQ2B")
                print 30 * "=" , "CONFIGURING" , 30 * "="
                print("\n")
            else:
                print("\n")
                print 30 * "=" , "CONFIGURING" , 30 * "="
                print("Config file not found.")
                print("Attempting to retrieve it.")
                savemacos(fusionconf,vmnetfile)
                print("Success.")
                cfgbackmacos(funsioncfgfile)
                importcfgmacos(vmnetfile)
                print("Successful import and backup.")
                print("For support goto https://goo.gl/cHtQ2B")
                print 30 * "=" , "CONFIGURING" , 30 * "="
                print("\n")
        except:
            print ("\n")
            print 30 * "-" , "ERROR" , 30 * "-"
            print("An error has occured.")
            print("For support goto https://goo.gl/cHtQ2B")
            print 30 * "-" , "ERROR" , 30 * "-"
            print ("\n")
    elif oscheck == "Windows":
        try:
            if filecheckwin(workstationcfgfile):
                print("\n")
                print 30 * "=" , "CONFIGURING" , 30 * "="
                cfgbackwin(workstationcfgfile)
                importcfgwin(workstationcfgfile)
                print("Successful import and backup.")
                print("For support goto https://goo.gl/cHtQ2B")
                print 30 * "=" , "CONFIGURING" , 30 * "="
                print("\n")
            else:
                print("\n")
                print 30 * "=" , "CONFIGURING" , 30 * "="
                print("Config file not found.")
                print("Attempting to retrieve it.")
                savemacos(workstationconf,workstationcfgfile)
                print("Success.")
                cfgbackwin(workstationcfgfile)
                importcfgwin(workstationcfgfile)
                print("Successful import and backup.")
                print("For support goto https://goo.gl/cHtQ2B")
                print 30 * "=" , "CONFIGURING" , 30 * "="
                print("\n")
        except:
            print ("\n")
            print 30 * "-" , "ERROR" , 30 * "-"
            print("An error has occured.")
            print("For support goto https://goo.gl/cHtQ2B")
            print 30 * "-" , "ERROR" , 30 * "-"
            print ("\n")
    else:
        print ("\n")
        print 30 * "-" , "ERROR" , 30 * "-"
        print("Operating System either unidentifed or not supported.")
        print("For support goto https://goo.gl/cHtQ2B.")
        print 30 * "-" , "ERROR" , 30 * "-"
        print ("\n")

if __name__ == "__main__":
    main()
