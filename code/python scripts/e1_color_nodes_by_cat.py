# run from the root graph

from tulip import tlp


def main(graph): 
  viewFontAwesomeIcon = graph.getStringProperty("viewFontAwesomeIcon")
  category_id = graph.getIntegerProperty("category_id")
  numComms = graph.getIntegerProperty("numComms")
  user_name = graph.getStringProperty("user_name")
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
  wordCount = graph.getDoubleProperty("wordCount")

  allCats = graph.getSubGraph('all langs Stacked') # was: all Cats Stacked
  mc = graph.getSubGraph('missing_codes')
  ignore = [allCats, mc]
  catGraphs = []
  for g in graph.getSubGraphs():
    if g not in ignore:
      catGraphs.append(g)
  print(catGraphs)

  blue = tlp.Color(102,204,255, 255)
  green = tlp.Color(51,255,204, 255)  
  red = tlp.Color(204,51, 0, 255)
  orange = tlp.Color(255, 153, 0, 255)
  steel = tlp.Color(160,160,160, 255) ## steel I keep for nodes that participate in more than one conversation
  colors = [green, orange, blue, red, steel] # need to add more colors
  for i in range(len(catGraphs)):
    for e in catGraphs[i].getEdges():
      viewColor[e] = colors[i]
  for n in graph.getNodes():
    viewColor[n] = steel # reset the color of nodes in case I have to run the script multiple times
  nodesFound = [] # accumulator for the nodes already processed
  for i in range(len(catGraphs)):
    counter = 0
    for n in catGraphs[i].getSubGraph('stacked').getNodes():
      if n not in nodesFound:
        viewColor[n] = colors[i]
        counter +=1
        nodesFound.append(n)
      else:
        viewColor[n] = steel

  # now count nodes by color:    

  for color in colors:
    counter = 0
    for n in graph.getNodes():
      if viewColor[n] == color:
        counter +=1
    print (str(color) + ': ' + str(counter))
  
