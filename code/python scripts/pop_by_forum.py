# run from the graph you want to examine
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
    uid = graph['uid']
    unixDate = graph['unixDate']
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

    # create the subgraphs corresponding to values of the forum property
    params = tlp.getDefaultPluginParameters("Equal Value", graph)
    params['Type'] = 'edges'
    params['Property'] = forum
    graph.applyAlgorithm('Equal Value', params)
    
    
    # color code edges
    
    czech_blue = tlp.Color.Sapphire 
    polish_red = tlp.Color.Red
    eu_blue = tlp.Color.Azure
    serbian_white = tlp.Color.White
    one_extra = tlp.Color.Green   
    colors = [czech_blue, polish_red, eu_blue, serbian_white, one_extra]
    i = 0
    for g in graph.getSubGraphs():
        for e in g.getEdges():
            viewColor[e] = colors[i]
        i += 1
    
  
