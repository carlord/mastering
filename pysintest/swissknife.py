#!/usr/bin/env python
# swissknife.py  script 
# planned to contain several sysadmin tools that could provide daily help
#

import os, re, subprocess, crypt, random, string, sys, getopt, platform, fileinput, shlex, socket

#-------- Global Var section:

tou_check  = ''
local_path = '/tmp/'               #-- path to locate work files
sadbfile   = 'siteservercat-extended.txt'
sitename   = 'dst.lexington.ibm.com'
remote_sadbpath = '/etc/DST/'
Verbose    = 0                     #-- Global mode to display information "0 = Off (default), 1 = ON"
class bcolor:
   #----- Ansi Colors
   BLACK        = '\x1b[0;30m'
   RED          = '\x1b[0;31m'
   GREEN        = '\x1b[0;32m'
   YELLOW       = '\x1b[0;33m'
   BLUE         = '\x1b[0;34m'
   PURPLE       = '\x1b[0;35m'
   CYAN         = '\x1b[0;36m'
   LGRAY        = '\x1b[0;37m'
   DGRAY        = '\x1b[1;30m'
   #----- Bold Colors   
   BRED         = '\x1b[1;31m'
   BGREEN       = '\x1b[1;32m'
   BYELLOW      = '\x1b[1;33m'
   BBLUE        = '\x1b[1;34m'
   BPURPLE      = '\x1b[1;35m'
   BCYAN        = '\x1b[1;36m'
   WHITE        = '\x1b[1;37m'
   #----- modifiers
   UND_line     = '\x1b[4m'
   OVR_line     = '\x1b[9m'
   get_colorbox = '\x1b[7m'       #Black text over a colored box from the before declared
   BOLD         = '\x1b[1m'
   #-
   no_effect    = '\x1b[0m'       #chop or neutrilize any applied effect after being invoqued
   #----- ColorBoxes
   UNDERBLACK   = '\x1b[40m'
   UNDERRED     = '\x1b[41m'
   UNDERGREEN   = '\x1b[42m'
   UNDERYELLOW  = '\x1b[43m' 
   UNDERBLUE    = '\x1b[44m'
   UNDERPURPLE  = '\x1b[45m'
   UNDERCYAN    = '\x1b[46m'
   UNDERWHITE   = '\x1b[47m'
BC = bcolor()       

#  re.split("\n", os.popen("ssh root@dst.lexington.ibm.com  \'cat /etc/DST/siteservercat-extended.txt\' ").read())

#-------- option retriever function for script arguments

def msgsystem(printmessage,Typemsg): ## Define a default system message 
   if Typemsg in ('o','O','OK'):
      print BC.YELLOW+"System output:\t"+BC.get_colorbox+BC.WHITE+" "+printmessage+" "+BC.BBLUE+"OK"+BC.no_effect
   elif Typemsg in ('e','E','ERROR'):
      print BC.YELLOW+"System output:\t"+BC.get_colorbox+BC.WHITE+" "+printmessage+" "+BC.BRED+"ERROR"+BC.no_effect 
   elif Typemsg in ('w','W','WARNING'):
      print BC.YELLOW+"System output:\t"+BC.get_colorbox+BC.WHITE+" "+printmessage+" "+BC.BYELLOW+"WARNING"+BC.no_effect
   elif Typemsg in ('i','I','INFO'):    
      print BC.YELLOW+"System output:\t"+BC.get_colorbox+BC.WHITE+" "+printmessage+" "+BC.DGRAY+"INFO"+BC.no_effect

def msgformat(printmessage, Format_Name):## TODO - Define a better way to format messages
   if Format_Name in ('BWT','WinB','TBWHITE'):
      print BC.UNDERBLACK+BC.BOLD+BC.BYELLOW+"\" "+BC.UND_line+BC.WHITE+printmessage+BC.no_effect+BC.UNDERBLACK+BC.BOLD+BC.BYELLOW+" \""+BC.no_effect
   if Format_Name in ('WG','GinW','TWGRAY'):
      print BC.BLACK+BC.UNDERWHITE+"\" "+BC.UND_line+BC.DGRAY+"Title"+BC.no_effect+BC.BLACK+BC.UNDERWHITE+" \""+BC.no_effect

