# run from a graph where edges have been assigned the user_gender property
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
					return None                       
		else:
			if create:    
				e = graph1.addEdge(node1, node2)
				return e
			else:
				return None

def main(graph):
    user_gender = graph['user_gender']
    ancestry = graph['ancestry']
    annotations_count = graph['annotations_count']
    association_breadth = graph['association_breadth']
    association_depth = graph['association_depth']
    cooccurrences = graph['co-occurrences']
    code_id = graph['code_id']
    connectors = graph['connectors']
    creator_id = graph['creator_id']
    description = graph['description']
    gender_list = graph['gender_list']
    name = graph['name']
    name_cs = graph['name_cs']
    name_de = graph['name_de']
    name_en = graph['name_en']
    name_it = graph['name_it']
    name_pl = graph['name_pl']
    name_sr = graph['name_sr']
    num_connectors = graph['num_connectors']
    num_posts = graph['num_posts']
    number_topics = graph['number_topics']
    parent_code = graph['parent_code']
    postDate = graph['postDate']
    post_id = graph['post_id']
    posts = graph['posts']
    topic_id = graph['topic_id']
    topics = graph['topics']
    unique_posts = graph['unique_posts']
    unixDate = graph['unixDate']
    user_id = graph['user_id']
    viewBorderColor = graph['viewBorderColor']
    viewBorderWidth = graph['viewBorderWidth']
    viewColor = graph['viewColor']
    viewFont = graph['viewFont']
    viewFontAwesomeIcon = graph['viewFontAwesomeIcon']
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

    stacked = graph.addSubGraph('stacked')
    nonStacked = graph.addCloneSubGraph('nonStacked')
    for n in graph.getNodes():
        stacked.addNode(n)
    for edge in nonStacked.getEdges():
        source = nonStacked.source(edge)
        target = nonStacked.target(edge)
        edgeColor = viewColor[edge]
        subEdge = findEdge(source, target, stacked, False, False)
        # go over all edges in nonStacked and add only one edge to Stacked
		# also collect the data you are interested in
		
        if subEdge == None: 
		    subEdge = stacked.addEdge(source, target) # I add the edge to the stacked if it is not there already
		    initialize_edge = stacked.setEdgePropertiesValues(subEdge, {'viewColor': edgeColor, 'connectors': [user_id[edge]], 'posts': [post_id[edge]], 'topics': [topic_id[edge]], 'gender_list': [user_gender[edge]]})
        else:
            postsList = stacked.getEdgePropertiesValues(subEdge)['posts']
            postsList.append(post_id[edge])
            update = stacked.setEdgePropertiesValues(subEdge, {'posts': postsList})
            gendersList = stacked.getEdgePropertiesValues(subEdge)['gender_list']
            gendersList.append(user_gender[edge])
            update = stacked.setEdgePropertiesValues(subEdge, {'gender_list': gendersList})
            association_depth[subEdge] += 1
            connectorsList = connectors[subEdge] # Bruno's version! graph.getEdgePropertiesValues(subEdge)['connectors']
            topicsList = topics[subEdge] 
            postsList = posts[subEdge]
            if user_id[edge] not in connectorsList:
                connectorsList.append(user_id[edge])
                update = stacked.setEdgePropertiesValues(subEdge, {'connectors': connectorsList})
            if topic_id[edge] not in topicsList:
                topicsList.append(topic_id[edge])
                update = stacked.setEdgePropertiesValues(subEdge, {'topics': topicsList})
				
	# last move: iterate over edges of the stacked and compute the numeric properties
	for subEdge in stacked.getEdges():
		association_breadth[subEdge] = len(connectors[subEdge])
		association_depth[subEdge] = len(posts[subEdge]) # define a function to compute num_posts based on posts_list
		number_topics[subEdge] = len(topics[subEdge])
		posts_seen = [] # to compute the number of unique contributions make a list where posts appear only once
		unique_posts[subEdge] = len(set(posts[subEdge])) # remove duplicates



