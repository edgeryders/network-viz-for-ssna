## iterate over the stacked graphs of each language forum and make a composite
## edges keep track of d and b PER EACH LANGUAGE
## run from the root

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
    association_breadth = graph['association breadth']
    association_depth = graph['association depth']
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

    def build_stacked_composite():
        '''
        (None) => graph
        build a graph with the STACKED edges from every language
        '''
        comp = graph.addSubGraph('composite')
        for lang in graph.getSubGraphs():
            l = lang.getName()
            print(l)
            if l not in ['all fora', 'composite']: # all fora must be excluded to avoid double counting
                stacked = lang.getSubGraph('stacked')
                for n in stacked.getNodes():
                    if n not in comp:
                        comp.addNode(n)
                for e in stacked.getEdges():
                    comp.addEdge(e)
        return comp
        
    success = build_stacked_composite()
    