def helpop(opt):
   thistool = BC.BYELLOW+'swissknife.py '+BC.no_effect
   print "<< - "+thistool+'usage: - >> \n'
   if opt in ('A','h'):
      if opt == 'A':
         msgsystem("Not Blade nor input arguments at all",'E')
      print thistool+' '+BC.YELLOW+'<-blade_tool>'+BC.GREEN+' [<-optionflag(s)>] +'+BC.no_effect+' [ <input_parameter(s)> ]'          
      print BC.UNDERCYAN+BC.WHITE+"     -Available tools-    "+BC.no_effect
      print BC.YELLOW+'\n-h | --help'+BC.no_effect+'\t\t Show this Help'
      print BC.YELLOW+'-p | --ping'+BC.no_effect+'\t\t Provides info status about instances, memory usage, ping reply, for specific help on this tool type: '+thistool+ '+'+BC.YELLOW+' -p'+BC.no_effect+' or '+BC.YELLOW+'--ping'+BC.no_effect+' without options'
      sys.exit(2)
   if opt == 'F':
      print 'Invalid file path'
      print thistool+'<-option_blade> [-F |--ifile] <input_file>'    
      sys.exit(2)
   if opt == 'S':
      print 'Invalid Search string'
      print thistool+'<-option_blade> <[-s |--search]> <string_to_search>'    
      sys.exit(2)
   if opt == 'T':
      print "some info about transfer" #TODO
      sys.exit(2)
   if opt == 'P':#------------------- ping option help
      print BC.WHITE+BC.UND_line+" Blade "+BC.no_effect+"\'"+BC.BCYAN+"--ping"+BC.no_effect+"\' Tool"+BC.no_effect+" works with one of below options:\n"
      print thistool+"<[-p | --ping]> <[-s | --search]> <\""+BC.YELLOW+"search_string"+BC.no_effect+"\"> "+BC.no_effect
      print " -  For Search string option you could combine: [-s | --search]> <\""+BC.YELLOW+"search_string\">"+BC.no_effect+" with <[--admin]> <\""+BC.YELLOW+"Primary Admin Name\"> \n"+BC.no_effect
      print thistool+"<[-p | --ping]> <[-s | --search]> <\""+BC.YELLOW+"search_string"+BC.no_effect+"\"> \n "+BC.WHITE+"or"+BC.no_effect
      print thistool+"<[-p | --ping]> <[-f | --ifile]> <\""+BC.YELLOW+"/valid/path/to/file"+BC.no_effect+"\"> \n "+BC.WHITE+"or"+BC.no_effect
      print thistool+"<[-p | --ping]> <[--admin]> <\""+BC.YELLOW+"Primary Admin Name"+BC.no_effect+"\"> \n "+BC.WHITE+"or"+BC.no_effect
      print thistool+"<[-p | --ping]> <[--ip]> <\""+BC.YELLOW+"xxx.xxx.xxx.xxx"+BC.no_effect+"\">\n"
      print BC.WHITE+BC.UND_line+"Repo_Enhance TOOLS\n"+BC.no_effect
      print BC.BRED+" -v \t\t    "+BC.no_effect+": Verbose flag, display performed operations by "+BC.BCYAN+"--ping"+BC.no_effect+" tool at the time they're being performed and show extra data "
      print BC.BRED+" <-r | --Repolevel> "+BC.no_effect+": Levels of Report on "+BC.BCYAN+"--ping"+BC.no_effect+" tool the options are: \'A\' = ALL \'M\' = Memory  "
      print "\nThe file for use ping-blade must contain one or several IP's or FQDN's separated with commas without spaces between\n\n"
      sys.exit(2)
   if opt == 'l':
      print 'invalid file content:\n'
      print 'file must contain an structured list in lines:\n'
      print '\t-Case of 5 field file'
      print '<user_name>|fs|<group>|fs|<shell>|fs|<info>|fs|<password>'
      print '\t-Case of 3 field file'
      print '<user_name>|fs|<group>|fs|<password>'
      print '\t-Case of 1 field file'
      print '<user_name>\t In this case you must provide a global password \n'
      print 'using the \"-p <password> option'
   if opt == 'U':
      print thistool+'<knowed_options>'
      sys.exit(2)

def chartord(mychar):   #---- will perform the variable type validation and return its int ascii representation or a negative value as error
   if ( isinstance(mychar,str) and len(mychar) == 1) and not mychar.isspace():
      ordinalis = ord(mychar)
      return ordinalis
   elif isinstance(mychar,str) and len(mychar) > 1:
      return -1         #---- it's a string not a char
   else:
      #ordinalis = 0    #---- which will represent an error type
      return -2

