'''
In Discourse:

- All contributions are called 'posts', whether they start a thread or not.
- Forum threads are called 'topics'
- Topics belong to 'categories'.
- The response to a GET call on posts returns the id of the topic that the post belongs to.
- The same response also contain and indication of the parent post.
- The response to a GET call on topic returns the id of the category that the topic belongs to.

- a call of the kind https://discourse.example.com/t/{topic_id}.json returns the whole topic, with all its posts

'''

import requests
import datetime
import time
import sys
import textwrap
import discourse_API_config as cng # your API key goes in this file to access non-public data
API_key = cng.API_key
baseUrl = cng.baseUrl


def fetch_category_names():
  '''
  (None) => list of str
  return a list of categories by name
  '''
  if API_key != '':
    call = 'https://edgeryders.eu/categories.json?api_key=' + API_key
  else:
    call = 'https://edgeryders.eu/categories.json'  
  
  
  
  print ('Fetching category names...')
  cats = [] # the accumulator 

  
  response = requests.get(call)
  allCats = response.json()
  catList = allCats['category_list']['categories'] # this is a list of dicts
  for cat in catList:
    cats.append(cat['slug']) # cat names may return errors when called through APIs (upper case letters, spaces...)
  return cats

  

def fetch_category_ids(name, exceptionNames = []):
    '''
    (str, list of str) => list of dicts
    calls the discourse APIs. It returns a list of all categories and their subcategories, in the form
    
    [ {category_id: 46; category_slug: "parentCategoryName/subcategoryName"}, ...]
    
    Take out exceptionNames (subcategories that we do not need, like 'OpenCare Research')
    Tests OK
    '''
    if API_key != '':
        call = 'https://edgeryders.eu/categories.json?api_key=' + API_key
    else:
        call = 'https://edgeryders.eu/categories.json'         
    
    print ('Fetching category ids...')
    cats = [] # the accumulator 
    exceptCats = [] # the accumulator for the exceptions

    call = 'https://edgeryders.eu/categories.json?api_key=' + API_key
    response = requests.get(call)
    allCats = response.json()
    catList = allCats['category_list']['categories'] # this is a list of dicts

    # now grab the categories themselves and their subcategories
    for cat in catList:
        if cat['name'] == name:
            catItem ={} # the element to append to the accumulator. It takes the form {category_id: slug}
            catItem['id'] = cat['id'] 
            catItem['slug'] = cat['slug']
            cats.append(catItem) # adding the dict of the specified category, like 'OpenCare'
            if cat['subcategory_ids']:
                for subcat in cat['subcategory_ids']:
                    catItem2 = {} # the element to append to the accumulator. This time it refers to the subcategory
                    subcatCall = 'https://edgeryders.eu/c/' + str(subcat) + '/show.json'
                    time.sleep(3)
                    subcatResponse = requests.get(subcatCall)
                    subcatInfo = subcatResponse.json()
                    if subcatInfo['category']['name'] not in exceptionNames: # this takes care of the exceptions
                        catItem2['id'] = subcat
                        catItem2['slug'] = cat['slug'] + '/' + subcatInfo['category']['slug']
                        cats.append(catItem2) # adding the ids of all subcategories, like 'OpenInsulin' sub 'OpenCare'
                        
    print (str(len(cats)) + ' category ids retrieved.')           
    return cats

#####    

