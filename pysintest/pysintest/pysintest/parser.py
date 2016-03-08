#!/usr/bin/env python
# parser.py 
# script to obtain specific string from a file
# test parser.py script to obtain specific string from a file; yet hardcoded
# TODO planned to use parameters to 
import os, re, subprocess, crypt, random, string, sys, getopt, fileinput, string

#------------- variable definition block

#   file = open(the_xml, 'r')

def splitter(the_xml, srchstring, thefield, FS):
   if fileval(the_file):
      for line in fileinput.FileInput(the_xml):
         if line.find(srchstring) >=0 :
      #if srchstring in line:
            myline = re.split(" ",line)
            xmi_serv_id = re.split(FS, myline[thefield])
            return xmi_serv_id[1].replace('"','')


def fileval(the_file):
   if os.path.isfile(the_file) and os.path.getsize(the_file) > 0:
      return True      
   else:
      return False


def main () :
   print splitter('server.xml', 'xmi:id=\"Server_', 25, '=')
   #print val1
   print splitter('server.xml', 'xmi:id=\"JavaVirtualMachine_', 5, '=')
   #print val1


if __name__=="__main__":
   main()
#------------ funtions to be imported
#  + splitter; based to work with the server.xml fields,  
#    how to import : 
#             copy the parser.py to /your/scripts/path/
#             type "import parser" in the header, always after the hashbang line
#    how to use : 
#             parser.splitter(the_xml, srchstring, thefield, FS)
#                 the_xml    = '/path/to/xml_file'
#                 srchstring = 'string_to_search'
#                 thefield   = field_to_take (must be an integer number)
#                 FS         = 'field_separator' (must be a character or space, this isn't
#                           the general field separator but the resultant value FS)

