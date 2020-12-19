# run this to stack edges on top of each other

# run from the supergraph of the graphs you want to stack. In general, this is the root graph.

from tulip import *


# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# the main(graph) function must be defined 
# to run the script on the current graph

def findEdge(node1, node2, graph1, directed = False, create = True):
	'''
   finds an edge connecting two given nodes if it exists,
   if not returns a newly created edge unless stated otherwise
   deals with either directed or undirected graphs
   '''
	e = graph1.existEdge(node1, node2)
	if e.isValid():
		return e
	else:
		if not directed:
			e = graph1.existEdge(node2, node1)
			if e.isValid():
				return e
			else:
				if create:
					e = graph1.addEdge(node1, node2)
					return e                        
		else:
			if create:    
				e = graph1.addEdge(node1, node2)
				return e
			else:
				return None


def main(graph): 
	name = graph.getStringProperty("name")
	postDate = graph.getStringProperty("postDate")
	user_id = graph.getStringProperty("user_id")
	unixDate = graph.getDoubleProperty("unixDate")
	viewBorderColor = graph.getColorProperty("viewBorderColor")
	viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
	viewColor = graph.getColorProperty("viewColor")
	viewFont = graph.getStringProperty("viewFont")
	viewFontAwesomeIcon = graph.getStringProperty("viewFontAwesomeIcon")
	viewFontSize = graph.getIntegerProperty("viewFontSize")
	viewLabel = graph.getStringProperty("viewLabel")
	viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
	viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
	viewLabelColor = graph.getColorProperty("viewLabelColor")
	viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
	viewLayout = graph.getLayoutProperty("viewLayout")
	viewMetric = graph.getDoubleProperty("viewMetric")
	viewRotation = graph.getDoubleProperty("viewRotation")
	viewSelection = graph.getBooleanProperty("viewSelection")
	viewShape = graph.getIntegerProperty("viewShape")
	viewSize = graph.getSizeProperty("viewSize")
	viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
	viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
	viewTexture = graph.getStringProperty("viewTexture")
	viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
	viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
	
	def stackAll():
		'''
		(None) => None
		for each subgraph of the main, it creates two subgraphs: one is a copy of the original,
		the other is a version of the original where are either zero or one edge between any two nodes.
		When the original graph has n edges between two nodes, the new subgraph has only one, with weight n.
		edge weight is stored in the integer property "weight".  
		If the main has no subgraphs, create one, and rename the root. 
		'''
		# initialize properties I need
		cooc = graph.getIntegerProperty('co-occurrences') # stores k(e)
		connectors = graph.getStringVectorProperty('connectors') # stores the list of people making the association. Its length is kn(e)
		uc = graph.getIntegerProperty('num_connectors') 
		gs = []
		for g in graph.getSubGraphs():
		    gs.append(g)
		if len(gs) == 0:
		    gname = graph.getName()
		    graph.setName('root')
		    graph.addCloneSubGraph(gname)

		for g in graph.getSubGraphs():
			# clone the parallel edges graph onto a new subgrah
			nonStacked = g.addCloneSubGraph('nonStacked')
							
			# create a stacked subgraph 
			stacked = g.addSubGraph('stacked')	
			
			# add all nodes in nonStacked to stacked
			for n in nonStacked.getNodes():	
				stacked.addNode(n)
				
			# you go over all edges in graph1 and add only one edge to graph2
			# also collect the data you are interested in
			for edge in nonStacked.getEdges():
				source = nonStacked.source(edge)
				target = nonStacked.target(edge)
				# source and target are nodes connect
				subEdge = findEdge(source, target, stacked, False, False)
				if subEdge == None: # the stacked does not contain any edge between source and target
					subEdge = stacked.addEdge(source, target)
					success = stacked.setEdgePropertiesValues(subEdge, {'viewColor': edgeColor, 'co-occurrences': 1, 'connectors': [user_id[edge]]})
				else:
					cooc[subEdge] += 1
					connectorsList = graph.getEdgePropertiesValues(subEdge)['connectors']
					if user_id[edge] not in connectorsList:
						connectorsList.append(user_id[edge])
						update = graph.setEdgePropertiesValues(subEdge, {'connectors': connectorsList})
			# last move: iterate over edges of the stacked and compute the kn(e) property
			for subEdge in stacked.getEdges():
				uc[subEdge] = len(connectors[subEdge])

	success = stackAll()
    
