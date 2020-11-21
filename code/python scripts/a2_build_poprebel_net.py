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
    
    def map_tops_to_fora():
        '''
        (str) => map of the form {topic_id(int): forum_id(str)}
        given a topic_id, assign it the name of the subcategory it is in
        ** this is a hack, not something that should hit production **
        '''
        # a dictionary of POPREBEL fora, of the form {slug: name}
        fora = {'wellbeing/pl': 'Polish', 'wellbeing/cz': 'Czech', 'wellbeing/rs': 'Serbian', 'wellbeing/eu': 'International', 'wellbeing/in-deutschland': 'German'} 
        theMap = {} # accumulator
        for forum in fora: 
            tops = api.fetch_topics_from_cat(forum)
            for top in tops:
                if top not in theMap:
                    theMap[top] = fora[forum]
        return theMap
    
    def make_ccn_from_tag(tag):
        '''
        (string) => None
        starts from a Discourse tag referring to an ethnographic research project (ethno-PROJECTNAME).
        returns the codes co-occurrence network of that project.
        nodes are codes. Edges are induced when two codes occur on the same post.
        all relevant information about codes are saved as node properties
        all relevant information about annotations are saved as edge properties.
        '''
        # change the name of the main graph 
        graph.setName(tag)
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
        # initialize the properties I need
        code_id = graph.getStringProperty('code_id')
        post_id = graph.getStringProperty('post_id')
        description = graph.getStringProperty('description')
        creator_id = graph.getStringProperty('creator_id')
        ancestry = graph.getStringProperty('ancestry')
        parent_code = graph.getStringProperty('parent_code')
        annotations_count = graph.getIntegerProperty('annotations_count')
        forum = graph.getStringProperty('forum') # introduced for POREBEL
        for locale in locales:
            # I need to derive the property names from the data, and then assign them to properties 
            # See https://stackoverflow.com/questions/8530694/use-iterator-as-variable-name-in-python-loop
            propertynames = dict(("name_" + locale, graph.getStringProperty('name_' + locale)) for locale in locales)
            # this becomes name_en = graph.getStringProperty('name_en'), name_pl = ...
        # now fill the properties   
        print('Writing code information into graph nodes...')       
        for code in codes:
            n = graph.addNode({'code_id': str(code['id'])})
            if code['description']: # if the description is None the code breaks
                description[n] = code['description']
            creator_id[n] = str(code['creator_id'])
            annotations_count[n] = code['annotations_count']
            ancestry[n] = str(code['ancestry'])
            if code['ancestry'] != None: # if the ancestry is None the code breaks
                parent_code[n] = api.decompose_ancestry(code['ancestry'])[0] # the first element of the list is the direct parent
            for item in code['names']:
                graph.setNodePropertiesValues(n, {'name_' + item['locale']: item['name']})  
        print('*** Nodes added ***')
        
        # before I create edges, I need to map topics to fora, then I will map posts to topics
        foraMap = map_tops_to_fora()                 
        
        theMap = {} # maps from posts to codes. Need it to create edges.
        for anno in myAnnos:
            code_id = anno['code_id']
            post_id = anno['post_id']
            topic_id = anno['topic_id']
            # incomplete_annos = [61549, 57699, 57796, 57711, 57696, 57626, 56882, 53607, 53423, 61311] # these annotations miss the topic_id field
            if topic_id == None:
                forum = 'Czech'
            else:            
                forum = foraMap[anno['topic_id']]
            if post_id not in theMap: # it is the first time we encounter this particular post, so we create the entry in the dict
                entry = {'codes':[code_id], 'forum': forum}
                theMap[post_id]= entry
            else: # there already is a dict as a value to this post_id, we just need to add the code_id
                theMap[post_id]['codes'].append(code_id)
        
                        
        # add edges from theMap
        # each key in theMap has a list of codes (nodes) as a value. Each list is a clique.
        for post in theMap:
            clique = theMap[post]['codes']
            for i in range (len(clique)):
                for j in range(i+1, len(clique)):
                    for n1 in graph['code_id'].getNodesEqualTo(str(clique[i])):
                        source = n1
                    for n2 in graph['code_id'].getNodesEqualTo(str(clique[j])):
                        target = n2
                    e = graph.addEdge(source, target)
                    graph.setEdgePropertiesValues(e, {'post_id': str(post), 'forum': theMap[post]['forum']})
        print ('*** Edges added ***')
        
        end_script = datetime.datetime.now()
        running_time = end_script - start_script
        print ('Executed in ' + str(running_time))
        return None
    success = make_ccn_from_tag('ethno-poprebel')
#    mapp = map_tops_to_fora()
#    print(mapp[4113])
#
 