def opargreader(argv): #---- Option parser function:  - This function performs the catch and read of the options passed to this program
   listedop  = 'hvpf:s:r:'                        #   - In general words its the interface or Option argument reader.
   bladetool = ''
   inputfile = ''
   sstr = ''
   myIP = ''
   sisadmin = ''
   level_report = '0' # -- 0=off , other values interpretantion will depend on choosen blade_tool 
   global Verbose
   if not argv: #and not argv.isspace():
      helpop('A')
   else:
      try:
         opts, args = getopt.getopt(argv, listedop,["help", "ping", "ifile=", "search=", "ip=", "admin=", "Repolevel="]) #---- getop funtion to getch a list of defined options and arguments.
      except getopt.GetoptError as err:                                                                                  #   - listedop tiene las opciones literales eg. '-h' y un listado de
         msgsystem(str(err),'E')                                                                                         #   - opciones longword eg. '--help'
         #print "\n"+BC.BYELLOW+BC.UNDERRED+"Error:"+BC.no_effect+" "+BC.BOLD+str(err)+BC.no_effect
         if ( str(err).find("--ifile") >=0 ) or ( str(err).find("-f") >=0 ):
            helpop('F')
         if ( str(err).find("not recognized") >=0 ):
            helpop('U')
         if ( str(err).find("--search") >=0 ) or ( str(err).find("-s") >=0 ):
            helpop('S') 
         else:
            helpop('U')
      else:
         for o, a in opts:
            if o in ("-v"):
               Verbose = 1
            elif o in ('-r', '--Repolevel'):           # I will replace strings to specific predefined chars and chars to
               if chartord(a) > 0:                     #  numbers to fulfill an specific report enhancement criteria.
                  level_report = chartord(a)
               elif chartord(a) == -1:
                     if a in ('all','ALL','All'):
                        level_report = chartord('A')
                     elif a in ('mem','memory','Mem','Memory','MEMORY'):
                        level_report = chartord('M')
                     elif a in ('was','WAS','Was'):
                        level_report = chartord('W')
                     else:
                        level_report = 'E'             # --- to catch a not designed option
               else:
                  level_report = 'E'                   
                  msgsystem('-r option doesn\' work with an empty option ','E')
                  helpop('P')
            elif o in ("-h", "--help"):               #--------- this will turn on the flag for help 
               helpop('h') 
            elif o in ('-p', '--ping'):               #--------- this will turn on the flag for ping toolblade
               bladetool = 'p'
            elif o in ('--ip'):                       #--------- option that get IP number as parameter
               if bladetool or not bladetool.isspace:
                  if a and not a.isspace():
                     try:
                        socket.inet_aton(a) #this will validate IP according to 32 bit IP representation
                     except socket.error as sinErr:
                        msgsystem("IP Address: \""+a+"\" Sintaxis mispelled :",'E')
                        print(sinErr)
                        helpop('P')
                     else:
                        myIP = a
               else:   
                  print "Wrong sintaxis"
                  helpop('h')
            elif o in ('-f', '--ifile'):
               if bladetool or not bladetool.isspace:
                  if fileval(a) == 'OK':
                     inputfile = a
                     print 'Input file: '+inputfile+' Validated step 1'+BC.BYELLOW+' OK'+BC.no_effect
                  else:
                     helpop('F')
               else:
                  print "Wrong sintaxis"
                  helpop('h')
            elif o in ("-s", "--search"):
               if bladetool or not bladetool.isspace:
                  sstr = re.sub('[\"\']', '', a)
               else:
                  print "Wrong sintaxis"
                  helpop('h')
            elif o in ("--admin"):
               if bladetool or not bladetool.isspace:
                  if a and not a.isspace():
                     sisadmin = 'ServerAdmin='+a
               else:
                  print "Wrong sintaxis"
                  helpop('h')
            else:
               print "Unknow Option Error "
               helpop('U')
   if bladetool == 'p': 
      pingblade( inputfile, sstr, myIP, sisadmin, level_report) # 1st blade splitted from

def verbose_print_reg( Row ):                             # --- print rows for verbose mode, invoqued by pingblade() function
   print "OS Ver:   "+BC.BYELLOW,Row[4]+BC.no_effect
   print "Adm.prim: "+BC.BYELLOW,Row[2]+BC.no_effect
   print "Adm.bk:   "+BC.BYELLOW,Row[5]+BC.no_effect
   print "Srv.zone: "+BC.BYELLOW,Row[8]+BC.no_effect
   print "Srv.IP:   "+BC.BYELLOW,Row[9]+BC.no_effect+'\n'

def memReporter_printer(i,os):
   print BC.BYELLOW+" ---  Memory Report  ---  "+BC.no_effect
   try:
      Totalmem, Usedmem, Freemem = re.split(' ',Server_mem_usage(i,os[0],'A'),3)
   except ValueError as err:
      msgsystem("No value retrieved: "+str(err),'E')
      Totalmem = 'N/A'
      Usedmem  = 'N/A'
      Freemem  = 'N/A'
      print "Total Memory:",BC.WHITE+Totalmem[:4]+" GB"+BC.no_effect+"\tUsed Memory:",BC.WHITE+Usedmem[:4]+" GB"+BC.no_effect+"\tFree Memory:",BC.WHITE+Freemem[:5]+" GB"+BC.no_effect
   else:
      print "Total Memory:",BC.WHITE+Totalmem[:4]+" GB"+BC.no_effect+"\tUsed Memory:",BC.WHITE+Usedmem[:4]+" GB"+BC.no_effect+"\tFree Memory:",BC.WHITE+Freemem[:5]+" GB"+BC.no_effect


