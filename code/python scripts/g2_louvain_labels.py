## exports to console node labels, divided by Louvain maximal modularity partition class
## run from the graph whose labels you want exported
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
    description = graph['description']
    name = graph['name']
    name_cs = graph['name_cs']
    name_de = graph['name_de']
    name_en = graph['name_en']
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

    def export_labels_community(tulipProperty):
        '''
        (tulipProperty) => None
        for each Louvain partition, writes the nodes' labels to console
        rank them by degree
        '''
        ## compute Louvain and store it in a property 
        mod_partition = graph['modularity partition']
        params = tlp.getDefaultPluginParameters("Louvain", graph)
        params['metric'] = tulipProperty
        params['result'] = mod_partition
##        graph.applyDoubleAlgorithm('Louvain', params)
        print('Modularity: ' + str(params['modularity']))
        
        
        ## compute degree and store it in a property 
        degree = graph['degree']
        params = tlp.getDefaultPluginParameters("Degree", graph)
        params['metric'] = tulipProperty
        params['result'] = degree
##        graph.applyDoubleAlgorithm('Degree', params)
        
        ## collect the nodes in a dict. 
        allnodes = []
        maxclass = 0
        for n in graph.getNodes():    
            thisnode = {}       
            thisnode['label'] = name_en[n]
            partitionClass = int(mod_partition[n])
            thisnode ['class'] = partitionClass
            thisnode['degree'] = int(degree[n])
            allnodes.append(thisnode)
            if partitionClass > maxclass:
                maxclass = partitionClass
        
        ## print 
        
        an = sorted(allnodes, key = lambda d: d['degree'])
        partclasses = []
        for i in range (maxclass + 1):
            thisclass = {}
            print('')
            print('Partition class: ' + str(i))
            classlist = []
            for item in allnodes:
                if item['class'] == i:
                    classlist.append(item)
            cl = sorted(classlist, key = lambda d: d['degree'], reverse = True)  
            thisclass['partition class'] = i
            thisclass['nodes in class'] = len(cl)
            partclasses.append(thisclass)
            print(str(len(cl)) + ' nodes')      
            for item2 in cl:
                print(item2['label'] + ' (' + str(item2['degree']) +')')
        pc = sorted(partclasses, key = lambda d: d['nodes in class'], reverse = True)
        print ('class, number of codes')
        for item3 in pc:
            print (item3['partition class'], item3['nodes in class'])
        
        return None
    success = export_labels_community(association_breadth)