def fetch_topics_from_cat(cat):
    '''
    (str) => list of ints
    calls the discourse APIs. Accepts as an input the category name.
    It returns a single list of all topic ids in the categories we want. 
    '''    
    print('Reading category: ' + cat)
    print ('Fetching topic ids..')
    tops = [] # the accumulator. Entries take the form {topic_id: category_id}
    i = 0 #page counter
    topicList = ['something'] # to avoid breaking the while loop
    
    # the following loop continues until the page number becomes so high that the topicList is empty 
    while len(topicList) > 0:
        if API_key != '':
            call = 'https://edgeryders.eu/c/' + cat + '.json?page=' + str(i) + '&api_key=' + API_key
        else:
            call = 'https://edgeryders.eu/c/' + cat + '.json?page=' + str(i)        
        print ('Reading topics: page ' + str(i))
        time.sleep(.1)
        response = requests.get(call)
        catTopics = response.json()
        topicList = catTopics['topic_list']['topics']
        for topic in topicList:
            tops.append(topic['id'])
        # the following condition returns True if the page is less than full (<30 topics). It saves a call to an empty page.
        # But I still need the while condition, because the number of topics could be 0 modulo 30.
        if len(topicList) < 30: 
            break 
        i +=1     
    print (str(len(tops)) + ' topic ids retrieved.')    
    return tops
    
    
##### public posts only

def fetch_public_topics_from_cat(cat):
    '''
    (str) => list of ints
    calls the discourse APIs. Accepts as an input the category name.
    It returns a single list of all topic ids in the categories we want. 
    '''
    
    print ('Fetching topic ids..')
    tops = [] # the accumulator. Entries take the form {topic_id: category_id}
    i = 0 #page counter
    topicList = ['something'] # to avoid breaking the while loop
    
    # the following loop continues until the page number becomes so high that the topicList is empty 
    while len(topicList) > 0:
        call = cng.baseUrl + 'c/' + catSlug + '.json?page=' + str(i)
        print(call)
        print ('Reading topics: page ' + str(i))
        time.sleep(1)
        response = requests.get(call)
        catTopics = response.json()
        topicList = catTopics['topic_list']['topics']
        for topic in topicList:
            tops.append(topic['id'])
        # the following condition returns True if the page is less than full (<30 topics). It saves a call to an empty page.
        # But I still need the while condition, because the number of topics could be 0 modulo 30.
        if len(topicList) < 30: 
            break 
        i +=1     
    print (str(len(tops)) + ' topic ids retrieved.')    
    return tops

###########    
def fetch_public_tops_with_subcat_from_cat(cat, theMap = {}):
    '''
    (str) => list of dicts
    calls the discourse APIs. Accepts as an input the category name.
    It returns a single list of dicts. representing tops in the categories we want.
    The key is the topic id. The value is the cat ID.
    This is useful for excluding tops, for example in the workspace.
    '''
    # start by finding out the correct slug for the cat. to do this, I first create the map
    if map == {}:
        theMap =  make_categories_map()
    slug = find_cat_info(cat, theMap)['slug']
    print ('Fetching topic ids..')
    tops = [] # the accumulator. Entries take the form {topic_id: category_id}
    i = 0 #page counter
    topicList = ['something'] # to avoid breaking the while loop
    
    # the following loop continues until the page number becomes so high that the topicList is empty 
    while len(topicList) > 0:
        call = cng.baseUrl + 'c/' + slug + '.json?page=' + str(i)
        print ('Reading posts: page ' + str(i))
        time.sleep(.2)
        response = requests.get(call)
        catTopics = response.json()
        topicList = catTopics['topic_list']['topics']
        for topic in topicList:
            top = []
            top.append(topic['id'])
            top.append(topic['category_id'])
            tops.append(top)
        # the following condition returns True if the page is less than full (<30 topics). It saves a call to an empty page.
        # But I still need the while condition, because the number of topics could be 0 modulo 30.
        if len(topicList) < 30: 
            break 
        i +=1     
    print (str(len(tops)) + ' topic ids retrieved.')    
    return tops

##########