def pingblade( inputfile, sstr, myIP, sisadmin, level_report ): # 1st blade splitted from: <<bladetool - 'P'
   ping_OK = 0                                                  #  - works on control the options and funtions that reply information about Pinged servers
   ping_NO = 0                                                  #  - further tests depends on replied ping catching 
   if level_report == 'E':
      msgsystem("Level Report, Unknow Option ",'E')
      helpop('P')
   if inputfile and not sstr:
      print 'we\'ll ping System(s) That comply with Input criteria: '+BC.BBLUE,inputfile,
   elif sstr and not inputfile and not sisadmin:
      print 'we\'ll ping System(s) That comply with Input criteria: '+BC.BBLUE,sstr+BC.no_effect+"\n"
      #for i in sadbseeker(tou_check, sstr):
      for i in [ row[1] for row in sadbseeker(tou_check,sstr)]:
         if pingfunc(i,1,0,Verbose) == 'OK':
            ping_OK = ping_OK + 1
            os = [ row[3] for row in sadbseeker(tou_check,i)]
            msgsystem("Remote System "+i+" Replied:",'O')
            print "OS-Type:  "+BC.BYELLOW,os[0]+BC.no_effect
            if Verbose == 1:
               verbose_print_reg(row)
            if level_report in (65,97,77,109):  #--- ping memory report for int ascii values 'A,a' or 'M,m'  
               memReporter_printer(i,os)
            if level_report in (65,97,83,87,119,88,120):
               print BC.BYELLOW+"\n ---  APP Report  --- "+BC.no_effect
               if level_report in (65,97,87,119):
                  print ' '+BC.BYELLOW+' WAS '+BC.no_effect+'report :',i
                  #registro = [hostname,midware_name,WAS_rootpath,WAS_Ver[a],WAS_Type[a],WAS_on_off]
                  Middleware_eval_main(i, 'WebSphere', os[0])
               print " TODO: this will be the output for APP's in the instance" 
            print "---------------------\n"
         else:
            msgsystem("Remote System "+i+" No Reply:",'W')
            print "---------------------\n"
            ping_NO = ping_NO + 1
   elif myIP and not sstr and not inputfile:
      print 'we\'ll ping System(s) which IP Address is: '+BC.BBLUE,myIP+BC.no_effect+"\n"
      for i in [ row for row in sadbseeker(tou_check,myIP)]:
         if myIP == i[9]:
            if pingfunc(i[1],1,0,Verbose) == 'OK':
               ping_OK = ping_OK + 1
               os = i[3]
            #[ row[3] for row in sadbseeker(tou_check,i)]
               msgsystem("Remote System "+i[1]+" Replied:",'O')
               print "OS-Type:  "+BC.BYELLOW,os+BC.no_effect
               if Verbose == 1:
                  verbose_print_reg(row)
               if level_report in (65,97,77,109):
                  memReporter_printer(i,os)
               if level_report in (65,97,83,88,120): 
                  print BC.BYELLOW+"\n ---  APP Report  --- "+BC.no_effect
                  print " TODO: this will be the output for APP's in the instance"
               print "---------------------\n"
            else:
               msgsystem("Remote System "+myIP+" No Reply:",'W')
               print "---------------------\n"
               ping_NO = ping_NO + 1
            #msgsystem("The Network address :"+myIP+" isn't found or is not valid:",'W'
   elif  sisadmin and not myIP and not sstr and not inputfile:   #---------------------------
      print 'we\'ll ping System(s) whose: '+BC.BBLUE,sisadmin+BC.no_effect+"\n" 
      #for i in sadbseeker(tou_check, sstr):
      for i in [ row[1] for row in sadbseeker(tou_check,sisadmin)]:
         if pingfunc(i,1,0,Verbose) == 'OK':
            ping_OK = ping_OK + 1
            os = [ row[3] for row in sadbseeker(tou_check,i)]
            msgsystem("Remote System "+i+" Replied:",'O')
            print "OS-Type:  "+BC.BYELLOW,os[0]+BC.no_effect
            if Verbose == 1:
               verbose_print_reg(row)
            if level_report in (65,97,77,109):
               memReporter_printer(i,os)
            if level_report in (65,97,83,88,120):
               print BC.BYELLOW+"\n ---  APP Report  --- "+BC.no_effect
               print " TODO: this will be the output for APP's in the instance"
            print "---------------------\n"
         else:
            msgsystem("Remote System "+i+" No Reply:",'W')
            print "---------------------\n"
            ping_NO = ping_NO + 1      
   elif  sisadmin and not myIP and sstr and not inputfile:   #--------------------------- Search for sis admin with
      print 'we\'ll ping System(s) whose: '+BC.BBLUE,sisadmin+BC.no_effect+" And comply with the search criteria "+sstr+"\n" 
      #for i in sadbseeker(tou_check, sstr):
      search = sstr+","+sisadmin
      for i in [ row[1] for row in sadbseeker(tou_check,search)]:
         if pingfunc(i,1,0,Verbose) == 'OK':
            ping_OK = ping_OK + 1 
            os = [ row[3] for row in sadbseeker(tou_check,i)]
            msgsystem("Remote System "+i+" Replied:",'O')
            print "OS-Type:  "+BC.BYELLOW,os[0]+BC.no_effect
            if Verbose == 1:
               verbose_print_reg(row)
            if level_report in (65,97,77,109): 
               memReporter_printer(i,os)
            if level_report == 83 or level_report == 65: 
               print BC.BYELLOW+"\n ---  APP Report  --- "+BC.no_effect
               print " TODO: this will be the output for APP's in the instance"
            print "---------------------\n"
         else:
            msgsystem("Remote System "+i+" No Reply:",'W')
            print "---------------------\n"
            ping_NO = ping_NO + 1 
   elif inputfile and sstr and myIP and sisadmin:
      msgsystem(" ALL options Can't be mixed",'E')
      helpop('P')
   else:
      helpop('P')
   print "Replied Servers :",ping_OK
   print "Non Reply Servers:",ping_NO

