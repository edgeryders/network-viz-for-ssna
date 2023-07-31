# this script creates a subgraph for each level of b

def main(graph):
    ab = graph['association_breadth']
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
    

    stacked = graph.getSubGraph('composite b') # changed this to account for the different graph structure in this project
    # determine the maximum value of d
    dmax = 0
    for e in stacked.getEdges():
        if ab[e] > dmax:
            dmax = ab[e]
    # add a subgraph that is simply the copy of the stack (for better visualization)
    thecopy = stacked.addCloneSubGraph('b = 001')
    # add a subgraph for each value of k. Copy all edges with co-occurrences >= k
    # however, make sure that each subgraph you add is not exactly identical to the one you added previously 
    # we do this check by number of nodes
    oldNumNodes = stacked.numberOfNodes()
    for b in range(2,dmax):
        if b < 10: # neat ranking of subgraphs on the list
            sgname = 'b = 00' + str(b)
        elif b < 100:
            sgname = 'b = 0' + str(b)
        else:
            sgname = 'b = ' + str(b)
        sg = stacked.addSubGraph(sgname)
        for e in stacked.getEdges():
            if ab[e] >= b:
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
