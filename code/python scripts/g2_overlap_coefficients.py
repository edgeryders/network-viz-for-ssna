'''
Calculates overlap coefficients between the sets of nodes and edges of two subgraphs. 

OL = A intersection B / min (A,B)

where A, B represent the cardinalities of the sets

'''
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
def main(graph):
    category_id = graph['category_id']
    numComms = graph['numComms']
    user_name = graph['user_name']
    viewFontAwesomeIcon = graph['viewFontAwesomeIcon']
    wordCount = graph['wordCount']
    ancestry = graph['ancestry']
    annotations_count = graph['annotations_count']
    association_breadth = graph['association_breadth']
    association_depth = graph['association_depth']
    cooccurrences = graph['co-occurrences']
    code_id = graph['code_id']
    connectors = graph['connectors']
    creator_id = graph['creator_id']
    description = graph['description']
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
    user_gender = graph['user_gender']
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

    def overlap(graph1, graph2):
        '''
        (graph, graph) => dict
        the dict contains overlap cofficients, like {'nodes_overlap: 0.5, edges_overlap: 0.1}
        '''
        
        nodesEdgesCount = {'nodes': {}, 'edges': {}} # store number of nodes and edges, exclusive or shared, here
        nodesEdgesCount['edges'][graph1.getName()] = 0 
        nodesEdgesCount['edges'][graph2.getName()] = 0 
        nodesEdgesCount['edges']['shared'] = 0 
        # create lists of nodes for both graphs
        nodes_graph1 = []
        for n in graph1.getNodes():
            nodes_graph1.append(n)
        nodesEdgesCount['nodes'][graph1.getName()] = len(nodes_graph1)
        nodes_graph2 = []
        for n in graph2.getNodes():
            nodes_graph2.append(n)
        nodesEdgesCount['nodes'][graph2.getName()] = len(nodes_graph2)
        sharedNodes = [] # I want a list of the shared codes
        for n in nodes_graph1:
            if n in nodes_graph2:
                sharedNodes.append(name_en[n])
            nodesEdgesCount['nodes']['shared'] = len(sharedNodes)
        
        # for edges, I cannot simply identify them, but need to look for the equivalent edges in the other graph
        # (same source, same target)
        
        sharedEdges = [] # a list of shared edges, needs actually to be a list of tuples to be more human readable
        for e in graph1.getEdges():
            source = graph1.source(e)
            target = graph1.target(e)
            if source in nodes_graph2 and target in nodes_graph2: # check that source and targets exist in the other graph
                e1 = graph2.existEdge(source, target, False)
                if e1.isValid():
                    nodesEdgesCount['edges']['shared'] += 1
                    sharedEdges.append((name_en[source], name_en[target]))
                else:
                    nodesEdgesCount['edges'][graph1.getName()] += 1
            else:
                nodesEdgesCount['edges'][graph1.getName()] += 1
                
        for e  in graph2.getEdges():
            source = graph2.source(e)
            target = graph2.target(e)
            if source in nodes_graph1 and target in nodes_graph1: # check that source and targets exist in the other graph
                e1 = graph1.existEdge(source, target, False)
                if e1.isValid():
                    pass # to avoid double counting
                else:
                    nodesEdgesCount['edges'][graph2.getName()] += 1
            else:
                nodesEdgesCount['edges'][graph2.getName()] += 1
        # compute the overlap coefficients
        ol = {'overlap_nodes': 0, 'overlap_edges': 0}
        values = [] # store the counts to take the min from
        for key in nodesEdgesCount['nodes']:
               if key != 'shared':
                   values.append(nodesEdgesCount['nodes'][key])
        ol['overlap_nodes'] = nodesEdgesCount['nodes']['shared'] / float(min(values))
        values = [] # repeat, but with edges
        for key in nodesEdgesCount['edges']:
               if key != 'shared':
                   values.append(nodesEdgesCount['edges'][key])
        ol['overlap_edges'] = nodesEdgesCount['edges']['shared'] / float(min(values))
                
        # now create a results object        
        results = {'nodes and edges count': nodesEdgesCount, 'shared nodes': sharedNodes, 'shared edges': sharedEdges, 'overlap': ol}
                    
        return results
    m4 = graph.getRoot().getSubGraph('german').getSubGraph('males').getSubGraph('stacked').getSubGraph('d>4 m')
    f4 = graph.getRoot().getSubGraph('german').getSubGraph('females').getSubGraph('stacked').getSubGraph('d>4 f')
    success = overlap(m4, f4)
    print (success)

        
  