def fetch_topics_from_tag(tag):
    '''
    (str) => list of ints
    calls the discourse APIs. Accepts as an input a tag.
    It returns a single list of all topic ids in the categories we want.
    '''
    print ('Fetching topic ids..')
    tops = [] # the accumulator
    i = 0 #page counter
    topicList = ['something'] # to avoid breaking the while loop   
    # the following loop continues until the page number becomes so high that the topicList is empty 
    while len(topicList) > 0:
        call = baseUrl + 'tags/' + str(tag) + '.json?page=' + str(i)
        print ('Reading topics: page ' + str(i))
        time.sleep(.2)
        response = requests.get(call)
        tagTopics = response.json()
        topicList = tagTopics['topic_list']['topics']
        for topic in topicList:
            tops.append(topic['id'])
            # the following condition returns True if the page is less than full (<30 topics). It saves a call to an empty page.
            # But I still need the while condition, because the number of topics could be 0 modulo 30.
        if len(topicList) < 30: 
            break
        i += 1
    print (str(len(tops)) + ' topics retrieved.')    
    return tops
    
def fetch_posts_in_topic(id):
    '''
    (int) => list of dicts
    calls the Discourse APis. Returns a list of dicts in topic id. Each dict contains raw data in one post.
    It also contains the usernames of the source and the target of each post.
    When the target is not specified, we assume it to be the person who authored the first post in the topic.
    '''
    allPosts = [] # accumulator
    pageCounter = 1
    postList = ['something'] # need this as a condition to start the while loop
    while len(postList) > 0:
      time.sleep(0.05)
      if API_key != '':
          call = 'https://edgeryders.eu/t/' + str(id) + '.json?page=' + str(pageCounter) + '&include_raw=1' + '&api_key=' + API_key # the field "raw" is handy for word count, but not included by default.
      else:
          call = 'https://edgeryders.eu/t/' + str(id) + '.json?page=' + str(pageCounter) + '&include_raw=1' # the field "raw" is handy for word count, but not included by default.
      topic = requests.get(call).json()
      if 'post_stream' in topic:
          postList = topic['post_stream']['posts']
          print ('Reading ' + str(len(postList)) + ' posts from topic ' + str(id))
          for post in postList:
              if post['post_number'] == 1:
                  topic_author = post['username'] 
          for post in postList:        
              thisPost = {} # this becomes the item in the allPosts list
              thisPost['post_id'] = post['id']       
              thisPost['username'] = post['username']
              thisPost['user_id'] = post['user_id']
              thisPost['created_at'] = post['created_at']
              thisPost['raw'] = post['raw']
              thisPost['post_number'] = post['post_number']
              thisPost['reply_count'] = post['reply_count']       
              if post['reply_to_post_number'] == None:
                  thisPost['reply_to_post_number'] = 1
                  thisPost['target_username'] = topic_author
              else:
                  thisPost['reply_to_post_number'] = post['reply_to_post_number']
                  if 'reply_to_user' in post:
                    thisPost['target_username'] = post['reply_to_user']['username']
                  else:
                    thisPost['target_username'] = topic_author              
              allPosts.append(thisPost)
                    # before we move on, we use the "reply_to_post" reference, which refers to the in-topic post_number,
          # to add an "absolute" reference to the post_id of the parent post. Also add reference to the username of the author of the parent post.
          for item1 in allPosts:
               for item2 in allPosts:
                   if item1['reply_to_post_number'] == item2['post_number']:
                       item1['reply_to_post_id'] = item2['post_id']
          if len(postList) < 20: # if we have fewer than 20 posts, there can be no other page in the topic. No point making an empty call to the APIs, so...
            break
          else:
            pageCounter += 1

    else:
        print('there was a problem with topic ' + str(id))
    return allPosts
    
    
##### edgeryders consent function, see https://edgeryders.eu/u/johncoate.json

def check_consent(username):
    '''
    (str) => bool
    Returns True if username has passed the consent funnel.
    Documentation: https://edgeryders.eu/t/consent-process-manual/11904
    '''
    consent = False
    call = 'https://edgeryders.eu/u/' + username + '.json?api_key=' + API_key
    response = requests.get(call).json()
    if 'edgeryders_consent' in response['user']['custom_fields']:
        if str(response['user']['custom_fields']['edgeryders_consent']) == '1':
            consent = True
    return consent
    
        
