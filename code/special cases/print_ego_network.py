# maps the ego network of a node
# first select the node and all its neighbour nodes including edges
# create a subgraph from the selection, then run the script from the selection subgraph
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
    association_breadth = graph['association_breadth']
    association_depth = graph['association_depth']
    code_id = graph['code_id']
    connectors = graph['connectors']
    creator_id = graph['creator_id']
    degree = graph['degree']
    description = graph['description']
    female_prevalence = graph['female_prevalence']
    name_cs = graph['name_cs']
    name_de = graph['name_de']
    name_en = graph['name_en']
    name_pl = graph['name_pl']
    name_sr = graph['name_sr']
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
    wordCount = graph['wordCount']
    
    def find_ego_network(egolabel):
        '''
        (string) => list of dicts. Each dict has the form  
        {'alter': string, 'depth': assdepth property, 
        'breadth': assbreadth property, 'female prevalence': femprev property}
        '''
        # find the node corresponding to  egolabel 
        for n in graph.getNodes():
            if name_en[n] == egolabel:
                ego = n
        to_return = []
    
        for e in graph.getEdges():
            thisEdge = {}
            source = graph.source(e)
            target = graph.target(e)
            if source != ego:
                thisEdge['alter'] = viewLabel[source]
            else: 
                thisEdge['alter'] = viewLabel[target]
            thisEdge['association depth'] = association_depth[e]
            thisEdge['association breadth'] = association_breadth[e]
            thisEdge['female_prevalence'] = female_prevalence[e]
            to_return.append(thisEdge)
        return to_return
    
    import csv
    dirPath = '/Users/albertocottica/Downloads/'
    egolabel = 'welfare state'
    my_data = find_ego_network(egolabel)
    with open (dirPath + egolabel + '.csv', 'w') as csvfile:
        fieldnames = []
        for key in my_data[0]:
            fieldnames.append(key)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in my_data:
            writer.writerow(row)
