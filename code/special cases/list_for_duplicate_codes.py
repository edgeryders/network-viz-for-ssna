# Powered by Python 2.7
# To cancel the modifications performed by the script
# on the current graph, click on the undo button.
# Some useful keyboard shortcuts:
#   * Ctrl + D: comment selected lines.
#   * Ctrl + Shift + D: uncomment selected lines.
#   * Ctrl + I: indent selected lines.
#   * Ctrl + Shift + I: unindent selected lines.
#   * Ctrl + Return: run script.
#   * Ctrl + F: find selected text.
#   * Ctrl + R: replace selected text.
#   * Ctrl + Space: show auto-completion dialog.
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
def main(graph):
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

    codesList = []
    for n in graph.getNodes():
        if name_en[n] == '':
            if name_pl[n] == '':
                name_en[n] = name_cs[n]
            else:
                name_en[n] = name_pl[n]
        codesList.append(name_en[n])
        codesList.sort(key= str.lower)
        
    duplicates = []
    thiscode = 'some_text' # need to initialize it to something
    for item in codesList:
        if item == thiscode:
            duplicates.append(item)
        thiscode = item
    
    print(duplicates)
    print(len(duplicates))
##        
    codesListPL = []
    for n in graph.getNodes():
        if name_en[n] == '' and name_pl[n] != '':
            codesListPL.append(name_cs[n])
    codesListPL.sort(key = str.lower)
    for item in codesListPL:
        print(item)
    print len(codesListPL)

    import csv
    with open ('/Users/albertocottica/Downloads/nodeLabels.csv', 'w') as csvfile: 
        fieldnames = ['link', 'name_en', 'name_de', 'name_cs', 'name_pl']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for  n in graph.getNodes():
            row = {}
            row['link'] = 'https://edgeryders.eu/annotator/codes/' + str(code_id[n])
            row['name_en'] = name_en[n]
            row['name_de'] = name_de[n]
            row['name_cs'] = name_cs[n]
            row['name_pl'] = name_pl[n]
            writer.writerow(row)

