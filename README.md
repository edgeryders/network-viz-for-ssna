# discourse-social-networks
Beautiful, fast social network representations of the conversation on online fora running Discourse. Made for https://edgeryders.eu. 


## What you need

The main file is of a type called Tulip perspective. To use it, you will need to install Tulip from [here](https://tulip.labri.fr/TulipDrupal/). A Tulip perspective includes Python scripts, which are accessible by clicking on the Python IDE button.

## What it does

This Tulip perspective allows you to create a social network representation of categories ("cats") in Discourse fora. Nodes represent people, edges represent replies. "Alice links to Bob" means "Alice has written a reply to one of Bob's posts". The resulting graph is directed and unweighted.

Categories are stored as subgraphs of the root graph. The root graph has no mathematical or social meaning, it is just a dataset. 

You can include as many categories as you want. The scripts control for double counting, so that node indentity is preserved. In other words, if a user participates in discussion in more than one category, she is still represented in the graph as *a single* node. However, this node is part of more than one category subgraphs. 

You can use the edge stacking script to generate a weighted graph of each category. An edge of weight N in the weighted graph means "Alice has written replies to N of Bob's posts". When you run the edge stacking script, the original unstacked graph and the stacked subgraph are stored into subgraphs of the category subgraph, so as sub-subgraphs of the root. In this case, the category subgraph loses mathematical and social meaning, whereas the two sub-subgraph, called "stacked" and "unstacked", preserve their interpretation as described above. 

A collating script creates a subgraph starting from the stacked subgraphs of all categories. This represent the social network of several categories in your Discourse forum. It is useful to check how different conversations are socially intertwined, in the sense that different (but possibly partially overlapping) communities form around each category. 

Layout scripts are included.

A node-coloring script is also included. This is useful to visually represent the communities around the different categories. 

Summary information on each category harvested is printed to the console and also saved to a logfile, graphBuildLog.txt. The format output is:

	wellbeing
	Contributors: 240
	Contributions: 2223 in 420 topics, with 396K words
	Executed in 0:11:14.846379


## API calls

Discourse comes with a full suite of JSON APIs. The first script in the Tulip perspective, called `10_build_network_from_cats.py`, accesses APIs by calling functions that are contained in another one of the scripts, `90_discourse_API_functions.py`. These functions call Edgeryders APIs: of course, you should replace the edgeryders.eu URLs in the functions module with the URLs of your own Discourse site.

## API keys

Discourse supports protected categories, invisible to users who have not been explicitly authorized. To access these, you will need (1) an account with the Discourse website that you want to harvest and (2) an API key associated to your username. Site admins can issue you with an API key. 