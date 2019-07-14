# @Brief This script generates a vhdl state machine template (based on a case statement) exported from the graph editor software yEd. 
#        This can be downloaded here: https://www.yworks.com/products/yed/download
#        The user will then copy from the generated file the template of the FSM and change according to his needs (declare signals, define conditions,..).
#        From https://yed.yworks.com/support/tutorial/create_graph.html:
#           "A graph consists of nodes and edges: Visual elements that represent entities from arbitrary application areas are called nodes, 
#           lines that connect two nodes and thus define a relationship between them are called edges."
#        The nodes will represent the states and edges will represent the transitions between states.
#
# @Rules: The following rules should be verified for the script to work:
#   - There are at least 2 states.
#   - All states have different names.
#   - A state is defined by any shape (Rectangle, Star, etc..), except for the Hexagon that is declaring the initial state.
#   - There MUST be 1 initial state.
#   - A state name must have letters. It might have numbers also, but it cannot have symbols or be just numbers. 
#       (Ex. Valid state names: idle, start, stop1, failure, 123failed. Invalid: 123, 1, ###
#   - For now the yEd file (.graphml) has to be in the same directory of the script
#   - The state transitions represented by Edges MUST be unidirectional.
#
#   @Note This script is work in progress. So i expect a few bugs around.
#
# @Author Manuel Mascarenhas. More information: bpmasc.info
# @Acknowledgements: yWorks @ www.yworks.com, Beautiful Soup @ www.crummy.com/software/BeautifulSoup/, docs.python.org
# Command:
# >> python proc_graphml.py yed_filename.graphml

#from numpy import *
from bs4 import BeautifulSoup
from operator import itemgetter, attrgetter
import os
import datetime
import sys

INITIAL_SHAPE = "hexagon"
SCRIPTNAME = 0
FILENAME = 1

script_rev = 0.1

class node_state:
	def __init__(self, id, label, shape):
		self.id = id
		self.label = label
		self.shape = shape
		self.next_state = []
		self.init = 1

	def set_init(self):
		self.init = 0

	def add_next_state(self,edge):
		self.next_state.append(edge)

class edge_state:
	def __init__(self, id, source, target, condition):
		self.id = id
		self.source = source
		self.target = target
		self.condition = condition

def check_initial_state(list):
	shapes = []
	# Check that there is EXACTLY 1 hexagon shaped state. This is what defines the initial state.
	for state in list:
		shapes.append(state.shape)
		if state.shape == INITIAL_SHAPE:
			state.set_init()
	if shapes.count(INITIAL_SHAPE) != 1:
		return False
	else:
		return True

def check_single_labels(list):
	lables = []
	# Check that there is EXACTLY 1 hexagon shaped state.
	for state in list:
		lables.append(state.label)
	return len(set(lables)) == len(lables)

def get_node(nodes, id):
	el = node_state(0,0,0)
	for node in nodes:
		#print "node_id "+str(node.id)+" "+str(id)
		if node.id == id:
			el = node
	return el

# sorting @ docs.python.org/3/howto/sorting.html    
def order_fsm(nodes, edges):
	for edge in edges:
		get_node(nodes,edge.source).add_next_state(edge)
    # sort list first by initial state and then by id    
	return sorted(nodes, key=attrgetter('init', 'id'), reverse=False)

def compute_yed_data(fsm_file):    
    nodes_list = []
    edges_list = []
    with open(fsm_file) as file:
        soup = BeautifulSoup(file, "lxml")
        nodes = soup.findAll("node", {"yfiles.foldertype":""})
        edges = soup.findAll("edge", {"yfiles.foldertype":""})
        shapes = soup.findAll("y:Shape")
    
    # Close FSM file
	#fsm_file.close()
    
    print " --- Available Nodes --- "
    for node in nodes:
        print node['id'] + " : " + node.find("y:nodelabel").text.strip() + " " + node.data.find("y:shapenode").find("y:shape")["type"]
        nodes_list.append(node_state(node['id'], node.find("y:nodelabel").text.strip(), node.data.find("y:shapenode").find("y:shape")["type"]))

    print " --- Available Edges --- "
    for edge in edges:
        print edge['id'] + " " + edge['source'] + " " + edge['target'] + " " + edge.find("y:edgelabel").text.strip() 
        edges_list.append(edge_state(edge['id'], edge['source'], edge['target'], edge.find("y:edgelabel").text.strip()))

    if not check_initial_state(nodes_list):
        print "[Failure] There is no initial state or there is more than one."
        return []

    if not check_single_labels(nodes_list):
        print "[Failure] There is more than one state with the same name."
        return []

    #sorted_nodes = order_fsm(nodes_list, edges_list)
    print "Succefully computed yEd data."
    return order_fsm(nodes_list, edges_list)

