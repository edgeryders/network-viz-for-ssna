# run from the stacked

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
    ancestry = graph['ancestry']
    annotations_count = graph['annotations_count']
    cooccurrences = graph['co-occurrences']
    code_id = graph['code_id']
    connectors = graph['connectors']
    creator_id = graph['creator_id']
    description = graph['description']
    name = graph['name']
    name_cs = graph['name_cs']
    name_de = graph['name_de']
    name_en = graph['name_en']
    name_pl = graph['name_pl']
    num_connectors = graph['num_connectors']
    parent_code = graph['parent_code']
    postDate = graph['postDate']
    post_id = graph['post_id']
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
    
    def ego_network(node, origingraph, resultgraph):
        '''
        (Tulip node, Tulip graph, Tulipgraph) => None
        finds all the neighbors of node in origingraph. 
        Adds to resultgraph node, its neigbors and the connecting edges
        '''
        
        for n in origingraph.getInOutNodes(node):
            if n not in resultgraph:
                resultgraph.addNode(n)
        for e in origingraph.getInOutEdges(node):
            if e not in resultgraph:
                resultgraph.addEdge(e)
        return None
    origin = graph.getSubGraph('k = 010')
    codes = graph.getSubGraph('codes')
    sus = graph.addSubGraph('sustainability')
    for n in codes.getNodes():
        sus.addNode(n)
        if n in origin:
            success = ego_network(n, origin, sus)
