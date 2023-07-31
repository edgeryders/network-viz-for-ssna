# run from the stacked
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
import functools

class Simmelian(object):
    '''
    computes the Simmelian backbone of a non-directed graph according to Bobo Nick's approach:
    Nick, B., C. Lee, et al. (2013). Simmelian Backbones: Amplifying Hidden Homophily in Facebook Networks.
    Advances in Social Network Analysis and Mining (ASONAM).

    Implements the non parametric version of edge redundancy (see paper for details).

    Uses an optional double property argument (that stores edge strength).
    '''
    def __init__(self, graph, strength_name_property=None):
        super(Simmelian, self).__init__()
        self.graph = graph
        self.strength_name_property = strength_name_property
        self.ranked_edges = {}
        self.rank_edges()
        self.edge_redundancy = self.graph.getLocalDoubleProperty('edge_redundancy')

    def compute_edge_strength(self, node):
        '''
        computes edge strength, if no double property is assigned
        edges are those incident to node
        (edge strength is not defined globally but locally to nodes)
        (see Bobo Nick's paper for details)
        '''
        if self.strength_name_property != None:
            self.edge_strength = self.graph.getDoubleProperty(self.strength_name_property)
            return
        self.strength_name_property = 'edge_strength'
        self.edge_strength = self.graph.getDoubleProperty(self.strength_name_property)
        for e in self.graph.getInOutEdges(node):
            ego = self.graph.source(e)
            alter = self.graph.target(e)
            ego_neighs = self.graph.getInOutNodes(ego)
            alter_neighs = self.graph.getInOutNodes(alter)

            mutuals = list(set(ego_neighs) & set(alter_neighs))
            # strength corresponds to the number of common neighbors
            self.edge_strength[e] = len(mutuals)

    def edge_compare(self, edge1, edge2):
        '''
        compares edges according to their strength
        -- used as a parameter function to sort edges

        edges are necessarily incident to a same node
        '''
        if self.edge_strength[edge1] > self.edge_strength[edge2]:
            return -1
        elif self.edge_strength[edge1] < self.edge_strength[edge2]:
            return 1
        else:
            return 0

    def rank_edges(self):
        for node in self.graph.getNodes():
            self.compute_edge_strength(node)
            edges = self.graph.getInOutEdges(node)
            self.ranked_edges[node] = sorted(edges, key=functools.cmp_to_key(self.edge_compare))

    def Jaccard(self, set1, set2):
        return float(len(set1.intersection(set2)))/float(len(set1.union(set2)))

    def incident_nodes(self, node, m):
        '''
        computes the set of incident vertices from m strongest ties attached to a node
        returns an ordered list of nodes
        '''
        incident_edges = self.ranked_edges[node][0:m]
        incident_nodes = []
        for e in incident_edges:
            if self.graph.source(e) == node:
                incident_nodes.append(self.graph.target(e))
            else:
                incident_nodes.append(self.graph.source(e))
        return incident_nodes

    def compute_edge_redundancy(self, max_rank, parametric=False):
        for e in self.graph.getEdges():
            ego = self.graph.source(e)
            alter = self.graph.target(e)

            ego_ranked_edges = self.ranked_edges[ego]
            alter_ranked_edges = self.ranked_edges[alter]

            if parametric:
                s_ego = set(self.incident_nodes(ego, max_rank))
                s_alter = set(self.incident_nodes(alter, max_rank))
                r = len(s_ego.intersection(s_alter))
            else:
                r = 0.0
                for k in range(1, max_rank + 1):
                    s_ego = set(self.incident_nodes(ego, k))
                    s_alter = set(self.incident_nodes(alter, k))
                    r = max(r, self.Jaccard(s_ego, s_alter))
            self.edge_redundancy[e] = r

    def simmelian_backbone(self, max_rank, redundancy_min_threshold):
        '''
        computes the Simmelian backbone according to a maximum rank for edges,
        that is redundancy will be computed but only for edges with rank below max_rank
        redundancy threshold x lies in [0, 1], and makes it so that only x% of edges
        are kept as part of the backbone
        '''
        parametric = True
        if redundancy_min_threshold >= 1.0:
            # parametric case
            min_redundancy = redundancy_min_threshold
            self.compute_edge_redundancy(max_rank, True)
        else:
            # non parametric, min_threshold in [0, 1]
            self.compute_edge_redundancy(max_rank, False)
            redundancy_values = sorted([self.edge_redundancy[e] for e in self.graph.getEdges()])
            min_redundancy = redundancy_values[int((1.0 - redundancy_min_threshold) * len(redundancy_values))]

        sg = self.graph.addCloneSubGraph()
        sg.setName('Simmelian_maxrank_' + str(max_rank) + '_redundancymin_' + str(min_redundancy))

        for e in self.graph.getEdges():
            # On retire les aretes dont le rang est trop eleve et/ou la redondance trop faible
            if self.edge_redundancy[e] < min_redundancy:
                sg.delEdge(e)
 