def declare_states(file, states, fsm_name):

    # declare type and respective available states
    file.write("--! FSM state declaration\n")
    file.write("type t_state_" + fsm_name + " is (")
    
    # check:
    #   - all state names are unique (e.g. only one state is called idle)
    #   - a state name cannot be only an integer
    for state in states:
    	label = state.label
        if label.isdigit():
            raise Exception('Invalid state name.')
        # Last element in the list is not written with a comma afterwords
        if states.index(state) == len(states)-1:
            file.write(state.label)
        else:
            file.write(state.label + ", ")

    file.write(");\n")
    file.write("--! FSM state instatiation\n")
    file.write("signal s_state_" + fsm_name + " : t_state_" + fsm_name + ";\n")
    
def convert_nodes_hdl(nodes_list, file, fsm_name):
    file.write("\n\n\n\n--! REMEMBER: Do NOT forget to initialize inital state value (at reset for example)! \n\n")
    file.write("\n\n")
    file.write("--! ####################################################################\n")
    file.write("--! @brief TODO\n")
    file.write("--! ####################################################################\n")
    file.write("case s_state_" + fsm_name + " is\n")
    
    for node in nodes_list:
        file.write("    when " + node.label + " =>\n")
        file.write("        --! TODO write your code..\n")
        if len(node.next_state) == 0:
            pass
        else:
            for i, edge in enumerate(node.next_state):
                if i == 0:
                    file.write("        if state_" + node.label + "_cond" + str(i+1) + " then    ")
                    file.write("        --! condition: " + edge.condition + "\n")
                    file.write("        	s_state_" + fsm_name +" <= " + get_node(nodes_list,edge.target).label  + "\n")
                else:
                    file.write("        elsif state_" + node.label + "_cond" + str(i+1) + " then    ")
                    file.write("        --! " + edge.condition + "\n")
                    file.write("        	s_state_" + fsm_name +" <= " + get_node(nodes_list,edge.target).label  + "\n")
            file.write("        end if;\n")
    file.write("    when others =>\n")

def main():
    # Get current date
    now = datetime.datetime.now()
        
    # count the arguments
    n_args = len(sys.argv) - 1
    
    # store current working directory
    fsm_dir = os.getcwd()
    
    # Check if arguments were written. There MUST be at least the filename
    if n_args < 1:
        raise Exception('Not enough arguments.')
    
    # Store all arguments
    arguments = sys.argv
    
    print "Filename: " + arguments[FILENAME]
    print "Script: " + arguments[FILENAME-1]
    # Try to open file.
    try:
        yed_file = open(arguments[FILENAME], 'r')
    except :
        print "File does not exist."

    # Try to compute data from yEd file. Raise exception if list of nodes is empty.
    nodes = compute_yed_data(arguments[FILENAME])
    if len(nodes) == 0:
        raise Exception('Failed to compute yEd file.')
    


    # FSM name is the same of the filename without extension (ex. for file "main.graphml", FSM name is "main")
    fsm_name = os.path.splitext(arguments[FILENAME])[0]
    print "FSM name: " + fsm_name
    script_name = arguments[SCRIPTNAME]

    # Create .vhd file (Picking up the previous example then the generated vhd file would be gen_fsm_main.vhd)
    gen_filename = "gen_fsm_" + fsm_name + ".vhd"
    gen_file = open(gen_filename,"w+")

    # Write generated file header
    gen_file.write("--! Generated template FSM file for " + fsm_name + " with script " + script_name + " rev. " + str(script_rev) + "\n")
    gen_file.write("--! File diretory: " + fsm_dir + "\n")
    gen_file.write("--! Generated file name: " + gen_filename + " from yEd file: " + fsm_name + "\n")
    gen_file.write("--! Date: "+ now.strftime("%Y-%m-%d %H:%M") +"\n")
    gen_file.write("--! Author: Manuel Mascarenhas\n\n\n\n\n\n")
    
    # Write states declaration
    declare_states(gen_file, nodes, fsm_name)
    # 
    convert_nodes_hdl(nodes, gen_file, fsm_name)
    
    # Terminate case
    gen_file.write("end case;")
    
    # Close file.
    gen_file.close()
    
    print "File succefully generated in " + str(datetime.datetime.now() - now)

print "Starting generation of template frm yEd state machine.."
main()    

