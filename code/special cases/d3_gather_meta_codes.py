'''
When dividing the edges by gender of the informant who expressed the associations, I leave out all codes
that are not used in any annotation. These are parent codes. 
This script stores parent codes in a separate subgraph for future use.
I also check that this graph has no co-occurrence edges (no annotations)
'''

from tulip import tlp

def main(graph):
    viewFontAwesomeIcon = graph['viewFontAwesomeIcon']
    wordCount = graph['wordCount']
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
    user_gender = graph['user_gender']
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
    
    def gather_meta_codes():
        '''
        (none) => Tulip subgraph
        returns a subgraph with the codes that are neither in the annotations of posts by females nor 
        in those of posts by males. These are the meta codes.
        '''
        mc = graph.addSubGraph('missing_codes')
        males = graph.getSubGraph('males')
        females = graph.getSubGraph('females')
        for n in graph.getNodes():
            orphan = True
            for n1 in males.getNodes():
                if n == n1:
                    orphan = False
                    break
            if orphan == True:
                for n2 in females.getNodes():
                    if n == n2:
                        orphan = False
                        break
            if orphan == True:
                mc.addNode(n)
                
        for n in mc.getNodes():
            for n1 in mc.getNodes():
                e = graph.existEdge(n1,n2, False)
                if e.isValid():
                    mc.addEdge(e)
        return mc
        
    def count_edges_by_subgraph(graph):
        '''
        (graph) => dict
        run from the supergraph of the stacked. 
        returns a dict containing a count of the edges that are in each stacked subgraph
        (except the collated!)
        '''
        # create a list of subgraph that we want to check the overlap of
        males = graph.getSubGraph('males')
        females = graph.getSubGraph('females')
        include = [males, females]
        results = {}
        for sg in include:
            results[sg.getName()] = 0
        results['shared'] = 0
        
        # first we do it from the perspective of males
        ms = males.getSubGraph('stacked')
        fs = females.getSubGraph('stacked')
        codes_ms = [] # a list of nodes for each gender, for quick checking
        codes_fs = []        
        
        for n in ms.getNodes():
            codes_ms.append(n)
        for n1 in fs.getNodes():
            codes_fs.append(n1)
        for e in ms.getEdges():
            source = ms.source(e)
            target = ms.target(e)
            if source in codes_fs and target in codes_fs:
                e1 = fs.existEdge(source, target, False)
                if e1.isValid():
                    results['shared'] += 1
                else:
                    results['males'] += 1
            else:
                results['males'] += 1
                
        # now females
        for e in fs.getEdges():
            source = fs.source(e)
            target = fs.target(e)
            if source in codes_ms and target in codes_ms:
                e1 = ms.existEdge(source, target, False)
                if e1.isValid():
                    pass # this is to avoid double counting of shared edges
                else:
                    results['females'] += 1
            else:
                results['females'] += 1
        return results
           
    success = count_edges_by_subgraph(graph)
    print(success)
