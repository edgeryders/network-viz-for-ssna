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
import time
import sys

def fetch_category_names():
  '''
  (None) => list of str
  return a list of categories by name
  '''
  username = '' # add your Edgeryders username to access non-public categories
  API_key = '' #add your Edgeryders API key to access non-public categories
  if API_key != '' and username != '':
    call = 'https://edgeryders.eu/categories.json?api_username=' + username + '&api_key=' + API_key
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
    username = '' # enter your Edgeryders username to access protected categories
    API_key = '' #enter your Edgeryders API key to access protected categories
    if API_key != '' and username != '':
        call = 'https://edgeryders.eu/categories.json?api_username=' + username + '&api_key=' + API_key
    else:
        call = 'https://edgeryders.eu/categories.json'         
    
    print ('Fetching category ids...')
    cats = [] # the accumulator 
    exceptCats = [] # the accumulator for the exceptions

    call = 'https://edgeryders.eu/categories.json?api_username=' + username + '&api_key=' + API_key
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
    username = '' # enter your Edgeryders username to access protected topics
    API_key = '' # enter your Edgeryders API key to access protected topics
    
    
    print('Reading category: ' + cat)
    print ('Fetching topic ids..')
    tops = [] # the accumulator. Entries take the form {topic_id: category_id}
    i = 0 #page counter
    topicList = ['something'] # to avoid breaking the while loop
    
    # the following loop continues until the page number becomes so high that the topicList is empty 
    while len(topicList) > 0:
        if API_key != '' and username != '':
            call = 'https://edgeryders.eu/c/' + cat + '.json?page=' + str(i) + '&api_username=' + username + '&api_key=' + API_key
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
        call = 'https://edgeryders.eu/c/' + cat + '.json?page=' + str(i)
        print ('Reading posts: page ' + str(i))
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
def fetch_public_tops_with_subcat_from_cat(cat):
    '''
    (str) => list of ints
    calls the discourse APIs. Accepts as an input the category name.
    It returns a single list of tuples. representing tops in the categories we want.
    The first element of each tuple is the topic id. The second one is the cat ID.
    This is useful for excluding tops, for example in the workspace.
    '''
    
    print ('Fetching topic ids..')
    tops = [] # the accumulator. Entries take the form {topic_id: category_id}
    i = 0 #page counter
    topicList = ['something'] # to avoid breaking the while loop
    
    # the following loop continues until the page number becomes so high that the topicList is empty 
    while len(topicList) > 0:
        call = 'https://edgeryders.eu/c/' + cat + '.json?page=' + str(i)
        print ('Reading posts: page ' + str(i))
        time.sleep(1)
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
        call = 'https://edgeryders.eu/tags/' + str(tag) + '.json?page=' + str(i)
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
    username = '' # add your Edgeryders username to access non-public posts
    API_key = '' #add your Edgeryders API key to access non-public posts
    if API_key != '' and username != '':
        call = 'https://edgeryders.eu/t/' + str(id) + '.json?page=' + str(pageCounter) + '&include_raw=1' + '&api_username=' + username + '&api_key=' + API_key # the field "raw" is handy for word count, but not included by default.
    else:
        call = 'https://edgeryders.eu/t/' + str(id) + '.json?page=' + str(pageCounter) + '&include_raw=1' # the field "raw" is handy for word count, but not included by default.     
        
    allPosts = [] # accumulator
    pageCounter = 1
    postList = ['something'] # need this as a condition to start the while loop
    while len(postList) > 0:
      time.sleep(0.1)
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
        
def fetch_consenting():
  '''
  (None) => list
  Returns a list of users who gave consent for their content to be used in research
  '''   
  API_key = '' # enter your Edgeryders API key here
  username = '' # Enter your Edgeryders username
  consenting = []
  call = 'https://edgeryders.eu/administration/annotator/users.json?api_key=' + API_key + '&username=' + username
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
  call = 'https://edgeryders.eu/administration/annotator/users.json?api_key=' + API_key + '&username=' + username
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
    API_key = '' # enter your Edgeryders API key here
    username = '' # Enter your Edgeryders username
    counter = 0
    tops = fetch_topics_from_cat(cat) # this returns the topics IDs
    for top in tops:
        if API_key != '' and username != '':
            call = 'https://edgeryders.eu/t/' + str(top) + '.json?username=' + username + '&API_key=' + API_key
        else:
            call = 'https://edgeryders.eu/t/' + str(top) + '.json'         
        response = requests.get(call).json()
        counter += response['views']
    return counter
        
            
if __name__ == '__main__':
    greetings = 'Hello world'
    print (greetings)
    # testing a function
    views = count_views_in_cat('earthos/the-reef')
    print(views)

