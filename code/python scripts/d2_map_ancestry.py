# This script induces a tree representing the hierarchy of codes. 
# directed edges are created from each parent code to its children. 
# A root node is created that takes the name of the tag.
# run from the ethno-PROJECTNAME

from tulip import tlp

def main(graph):
    ancestry = graph['ancestry']
    annotations_count = graph['annotations_count']
    cooccurrences = graph['co-occurrences']
    code_id = graph['code_id']
    creator_id = graph['creator_id']
    description = graph['description']
    name_cs = graph['name_cs']
    name_en = graph['name_en']
    name_pl = graph['name_pl']
    name_sr = graph['name_sr']
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

    def create_ancestry_graph():
        '''
        (None)=> graph
        the returned subgraph has to be a tree
        '''
        parent_code = graph.getStringProperty('parent_code')
        ch = graph.addSubGraph('codes hierarchy')
        # create the root node
        projectName = graph.getName()
#        root = ch.addNode({'name_en': projectName, 'ancestry': 'root'})
#        # add all the other nodes. 
        for n in graph.getNodes():
            newNode = ch.addNode(n)
        # add ancestry edges
        for n in graph.getNodes():
            if parent_code[n] == 'None':
                a = 1
#                e = ch.addEdge(root, n)
            else: 
               parent = parent_code[n]
               for p in graph['code_id'].getNodesEqualTo(parent):
                   e = ch.addEdge(p, n)            

        return ch    
        
    success = create_ancestry_graph()
