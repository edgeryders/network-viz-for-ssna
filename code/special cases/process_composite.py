# Powered by Python 2.7
# To cancel the modifications performed by the script
# on the current graph, click on the undo button.
# Some useful keyboard shortcuts:
#   * Ctrl + D: comment selected lines.
#   * Ctrl + Shift + D: uncomment selected lines.
#   * Ctrl + I: indent selected lines.
#   * Ctrl + Shift + I: unindent selected lines.
#   * Ctrl + Return: run script.
#   * Ctrl + F: find selected text.
#   * Ctrl + R: replace selected text.
#   * Ctrl + Space: show auto-completion dialog.
from tulip import tlp
# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views
# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the
# "Run script " button.
# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call
# (in the form [a-zA-Z0-9_]+.py)
# The main(graph) function must be defined
# to run the script on the current graph



def findEdge(node1, node2, graph1, directed = False, create = True):

	'''
   finds an edge connecting two given nodes if it exists,
   if not returns a newly created edge unless stated otherwise
   deals with either directed or undirected graphs
   '''

	e = graph1.existEdge(node1, node2, directed)
	if e.isValid():
		return e
	else:
		if create:
			e = graph1.addEdge(node1, node2)
			return e                        
		else:
		    return None

def main(graph):
    ancestry = graph['ancestry']
    annotations_count = graph['annotations_count']
    code_id = graph['code_id']
    connectors = graph['connectors']
    creator_id = graph['creator_id']
    description = graph['description']
    forum = graph['forum']
    name = graph['name']
    name_cs = graph['name_cs']
    name_de = graph['name_de']
    name_en = graph['name_en']
    name_pl = graph['name_pl']
    name_sr = graph['name_sr']
    parent_code = graph['parent_code']
    postDate = graph['postDate']
    post_id = graph['post_id']
    posts = graph['posts']
    topic_id = graph['topic_id']
    unixDate = graph['unixDate']
    user_id = graph['user_id']
    viewBorderColor = graph['viewBorderColor']
    viewBorderWidth = graph['viewBorderWidth']
    viewColor = graph['viewColor']
    viewFont = graph['viewFont']
    viewFontSize = graph['viewFontSize']
    viewIcon = graph['viewIcon']
    viewLabel = graph['viewLabel']
    viewLabelBorderColor = graph['viewLabelBorderColor']
    viewLabelBorderWidth = graph['viewLabelBorderWidth']
    viewLabelColor = graph['viewLabelColor']
    viewLabelPosition = graph['viewLabelPosition']
    viewLayout = graph['viewLayout']
    viewMetric = graph['viewMetric']
    viewRotation = graph['viewRotation']
    viewSelection = graph['viewSelection']
    viewShape = graph['viewShape']
    viewSize = graph['viewSize']
    viewSrcAnchorShape = graph['viewSrcAnchorShape']
    viewSrcAnchorSize = graph['viewSrcAnchorSize']
    viewTexture = graph['viewTexture']
    viewTgtAnchorShape = graph['viewTgtAnchorShape']
    viewTgtAnchorSize = graph['viewTgtAnchorSize']

#    totEdges = 0
#    comp = graph.getSubGraph('composite')
#    for sg in graph.getSubGraphs():
#        if sg != comp:
#            stacked = sg.getSubGraph('stacked')
#            totEdges += stacked.numberOfEdges()
#    print(totEdges)
#
#    comp = graph.addSubGraph('composite')
#    for n in graph.getNodes():
#        comp.addNode(n)
#    for sg in graph.getSubGraphs():
#        if sg != comp:
#            stacked = sg.getSubGraph('stacked')
#            for e in stacked.getEdges():
#                comp.addEdge(e)

#	    pl = graph.getSubGraph('pl')
#	    de = graph.getSubGraph('cz')
#	    pl_de_edges = 0
#	    for e in pl.getEdges():
#	        source = pl.source(e)
#	        target = pl.target(e)
#	        if source in de and target in de and findEdge (pl.source(e), pl.target(e), de, False, False):
#	            pl_de_edges += 1
#    print (pl_de_edges)

    def find_multilanguage_edges(graph1):
		'''
		(graph) list of dicts
		returns a list of couples of edges with the same source and target, but different values of the forum property
		[{'source': name_en[node1], 'target': name_en[node2], 'languages': [lang1, lang2]}]
		'''
		mlEdges = []
		fora = ['Polish', 'Czech', 'International', 'German', 'Serbian'] 
		for forum1 in fora:
		 	for forum2 in fora:
		 		if forum1 != forum2:
		 			print (forum1, forum2)
		 			for e1 in forum.getEdgesEqualTo(forum1):
		 				item = {'languages': []}
		 				if e1 in graph1.getEdges():
			 				source = graph1.source(e1)
			 				target = graph1.target(e1)
			 				for e2 in forum.getEdgesEqualTo(forum2):
			 					if e2 in graph1.getEdges():
				 					if (graph1.source(e2) == source) and ((graph1.target(e2) == target) or
				 					(graph1.source(e2) == target and graph1.target(e2) == source)):
				 						item['source'] = name_en[source]
				 						item['target'] = name_en[target]
				 						item['languages'].append(forum[e1])
				 						item['languages'].append(forum[e2])
				 						mlEdges.append(item)
			return mlEdges
    def count_edges_by_language(graph1):
		'''
		(graph) => dict
		returns a dict where keys are languages, values numbers of edges in that language
		'''		
		edgeCount = {}
		fora = [] # build a list of languages 
		for e in graph1.getEdges():
			if forum[e] not in fora:
				fora.append(forum[e])
		
		for f in fora: 
			edgeCount[f] = 0
			for e in graph1.getEdges():
				if forum[e] == f:
					edgeCount[f] += 1
		return edgeCount
		
#    success = count_edges_by_language(graph)
#    print(success)
#
    success = find_multilanguage_edges(graph)
    print (success[0])
    print(len(success))

