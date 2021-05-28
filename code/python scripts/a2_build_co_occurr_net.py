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

dirPath = '/Users/albertocottica/Downloads/'
import datetime
start_script = datetime.datetime.now()
from tulip import tlp
import z_discourse_API_functions as api

def main(graph):
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
    
    def make_ccn_from_tag(tag):
        '''
        (string) => None
        starts from a Discourse tag referring to an ethnographic research project (ethno-PROJECTNAME).
        returns the codes co-occurrence network of that project.
        nodes are codes. Edges are induced when two codes occur on the same post.
        all relevant information about codes are saved as node properties
        all relevant information about annotations are saved as edge properties.
        '''
        # I need a map from post ID to the author_ID of the posts being annotated
        # also need one fro post ID to the topic ID to track thjat measure of diversity
        authorMap = {}
        topicMap = {}
        tops = api.fetch_topics_from_tag(tag)
        for top in tops:
            posts = api.fetch_posts_in_topic(top) 
            for post in posts: 
                authorMap[post['post_id']] = post['user_id']
                topicMap[post['post_id']] = post['topic_id']
        # create a subgraph corresponding to the project
        proj = graph.addSubGraph(tag) 
        myAnnos = api.fetch_annos(tag)
        codes = api.fetch_codes_from_annos(myAnnos)
        # first, pull the nodes from the codes list:
        # to deal with languages, I first look into the codes to see with locales I have
        locales = []
        for code in codes:
            for item in code['names']:
                locale = item['locale']
                if str(locale) not in locales:
                    locales.append(str(locale))
        # initialize the properties I need. These are main graph properties.
        code_id = graph.getStringProperty('code_id')
        post_id = graph.getStringProperty('post_id')
        description = graph.getStringProperty('description')
        creator_id = graph.getStringProperty('creator_id')
        ancestry = graph.getStringProperty('ancestry')
        parent_code = graph.getStringProperty('parent_code')
        annotations_count = graph.getIntegerProperty('annotations_count')
        user_id = graph.getStringProperty('user_id')
        topic_id = graph.getStringProperty('topic_id')
        for locale in locales:
            # I need to derive the property names from the data, and then assign them to properties 
            # See https://stackoverflow.com/questions/8530694/use-iterator-as-variable-name-in-python-loop
            propertynames = dict(("name_" + locale, graph.getStringProperty('name_' + locale)) for locale in locales)
            # this becomes name_en = graph.getStringProperty('name_en'), name_pl = ...
        # now fill the properties. Do it in the subgraphs relative to the project   
        print('Writing code information into graph nodes...')       
        for code in codes:
            n = proj.addNode({'code_id': str(code['id'])})
            if code['description']: # if the description is None the code breaks
                description[n] = code['description']
            creator_id[n] = str(code['creator_id'])
            annotations_count[n] = code['annotations_count']
            ancestry[n] = str(code['ancestry'])
            if code['ancestry'] != None: # if the ancestry is None the code breaks
                parent_code[n] = api.decompose_ancestry(code['ancestry'])[0] # the first element of the list is the direct parent
            for item in code['names']:
                proj.setNodePropertiesValues(n, {'name_' + item['locale']: item['name']})  
        print('*** Nodes added ***')
             
        theMap = {} # maps from posts to codes. Need it to create edges.
        # also adding the posts' author for "one man one vote" network reduction
        # and also the topic_id for diversity indices computation
        for anno in myAnnos:
            code_id = anno['code_id']
            post_id = anno['post_id']
            if post_id not in theMap:
                theMap[post_id]= [code_id]
            else:
                theMap[post_id].append(code_id)
                        
        # add edges from theMap to the project's subgraph.
        # each key in theMap has a list of codes (nodes) as a value. Each list is a clique.
        for post in theMap:
            clique = theMap[post]
            post_author = authorMap[post]
            post_topic = topicMap[post]
            for i in range (len(clique)):
                for j in range(i+1, len(clique)):
                    for n1 in proj['code_id'].getNodesEqualTo(str(clique[i])):
                        source = n1
                    for n2 in proj['code_id'].getNodesEqualTo(str(clique[j])):
                        target = n2
                    if n1 != n2: # self-loops do not make sense in a semantic network
                        e = proj.addEdge(source, target)
                        proj.setEdgePropertiesValues(e, {'post_id': str(post), 'user_id': str(post_author), 'topic_id': str(post_topic)})
        print ('*** Edges added ***')
        
        end_script = datetime.datetime.now()
        running_time = end_script - start_script
        print ('Executed in ' + str(running_time))
        return None
    tags = ['ethno-ngi-forward', 'ethno-poprebel', 'ethno-opencare']
    # tags = ['ethno-opencare']
    for tag in tags:
        success = make_ccn_from_tag(tag)
