from bs4 import BeautifulSoup

fsm_file = "example2.graphml"

INITIAL_SHAPE = "hexagon"

class node_state:
	def __init__(self, id, label, shape):
		self.id = id
		self.label = label
		self.shape = shape
		self.edges = []
		self.init = False

	def set_init(self):
		self.init = True

nodes_list = []

class edge_state:
	def __init__(self, id, source, target):
		self.id = id
		self.source = source
		self.target = target

edges_list = []

with open(fsm_file) as file:
    soup = BeautifulSoup(file, "lxml")
    nodes = soup.findAll("node", {"yfiles.foldertype":""})
    edges = soup.findAll("edge", {"yfiles.foldertype":""})
    shapes = soup.findAll("y:Shape")

print " --- Nodes --- "
for node in nodes:
    print node['id'] + " : " + node.find("y:nodelabel").text.strip() + " " + node.data.find("y:shapenode").find("y:shape")["type"]
    nodes_list.append(node_state(node['id'],node.find("y:nodelabel").text.strip(),node.data.find("y:shapenode").find("y:shape")["type"]))

print " --- Edges --- "
for edge in edges:
	print edge['id'] + " " + edge['source'] + " " + edge['target']
	edges_list.append(node_state(edge['id'],edge['source'], edge['target']))


def check_initial_state(list):
	shapes = []
	# Check that there is EXACTLY 1 hexagon shaped state.
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

if check_initial_state(nodes_list):
	print "Success!!"

if check_single_labels(nodes_list):
	print "Success!!"

def get_node(nodes, id):
	for node in nodes:
		if node.id == id:
			el = node
	return el

def order_fsm(nodes, edges):
	final_nodes = nodes

	for edge in edges:
		get_node(final_nodes).edges.append(edge)

	#for state in nodes:
#		if state.init:
#			final_list.append(state)

	return True
