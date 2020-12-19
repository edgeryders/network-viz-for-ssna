# this script creates a subgraph for each level of kp (number of PEOPLE who made the connection), from 2 up. 
# run from the ethno-PROJECTNAME graph

def main(graph):
    cooc = graph['co-occurrences']
    nc = graph['num_connectors']
    code_id = graph['code_id']
    name = graph['name']
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
    
    stacked = graph.getSubGraph('stacked')
    # determine the maximum value of kp
    kpmax = 0
    for e in stacked.getEdges():
        if nc[e] > kpmax:
            kpmax = cooc[e]
    # add a subgraph that is simply the copy of the stack (for better visualization)
    thecopy = stacked.addCloneSubGraph('kp = 001')
    # add a subgraph for each value of k. Copy all edges with co-occurrences >= k
    # however, make sure that each subgraph you add is not exactly identical to the one you added previously 
    # we do this check by number of nodes
    oldNumNodes = stacked.numberOfNodes()
    for kp in range(2,kpmax):
        if kp < 10: # neat ranking of subgraphs on the list
            sgname = 'kp = 00' + str(kp)
        elif kp < 100:
            sgname = 'kp = 0' + str(kp)
        else:
            sgname = 'kp = ' + str(kp)
        sg = stacked.addSubGraph(sgname)
        for e in stacked.getEdges():
            if nc[e] >= kp:
                source = stacked.source(e)
                target = stacked.target(e)
                if source not in sg.getNodes():
                    sg.addNode(source)
                if target not in sg.getNodes():
                    sg.addNode(target)
                sg.addEdge(e)
        newNumNodes = sg.numberOfNodes()
        if newNumNodes == oldNumNodes:
            stacked.delSubGraph(sg)
        oldNumNodes = newNumNodes
