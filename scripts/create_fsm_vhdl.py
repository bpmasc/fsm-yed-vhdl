from numpy import *
import datetime
import sys
import os

# TODO:
#   yEd interface
#   @yed multiple state machines in one file
#   if condition : if stateX_condY then
script_rev = 0.1
FILENAME = 0
FSM_NAME = 1

def check_unique_arg(arguments):
    return len(set(arguments)) == len(arguments)

def declare_states(file, arguments):
    

    # declare type and respective available states
    file.write("--! FSM state declaration\n")
    file.write("type t_state_" + arguments[FSM_NAME] + " is (")
    
    # check:
    #   - all state names are unique (e.g. only one state is called idle)
    #   - a state name cannot be only an integer
    for arg in arguments[2:]:
        if str.isdigit(arg):
            raise Exception('Invalid state name.')
        # Last element in the list is not written with a comma afterwords
        if arguments.index(arg) == len(arguments)-1:
            file.write(arg)
        else:
            file.write(arg + ", ")

    file.write(");\n")
    file.write("--! FSM state instatiation\n")
    file.write("signal s_state_" + arguments[FSM_NAME] + " : t_state_" + arguments[1] + ";\n")

def instatiate_fsm(file, arguments):
    file.write("\n\n\n\n--! WARNING: Do NOT forget to initialize inital state value (at reset for example)! \n\n")
    file.write("\n\n")
    file.write("--! ####################################################################\n")
    file.write("--! @brief TODO\n")
    file.write("--! ####################################################################\n")
    file.write("case s_state_" + arguments[FSM_NAME] + " is\n")
    for arg in arguments[2:]:
        file.write("    when " + arg + " =>\n")
        file.write("        --! TODO define action\n")
    file.write("    when others =>\n")
    file.write("        --! TODO define action\n")
    file.write("end case;")
    
def main_loop():
    # Get current date
    now = datetime.datetime.now()
        
    # count the arguments
    n_args = len(sys.argv) - 1
    
    # store current working directory
    fsm_dir = os.getcwd()
    
    # Check if arguments were written. There MUST be at least 2 states
    if n_args < 3:
        raise Exception('Not enough arguments.')
    
    # Store all arguments
    arguments = sys.argv
    
    if not check_unique_arg(arguments):
        raise Exception('Invalid args selection. Make sure all args are unique.')

    fsm_filename = arguments[FILENAME]
    fsm_name = arguments[FSM_NAME]
    
    # Create .vhd file. get name from arg!!
    gen_filename = "gen_fsm_" + fsm_name + ".vhd"
    f = open(gen_filename,"w+")

    # Write generated file header
    f.write("--! Generated template FSM file for " + fsm_name + " with script " + fsm_filename + " rev. " + str(script_rev) + "\n")
    f.write("--! File diretory: " + fsm_dir + "\n")
    f.write("--! Generated file name: " + gen_filename + "\n")
    f.write("--! Date: "+ now.strftime("%Y-%m-%d %H:%M") +"\n")
    f.write("--! Author: Manuel Mascarenhas\n\n\n\n\n\n")
    
    # Declare states
    declare_states(f, arguments)
    # instatiate FSM
    instatiate_fsm(f, arguments)
    
    # Close file.
    f.close()
    
    print "File succefully generated in " + str(datetime.datetime.now() - now)
    
main_loop()








