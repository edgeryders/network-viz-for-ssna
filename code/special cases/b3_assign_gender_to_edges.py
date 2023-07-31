'''
This script takes a code co-occurrence network and adds to each edge information on the gender of the informant who has authored the contribution that originates the co-occurrence.
This information is written into an edge property.
I start from a codes co-occurrence network (unstacked)  a csv file containing usernames and their gender.
Run from the codes co-occurrence network.

After running the script, use Tulip's GUI to run EqualValue on the new property user_gender. 
Next, run the stacking script on each of the resulting graphs, and apply reduction on the stacked graphs as needed.
'''
from tulip import tlp
import csv
import requests
import z_discourse_API_functions as api
dirPath = '/Users/albertocottica/Downloads/'
baseUrl = api.baseUrl
API_key = api.API_key

# set a request session to be used in the whole script. This is now necessary after Discourse deprecated 
# authentication by passing parameters to the url. Read more: https://github.com/edgeryders/discourse/issues/245#issuecomment-657905349
#responses = requests.Session()
#responses.headers.update({"Api-Key": API_key})

def complete_gender_info(filename):
    '''
    (str) => dict of the form {userid: gender}
    filename.csv contains rows of the form username, gender
    Loads the file; then queries Edgeryders APIs to find the user ID; 
    then builds and returns the dict.
    '''
    informants_gender = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            call = baseUrl + 'u/' + row['username'] + '.json'
            user = responses.get(call).json()
            try:
                user_id = user['user']['id']
                informants_gender[user_id] = row['gender']
            except:
                print (row['name'] + ' not found.')
    return informants_gender
    
def main(graph):
    user_id = graph['user_id']
    user_gender = graph.getStringProperty('user_gender')
    
    filename = '/Users/albertocottica/Downloads/czech_genders.csv'
    genderdata = complete_gender_info(filename)
    print (len(genderdata))
    print(genderdata)
    for e in graph.getEdges(): 
        if int(user_id[e]) in genderdata:
            user_gender[e] = genderdata[int(user_id[e])]
        