def fetch_consenting():
  '''
  (None) => list
  Returns a list of users who gave consent for their content to be used in research
  '''   
  consenting = []
  call = 'https://edgeryders.eu/administration/annotator/users.json?api_key=' + API_key
  response = requests.get(call).json()
  for person in response:
    if person['edgeryders_consent'] == '1':
      consenting.append(person['username'])
  return consenting

def fetch_nonConsenting():
  '''
  (None) => list
  Returns a list of users who denied consent for their content to be used in research
  '''   
  API_key = '' # enter your Edgeryders API key here
  username = '' # Enter your Edgeryders username
  nonConsenting = []
  call = 'https://edgeryders.eu/administration/annotator/users.json?api_key=' + API_key
  response = requests.get(call).json()
  for person in response:
    if person['edgeryders_consent'] == '0':
      nonConsenting.append(person['username'])
  return nonConsenting  
  
def fetch_top_level_categories():
  '''
  (None) => list
  Returns a list of slugs of only the top-level cats (no parent cats)
  '''
  call = 'https://edgeryders.eu/site.json'
  response = requests.get(call).json()
  catList = []
  for cat in response['categories']:
    if 'parent_category_id' not in cat:
      catList.append(cat['slug'])
  return catList
  
def save_string(message, filename):
  '''
  (string, string) => None
  Append message to filename. If filename is not present, create it
  '''
  with open (filename, 'a+') as outfile:
    outfile.write(message + '\n')
    
def count_views_in_cat(cat):
    '''
    (string) => int
    Counts the number of views in a category
    '''
    counter = 0
    tops = fetch_topics_from_cat(cat) # this returns the topics IDs
    for top in tops:
        if API_key != '':
            call = 'https://edgeryders.eu/t/' + str(top) + '.json?api_key=' + API_key
        else:
            call = 'https://edgeryders.eu/t/' + str(top) + '.json'         
        response = requests.get(call).json()
        counter += response['views']
    return counter
    
def fetch_annos(tag = ''):
    '''
    (str) => list of dicts
    Return a list of annotations filtered by tag
    '''
    allAnnotations = []
    baseCall = 'https://edgeryders.eu/annotator/annotations.json?api_key=' + API_key
    if tag != '':
        baseCall = baseCall + '&discourse_tag=' + tag                    
    found = 100 # initializing like this to meet the WHILE condition the first time
    pageCounter = 1 
    while found == 100:
        print ('Now reading page ' + str (pageCounter))
        call = baseCall + '&page=' + str(pageCounter)
        response = requests.get(call).json()
        found = len(response)
        allAnnotations = allAnnotations + response
        pageCounter += 1        
    print ('Annotations found: ' + str(len(allAnnotations)))
    return allAnnotations
    
    
def fetch_codes():
    '''
    (list of dicts) => list of dicts
    the argument is a list of annotations, as returned from fetch_anno_from _posts. 
    Returns a list of dicts, each one containing the information about one code.
    High level: read all codes from the endpoint: https://edgeryders.eu/t/using-the-edgeryders-eu-apis/7904#heading--3-1
    Then iterate across the input annotations and store in a list the codes that refer to those annotations.
    '''
    allCodes = []
    baseCall = 'https://edgeryders.eu/annotator/codes.json?per_page=500&api_key=' + API_key
    found = 500 # initializing like this to meet the WHILE condition the first time
    pageCounter = 1 
    while found == 500:
        print ('Now reading page ' + str (pageCounter))
        call = baseCall + '&page=' + str(pageCounter)
        response = requests.get(call).json()
        found = len(response)
        allCodes = allCodes + response
        pageCounter += 1        
    print ('Codes found: ' + str(len(allCodes)))
    return allCodes
    
def fetch_codes_from_annos(annoList):
    '''
    (list of dicts) => list of dicts
    return the codes associated to a list of annotations
    '''
    # start by creating a list of all codes:
    codes = []
    checkCodes = [] # use this to make sure codes are only added once to codes
    allCodes = fetch_codes()    
    for anno in annoList:
        for code in allCodes:
            if code['id'] == anno['code_id'] and code['id'] not in checkCodes:
                codes.append(code)
                checkCodes.append(code['id'])
    return codes

