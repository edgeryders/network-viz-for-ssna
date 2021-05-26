The root graph contains subgraphs pertaining to the three datasets: "ethno-PROJECTNAME". nodes are codes. edges represent co-occurrence on the same post (the property "post_id" on the unstacked edges encodes this). 

Each "ethno-PROJECTNAME" subgraph contains two subgraphs. "unstacked" is a clone of the pre-stacking graph. It contains many parallel edges, because each co-occurrence is instantiated in an edge. "stacked" is built from the former. It contains no parallel edges. If there are several co-occurrences between the same two codes (because they appear in more than one post), they are represented by a single edge. The property "co-occurrences" stores the number of posts on which the co-occurrence appears.


Notable properties of the stacked graphs are:

* "co-occurrences", already described above.
* "num_connectors". This stores the number of participants in the conversation that have authored posts on which the co-occurrence appears. It is built from the unstacked edge property "user_id". 
* "connectors". This is a vector property that stores all the user_ids behind a stacked edge. The length of the vector stored in this property is equal to the integer in "num_connectors".
* 