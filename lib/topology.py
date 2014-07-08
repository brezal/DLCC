class Topology:
	
	def __init__(self):
		import matplotlib.pyplot as plt
		self.plt = plt
		
		import networkx as nx
		self.nx = nx
		
		from sets import Set #chomp_tree needs this - define it here because chomp_tree is recursive
		self.Set = Set

		from lib.xml_input import Inputs
		self.Inputs = Inputs

	
	def gate_topology(self,graph,inputs,gate,counter):
		gate_type = gate.translate(None,'0')
		if gate_type == 'Not':
		        graph.add_edge(inputs[0],'1_'+str(counter))
			terminal_node = '1_'+str(counter)
		        counter = counter + 1
		if gate_type == 'Or':
		        graph.add_edge(inputs[0],'1_'+str(counter))
		        graph.add_edge(inputs[1],'1_'+str(counter))
		        graph.add_edge('1_'+str(counter),'1_'+str(counter+1))
			terminal_node = '1_'+str(counter+1)
		        counter = counter + 2
		if gate_type == 'And':
		        graph.add_edge(inputs[1],'1_'+str(counter))
		        graph.add_edge('1_'+str(counter),inputs[0])
			terminal_node = inputs[0]
		        counter = counter + 1
		return [terminal_node,counter]


	def chomp_tree(self,graph,tree,counter):
		# the counter allows us to give each '1' track a unique name in the gate_topology function above
		stop = 0
		# find the leaves of the tree
		leaves_array = tree.leaves(tree.root)
		# build an array of the parents of each of those leaves		
		parent_array = []
		for leaf in leaves_array:
			parent_array.append(tree.parent(leaf).identifier)
		parent_array = list(self.Set(parent_array)) # eliminate repeats in parent_array
		for parent in parent_array:
			if self.Set(tree.is_branch(parent)).issubset(self.Set(leaves_array)): # if the children of the parent are in the leaves...
				if parent == tree.root: # break out of the loop if we've reached the root of the tree
					stop = 1
				inputs = tree.is_branch(parent) # find the inputs going to this parent
				compute_topology = self.gate_topology(graph,inputs,parent,counter) # based on the type of gate, the parent, fetch the gate topology from gate_topology
				counter = compute_topology[1] # allows us to continue on giving '1' tracks unique names
				new_node = compute_topology[0] # the terminal node of the gate, based on the gate topology
				if stop == 0:
					target = tree.parent(parent).identifier # target is parent of the parent (what the gate connects to)
					tree.remove_node(parent) # get rid of the parent node...
					tree.create_node(new_node,new_node,parent=target) # ... and make the terminal node of the gate the child of the parent's parent (the 'target')

		if stop == 0:
			self.chomp_tree(graph,tree,compute_topology[1]) # if we didn't tell it to stop (i.e. we're not yet at the root node), repeat 

	def topology_plot(self,G,cmd_arg):
		i = self.Inputs()
		args = i.extract_topology(cmd_arg)
		self.plt.figure()
		pos=self.nx.spring_layout(G,iterations=10)
		self.nx.draw(G,pos,node_size=0,alpha=0.4,edge_color='r',font_size=16)
		self.plt.savefig("out/track_topology"+args[1])
		if args[0].lower() == 'yes':
			self.plt.show()

	def refine_topology(self,G,cmd_arg):
		i = self.Inputs()
		args = i.extract_topology(cmd_arg)
		nodes = G.nodes()
		for node in nodes:
			try:
				lev_1_successors = G.successors(node)
				if lev_1_successors and len(lev_1_successors) == 1:
					lev_2_successors = G.successors(lev_1_successors[0])
					if lev_2_successors and len(lev_2_successors) == 1:
						lev_3_successors = G.successors(lev_2_successors[0])
					
						if lev_1_successors[0][0] == '1' and lev_2_successors[0][0] == '1'and len(lev_3_successors) == 1:
							G.add_edge(node,lev_3_successors[0])
							G.remove_node(lev_1_successors[0])
							G.remove_node(lev_2_successors[0])
			except:
				pass
		self.plt.figure()
		pos=self.nx.spring_layout(G,iterations=10)
		self.nx.draw(G,pos,node_size=0,alpha=0.4,edge_color='r',font_size=16)
		self.plt.savefig("out/topology_refinement"+args[1])
		return G