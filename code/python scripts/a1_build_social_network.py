'''
Run this to build the graph on live data from the new discourse platform
Scroll to the end of the script to add a list of categories that you want the social network of,
then run the script

Blocks:

=> There are two functions:
   => build_graph_from_cats takes as an argument a list of cats
   => build_graph_from_tags takes as an argument a list of tags
   both start by calling functions in the discourse_API_functions moduleand return lists of dicts
   encoding topics, of the form [{topic_id: category_id}] 
=> Next, the scripts go through the items of the list and invoke another function to read all posts in that cat.
=> Finally, they process each post to instantiate an edge, creating the nodes as needed
'''

import sys ## remember to delete this 
sys.path.append('/Users/albertocottica/Documents/Edgeryders the company/Make networks here/make social networks') 

from tulip import *
import time
import datetime
import z_discourse_API_functions as api
start_script = datetime.datetime.now()

from tulip import tlp

# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# The main(graph) function must be defined 
# to run the script on the current graph

def main(graph): 
  viewBorderColor = graph.getColorProperty("viewBorderColor")
  viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
  viewColor = graph.getColorProperty("viewColor")
  viewFont = graph.getStringProperty("viewFont")
  viewFontSize = graph.getIntegerProperty("viewFontSize")
  viewIcon = graph.getStringProperty("viewIcon")
  viewLabel = graph.getStringProperty("viewLabel")
  viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
  viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
  viewLabelColor = graph.getColorProperty("viewLabelColor")
  viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
  viewLayout = graph.getLayoutProperty("viewLayout")
  viewMetric = graph.getDoubleProperty("viewMetric")
  viewRotation = graph.getDoubleProperty("viewRotation")
  viewSelection = graph.getBooleanProperty("viewSelection")
  viewShape = graph.getIntegerProperty("viewShape")
  viewSize = graph.getSizeProperty("viewSize")
  viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
  viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
  viewTexture = graph.getStringProperty("viewTexture")
  viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
  viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")

  # initialize custom properties
  user_name = graph.getStringProperty('user_name')
  user_id = graph.getIntegerProperty('user_id')
  created_at = graph.getStringProperty('created_at')
  wordCount = graph.getDoubleProperty('wordCount')
  post_id = graph.getIntegerProperty('post_id')
  category_id = graph.getIntegerProperty('category_id')
  
  def build_graph_from_cats(catList):
      '''
      (list of str) => None
      go through the cats in catList and build ONE network from all of them.
      useful to build a network from one top-level cat, excluding one or more subcats (eg. workspace)
      '''
  
      logfile = '/Users/albertocottica/public folder/graphBuildLog.txt' # my log file
      success = api.save_string(str(datetime.date.today()), logfile)
      for cat in catList:
          fest = graph.addSubGraph(cat)
          success = api.save_string(cat, logfile)
          specialUsers = {'Alberto': 0, 'Nadia': 0, 'Noemi': 0} # keeping track of special users, like community managers
          involved = {}
          allPosts = {} # accumulator of the form {topic:[post0, post1...]}
          numTopics = 0
          numContributions = 0
          words = 0
          nodeMap = {}
          topics = api.fetch_public_topics_from_cat(cat) # replace with the public_topics function for displaying only the graph of public interactions
          for topic in topics:
              numTopics += 1
              allPosts[topic] = []
              topicPosts = api.fetch_posts_in_topic(topic)
              for post in topicPosts:
                  numContributions += 1
                  allPosts[topic].append(post)  
                  words += len(post['raw'].split())
                  author = post['username']
                  if author in specialUsers:
                    specialUsers[author] += 1
                  if author not in involved:
                      involved[author] ={'username': author, 'user_id': post['user_id']}
          print (str(len(involved)) + ' unique participants in the added convo')
              
          extant_nodes = {} # build a map of already existing nodes, to keep track of who is who
          for n in graph.getNodes():
            name = user_name.getNodeStringValue(n)
            extant_nodes[name] = n
          print (str(len(extant_nodes)) + ' nodes in the map')
    
          # build the network. Add nodes first 
          # if the node already exists, it is added only to the subgraph 
          counter1 = 0
          counter2 = 0
          for person in involved:
            if person in extant_nodes:
              n = extant_nodes[person]
              fest.addNode(n)
              nodeMap[person] = n
              counter1 += 1
            else:
              n = fest.addNode()
              graph.setNodePropertiesValues(n, {'user_name': involved[person]['username'], 'user_id':involved[person]['user_id'] })
              nodeMap[person] = n
              counter2 += 1
          print (str(counter1) + ' nodes added from map')
          print (str(counter2) + ' nodes added ex novo')
          # for edges, iterate on allPosts. Within each topic, each post is either a response the post stored in the 'reply_to_user' field.
          # if reply_to_post_number = null, the post is considered a reply to the first post in the topic.
          print ('Adding edges...')
          for topic in allPosts:
            threadPosts = allPosts[topic]
            for post in threadPosts: # this is a list, corresponding to 'posts-stream'
              if post['post_number'] == 1:
                topicStarter = post['username']
              source = nodeMap[post['username']]
              if 'reply_to_user' in post:
                target = nodeMap[post['reply_to_user']]
              else:
                target = nodeMap[topicStarter] # if no user was specified as target, we assume the comment is directed to the initiator of the thread
              e = fest.addEdge(source, target)
              graph.setEdgePropertiesValues(e, {'wordCount':words, 'created_at':post['created_at']})
          message1 = 'Contributors: ' + str(len(involved))
          print (message1)
          api.save_string(message1, logfile)
          message2 = 'Contributions: ' + str(numContributions) + ' in ' + str(numTopics) + ' topics, with ' + str(words/1000) + 'K words'
          print (message2)
          api.save_string(message2, logfile)
          print ('Adding nodes...')
          end_script = datetime.datetime.now()
          running_time = end_script - start_script
          message3 = ('Executed in ' + str(running_time))
          print(message3)
          api.save_string(message3 +'\n', logfile)
      return None
          
  def build_graph_from_tags(tagList):
      '''
      (list of str) => None
      go through the tags in tagList and build ONE network from all of them.
      useful to build a network from one top-level cat, excluding one or more subcats (eg. workspace)
      '''
  
      logfile = '/Users/albertocottica/Documents/graphBuildLog.txt' # my log file
      for tag in tagList:
          fest = graph.addSubGraph(tag)
          success = api.save_string(tag, logfile)
          specialUsers = {'Alberto': 0, 'Nadia': 0, 'Noemi': 0} # keeping track of special users, like community managers
          involved = {}
          allPosts = {} # accumulator of the form {topic:[post0, post1...]}
          numTopics = 0
          numContributions = 0
          words = 0
          nodeMap = {}
          topics = api.fetch_topics_from_tag(tag) # replace with the public_topics function for displaying only the graph of public interactions
          for topic in topics:
              numTopics += 1
              allPosts[topic] = []
              topicPosts = api.fetch_posts_in_topic(topic)
              for post in topicPosts:
                  numContributions += 1
                  allPosts[topic].append(post)  
                  words += len(post['raw'].split())
                  author = post['username']
                  if author in specialUsers:
                    specialUsers[author] += 1
                  if author not in involved:
                      involved[author] ={'username': author, 'user_id': post['user_id']}
          print (str(len(involved)) + ' unique participants in the added convo')
              
          extant_nodes = {} # build a map of already existing nodes, to keep track of who is who
          for n in graph.getNodes():
            name = user_name.getNodeStringValue(n)
            extant_nodes[name] = n
          print (str(len(extant_nodes)) + ' nodes in the map')
    
          # build the network. Add nodes first 
          # if the node already exists, it is added only to the subgraph 
          counter1 = 0
          counter2 = 0
          for person in involved:
            if person in extant_nodes:
              n = extant_nodes[person]
              fest.addNode(n)
              nodeMap[person] = n
              counter1 += 1
            else:
              n = fest.addNode()
              graph.setNodePropertiesValues(n, {'user_name': involved[person]['username'], 'user_id':involved[person]['user_id'] })
              nodeMap[person] = n
              counter2 += 1
          print (str(counter1) + ' nodes added from map')
          print (str(counter2) + ' nodes added ex novo')
          # for edges, iterate on allPosts. Within each topic, each post is either a response the post stored in the 'reply_to_user' field.
          # if reply_to_post_number = null, the post is considered a reply to the first post in the topic.
          print ('Adding edges...')
          for topic in allPosts:
            threadPosts = allPosts[topic]
            for post in threadPosts: # this is a list, corresponding to 'posts-stream'
              if post['post_number'] == 1:
                topicStarter = post['username']
              source = nodeMap[post['username']]
              if 'reply_to_user' in post:
                target = nodeMap[post['reply_to_user']]
              else:
                target = nodeMap[topicStarter] # if no user was specified as target, we assume the comment is directed to the initiator of the thread
              e = fest.addEdge(source, target)
              graph.setEdgePropertiesValues(e, {'wordCount':words, 'created_at':post['created_at']})
          message1 = 'Contributors: ' + str(len(involved))
          print (message1)
          api.save_string(message1, logfile)
          message2 = 'Contributions: ' + str(numContributions) + ' in ' + str(numTopics) + ' topics, with ' + str(words/1000) + 'K words'
          print (message2)
          api.save_string(message2, logfile)
          end_script = datetime.datetime.now()
          running_time = end_script - start_script
          message3 = ('Executed in ' + str(running_time))
          print(message3)
          api.save_string(message3 +'\n', logfile)
      return None
      
#  cats = ['witness', 'earthos/scifi-economics']
#  build_graph_from_cats(cats) 
#    
  listOfTags = ['ethno-rebelpop-polska-interviews'] # replace this list with the list of categories you want 
  build_graph_from_tags(listOfTags)

