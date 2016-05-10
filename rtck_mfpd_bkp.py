#!/usr/bin/env python
# -- python script to perform Mobile First Platform Server backup
# -- Racetrack MFPS backup 
# -- ver 0.161 
# -- changes; + this version include an enhancement to function synchbkpfolder(folder,foldname) that now accepts 2 parameters and not pass any path to docompfold() funtion
# --          + getdb2pluginpath() retrieves value for DB2 plugin
# --          + sweepoldtars() now cleanup files on and validate and ok status to exit (0) also invoque
# --          + mail_preformatter() e-mail preformated messages
# --          + snd_mail() e-mail event system function 
# --          + memcleaner() New function that cleanup inactive memory preventing a memory leak
# --          + Add a validation before error exit to cleanup temp files
import os, re, subprocess, crypt, random, string, sys, getopt, platform, fileinput, shlex, socket, glob
# -------------- Send mail system  import libraries: 
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
# --------------
currdate           = re.sub('\n','',os.popen("date +%y\'-\'%m\'-\'%d").read())
mfps_Main_path     = "/opt/IBM/MobileFirst_Platform_Server"
IM_binaries        = "/opt/IBM/InstallationManager"
IM_AgentDataloc    = "/var/ibm/InstallationManager"
IM_Sharedfolder    = "/opt/IBM/IMShared"
WAS_libertyfolder  = "/opt/IBM/WebSphere/Liberty"
DB2_plugin         = ""                             #---> this variable isn't harcoded as in our servers the path name changes so "getdb2pluginpath() funtion will get path
Backup_root_folder = "/backuphist/MFPS/"
logfilename        = "/backuphist/mpfs_bkp.log"
myhostname=socket.gethostname().split('.')[0]


def snd_mail(SUBJECT, TEXT, FILES, SERVER, SENDER, RECEIVERS): #--- e-mail (status & Alert) system function t
   msj = MIMEMultipart( Subject=SUBJECT, From=SENDER, To=COMMASPACE.join(RECEIVERS),Date=formatdate(localtime=True))
   msj.attach(MIMEText(TEXT))
   msj['Subject']=SUBJECT
   for f in FILES or []:
     with open(f, 'rb') as fil:
         msj.attach(MIMEApplication(fil.read(), Content_Disposition='attachment; filename="%s"' %basename(f), NAME=basename(f)))
   try:
      smtp = smtplib.SMTP(SERVER)
      smtp.sendmail(SENDER, RECEIVERS, msj.as_string())
      return "Enviado con exito"
   except SMTPException:
      return "no enviado"


def mail_preformatter(status,datta,logfile): #this manages the format of the message to be sended by email, with the mail sender & receiver the smtp configurations
   server    = 'localhost'
   send_from = 'bkp_msg_System@'+socket.gethostname()
   send_to   = ['carlosgo@mx1.ibm.com']  #-- TODO change the email box to dstalert@us.ibm.com
   #send_to   = ['carlosgo@mx1.ibm.com','eruvalca@mx1.ibm.com']
   files     = [logfile]
   text1     = """This is the Worklight Backup message system on server: \' """+socket.gethostname()+""" \' You're receiving this e-mail as part of the Support contact list \n """
   if status == 'OK':
      subject = "Worklight ENV; Backup Operations from, "+socket.gethostname()+" At "+currdate+" Successfully concluded"
      text2   = text1+"""\nThe Backup Operations Finish successfully as programmed  see below for more information about: \n\n"""+datta+"""\n\nFind Attached the logfile for more reference.\nDo not Reply to sender, Automatic System have not inbox receiver.
                """
      snd_mail(subject,text2,files,server,send_from,send_to)
   elif status == 'ERROR':
      subject = "Worklight ENV; Backup Operations from,"+socket.gethostname()+" At "+currdate+" Not concluded"
      text2   = text1+"""\nThe Backup Operations Not concluded as programmed  see below more information about Issue(s) : \n\n"""+datta+"""\n\nFind Attached the logfile for more reference.\nDo not Reply to sender, Automatic System have not inbox receiver.
                """
      snd_mail(subject,text2,files,server,send_from,send_to)