def Middleware_eval_main(hostname, midware_name, os_name): ## will review the existance of the specified middleware in a host
   if os_name in ('AIX','aix','LINUX','Linux'):
      if midware_name =='WebSphere':
         WAS_register = WebSphere_eval(hostname)
         if len(WAS_register) > 0:
            for i in WAS_register:
               print '\tMiddleware Name:   '+BC.BYELLOW,i[1]+BC.no_effect
               print '\tRoot Install Path: '+BC.BYELLOW,i[2]+BC.no_effect
               print '\tMiddleware Ver.:   '+BC.BYELLOW,i[3]+BC.no_effect
               print '\tWAS Type       :   '+BC.BYELLOW,i[4]+BC.no_effect
               print '\tSoftware Status:   '+BC.BYELLOW,i[5]+BC.no_effect+'\n'
            return WAS_register
         else:
            msgsystem('No Version of Websphere software installed','i')  
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
               registro = [hostname,midware_name,WAS_rootpath,WAS_Ver[a],WAS_Type[a],WAS_on_off]
               WAS_register.append(registro)
            WAS_Ver  = []
            WAS_Type = []
   if len(WAS_register) > 0:
      return WAS_register
   else:
      WAS_register = []
      return WAS_register
      #for i in WAS_register:                                            #return WAS_register
      #   print i

#no delete below line: 
#tou_check =  re.split("\n", os.popen("ssh root@dst.lexington.ibm.com  \'cat /etc/DST/siteservercat-extended.txt\' ").read())

