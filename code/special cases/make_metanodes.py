''' 
run from the graph that you want to add the metanode to
We start from an original graph (og), which has a subgraph (ssg). This subgraph contains nodes that we want
to collapse into a metanode. The easiest way is to select manually some nodes, then select 
"create subgraph from selection"

High level:
    
1. Make a clone subgraph (csg). This preserves the original graph with no metanodes.
2. In the csg, use the createMetaNode(ssg, False, False) primitive to create the metanode.
Also compute the properties of the metanode from those of the nodes in ssg.
3. Go through og and select all the edges incident to the nodes in ssg. 
4. For each node incident to one of those edges, create (in csg) a new edge connecting that node 
to the metanode. This way, each one of those nodes has exactly one edge connecting it to 
the metanode. 
5. From the selected edges, compute the values of the properties of the newly created edges.
'''
from tulip import tlp

def main(graph):
    ancestry = graph['ancestry']
    annotations_count = graph['annotations_count']
    cooccurrences = graph['co-occurrences']
    code_id = graph['code_id']
    connectors = graph['connectors']
    creator_id = graph['creator_id']
    degree = graph['degree']
    description = graph['description']
    forum = graph['forum']
    name = graph['name']
    name_cs = graph['name_cs']
    name_en = graph['name_en']
    name_pl = graph['name_pl']
    name_sr = graph['name_sr']
    numComms = graph['numComms']
    num_connectors = graph['num_connectors']
    parent_code = graph['parent_code']
    postDate = graph['postDate']
    post_id = graph['post_id']
    unixDate = graph['unixDate']
    user_id = graph['user_id']
    user_name = graph['user_name']
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
    wordCount = graph['wordCount']

    def make_metanode(sg):
        '''
        (str) => Tulip subgraph
        the argument is the name of a subgraph. Returns another subgraph, where the nodes in sg
        are replaced by a single metanode. Edges incident to the nodes in the metanode
        are rewired to the metanode itself, and the relevant properties recomputed.
        '''
        # create the graph tree, do the renaming as needed
        gname = graph.getName()
        ssg = graph.getSubGraph(sg)
        ssgname = ssg.getName()
        og = graph.addCloneSubGraph(gname + '_unchanged' , True)
        csg = graph.addCloneSubGraph(gname + '_mn_' + ssgname)
        
        # create the "metanode" and populate its properties
        mn = csg.createMetaNode(ssg)
        name_en[mn] = ssg.getName()
        anns = 0 # to populate later when I iterate through nodes in ssn
        steel = tlp.Color(160,160,160, 255)
        viewColor[mn] = steel # default color
        # immediately erase incident edges
        for e in csg.getInOutEdges(mn):
            csg.delEdge(e)
        edgebox = {} # a dict of lists of edges incident to the original nodes. The latter are used as keys.
        colors = []
        for n in ssg.getNodes():
            anns += annotations_count[n]
            if viewColor[n] not in colors:
                colors.append(viewColor[n])
            for e in og.getInOutEdges(n):
                the_source = og.source(e)
                the_target = og.target(e)
                if the_source not in ssg:
                    incident = the_source
                else:
                    if the_target not in ssg:
                        incident = the_target
                    else:
                        continue
                if incident not in edgebox: 
                    edgebox[incident] = [e]
                else:
                    edgebox[incident].append(e)
        annotations_count[mn] = anns
        if len(colors) == 1:
            viewColor[mn] = colors[0]
        for key in edgebox:
            print(name_en[key])
        print ('Edges in the box: ' + str(len(edgebox)))
        for n in edgebox: 
            newedge = csg.addEdge(n,mn) # each of these nodes induce an edge
            viewColor[newedge] = steel # default color
            co_occ = 0 # the three edge properties I want to populate
            num_con = 0
            conn = []
            colors = []
            for e in edgebox[n]:
                co_occ += cooccurrences[e]
                num_con += num_connectors[e]
                conn += connectors[e]
                if viewColor[e] not in colors:
                    colors.append(viewColor[e])
            if len (colors) == 1:
                viewColor[newedge] = colors[0]
            cooccurrences[newedge] = co_occ
            num_connectors[newedge] = num_con
            connectors[newedge] = conn
 
        # count the metanode's edges as a check
        mn_edges = 0
        for mne in csg.getInOutEdges(mn):
            mn_edges += 1
        print ('edges incident to the metanode: ' + str(mn_edges)) 
 
        return csg
        
    success = make_metanode('inequality 6')
  