def filter1(prop,graph,threshold):
    print(graph.getName())
    viewLayout = graph['viewLayout']
    min_occur = []
    g_old = graph
    for i in range(threshold):
        g = graph.addCloneSubGraph()
        min_occur.append(prop.getEdgeMin(g_old))
        g_old = g
        print(prop.getName()," values to remove: ",min_occur)
        if min_occur[-1] < 10: ## I need this routing to shorten the names of graph, and still keep them sorted in the subgraphs list
            rValue = '00' + str(int(min_occur[-1]))
        elif min_occur >= 10 and min_occur < 100:
            rValue = '0' + str(int(min_occur[-1]))
        else: 
            rValue = str(int(min_occur[-1]))
        g.setName("r > "+ rValue)
        for e in g.getEdges():
            if(prop[e] in min_occur):
                g.delEdge(e)
        #remove nodes without edges
        for n in g.getNodes():
            if g.deg(n)==0:
                g.delNode(n)
        if g.numberOfNodes()==0:
            break
        #draw the graph
        ds = tlp.getDefaultPluginParameters("FM^3 (OGDF)",g)
        ds['new initial placement']=False
        ds['edge length property']=prop
        l = g.getLocalLayoutProperty("viewLayout")
        l.copy(viewLayout)
        g.applyLayoutAlgorithm("FM^3 (OGDF)", l, ds) 
        g.applyLayoutAlgorithm("Fast Overlap Removal", l)
        #m = g.getLocalDoubleProperty("viewMetric")      
        #ds2 = tlp.getDefaultPluginParameters("Louvain",g)
        #ds2 = tlp.getDefaultPluginParameters("Connected Component",g)
        #ds2['metric'] = num_connectors
        #g.applyDoubleAlgorithm("Louvain", m, ds2)
        #print(name, " => ", str(ds2['#communities']), " communities") 
        
        
def filter2(prop,graph,threshold):
    print(graph.getName())
    viewLayout = graph['viewLayout']
    min_occur = []
    g_old = graph
    for i in range(threshold):
        g = graph.addCloneSubGraph()
        min_occur.append(prop.getNodeMin(g_old))
        g_old = g
        print(prop.getName()," values to remove: ",min_occur)
        g.setName("removed "+str(min_occur))
        for n in g.getNodes():
            if(prop[n] in min_occur):
                g.delNode(n)
        if g.numberOfNodes()==0:
            break        
        #draw the graph
        ds = tlp.getDefaultPluginParameters("FM^3 (OGDF)",g)
        ds['new initial placement']=False
        ds['edge length property']=prop
        l = g.getLocalLayoutProperty("viewLayout")
        l.copy(viewLayout)
        g.applyLayoutAlgorithm("FM^3 (OGDF)", l, ds) 
        g.applyLayoutAlgorithm("Fast Overlap Removal", l)
        #m = g.getLocalDoubleProperty("viewMetric")      
        #ds2 = tlp.getDefaultPluginParameters("Louvain",g)
        #ds2 = tlp.getDefaultPluginParameters("Connected Component",g)
        #ds2['metric'] = num_connectors
        #g.applyDoubleAlgorithm("Louvain", m, ds2)

  

def main(graph):
    ancestry = graph['ancestry']
    annotations_count = graph['annotations_count']
    association_breadth = graph['association_breadth']
    code_id = graph['code_id']
    association_depth = graph['association_depth']
    creator_id = graph['creator_id']
    description = graph['description']
    name = graph['name']
    name_cs = graph['name_cs']
    name_de = graph['name_de']
    name_en = graph['name_en']
    name_pl = graph['name_pl']
    name_sr = graph['name_sr']
    num_connectors = graph['num_connectors']
    number_topics = graph['number_topics']
    parent_code = graph['parent_code']
    postDate = graph['postDate']
    post_id = graph['post_id']
    posts = graph['posts']
    topic_id = graph['topic_id']
    topics = graph['topics']
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
    
#    gl=[]
#    gl.append(graph.getRoot().getSubGraph("ethno-poprebel").getSubGraph("stacked"))
#    gl.append(graph.getRoot().getSubGraph("ethno-opencare").getSubGraph("stacked"))
#    gl.append(graph.getRoot().getSubGraph("ethno-ngi-forward").getSubGraph("stacked"))
    THRESHOLD=10
    #for g in graph.getSubGraphs():
#    print (graph.getName())
#    change the next line
    stacked = graph.getSubGraph('stacked')
  #  for g in gl:
#        sub = g.getSubGraph("association_breadth")
###    filter1(association_breadth,stacked,THRESHOLD)
        
  #  sub = graph.getSubGraph("association_depth")
###    filter1(association_depth,stacked,19)
        
#    sub = graph.getSubGraph("k-cores")
#    kcores=stacked.getLocalDoubleProperty("kcores")
#    stacked.applyDoubleAlgorithm("K-Cores", kcores)
#    filter2(kcores,stacked,80)
    
    sub = graph.getRoot().getSubGraph("german_interviews").getSubGraph("stacked").addSubGraph("simmelian") 
    stacked = graph.getRoot().getSubGraph("german_interviews").getSubGraph("stacked")
    print(type(sub))  
    edge_redundancy = stacked.getLocalDoubleProperty("edge_redundancy")
    print("Computing Simmelian backbone")
    adepth = sub.getDoubleProperty('association_depth')
    sb = Simmelian(stacked, 'association_depth')
    max_rank=72
    min_redundancy=1
    sb.simmelian_backbone(max_rank, min_redundancy)  
#        print("done")
    filter1(edge_redundancy,stacked.getSubGraph('Simmelian_maxrank_' + str(max_rank) + '_redundancymin_' + str(min_redundancy)),72)

