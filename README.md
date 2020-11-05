# Network Visualizations for Social Semantic Network Analysis on a Discourse forum


Beautiful, fast network representations of the conversation on online fora running Discourse. Made for https://edgeryders.eu. 

##  Content

* [What it does](#heading--what-does)
* [What you need](#heading--what-need)
* [Getting started](#heading--getting-started)
* [Repository structure](#heading--repo-structure)
* [How to use a Tulip perspective](#heading--use-perspective)
* [Create a social network graph](#heading--create-social-network)
* [Create a codes co-occurrence network graph](#heading--create-codes-network)
* [Dynamic visualizations with Gource](#heading--gource)


## <h2 id="heading--what-does">What it does</h2>

This software builds graph representations of an ethnographic corpus that lives as an online conversation in a [Discourse](https://discourse.org) forum. Such representations are maeant as tools for ethnographic analysis, and are part of a more general method called **Semantic Social Network Analysis (SSNA)**, described in [this paper](https://doi.org/10.1177%2F1525822X20908236). 

You can build two main types of network. 

1. A **social network of interaction** between people participating in the forum. Nodes represent forum users; edges (directed, weighted) represent replies to posts.
2. A **semantic network of co-occurrence** between ethnographic codes. Nodes represent codes; edges (undirected, weighted) connect codes that have been used to annotate the same post. 


## <h2 id="heading--what-need">What you need</h2>

In order to use this software, you need [Tulip](https://tulip.labri.fr/TulipDrupal/). If you want to work with graphs that encode semantics (ethnographic codes), there are two additional requirements. The first one is, of course, that the Discourse forum you are working on supports OpenEthnographer, and has API endpoints for ethnographic annotations and codes. The second one is an API key for the Discourse forum, as these endpoints are not public. We developed it  for [Edgeryders](https://edgeryders.eu), and in that case instructions on how to obtain an API key are [here](https://edgeryders.eu/t/using-the-edgeryders-eu-apis/7904).  

## <h2 id="heading--getting-started">Getting started</h2>

1. Download and unpack this repository. 
2. Download [Tulip](https://tulip.labri.fr/TulipDrupal/).
3. Rename the file `example_discourse_API_config.py` to `discourse_API_config.py`. 
4. Edit `discourse_API_config.py`, replacing the empty strings with the corresponding information relating to your Discourse site, working directory and API key. 


## <h2 id="heading--repo-structure">Repository structure</h2>

* To build a graph, load the Tulip perspective file corresponding to the graph you want; call its Python IDE; and execute the scripts therein as appropriate. 
* The `code` directory contains the two main Tulip perspectives, corresponding to social interaction networks and codes co-occurrence networks (see below).
* The `special cases` directory contains Tulip perspectives related to project-specific graphs. 
* The `python scripts` directory contains the python scripts. The scripts names start with a letter, sometimes a number, and an underscore, like this: `a1_scriptname`. The letter indicates the order of execution. The number indicates the type of network: `1` stands for the social network, `2` for the codes co-occrrence network. No number indicates that the script will work to build either network. 
* The file called `z_discourse_API_functions.py`is a Python module that contains functions to query the Discourse APIs. It is not meant to be executed, only imported in other scripts.


## <h2 id="heading--use-perspective">How to use a Tulip perspective</h2>

The main files are of a type called Tulip perspective (extension `.tlpx`). A Tulip perspective includes Python scripts, which are accessible by clicking on the Python IDE button on the left. Tulip perspectives contain the scripts themselves, the graph data, and some visualizations options. 

The perspectives used here start with an empty graph and some Python scripts. Running the first script loads live data from Discourse APIs and arrange them in graph form. After that, you can use Tulip to manipulate the graphs any way you want: the GUI provides plenty of options. We, however, found ourselves building visalizations in more or less always the same ways; so we automated the process of building them as a sequence of scripts for eact type of network. Each script provided here executes one step of that process. To work your way through the process, start with the leftmost script in the IDE and execute it. Then, move on to the next one to the right, and so on. 

At the top of the IDE window you will find a selector bar. Use it to choose which of the graphs you are working with your script should operate on. All scripts in this repository here have a comment at the very top, indicating what graph you should select befor runnign the script.

![selecting a graph on which to run the script](https://github.com/edgeryders/network-viz-for-ssna/blob/master/pictures/graph_select_bar.jpg)
![comment at the top of the script](https://github.com/edgeryders/network-viz-for-ssna/blob/master/pictures/comment_top.jpg)

Note: if the IDE loads empty, that's an elusive bug. Click on the `Load` button and load the scripts from the `python scripts` directory.

## <h2 id="heading--create-social-network">Create a social network graph</h2>

![social network graph](https://github.com/edgeryders/network-viz-for-ssna/blob/master/pictures/social_network_3_categories.png)

The `social network` Tulip perspective allows you to create a social network representation of categories ("cats") or tags in Discourse fora. Nodes represent people, edges represent replies. "Alice links to Bob" means "Alice has written a reply to one of Bob's posts". The resulting graph is directed and unweighted.

Categories are stored as subgraphs of the root graph. The root graph has no mathematical or social meaning, it is just a dataset. 

You can include as many categories or Discourse tags as you want as you want. The scripts control for double counting, so that node identity is preserved. In other words, if a user participates in discussion in more than one category, she is still represented in the graph as *a single* node. However, this node is part of more than one category subgraphs. To do this:

1. Call the Python IDE and select the first script, `a1_build_social_network.py`. 
2. Scroll to the end. If you are working with Discourse categories, add their names in the `cats` list. If you are working with tags, add their names in the `tags` list. 
3. Run the script.
4. Use the edge stacking script to generate a weighted graph of each category. An edge of weight N in the weighted graph means "Alice has written replies to N of Bob's posts". When you run the edge stacking script, the original unstacked graph and the stacked subgraph are stored into subgraphs of the category subgraph, so as sub-subgraphs of the root. In this case, the category subgraph loses mathematical and social meaning, whereas the two sub-subgraph, called "stacked" and "unstacked", preserve their interpretation as described above. 
5. Use the collating script creates a subgraph starting from the stacked subgraphs of all categories. This represent the social network of several categories in your Discourse forum. It is useful to check how different conversations are socially intertwined, in the sense that different (but possibly partially overlapping) communities form around each category. 
6. Use the included layout and node-coloring scripts to obtain results like the figure above. The latter is useful to visually represent the communities around the different categories. 

Summary information on each category harvested is printed to the console and also saved to a logfile, graphBuildLog.txt. The format output is:

	wellbeing
	Contributors: 240
	Contributions: 2223 in 420 topics, with 396K words
	Executed in 0:11:14.846379

## <h2 id="heading--create-codes-network">Create a codes co-occurrence network graph</h2>

![codes co-occurrence graph](https://github.com/edgeryders/network-viz-for-ssna/blob/master/pictures/codes_co-occurrence_network.png)

The `co_occurrence_network` Tulip perspective allows you to create a network representation of the semantics of your Discourse conversation. Nodes represent codes; edges connect codes that have been used to annotate the same post. To build it:

1. Call the Python IDE and select the first script, `a2_build_forum_net.py`. 
2. Scroll to the end. In the line `success = make_ccn_from_tag('ethno-poprebel')` replace `ethno-poprebel` with the Discourse tag that indicates your projects.
3. Run the script. 
4. Use the edge stacking script to generate a weighted graph of each category. An edge of weight `k` in the weighted graph means "*both* code A and code B have been used to annotate `k` posts in the corpus". We interpret higher Ns as the signature of stronger association. When you run the edge stacking script, the original unstacked graph and the stacked subgraph are stored into subgraphs of the root. In this case, the category subgraph loses mathematical and social meaning. 
5. To facilitate the interpretation of the codes co-occurrence network by human analysts, it may be useful to discard weaker connections between codes (edges with lower values of `k`). To do this, run the `levels_of_k` script, then select a readable graph. This generates a subgraph of the stacked graph for each level of `k`. You can then switch back and forth between them. High levels of `k` yield smaller, more legible graphs that focus on the strongest associations. Low levels of `k` preserve more of the richness of the original corpus.
5. Use the layout script provided to create results like the one below. Brighter edges correspond to higher-`k` edges. 



## <h2 id="heading--gource">Dynamic visualizations with Gource</h2>

The Python module contains functions that generate a custom log file compatible with [Gource](https://gource.io). You can use it to generate videos like [this](https://youtu.be/0uYQZbfFmlA). Refer to the documentation string in each function. 




