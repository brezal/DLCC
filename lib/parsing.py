class Parsing:

        def check_duplicates(self,name,parent_Names):
		# You might have multiple 'And's or 'Or's in a given logic statement: assign them each a unique name by pinning on 0s
		# parent_Names is a list of names we've used already
                if name in parent_Names: 
			
                        parent_Names.append(name+'0')
                        return name + '0'
                else:
                        parent_Names.append(name)
                        return name



	def fun_recursive_add_to_logic_graph(self,lst_nested_logic_statement,parent_Name,parent_Names,G_nested_logic_statement):
		if ',' not in lst_nested_logic_statement[-1]:
			if len(lst_nested_logic_statement) == 2:
				key = lst_nested_logic_statement[-1]
				if len(key) == 2:
					G_nested_logic_statement.add_edge(key[0][0],parent_Name)
					G_nested_logic_statement.add_edge(key[1],parent_Name)
				else:
					G_nested_logic_statement.add_edge(key[0],parent_Name)

		else:
			comma_index = lst_nested_logic_statement[1].index(',')
			first_partition = lst_nested_logic_statement[1][0:comma_index]
			second_partition = lst_nested_logic_statement[1][comma_index + 1:]
			first_ID = self.check_duplicates(str(first_partition[0]),parent_Names)
			second_ID = self.check_duplicates(str(second_partition[0]),parent_Names)
			G_nested_logic_statement.add_edge(first_ID,parent_Name)
			G_nested_logic_statement.add_edge(second_ID,parent_Name)
			self.fun_recursive_add_to_logic_graph(first_partition,first_ID,parent_Names,G_nested_logic_statement)
			self.fun_recursive_add_to_logic_graph(second_partition,second_ID,parent_Names,G_nested_logic_statement)

	def fun_build_parsed_logic_graph(self,lst_nested_logic_statement):
		
		import networkx as nx
		from lib.graph_tools import Graph_Tools
		gt = Graph_Tools()

		print('Parsing Boolean logic equation into digraph...')
		G_nested_logic_statement = nx.MultiDiGraph()
		G_nested_logic_statement.add_node(str(lst_nested_logic_statement[0][0])) # add the first parent to the graph
		reduced_list = lst_nested_logic_statement[0][1] # take everything else in the nested list
		parent_Names = [] # make an empty array for names we've already used
		parent_Name = str(lst_nested_logic_statement[0][0]) 
		self.fun_recursive_add_to_logic_graph(lst_nested_logic_statement[0],parent_Name,parent_Names,G_nested_logic_statement) # call the recursive funciton until we're done
	
		gt.fun_save_graph(G_nested_logic_statement,'nested_logic_statement')
		
		print('Done.')

		return G_nested_logic_statement