def make_categories_map():
    '''
    (none) => dict of dicts
    the result had the form {catId: {'slug': catFullSlug, 'color': catColor}}
    A full slug includes the slug of the parent category, if any: 'parent_cat_slug/child_cat_slug'.
    ''' 
    print ('making a categories map. This may take a minute or so.')
    theMap = {}    
    call = cng.baseUrl + 'categories.json'
    top_level_categories = requests.get(call).json()['category_list']['categories']
    for topCat in top_level_categories:
        topCatInfo ={}
        topCatInfo['slug'] = topCat['slug'] # top level categories have no parent, so their slug is already complete
        topCatInfo['color'] = topCat['color']
        theMap[topCat['id']]  = topCatInfo 
        if topCat['has_children'] == True:
            try: # some subcats seem inaccessible 
                for subCat in topCat['subcategory_ids']:
                    call2 = cng.baseUrl + 'c/' + str(subCat) + '/show.json'
                    response = requests.get(call2).json()['category']
                    subCatInfo = {}
                    subCatInfo['slug'] = topCatInfo['slug'] + '/' + response['slug']
                    subCatInfo['color']= response['color']
                    theMap[subCat] = subCatInfo
            except KeyError:
                print ('Inaccessible sub-category. Id: ' + str(subCat))
    return theMap
    
def find_cat_info(cat, theMap):
    '''
    (str or int, dict) => dict}
    finds the info about a category stored in theMap. 
    We want the endpoint 'example.com/c/top-level-category/subcategory.json'
    the dict is a map made with make_categories_map(). It is quite slow, so better to run it once.
    '''
    # the slug of this cat
    if type(cat) == int:
        theInfo = theMap[cat]
    else:
        for key in theMap:
            if theMap[key]['slug'] == cat:
                theInfo = theMap[key]
        for key in theMap: # if  no slug is exactly the same as the cat's name, we are looking at a subcat
            if cat in theMap[key]['slug']:
                theInfo = theMap[key]
    return theInfo

