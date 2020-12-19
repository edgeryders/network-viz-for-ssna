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
def main(graph):
    ancestry = graph['ancestry']
    annotations_count = graph['annotations_count']
    code_id = graph['code_id']
    creator_id = graph['creator_id']
    degree = graph['degree']
    description = graph['description']
    forum = graph['forum']
    name_cs = graph['name_cs']
    name_en = graph['name_en']
    name_pl = graph['name_pl']
    name_sr = graph['name_sr']
    numComms = graph['numComms']
    parent_code = graph['parent_code']
    post_id = graph['post_id']
    user_id = graph['user_id']
    user_name = graph['user_name']
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
    # initialize the colors
    blue = tlp.Color(102,204,255, 255)  
    red = tlp.Color(204,51, 0, 255)
    green = tlp.Color(51,255,204, 255)
    orange = tlp.Color(255, 153, 0, 255)
    steel = tlp.Color(160,160,160, 255) ## steel I keep for nodes that participate in more than one conversation
    colors = [blue, red, green, orange, steel] # need to add more colors


    def color_edges():
        '''
        (None) => None
        colors the edges according to the value of the forum property
        '''
        fora = {} # map from value of forum to color
        i = 0 
        for e in graph.getEdges():
            if forum[e] not in fora:
                fora[forum[e]] = colors[i]
                i += 1
            graph.setEdgePropertiesValues(e, {'viewColor': fora[forum[e]]})
        print(fora)
        return None
        
    def color_nodes():
        '''
        (None) => None
        color nodes according to the colors of the incident edges.
        * if all edges are of the same color, the node imherits that color
        * if there are at least two edges of different colors, the node is colored in steel
        '''    
        for n in graph.getNodes():
            incidentEdgeColors = []
            for e in graph.getInOutEdges(n):
                if viewColor[e] not in incidentEdgeColors:
                    incidentEdgeColors.append(viewColor[e])
            if len(incidentEdgeColors) == 1:
                viewColor[n] = incidentEdgeColors[0]
            else:
                viewColor[n] = steel
                
        
        
        
    success = color_nodes()
