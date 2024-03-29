# run from the graph you want to prettify. 
# for POPREBEL, edges are already color coded

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
    association_depth = graph['association_depth']
    association_breadth = graph['association_breadth']
    code_id = graph['code_id']
    creator_id = graph['creator_id']
    description = graph['description']
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

    def prettify_cooc_graph(graph, intensity=True):
        '''
        (graph, bool) => None
        applies a force directed layout algo on graph.
        Also maps number of annotiations onto node size
        if intensity == True, also map edge color intensity to number of co-occurrences
        '''
        	# apply the layout
        params = tlp.getDefaultPluginParameters("FM^3 (OGDF)", graph)
        params['Unit edge length'] = 100
        params['Page Format'] = 'Landscape'
        graph.applyLayoutAlgorithm('FM^3 (OGDF)', viewLayout, params)
        params = tlp.getDefaultPluginParameters("Curve edges", graph)
        graph.applyAlgorithm('Curve edges')
        
        # set labels
        params = tlp.getDefaultPluginParameters("To labels", graph)
        params['input'] = name_en
        graph.applyStringAlgorithm('To labels', params)
        white = tlp.Color(255, 255, 255, 255)
        for n in graph.getNodes():
            viewLabelBorderWidth[n] = 0
            viewLabelColor[n] = white
        
        # apply size mapping
        params = tlp.getDefaultPluginParameters("Size Mapping", graph)
        params['min size'] = 2
        params['max size'] = 20 
        params['property'] = annotations_count
        graph.applySizeAlgorithm('Size Mapping', params)
        
            
    success = prettify_cooc_graph(graph, True)
