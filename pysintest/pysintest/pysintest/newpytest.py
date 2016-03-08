#!/usr/bin/env python
import re, os, subprocess
#simple text script to work with 
# is a commodin file where I do some test to python statements & functions
myfile="yum_save*"
#perform multiplication ops

def funmult( var1, var2):
    sum = var1 * var2
    print "resultado = %s" %sum

# performs add operations
def funsum( var1, var2):
    sum = var1 + var2
    print "resultado = %s" %sum


def main():
    print "escribe un commando \n"
    un_commando_test = raw_input()
    #pingval = subprocess.check_call(["ping","-w", str(0),"-c", str(1), "dst.lexington.ibm.com"])
    #getch = re.split(" ",os.popen("ls -l /tmp/"+myfile+" | awk  '{ print $6\" \"$7 }'").read() )
    print un_commando_test
    #funmult(10, 30)
    #funsum(10,30)


if __name__=="__main__":
    main()
