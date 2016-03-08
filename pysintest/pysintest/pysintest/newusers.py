#!/usr/bin/env python
# newusers.py script creates users from a list
# TODO planned to use parameters to 
import os, re, subprocess, crypt, random, string, sys, getopt, platform, fileinput

FS = ","         # field Separator for the file 
listedop = 'hf:p:' # list of possible options
file = " "       # will be used to contain the users list file 


###----- functions block

def helpop(opt):
    print 'newusers.py usage: \n'
    if opt == 'A':
       print 'No Arguments'   
       print 'tstgetarg.py -i <inputfile>'   
       sys.exit(2)
    if opt == 'f':
       print 'invalid file path'
       print 'newusers.py [-f | --file] </valid/path/to/file>  \n'
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
     
    elif opt == 'h' :
        
#------- # validates a file, as file and non empty
def fileval(the_file):
   if os.path.isfile(the_file) and os.path.getsize(the_file) > 0:
      return 'True'     ##fixed return value to work with wasdm     
   else:
      return 'False'

#------- # return the length of the first file-line occurrence
def linelengh(the_file,FiS):
   mafile = open(the_file,'r')
   return len(re.split(FiS,mafile.readline()))

#---------------------------------------- # option + argument reader parser
def opargreader(argv, lopt):
   if not argv: # check empty arguments  not argv.isspace():
      helpop('A')
   else:
      #print argv 
      inputfile = ''
      try:   # parses options & parameters
         opts, args = getopt.getopt(argv, lopt,["help","ifile=", "passwd="])
      except getopt.GetoptError as err:            # getopt.getopt(args, options[, long_options])
         print(err)
         print 'tstgetarg.py -i <inputfile>'     
         sys.exit(2)
      for o, a in opts:
         if o in ("-h", "--help"):
            print 'tstgetarg.py -i <inputfile>'
            sys.exit()
         elif o in ("-i", "--ifile"):
            if fileval(a) == 'True':
               inputfile = a 
               print 'Input file:'+inputfile+' Validated step 1 OK'
               if linelengh(inputfile,FS) > 0:
                  splitter(inputfile,linelengh(inputfile,FS))
               else: 
                  helpop('l')                  
            else:
               helpop('f')
         if o in ("-p", "--passw"):
            genpwd = a 
            print ' global passwd is: ', genpwd
     
            #TODO file =  open('misusers', 'r')   #will read the new users list file

#---------------------------------------- #splits the file in lines, each line in fields to use the info
def splitter(thelist,field_number):
    for line in fileinput.FileInput(thelist):
        if line == '\n':
            print "end of file or empty line"
        else:
            mystringer = re.split(FS,line)
            usname   = mystringer[0]
            group    = mystringer[1]
            shell    = mystringer[2]
            gecos    = mystringer[3]
            passwd   = cryptpasswd(mystringer[4])
            adduser(usname, group, shell, gecos,passwd)


#---------------------------------------- #splits the file in lines, each line in fields to use the info
def cryptpasswd(pasguord):
    passte = os.popen("perl -e 'print crypt($ARGV[0],"+"password"+")' "+pasguord).read()
    return passte

#---------------------------------------- #add user following an specific format
def adduser(user, grp, shll, gecs, passwd): 
   # if ( os.system("cat /etc/group |grep grupo") != 0):
    if  myOS() == 'Linux':
          #(os.popen("uname -a | awk '{print $1}'").read()) == 'Linux\n':
          print "Adding user, on this Linux myOS() "
          if ( os.system("useradd -m -s "+shll+" -g "+grp+" -c \""+gecs+"\" -p "+passwd+" "+user ) == 0 ):
               uid = os.popen("cat /etc/passwd | grep "+user+" | awk 'BEGIN {FS=\":\"}{print $3}'").read()
               print "user: "+user+" uid: "+uid+" Created OK"
          else:
               print "user: "+user+" Not added correctly, check your setup"
    elif myOS() == 'AIX':
          #elif (os.popen("uname -a | awk '{print $1}'").read()) == 'AIX\n':
          print " This is an AIX myOS()"
          #useradd -m  -s /bin/ksh -G wheel,system pasholas               
          if ( os.system("useradd -m -s"+shll+" -g "+grp+" "+user ) == 0 ):
               aixuspsswd(user, passwd)
               uid = os.popen("cat /etc/passwd | grep "+user+" | awk 'BEGIN {FS=\":\"}{print $3}'").read()
               print "user: "+user+" uid: "+uid+" Created OK"
          else:
               print "user: "+user+" Not added correctly, check your setup"
    else:
          print "myOS() operations not defined yet "

#---------------------------------------- #set user password (pre-encrypted) AIX
def aixuspsswd(usname, passwd)
    os.popen("echo"+usname+":"+passwd*" | chpasswd -c -e")

def groupadd(group):
    if myOS() == 'Linux':
       os.popen("groupadd -f "+group)
    elif myOS() == 'AIX':
       os.popen("mkgroup -a "+group)     
    else:
       print " Function not set for this myOS(), Sorry" 

#---------------------------------------- # get OS name
def myOS():
    os = platform.system()
    return os

def main():
    if os.geteuid() == 0 :         
       opargreader(sys.argv[1:], listedop)
       #splitter(file) 
    else
        print "You aren't root, exit program and not perform operations"
        sys.exit(2)
