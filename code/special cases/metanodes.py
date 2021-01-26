'''
PSEUDO CODE
original graph (already stacked) => og
csg = og.cloneSubGraph('NAME OF OG')
ssg = og.getSubGraph (nodes acquired from selection or via hierarchy)
'''

mn = og.createMetaNode(ssg, False, False) # creates a disconnected metanode in og

edges_to_stack = {} # keys are nodes connected to any node in ssg. Values are a list of edges connecting those nodes to any node in ssg.
for n in ssg.getNodes():
    edges = []
    # found_edge  = find all incident edges
    n1 = og.source(found_edge)
    if n1 = n:
        n1 = og.target(found_edge)
    if n1 not in edges_to_stack:
        edges_to_stack[n1] = [found_edge]
    else:
        edges_to_stack[n1].append(found_edge)
for n in edges_to_stack:
    newEdge = og.addEdge(n, mn)
    # sum the property values in edges_to_stack[n] to populate the properties of NewEdge
    