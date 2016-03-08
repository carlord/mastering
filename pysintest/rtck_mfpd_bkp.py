#!/usr/bin/env python
# -- python script to perform Mobile First Platform Server backup
# -- Racetrack 
import os, re, subprocess, crypt, random, string, sys, getopt, platform, fileinput, shlex,socket

currdate           = re.sub('\n','',os.popen("date +%y\'-\'%m\'-\'%d").read())
mfps_Main_path     = "/opt/IBM/MobileFirst_Platform_Server"
Backup_root_folder = "/backuphist/MFPS/"
logfilename        = "/backuphist/MFPS/mpfs_bkp.log"

def fileval(the_inode, the_type): #---- Validate inode existance (file or path validation)
   if the_type == 'f':
      if os.path.isfile(the_inode):
         return 'OK'       
      else:
         return 'NO'
   elif the_type == 'd':
      if os.path.isdir(the_inode):
         return 'OK'          
      else:
         return 'NO'
      
def reclogevent(event): ##Apend events performed by backup operations
   logobj =''
   if fileval(logfilename,'f') == 'NO':
       logobj = open(logfilename, 'a+')
       logobj.writelines(msgsystem(event,'i')) 
       logobj.writelines(msgsystem('-','L'))
       logobj.close()
   else:
       logobj = open(logfilename, 'a+')
       logobj.writelines(event)
       logobj.close()


def msgsystem(printmessage,Typemsg): ## Define a default system log message format 
   timestamp =str(re.sub('\n','',os.popen("date +%T").read()))
   if Typemsg in ('o','O','OK'):
      return "System output:\t OK "+printmessage+" At "+timestamp+". \n"
   elif Typemsg in ('e','E','ERROR'):
      return "System output:\t ERROR "+printmessage+" At "+timestamp+". \n"
   elif Typemsg in ('w','W','WARNING'):
      return "System output:\t WARNING "+printmessage+" At "+timestamp+". \n"
   elif Typemsg in ('i','I','INFO'):    
      return " "+printmessage+". \n"
   elif Typemsg in ('l','L','LINE'):
      return printmessage *80 +"\n"


def check_tune_setup(): ##verify and pre-set folders and logs
   if fileval(Backup_root_folder,'d') != 'NO':
      os.path.os.mkdir(Backup_root_folder)
      reclogevent("Backup Folder : "+Backup_root_folder+" Created at "+str(re.sub('\n','',os.popen("date +%D ").read())))


def synchbkpfolder(): ##perform local sycronization between MFPS(install folder) and MFPS (backup folder)
   ## synch_res=os.popen("rsync -av /origin/ /dest/ | tail -n2").read() #this works
   standout,standerr = subprocess.Popen(['rsync', '-a', '-v', mfps_Main_path, mistest], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
   if standerr:
      reclogevent(msgsystem('Backup Synchronization Failed: ','i')
      reclogevent(msgsystem(standerr,'e')
      reclogevent(msgsystem('Backup System will logout with status \'2\' ','w')
      sys.exit(2)
   else:
      reclogevent(msgsystem('Backup Synchronization Concluded Successfully: ','O')
      reclogevent(msgsystem(standout.splitlines()[-2],'i'))
      reclogevent(msgsystem(standout.splitlines()[-1],'i'))


def main():
   if os.getuid() != 0:
      msgsystem('Unauthorized user is trying to perform reserved operations','E')
      sys.exit(1)
   else:
      check_tune_setup()    
      reclogevent(msgsystem('Running Backup operations','i')
      

if __name__=="__main__":
   main()
