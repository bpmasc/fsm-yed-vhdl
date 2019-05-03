from numpy import *
import datetime
import sys
import os

script_rev = 1
fsm_filename = sys.argv[0]
fsm_name = sys.argv[1]
fsm_dir = os.getcwd()
gen_filename = "gen_fsm_" + fsm_name + ".vhd"
# Create .cpj file. get name from arg!!
f = open(gen_filename,"w+")

#
f.write("# Generated FSM file for " + fsm_name + " with script " + fsm_filename + " rev. " + str(script_rev) + "\n")
f.write("# File diretory: " + fsm_dir + "\n")
f.write("# Generated file name: " + gen_filename + "\n")

#
# Get current date
now = datetime.datetime.now()
f.write("# Date: "+ now.strftime("%Y-%m-%d %H:%M") +"\n")
f.write("# Author: Manuel Mascarenhas\n\n\n\n\n\n")

# Declare states


# Create process

# Close file.
f.close()