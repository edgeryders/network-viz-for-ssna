'''
## HIGH LEVEL ##

start from an already stacked graph.

1. load the gender CSV files, and create a dictionary mapping from user_id to gender
2. on the unstacked, use the dict to assign user_gender
3. on the stacked, we have a StringVectorProperty "connectors", that is a list of usernames.
   Instantiate a gender_balance DoubleProperty. Use the content of connectors to compute:
   number of female informants/number of informants
run the "assign gender to edges" script

'''
from tulip import tlp
import csv
import requests
import z_discourse_API_functions as api
dirPath = '/Users/albertocottica/Downloads/'
baseUrl = api.baseUrl
API_key = api.API_key


def complete_gender_info(filename):
    '''
    (str) => dict of the form {userid: gender}
    filename.csv contains rows of the form username, gender
    Loads the file; then queries Edgeryders APIs to find the user ID; 
    then builds and returns the dict.
    '''
    print('Retrieving gender info...')
    informants_gender = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            call = baseUrl + 'u/' + row['username'] + '.json'
            user = api.responses.get(call).json()
            try:
                user_id = user['user']['id']
                informants_gender[str(user_id)] = row['gender']
            except:
                print (call + ' not found.')
    print('Retrieved.')
    return informants_gender
    
    
def main(graph):
    ancestry = graph['ancestry']
    annotations_count = graph['annotations_count']
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
    parent_code = graph['parent_code']
    postDate = graph['postDate']
    post_id = graph['post_id']
    posts = graph['posts']
    topic_id = graph['topic_id']
    topics = graph['topics']
    unique_posts = graph['unique_posts']
    unixDate = graph['unixDate']
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
    
    def femPrev(e, data):
        '''
        (edge, dict) => float
        computes (number of times the association was made in the post of a female informants)
        /(total association depth)
        dict contains the data, in the form {user_id: 'gender'}
        '''
        femdepth = 0
        totdepth = 0
        theList = connectors[e]
        for item in theList:
            totdepth += 1
            if genderdata[item] in ['f', 'F'] :
                femdepth += 1
        if totdepth == 0:
            return 2
        else:
            return femdepth/float(totdepth)
        
    filename = '/Users/albertocottica/Downloads/polish_genders.csv'
    genderdata = complete_gender_info(filename)
    print('There are ' + str(len(genderdata)) + ' informants')
    print (genderdata)
    female_prevalence = graph.getDoubleProperty('female_prevalence')
    for e in graph.getEdges():
        female_prevalence[e] = femPrev(e, genderdata)
        
