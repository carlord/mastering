#!/usr/bin/env python
import os, re, subprocess, crypt, random, string, sys, getopt, platform, fileinput


def splitter(thelist,FS):
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
            print usname, group, shell, gecos,passwd


def parser(the_xml, srchstring, thefield, FS):
   if fileval(the_xml) == 'True' :   
      for line in fileinput.FileInput(the_xml):
         if line.find(srchstring) >=0 :
            myline = re.split(" ",line)
            xmi_serv_id = re.split(FS, myline[thefield])
            return xmi_serv_id[1].replace('"','')


def cryptpasswd(pasguord):
    passte = os.popen("perl -e 'print crypt($ARGV[0],"+"password"+")' "+pasguord).read()
    return passte


def fileval(the_file):
   if os.path.isfile(the_file) and os.path.getsize(the_file) > 0:
      return 'True'     ##fixed return value to work with wasdm     
   else:
      return 'False'


print parser('server.xml', 'xmi:id=\"Server_', 25, '=')
print splitter('misusers',',')