def sadbseeker( sadbfile, search_string ): #--- retrieves information from site dst, file, to use in its main ops. read above line 
   tabla = []
   with open(sadbfile) as file:
      afs = linelengh(search_string,",") #-- (a)mount of (f)ields to (s)earch
      if afs == 2:
         a, b = re.split(',', search_string)
         for i in file:
            if (a in i) and (b in i):
               splitted     = re.split(",",i)
               site_nam     = splitted[0]                               #---Name of site
               fqdn_val     = splitted[1]                               #---FQDN
               S_adm        = tuple_val_split(splitted[7], "=","r")
               OS_name      = tuple_val_split(splitted[8], "=","r")
               OS_Version   = tuple_val_split(splitted[9], "=","r")
               Adm_bk_name  = tuple_val_split(splitted[39], "=","r")
               ServHostEnv  = tuple_val_split(splitted[11], "=","r")
               HW_type      = tuple_val_split(splitted[12], "=","r")
               SrvNetZone   = tuple_val_split(splitted[15], "=","r")
               ServerIP     = tuple_val_split(splitted[16], "=","r")
               Server_uID   = tuple_val_split(splitted[26], "=","r")
               Srv_Hosting  = tuple_val_split(splitted[27], "=","r")
               ServerMAD_ID = tuple_val_split(splitted[30], "=","r")
               registro     = [site_nam,fqdn_val,S_adm,OS_name,OS_Version,Adm_bk_name,ServHostEnv,HW_type,SrvNetZone,ServerIP,Server_uID,Srv_Hosting,ServerMAD_ID]
               tabla.append(registro)
      if afs == 3:
         a, b, c = re.split(',', search_string)
         for i in file:
            if (a in i) and (b in i) and (c in i):
               splitted     = re.split(",",i)
               site_nam     = splitted[0]                               #---Name of site
               fqdn_val     = splitted[1]                               #---FQDN
               S_adm        = tuple_val_split(splitted[7], "=","r")
               OS_name      = tuple_val_split(splitted[8], "=","r")
               OS_Version   = tuple_val_split(splitted[9], "=","r")
               Adm_bk_name  = tuple_val_split(splitted[39], "=","r")
               ServHostEnv  = tuple_val_split(splitted[11], "=","r")
               HW_type      = tuple_val_split(splitted[12], "=","r")
               SrvNetZone   = tuple_val_split(splitted[15], "=","r")
               ServerIP     = tuple_val_split(splitted[16], "=","r")
               Server_uID   = tuple_val_split(splitted[26], "=","r")
               Srv_Hosting  = tuple_val_split(splitted[27], "=","r")
               ServerMAD_ID = tuple_val_split(splitted[30], "=","r")
               registro     = [site_nam,fqdn_val,S_adm,OS_name,OS_Version,Adm_bk_name,ServHostEnv,HW_type,SrvNetZone,ServerIP,Server_uID,Srv_Hosting,ServerMAD_ID]
               tabla.append(registro)
      if afs == 4:
         a, b, c, d = re.split(',', search_string)
         for i in file:
            if (a in i) and (b in i) and (c in i) and (d in i):
               splitted     = re.split(",",i)
               site_nam     = splitted[0]                               #---Name of site
               fqdn_val     = splitted[1]                               #---FQDN
               S_adm        = tuple_val_split(splitted[7], "=","r")
               OS_name      = tuple_val_split(splitted[8], "=","r")
               OS_Version   = tuple_val_split(splitted[9], "=","r")
               Adm_bk_name  = tuple_val_split(splitted[39], "=","r")
               ServHostEnv  = tuple_val_split(splitted[11], "=","r")
               HW_type      = tuple_val_split(splitted[12], "=","r")
               SrvNetZone   = tuple_val_split(splitted[15], "=","r")
               ServerIP     = tuple_val_split(splitted[16], "=","r")
               Server_uID   = tuple_val_split(splitted[26], "=","r")
               Srv_Hosting  = tuple_val_split(splitted[27], "=","r")
               ServerMAD_ID = tuple_val_split(splitted[30], "=","r")
               registro     = [site_nam,fqdn_val,S_adm,OS_name,OS_Version,Adm_bk_name,ServHostEnv,HW_type,SrvNetZone,ServerIP,Server_uID,Srv_Hosting,ServerMAD_ID]
               tabla.append(registro)
      if afs == 5:
         a, b, c, d, e = re.split(',', search_string)
         for i in file:
            if (a in i) and (b in i) and (c in i) and (d in i) and (e in i):
               splitted     = re.split(",",i)
               site_nam     = splitted[0]                               #---Name of site
               fqdn_val     = splitted[1]                               #---FQDN
               S_adm        = tuple_val_split(splitted[7], "=","r")
               OS_name      = tuple_val_split(splitted[8], "=","r")
               OS_Version   = tuple_val_split(splitted[9], "=","r")
               Adm_bk_name  = tuple_val_split(splitted[39], "=","r")
               ServHostEnv  = tuple_val_split(splitted[11], "=","r")
               HW_type      = tuple_val_split(splitted[12], "=","r")
               SrvNetZone   = tuple_val_split(splitted[15], "=","r")
               ServerIP     = tuple_val_split(splitted[16], "=","r")
               Server_uID   = tuple_val_split(splitted[26], "=","r")
               Srv_Hosting  = tuple_val_split(splitted[27], "=","r")
               ServerMAD_ID = tuple_val_split(splitted[30], "=","r")
               registro     = [site_nam,fqdn_val,S_adm,OS_name,OS_Version,Adm_bk_name,ServHostEnv,HW_type,SrvNetZone,ServerIP,Server_uID,Srv_Hosting,ServerMAD_ID]
               tabla.append(registro)
      if afs == 1:
         for i in file:
            if search_string in i:
               splitted     = re.split(",",i)
               site_nam     = splitted[0]                               #---Name of site
               fqdn_val     = splitted[1]                               #---FQDN
               S_adm        = tuple_val_split(splitted[7], "=","r")
               OS_name      = tuple_val_split(splitted[8], "=","r")
               OS_Version   = tuple_val_split(splitted[9], "=","r")
               Adm_bk_name  = tuple_val_split(splitted[39], "=","r")
               ServHostEnv  = tuple_val_split(splitted[11], "=","r")
               HW_type      = tuple_val_split(splitted[12], "=","r")
               SrvNetZone   = tuple_val_split(splitted[15], "=","r")
               ServerIP     = tuple_val_split(splitted[16], "=","r")
               Server_uID   = tuple_val_split(splitted[26], "=","r")
               Srv_Hosting  = tuple_val_split(splitted[27], "=","r")
               ServerMAD_ID = tuple_val_split(splitted[30], "=","r")
               registro     = [site_nam,fqdn_val,S_adm,OS_name,OS_Version,Adm_bk_name,ServHostEnv,HW_type,SrvNetZone,ServerIP,Server_uID,Srv_Hosting,ServerMAD_ID]
               tabla.append(registro)      
   if tabla and len(tabla)>0:
      return tabla
   else:
      msgsystem("No Match found using: "+search_string+" parameter(s) ",'W')   
      print "\nReview your search parameter(s) or their combination & try again"
      print "No further Operations will continue, Sorry for the inconvenience"
      sys.exit(2)
   
def tuple_val_split(thestring,FiS,LorR):  #---- obtain right or left value from a string
   left_val, right_val = re.split(FiS,thestring,2)
   if LorR in ( "r", "right"):      
      return right_val 
   elif LorR in ( "l", "left"):
      return left_val      
       
def uptodatecomp(n_file): #---- check the date from a file given as parameter
    if fileval(n_file) == 'OK':
       mfile, dfile = re.split(" ",os.popen("ls -l "+n_file+" | awk  '{ print $6\" \"$7 }'").read() )
       currmonth, currday =re.split(" ",os.popen("date +%b\" \"%d").read() )
       if ( mfile == currmonth) and (int(dfile) == int(currday)):
          return "current"
       else:
          return "older"
    else:#-------------------when file validation is NO
          return "NA"