def getdb2pluginpath():
   standout, standerr = subprocess.Popen(['find','/opt/IBM/','-maxdepth', '1','-type', 'd', '-name', 'db2'+'*'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
   DB2_plugin =re.sub('\n','',standout)
   if fileval(DB2_plugin,'d') == 'OK':
      return DB2_plugin
   else:
      reclogevent(msgsystem('DB2_plugins folder: \"'+DB2_plugin+'\" Validation Error ','e'))
      text = """DB2_plugins folder: \"'"""+DB2_plugin+"""\" Validation Error 
             System output: \n """+standerr+"""\n"""
      reclogevent(msgsystem('Mail System sending message ','i'))
      reclogevent(msgsystem('Backup System will logout with status \'5\' ','w'))
      mail_preformatter('ERROR',text,logfilename)
      sys.exit(5)


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
   if fileval(Backup_root_folder,'d') == 'NO':
      os.makedirs(Backup_root_folder)
      reclogevent("Backup Folder : "+Backup_root_folder+" Created at "+str(re.sub('\n','',os.popen("date +%D ").read())))
   
def memcleaner():  ##will get unused memory based on vmstat command and free inactive memory
   cleanout = os.popen(" free &&  sync && echo 3 > /proc/sys/vm/drop_caches && echo \"\" && free ").read()   
   reclogevent(msgsystem('Cached & inactive memory cleanup done','i'))   

def sweepoldtars(status): # check mfps tar files older than 1 day and cleanup main_backup_folder
   reclogevent("Cleanup Tasks Operation begin at "+str(re.sub('\n','',os.popen("date +%T ").read()))+"\n")
   files = glob.glob(Backup_root_folder+"*")
   args = ['rm', '-rf'] + files
   standout, standerr = subprocess.Popen(args,  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
   memcleaner()
   if status == 'ok':
      standout, standerr = subprocess.Popen(['find','/backuphist/', '-type', 'f', '-name', myhostname+'*', '-mtime', '+0', '-exec', 'rm', '-f', '{}', ";"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
      reclogevent(msgsystem('Backup process Completed','O'))
      reclogevent(msgsystem('Backup System will exit with status \'0\'','O'))
      text = """Backup Compression tasks Successfull finished: \nSystem output:\n"""+standout+"""\n"""
      reclogevent(msgsystem('Mail System sending message ','i'))
      mail_preformatter('OK',text,logfilename)
      sys.exit(0)

def docompfold(folder): #will compress the contents of the synchronized MFPS backup_folder
   reclogevent("Compressing main backup Folder : "+Backup_root_folder+" Operation begin at "+str(re.sub('\n','',os.popen("date +%T ").read()))+"\n")
   tarname = "/backuphist/"+myhostname+"mfps"+currdate+".tar.gz"
   standout, standerr = subprocess.Popen(['tar', '-pPcvzf', tarname, folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
   if standerr:
      reclogevent(msgsystem('Backup Compression tasks Failed: ','i'))
      reclogevent(msgsystem(standerr,'e'))
      reclogevent(msgsystem('Backup System will logout with status \'3\' ','w'))
      text = """Backup Compression tasks Failed: \nSystem output:\n"""+standerr+"""\n"""
      sweepoldtars("error")
      reclogevent(msgsystem('Mail System sending message ','i'))
      mail_preformatter('ERROR',text,logfilename)
      sys.exit(3)
   elif fileval(tarname, 'f') == 'OK':
      reclogevent(msgsystem('Backup compression Concluded Successfully: ','O'))
      reclogevent(msgsystem('Backup Path location: '+tarname,'i'))
      reclogevent(msgsystem('Will proceed with cleanup process','i'))
      sweepoldtars('ok')

def synchbkpfolder(folder,foldname): ##perform local sycronization between MFPS(env critical folders) and MFPS (backup folder)
   if fileval(folder,'d') == 'OK':
      reclogevent(msgsystem('Source folder: \"'+folder+'\" Correct Validated ','O'))
      ## synch_res=os.popen("rsync -av /origin/ /dest/ | tail -n2").read() #this works
      reclogevent("Synchronizing Folder : "+foldname+" Operation begin at "+str(re.sub('\n','',os.popen("date +%T ").read()))+"\n")
      if folder == IM_AgentDataloc:
         standout,standerr = subprocess.Popen(['rsync', '-a', '-v', folder, Backup_root_folder+'IM_agent'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
      else:
         standout,standerr = subprocess.Popen(['rsync', '-a', '-v', folder, Backup_root_folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
      if standerr:
         reclogevent(msgsystem('Backup Synchronization Failed: ','i'))
         reclogevent(msgsystem(standerr,'e'))
         reclogevent(msgsystem('Backup System will logout with status \'2\' ','w'))
         text = """Backup Synchronization Failed: """+folder+""" \nSystem output:\n"""+standerr+"""\n"""
         sweepoldtars("error")
         reclogevent(msgsystem('Mail System sending message ','i'))
         mail_preformatter('ERROR',text,logfilename)
         sys.exit(2)
      else:
         reclogevent(msgsystem('Backup Synchronization Concluded Successfully: ','O'))
         reclogevent(msgsystem(standout.splitlines()[-2],'i'))
         reclogevent(msgsystem(standout.splitlines()[-1],'i'))
   else:
      reclogevent(msgsystem('Source folder: \"'+folder+'\" Validation Error ','e'))
      reclogevent(msgsystem('Backup System will logout with status \'21\' ','w'))
      text = """Source folder: \'"""+folder+"""\' Validation Error.  \nSystem output:\n"""+standerr+"""\n"""
      sweepoldtars("error")
      reclogevent(msgsystem('Mail System sending message ','i'))
      mail_preformatter('ERROR',text,logfilename)
      sys.exit(21)

def main():
   if os.getuid() != 0:
      msgsystem('Unauthorized user is trying to perform reserved operations','E')
      text = """Unauthorized user is trying to perform reserved Admin Backup operations:\n"""+" User:"+os.getlogin()
      reclogevent(msgsystem('Mail System sending message ','i'))
      mail_preformatter('ERROR',text,logfilename)     
      sys.exit(1)
   else:
      check_tune_setup()    
      reclogevent(msgsystem('Running Backup operations','i'))
      synchbkpfolder(mfps_Main_path,'Mobile First Binaries folder')
      synchbkpfolder(IM_binaries,'Install Manager Binaries Folder')
      synchbkpfolder(IM_AgentDataloc,'Install Manager Agent Data Folder')
      synchbkpfolder(IM_Sharedfolder,'Install Manager Shared folder')
      synchbkpfolder(WAS_libertyfolder,'WAS Liberty folder')
      synchbkpfolder(getdb2pluginpath(),'DB2 Plugin folder')
      docompfold(Backup_root_folder)

if __name__=="__main__":
   main()