def make_gource_file_from_cat(cat, theMap = {}):
    '''
    (str) => list
    writes a file digestible by Gource (https://gource.io/).
    See: https://edgeryders.eu/t/11905
    '''   
    if theMap == {}:
        theMap = make_categories_map()
    if type(cat) != int: # if the cat is called by name, get the int
        for key in theMap:
            if theMap[key]['slug'] == cat: 
                print ('the cat id is ' + str(key))
                catName = cat # preserving the name of the cat, so it goes on the filename
                cat = key # in this case, make the cat numeric
        
    tops = fetch_public_tops_with_subcat_from_cat(cat, theMap) # get the topics to go into the Gource viz
    gourceList = []
    for top in tops:
        # first, the part of the slug common to all posts in the same topic
        catInfo = find_cat_info(top[1], theMap)
        catSlug = catInfo['slug']
        catColor = catInfo['color']
        topSlug = catSlug + '/' + str(top[0])
        # now add the part of the slug that describes in-category threading
        posts = fetch_posts_in_topic(top[0]) #!! this function assigns value 1 to posts that have value 
        # Null to reply_to_post_id 
        ancestry = {} # I need a map to track which post is child to which. The map is specific to each topic
        for post in posts:
            s = post['created_at']
            timestamp = str(int(datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%s")))
            author = post['username']
            '''
            for each post in the topic, generate a slug that keeps track of the post's threading within the 
            topic, with the parent post's number to the left of the child post's. 1 is omitted For example
            {1: '', 2: '/2', 3: '/3', 4: '/3/4', 5: '/3/4/5'} and so on. 
            The rightmost number is always the post number in the topic.
            '''
            post_number = post['post_number']
            parent = post ['reply_to_post_number']
            post_text = textwrap.shorten(post['raw'], 30, placeholder="...")
            if post_number == 1 :
                slug = '/' + post_text
            elif post_number > 1 and parent == 1:
                ancestry[post_number] = 1
                slug = '/1/' + post_text 
            elif post_number == parent:
                continue
            else: 
                sluglist = []
                ancestry[post_number] = parent
                while parent > 1:
                    sluglist.append(str(parent))
                    if parent in ancestry:
                        parent = ancestry[parent]
                    else: # example, hidden reply, like post 22 in https://edgeryders.eu/t/open-source-coffee-sorter-project/7122
                        parent = 1 # breaks the while loop
                slug = ''
                for i in reversed(sluglist):
                    slug = slug + '/' + i 
                slug = slug + '/' + post_text
            gourceList.append(timestamp + '|' + author + '|A|' + topSlug + '/' + slug + '|' + str(catColor))
            if post['reply_count'] > 0: # the post does have children, take care of the post-as-directory
                if post_number == 1:
                    slug = '/1'
                elif post_number > 1 and parent == 1:
                    slug = '/1/' + str(post_number) 
                elif post_number == parent:
                    continue
                else: 
                    sluglist = []
                    ancestry[post_number] = parent
                    while parent > 1:
                        sluglist.append(str(parent))
                        if parent in ancestry:
                            parent = ancestry[parent]
                        else: # example, hidden reply, like post 22 in https://edgeryders.eu/t/open-source-coffee-sorter-project/7122
                            parent = 1 # breaks the while loop
                    slug = ''
                    for i in reversed(sluglist):
                        slug = slug + '/' + str(i) 
                    slug = slug + '/' + str(post_number)
                timestamp1 = str(int(timestamp) - 1) # this prevents the two entities representing the post appearing at exactly the same time in the log
                gourceList.append(timestamp1 + '|' + author + '|A|' + topSlug + slug + '|' + str(catColor))

    with open (cng.dirPath + 'gourcefile_' + catName + '.csv', 'w', encoding='utf-8-sig') as gourcefile:
        for item in sorted(gourceList):
            gourcefile.write(item + ',\n')
        print ('gourcefile_' + catName + '.csv saved at ' + cng.dirPath)
    return sorted(gourceList)
    
    
def make_gource_file_from_tag(tag, theMap={}):
    '''
    (str) => list
    writes a file digestible by Gource (https://gource.io/), starting with a tag or project.
    See: https://edgeryders.eu/t/11905
    High level:
    - have, or make, a disctionary mapping to category ID to category name and parent category name
    - grab all the topics with the tag. The tag endpoint contains the cat id. 
    - Use the map to discover the top's slug: topCatName/subCatName/topTitle
    - for each top, get posts and build the threading in the same way as make_gource_file_from_cat
    - each post with no replies becomes an entry in the accumulator list
    - each post with at least one reply becomes TWO entries, one as a post (.../post_number/raw) and one as a "directory"
      for the replies (.../post_number)
    '''
    if theMap == {}:
        theMap = make_categories_map()
    tops = fetch_topics_from_tag(tag)
    gourceList = []
    for top in tops:
        # first, the part of the slug common to all posts in the same topic
        # tops contains only topic IDs, I need to call them to get to the cat ID
        callTopic = baseUrl + 't/' + str(top) + '.json'
        cat_id = requests.get(callTopic).json()['category_id']
        catInfo = find_cat_info(cat_id, theMap)
        catSlug = catInfo['slug']
        catColor = catInfo['color']
        topSlug = catSlug + '/' + str(top)
        # now add the part of the slug that describes in-topic threading
        posts = fetch_posts_in_topic(top) #!! this function assigns value 1 to posts that have value 
        # Null to reply_to_post_id 
        ancestry = {} # I need a map to track which post is child to which. The map is specific to each topic
        for post in posts:
            s = post['created_at']
            timestamp = str(int(datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%s")))
            author = post['username']
            '''
            for each post in the topic, generate a slug that keeps track of the post's threading within the 
            topic, with the parent post's number to the left of the child post's. 1 is omitted For example
            {1: '', 2: '/2', 3: '/3', 4: '/3/4', 5: '/3/4/5'} and so on. 
            The rightmost number is always the post number in the topic.
            '''
            post_number = post['post_number']
            parent = post ['reply_to_post_number']
            post_text = textwrap.shorten(post['raw'], 30, placeholder="...")
            if post_number == 1 :
                slug = '/1/' + post_text
            elif post_number > 1 and parent == 1:
                ancestry[post_number] = 1
                slug = '/1/' + post_text 
            elif post_number == parent:
                continue
            else: 
                sluglist = []
                ancestry[post_number] = parent
                while parent > 1:
                    sluglist.append(str(parent))
                    if parent in ancestry:
                        parent = ancestry[parent]
                    else: # example, hidden reply, like post 22 in https://edgeryders.eu/t/open-source-coffee-sorter-project/7122
                        parent = 1 # breaks the while loop
                slug = ''
                for i in reversed(sluglist):
                    slug = slug + '/' + i 
                slug = slug + '/' + str(post_number) + post_text
            gourceList.append(timestamp + '|' + author + '|A|' + topSlug + slug + '|' + str(catColor))
            if post['reply_count'] > 0: # the post does have children, take care of the post-as-directory
                if post_number == 1:
                    slug = '/1'
                elif post_number > 1 and parent == 1:
                    slug = '/1/' + str(post_number) 
                elif post_number == parent:
                    continue
                else: 
                    sluglist = []
                    ancestry[post_number] = parent
                    while parent > 1:
                        sluglist.append(str(parent))
                        if parent in ancestry:
                            parent = ancestry[parent]
                        else: # example, hidden reply, like post 22 in https://edgeryders.eu/t/open-source-coffee-sorter-project/7122
                            parent = 1 # breaks the while loop
                    slug = ''
                    for i in reversed(sluglist):
                        slug = slug + '/' + str(i) 
                    slug = slug + '/' + str(post_number)
                timestamp1 = str(int(timestamp) - 1) # this prevents the two entities representing the post appearing at exactly the same time in the log
                gourceList.append(timestamp1 + '|' + author + '|A|' + topSlug + slug + '|' + str(catColor))

    with open (cng.dirPath + 'gourcefile_' + tag + '.csv', 'w', encoding='utf-8-sig') as gourcefile:
        for item in sorted(gourceList):
            gourcefile.write(item + ',\n')
        print ('gourcefile_' + tag + '.csv saved at ' + cng.dirPath)
    return sorted(gourceList)    
    
def join_csv_files(filelist):
    '''
    (list of str) => list of str
    loads several files of the smae formats, sorts them and saves them as one
    Used for generating gource-compatible files from Discourse
    '''
    theList = []
    for filename in filelist:
        with open (cng.dirPath + filename +'.csv', 'r') as inFile: 
            thisFileList = inFile.readlines()
            for line in thisFileList:
                theList.append(line)
    with open (cng.dirPath + 'joined-file.csv', 'w') as outFile:
        for item in sorted(theList):
            outFile.write(item)
        print ('joined-file.csv saved at ' + cng.dirPath)
        
if __name__ == '__main__':
    greetings = 'Hello world'
    print (greetings)
    # testing a function
    theMap = make_categories_map()
#    success = make_gource_file('workspaces', theMap)
#    topLevelCats = fetch_category_names()
#    theList = []
#    for cat in topLevelCats:
#        catGourceList = make_gource_file(cat, theMap)
#        theList.append(catGourceList)
#    with open (cng.dirPath + 'completeGourceLog.csv', 'w') as theFile:
#        for item in sorted(theList):
#            theFile.write(item + ',\n')
#        print ('completeGourceLog.csv saved at ' + cng.dirPath)
    success = make_gource_file_from_tag('cat2-societal-balances', theMap)
    
