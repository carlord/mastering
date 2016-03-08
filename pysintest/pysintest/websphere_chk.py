#!/usr/bin/env python/
#this modul grabs operations performed with WAS (IBM - Websphere Application)
# - Websphere_eval function retrieves Data (info) about current installation 
#    inf, version, paths
import os, re, subprocess, crypt, random, string, sys, getopt, platform, fileinput, shlex, socket, paramiko
#lexbz1015.lexington.ibm.com
#lexbz181189.lex.dst.ibm.com
#sbybz3106.sby.ibm.com
#sbybz3107.sby.ibm.co#lexbz1156.lexington.ibm.com
#--------- PARAMIKO block ------------------------------------------ 
mySSHKEY='/home/carlos/.ssh/id_rsa.pub'   ##-- to be defined with personal user's pub key'
sshcon = paramiko.SSHClient()             #- will define the object to work
sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hostname_uno ="9.45.2.114"  #- set temporal variable to get hostname
usrname = 'root'

def myconnect(hostname, my_user, my_sshkey):
    

                                            #- thus a global var, for local, tests.


def WebSphere_eval(hostname):#performs WAS search, retrieving information about install, User & Version
   midware_name = 'WebSphere'
   instbinPath  = []
   WAS_register = []
   WAS_rootpath = ''
   WAS_on_off   = ''
   WAS_Ver      = []
   WAS_Type     = []

   poss_paths   = '/usr /opt /home /var'
   WAS_bin_cmds, standerr = subprocess.Popen(['ssh',hostname,'variable=($(find',poss_paths,'-type','d','-name',midware_name+"*",'-prune));','for','i','in','${variable[@]};', 'do', 'find', '$i', '-name', '\"versionInfo.sh\"', '|', 'awk', '\'/AppServer?\/bin/ {print }\'', ';', 'find', '$i', '-name', '\"serverStatus.sh\"', '|', 'awk', '\'/AppServer?\/bin/ {print }\'', ';', 'done;'], stdout=subprocess.PIPE, stderr=subprocess.PIPE ).communicate()
         #WAS_bin_cmds, standerr = subprocess.Popen(shlex.split("ssh "+hostname+" variable=($(find "+poss_paths+" -type d -name "+midware_name+"* -prune)); for i in ${variable[@]}; do find $i -name \"versionInfo.sh\" | head -n1 ; find $i -name \"serverStatus.sh\" | head -n1 ; done; "), stdout=subprocess.PIPE, stderr=subprocess.PIPE ).communicate()
   if len(WAS_bin_cmds) > 0:
      WAS_bin_cmds = WAS_bin_cmds.rsplit('\n')
      for i in WAS_bin_cmds:
         if 'versionInfo.sh' in i:
            WAS_rootpath, standerr = subprocess.Popen(['ssh',hostname,i,'|','awk','\'/^Product/ { print $3 }\''], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            ver_type, standerr = subprocess.Popen(['ssh',hostname,i,'|','awk','\'/^Version\ \ |^ID/ { print $2 }\''], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if WAS_rootpath and not WAS_rootpath.isspace():
               WAS_rootpath = re.sub('\n','',WAS_rootpath)
            if ver_type and not ver_type.isspace():
               #WAS_Ver, WAS_Type, none = re.split('\n',ver_type,2)
               vertype = re.split('\n',ver_type)
               for e in vertype:
                  if e and not e.isspace():
                     if e[:1].isdigit():
                        WAS_Ver.append(e)
                     else:
                        WAS_Type.append(e)
         if 'serverStatus.sh' in i:
            WAS_on_off, standerr   = subprocess.Popen(['ssh','-T','-o', 'BatchMode=yes',hostname,i,'-all','|','awk','\'/^ADMU0508I:|^ADMU0509I:|stopped/ {print $NF}\''], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if 'stopped' in WAS_on_off:
               WAS_on_off = 'Off'
            else:
               elPS, elerror = subprocess.Popen(['ssh','-T','-o', 'BatchMode=yes', hostname, 'ps', '-ef','|', 'grep', 'java'],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
               if elPS.find(WAS_rootpath+'/java') > 0:
                  WAS_on_off = 'On'
               else:
                  WAS_on_off = 'Off'
            for a in range (len(WAS_Ver) ):
               registro = [hostname,midware_name,WAS_rootpath,WAS_Ver[a],WAS_Type[a],WAS_on_off,]
               WAS_register.append(registro)
            WAS_Ver  = []
            WAS_Type = []
   if len(WAS_register) > 0:
      return WAS_register
   else:
      WAS_register = []
      return WAS_register


def InstManager_eval(hostname):   # ---- Performs the pertinent operations to retrieve current status of Installation Manager Information 
   poss_paths ="/usr /opt /home /var"
   middlewarename ="InstallationManager"
   InstManager_Paths= subprocess.Popen(['ssh',hostname,'instmanpath=($(find',poss_paths,'-type','d','-name',midware_name+"*",'-prune));','for','i','in','${instmanpath[@]};', 'do',     'find', '$i', '-name', '\"installed.xml\"', '|', 'awk', '\'/AppServer?\/bin/ {print }\'', ';', 'find', '$i', '-name', '\"serverStatus.sh\"', '|', 'awk', '\'/AppServer?\/bin/ {print }\'', ';', 'done;'], stdout=subprocess.PIPE, stderr=subprocess.PIPE ).communicate()
     
registro = WebSphere_eval(hostname_uno)
print registro
