#!/usr/bin/env python/
import os, re, subprocess, crypt, random, string, sys, getopt, platform, fileinput, shlex, socket, paramiko
#this pretends to be a class with all ssh subrutines needed for an specific remote server conexion
class sshconx:
   #self.mySSHKEY  #'/home/carlos/.ssh/id_rsa.pub'   ##-- to be defined with personal user's pub key'
   #self.hostname_uno  #"9.45.2.114"  #- set temporal variable to get hostname
   #self.my_fqdn
   #self.usrname          # "root"
   def myconnect(self,fqdn_or_ip,myuser,mysshk):
       sshcon =   paramiko.SSHClient()             #- will define the object to work
       sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       sshcon.connect(hostname=fqdn_or_ip, username=myuser, key_filename=mysshk)
       return sshcon

   def __init__(self, fqdn, my_user, mysshkey, myhostname):
       self.my_fqdn  = fqdn
       self.usrname  = my_user          # "root"
       self.mySSHKEY = mysshkey
       self.hostname = myhostname
       self.conexion  = self.myconnect(self.my_fqdn,self.usrname,self.mySSHKEY)
       
   def runcommand(self,mycommand): # general remote command executer, print output
       stdin, stdout, stderr = self.conexion.exec_command(mycommand)
       errores = stderr.read()
       salida  = stdout.readlines()
       if len(errores) > 0:
           print "command error please check below system message:"
       elif len(salida) > 0:  
           return salida  
       
   def WebSphere_eval(self,fqdn_or_ip): #performs WAS search, retrieving information about install, User & Version
       midware_name = 'WebSphere'
       instbinPath  = []
       WAS_register = []
       WAS_rootpath = []
       WAS_on_off   = ''
       WAS_Ver      = []
       WAS_Type     = []
       poss_paths   = '/usr /opt /home /var'
       WAS_bin_cmds = self.runcommand("waspaths=($(find "+poss_paths+" -type d -name "+midware_name+" -prune)); for i in ${waspaths[@]}; do find $i -name versionInfo.sh | awk \'/AppServer[0-9,A-Z,a-z]*\/bin/ { print } \'; find $i -name serverStatus.sh | awk \'/AppServer[0-9,A-Z,a-z]*\/bin/ { print } \'; done;") 
       if len(WAS_bin_cmds) > 0:
          WAS_bin_cmds = WAS_bin_cmds.rsplit('\n')
          for i in WAS_bin_cmds:
              if 'versionInfo.sh' in i:
                  verinfosh    = str(re.sub('\n','',str(i)))
                  WAS_rootpath.append(re.sub('\n', '', str(self.runcommand(verinfosh+" | awk \'/^Product/ {print $3} \' "))))
                  ver_type     = self.runcommand(verinfosh+" | awk \'/^Version\ \ |^ID/ {print $2} \' ")                               
                  #if len(WAS_rootpath) > 0:
                  #    WAS_rootpath = re.sub('\n', '', str(WAS_rootpath[0]))
                  if len(ver_type) > 0:
                     for e in ver_type:
                          if e and not e.isspace():
                              if e[:1].isdigit():
                                  WAS_Ver.append(re.sub('\n','',e))
                              else:
                                  WAS_Type.append(re.sub('\n','',e))
              if 'serverStatus.sh' in i:
                  #WAS_on_off, standerr   = subprocess.Popen(['ssh','-T','-o', 'BatchMode=yes',hostname,i,'-all','|','awk','\'/^ADMU0508I:|^ADMU0509I:|stopped/ {print $NF}\''], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                  #if 'stopped' in WAS_on_off:
                  #    WAS_on_off = 'Off'
                  #else:
                  elPS, elerror = subprocess.Popen(['ssh','-T','-o', 'BatchMode=yes', hostname, 'ps', '-ef','|', 'grep', 'java'],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                      if elPS.find(WAS_rootpath+'/java') > 0:
                          WAS_on_off = 'On'
                      else:
                          WAS_on_off = 'Off'
          for a in range (len(WAS_Ver) ):
                   registro = [self.hostname,midware_name,WAS_rootpath,WAS_Ver[a],WAS_Type[a],WAS_on_off,]
                   WAS_register.append(registro)
                   WAahS_Ver  = []
                   WAS_Type = []
       if len(WAS_register) > 0:
          return WAS_register
       else:
          WAS_register = []
          return WAS_register
