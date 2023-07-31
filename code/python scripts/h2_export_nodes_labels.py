'''
Use this script to export a list of nodes' labels. 
For example, a list of the codes with the maximum core value in the stacked graph.
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
    
    def export_labels(g):
        '''
        (graph) => None
        print and export the labels of the nodes in graph
        '''
        import csv
        with open ('/Users/albertocottica/Downloads/nodeLabels.csv', 'w') as csvfile: 
            writer = csv.writer(csvfile, delimiter = ',')
            nodesList = [] # store in a list to produce an alphabetically sorted list in the end.
            for n in g.getNodes():
                nodesList.append(viewLabel[n])
                nodesList.sort(key=str.lower)
            for item in nodesList:
                print(item)
                writer.writerow([item])
    
    success = export_labels(graph)
  
