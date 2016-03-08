#!/usr/bin/env python
import sys, getopt
#tstgetarg.py script
#implements a function that validates the entrance of specific flags and arguments from command line
#



def opargreader(argv):
   listedop = 'hpi:'  
   inputfile = ''
   optswitch = ''
   if not argv: #and not argv.isspace():
      print 've y chinga tu madre'
      print 'tstgetarg.py -i <inputfile>'                # http://www.tutorialspoint.com/python/python_command_line_arguments.htm
   else:
      try:
         opts, args = getopt.getopt(argv, listedop,["help", "ping", "ifile="])  # getopt.getopt method: parses command line options & parameter list
      except getopt.GetoptError as err:                            # getopt.getopt(args, options[, long_options]) "check below link:"
         print(err)
         if ( str(err).find("--ifile") >=0 ) or ( str(err).find("-i") >=0 ):
            print 'tstgetarg.py <option> [-i|--ifile] <inputfile>'           # http://www.tutorialspoint.com/python/python_command_line_arguments.htm
         if ( str(err).find("not recognized") >=0 ):
            print 'tstgetarg.py <knowed_options>'
         sys.exit(2)
      for o, a in opts:
         if o == '-h':
            print 'tstgetarg.py <option>  [<option> + <parameter>]'
            sys.exit(1)
         if o in ("-p", "--ping"):
            optswitch = 'p' 
         if optswitch  and ( o in ("-i", "--ifile")):       
         #elif o and not o.isspace():
            inputfile = a
            if optswitch == 'p':
               print 'we\'ll ping using this Input file: ', inputfile
         #assert False, "unhandled option"

def main():
   listedop = "hi:"
   opargreader(sys.argv[1:])

if __name__=="__main__":
   main()