def sshcopyfile(R_file_or_dir, server, L_file_or_dir, operation): #---- remote transfer of file (up or down)
    result =''
    if r_dir_Validator(R_file_or_dir, server) == 'OK' or r_file_Validator(R_file_or_dir, server) == 'OK':
       if operation in ("down", "d"):
          if fileval(L_file_or_dir) == 'OK' or dirval(L_file_or_dir) == 'OK': 
             scpcommand = "scp -rB "+server+":"+R_file_or_dir+" "+L_file_or_dir
             result = subprocess.call(shlex.split(scpcommand))
             if result ==0:
                return 'OK'
             else:
                return 'NO'
          else:
             print "Invalid local path or file"
             return 'NO'
       elif operation in ("up", "u"):
          if fileval(L_file_or_dir) == 'OK' or dirval(L_file_or_dir) == 'OK': 
             scpcommand = "scp -rB "+L_file_or_dir+" "+server+":"+R_file_or_dir
             result = subprocess.call(shlex.split(scpcommand))
             if result ==0:
                return 'OK'
             else:
                return 'NO'
    else:
       print "Invalid remote path or file"
       helpop('T') 

def Server_mem_usage(hostname,OS,info):     #---- Will retrieve Server memory statistics
    gb=str(1000*1000*1000)
    klb='4096'
    if OS in ('AIX', 'VIO AIX'):
       #-o TCPKeepAlive=yes -o ServerAliveCountMax=0 -o ServerAliveInterval=2 -o BatchMode=yes -o ConnectionAttempts=4 -o ConnectTimeout=5
       standout, standerr = subprocess.Popen(['ssh','-T','-o','TCPKeepAlive=yes','-o','ServerAliveCountMax=0','-o','ServerAliveInterval=2','-o','BatchMode=yes','-o','ConnectionAttempts=1','-o','ConnectTimeout=2',hostname,'svmon','-G','|','sed','-n','2p','|','awk','\'{ print (($2*'+klb+')/'+gb+')" "(($3*'+klb+')/'+gb+')" "(($4*'+klb+')/'+gb+') } \''],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
       totmem, usedmem, freemem = re.split(' ',re.sub('\n','',standout),3)
       if len(standout) < 1:
          print(standerr)
          return ' '
       else:
          if   info == 'A': #--- All Usage info (total, used, free)
             #return str(re.sub('\n','',os.popen("ssh -T "+hostname+" svmon -G  | sed -n '2p' | awk '{ print (($2*"+klb+")/"+gb+")\" \"(($3*"+klb+")/"+gb+")\" \"(($4*"+klb+")/"+gb+") }'").read()))
             return totmem+" "+usedmem+" "+freemem
          elif info == 'T':#--- Total Memory amount
             #return str(re.sub('\n','',os.popen("ssh -T "+hostname+" svmon -G  | sed -n '2p' | awk '{ print (($2*"+klb+")/"+gb+") }'").read()))
             return totmem
          elif info == 'U':#--- Used Memory
             #return str(re.sub('\n','',os.popen("ssh -T "+hostname+" svmon -G  | sed -n '2p' | awk '{ print (($3*"+klb+")/"+gb+") }'").read()))
             return usedmem
          elif info == 'F':#--- Free Memory
             #return str(re.sub('\n','',os.popen("ssh -T "+hostname+" svmon -G  | sed -n '2p' | awk '{ print (($4*"+klb+")/"+gb+") }'").read()))
             return freemem
    elif OS =='Linux':
        if info == 'A':
          return str(re.sub('\n','',os.popen("ssh -T -o BatchMode=yes -o ConnectionAttempts=3 -o ConnectTimeout=4 "+hostname+" free -m | sed -n '2p' | awk '{print ($2 /1000)\" \"($3 /1000)\" \"($4 /1000) }'  ").read()))
        if info == 'T':
          return str(re.sub('\n','',os.popen("ssh -T -o BatchMode=yes -o ConnectionAttempts=3 -o ConnectTimeout=4 "+hostname+" free -m | sed -n '2p' | awk '{print ($2 /1000) }'  ").read()))
        if info == 'U':
          return str(re.sub('\n','',os.popen("ssh -T -o BatchMode=yes -o ConnectionAttempts=3 -o ConnectTimeout=4 "+hostname+" free -m | sed -n '2p' | awk '{print ($3 /1000) }'  ").read()))
        if info == 'F':
          return str(re.sub('\n','',os.popen("ssh -T -o BatchMode=yes -o ConnectionAttempts=3 -o ConnectTimeout=4 "+hostname+" free -m | sed -n '2p' | awk '{print ($4 /1000) }'  ").read()))
    elif OS =='Macintosh': 
        free, active, inactive, speculative, extra = re.split(' ',re.sub('\n',' ',os.popen("ssh -T "+hostname+" vm_stat | sed -n -e /free/p -e /active:/p -e /speculative:/p | awk '{print $3}' |cut -d'.' -f1 ").read()))
        memfreetot =  str( ( ( int(speculative) + int (free) ) * int(klb) ) / int(gb) )
        usedmemtot =  str( ( ( int(free) + int(active) + int(inactive) ) * int(klb) ) / int(gb) ) 
        #usedmemtot, memfreetot = re.split(',',re.sub('G\n','',os.popen("ssh "+hostname+" top -l 1 |head -n 10 | awk '/^PhysMem/ {print $8\",\"$10}' ").read()))
        #usedmemtot = re.sub('G','',usedmemtot)
        totalmem   = str(float(usedmemtot) + float(memfreetot))
        if info == 'A':
           return str(totalmem+" "+usedmemtot+" "+memfreetot)
        if info == 'T':
           return totalmem
        if info == 'U':
           return usedmemtot
        if info == 'F':
           return memfreetot
    # hostinfo |grep memory | awk '{print $4}'
    else:
        return 'N/A N/A N/A'
        
def r_dir_Validator(r_path,hostname):  #---- Validate remote path existance
    if not r_path or r_path.isspace():
        print "error empty path parameter"
        sys.exit(1)
    else:
        checkpath = re.sub('\n','',os.popen( "ssh -T "+hostname+" \"if [ -d '"+r_path+"' ]; then echo 'OK'; else echo 'NA'; fi\" ").read())
        return checkpath

def r_file_Validator(r_file,hostname):  #---- Validate remote path existance
    if not r_file or r_file.isspace():
        print "error empty path parameter to verify"
        sys.exit(1)
    else:
        checkpath = re.sub('\n','',os.popen( "ssh -T "+hostname+" \"if [ -f '"+r_file+"' ]; then echo 'OK'; else echo 'NA'; fi\" ").read())
        return checkpath   

def pingfunc(fqdn_orIP, c_pack, wait_time, verb): #---- Performs the ping task (name_orIP, number_of packages to send, seconds_to_wait reply, Verbose_mode)
    if (len(fqdn_orIP) < 1) or ( fqdn_orIP.isspace() ):
        sys.exit(2)
    if c_pack < 1:
        sys.exit(2)
    if verb == 0:
       if (subprocess.Popen(shlex.split("ping -w "+str(wait_time)+" -c "+str(c_pack)+" "+fqdn_orIP),stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()) == 0:
          return 'OK'
       else:
          return 'NO'
    elif verb == 1:
       ping = subprocess.Popen(shlex.split("ping -w "+str(wait_time)+" -c "+str(c_pack)+" "+fqdn_orIP),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       err  = ping.stderr.read()
       aout = ping.stdout.read()
       if (len(err) > 0) and not err.isspace():
            print err," Return Code: ",ping.wait()    
            return 'NO'
       if (len(aout) > 0) and not aout.isspace():
            print aout
            print " Return Code: ",ping.wait()
            return 'OK'
    #(os.system("ping -w "+str(wait_time)+" -c "+str(c_pack)+" "+fqdn_orIP)) == 0: # this line shows the command standard output


def fileval(the_file): #---- Validate a provided path as file
   if os.path.isfile(the_file) and os.path.getsize(the_file) > 0:
      return 'OK'     ##fixed return value to work with wasdm     
   else:
      return 'NO'    

def dirval(the_dir): #---- Validate a provided path as dir
   if os.path.isdir(the_dir):
      return 'OK'     ##fixed return value to work with wasdm     
   else:
      return 'NO'


def linelengh(file_or_line,FiS): #---- return the length of the first file-line occurrence or lenght of a line
   if os.path.isfile(file_or_line):
      mafile = open(file_or_line,'r')
      return len(re.split(FiS,mafile.readline()))
   else:
      return len(re.split(FiS,file_or_line))

def check_tune_setup(): #---- sets & checks local conf.
   global tou_check
   tou_check = local_path+sadbfile
   remotefile = remote_sadbpath+sadbfile
   if  uptodatecomp(tou_check) == 'current' :
       return 'OK'
   else:
       print BC.UNDERBLACK+BC.BYELLOW+"Warning:"+BC.no_effect+" Performing SADB file actualization,\n"+BC.RED+BC.get_colorbox+"Avoid Cancel process"+BC.no_effect
       if pingfunc(sitename,1,0,Verbose) == 'OK':
          msgsystem("Remote system "+sitename+"Replied",'O')
          print BC.YELLOW+"Remote system "+BC.BGREEN+"\'"+sitename+"\'"+BC.no_effect+" Replied --- OK"+BC.BYELLOW
          if sshcopyfile(remotefile, sitename, local_path, "down") == 'OK':
             print BC.WHITE+BC.get_colorbox+"Update Operation performed "+BC.BBLUE+"OK"
             print BC.no_effect+""
          else:
             print BC.WHITE+BC.get_colorbox+"Update Operation not concluded "+BC.BRED+"ERROR"
       else:
          print "remote server doesn't reply"
          print BC.WHITE+BC.get_colorbox+"Verify connection or remote server availability "+BC.BYELLOW+"WARNING"
    
          
#def trasToCmd_andRun(cmd_and_args):
#   subprocess.call(shlex.split(cmd_and_args))


def main():
   check_tune_setup()   
   print BC.WHITE+"|Opening knive Tool|"+BC.no_effect+"\n"
   opargreader(sys.argv[1:])

if __name__=="__main__":
   main()
