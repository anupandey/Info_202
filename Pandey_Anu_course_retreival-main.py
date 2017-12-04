


import numpy as np
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from sklearn import feature_extraction

from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from itertools import chain
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.model_selection import train_test_split


courses= pd.read_csv("courses_list_final.csv")

#courses['Title'] = courses['Title'].dropna()

courses.head()
#len(courses)



title_list= courses['Title'].tolist()
title_list[:5]



from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

ps = PorterStemmer() #for stemming - taking care of mistakes etc.
stopWords = set(stopwords.words('english')) #set of stop words 

#making inverted index for titles - we can't apply cosine similarity due to less number of items- 
#cosine similarity does not gave very low similarity indexes
def makeInvertedIndex(strlist):
    inverted_index = {}
    for index, item in enumerate(strlist):
        words = item.split(' ') #['hello','world']
        for word in words:
            if word not in stopWords:#taking care of stop words
                word = ps.stem(word)#Doing stemming
                doc_set = inverted_index.get(word.lower(), set())
                doc_set.add(index)
                inverted_index[word.lower()] = doc_set
            
    return inverted_index

inverted_index = makeInvertedIndex(title_list)




def orSearch(invertedIndex, query):
    result_set= set()
    for item in query:
        if item not in stopWords:
            item = ps.stem(item)
            doc_set = invertedIndex.get(item.lower(), set())
            result_set = result_set.union(doc_set)
        
    return result_set

orSearch(inverted_index, ['machine', 'structure'])




def andSearch(invertedIndex, query):
    result_set= set()
    for item in query:
        if item in stopWords:
            query.remove(item)
    
    for index,item in enumerate(query):
        item = ps.stem(item)
        doc_set = invertedIndex.get(item.lower(), set())
        if index == 0:
            result_set = doc_set
        else:
            result_set = result_set.intersection(doc_set)
        
    return result_set


andSearch(inverted_index, ['machine', 'structure'])




def search_input(inverted_index, query):
    words = word_tokenize(query)
    
    doc_ids = list(andSearch(inverted_index, words))
    doc_ids.extend(list(orSearch(inverted_index, words)))
    
    search_results = []
    for id in doc_ids:
        course_info = courses.loc[id]
        course_dict = course_info.to_dict()
        course_converted_dict = {}
        for key, value in course_dict.items():
            try:
                course_converted_dict[key] = np.asscalar(value)
            except AttributeError:
                course_converted_dict[key] = value
        search_results.append(course_converted_dict)
    #right now- our results is dispalyed in a manner that lists 'and' queries first followed by "or" queries 
    #this is useful for presenting ranked response
        
    return search_results
    
search_results = search_input(inverted_index, 'machine structures')
print(len(search_results))




# Filter search_results by ShortDuration
def filter_result_by_shortduration(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:ShortDuration']:
            filtered_search_results.append(search_result)
    return filtered_search_results

#filtered_search_results = filter_result_by_shortduration(search_results)
#print(filtered_search_results)




# Filter search_results by free courses
def filter_result_by_free_courses(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:Free']:
            filtered_search_results.append(search_result)
    return filtered_search_results
#filtered_search_results = filter_result_by_shortduration(search_results)
#print(len(filtered_search_results))



# Filter search_results by ShortDuration
def filter_result_by_highworkload(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:HighWorkload']:
            filtered_search_results.append(search_result)
    return filtered_search_results



# Filter search_results by enrollment
def filter_result_by_enrollment(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:Enroll']:
            filtered_search_results.append(search_result)
    return filtered_search_results



# Filter search_results by self pace
def filter_result_by_selfpace(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:Self Paced Courses']:
            filtered_search_results.append(search_result)
    return filtered_search_results


# Filter search_results by rating
def filter_result_by_highrating(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:HighRating']:
            filtered_search_results.append(search_result)
    return filtered_search_results



# Filter search_results by enrollment
def filter_result_by_language(search_results, language='English'):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:%s' %(language)]:
            filtered_search_results.append(search_result)
    return filtered_search_results


# Filter search_results by institute and provider
def filter_result_by_institute(search_results, institute='Coursera'):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:Offered by %s' %(institute)]:
            filtered_search_results.append(search_result)
    return filtered_search_results



#Filter search_results by paid certifcation
def filter_result_by_paid_certification(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:PaidCertification']:
            filtered_search_results.append(search_result)
    return filtered_search_results



search_results = search_input(inverted_index, 'github machine')
search_results = filter_result_by_highworkload(search_results)
#print(len(search_results))
#print(search_results)




search_results = filter_result_by_paid_certification(search_results)

search_results = filter_result_by_institute(search_results, 'Coursera')

#To query with - edX, Udacity, FutureLearn,Stanford University,NPTEL,gacco,Microsoft,Georgia Institute of Technology,Massachusetts Institute of Technology
#To query with -'University of California, Berkeley', 'University of Washington' , 'University of Michigan','Google', 



search_results = filter_result_by_shortduration(search_results)


search_results = filter_result_by_free_courses(search_results)


search_results = filter_result_by_language(search_results,'English')


search_results = filter_result_by_enrollment(search_results)


search_results = filter_result_by_selfpace(search_results)


search_results = filter_result_by_highrating(search_results)




import json
def clean_json(search_results):
    # converting our output to json format

    # Removing f: keys for cleaner display to %%HTML
    clean_search_results = []
    for item_dict in search_results:
        new_item_dict = {}
        for key,value in item_dict.items():
            if 'f:' not in key:
                new_item_dict[key] = value
            
        clean_search_results.append(new_item_dict)

    json_str = json.dumps(clean_search_results)
    return json_str



#print(clean_json(search_results))

#applying cosine similarity in descriptions

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cosine_similarity_description(doc_id=0, total_ranks=5):
    tfidf = TfidfVectorizer().fit_transform(courses['Description'].values.astype('U'))
    cosine_similarities = cosine_similarity(tfidf[doc_id], tfidf).flatten()
    
    total_ranks = int(0 - total_ranks - 1)
    most_similar_courses = cosine_similarities.argsort()[:total_ranks:-1]

    search_results=[]
    for id in most_similar_courses:
        course_info = courses.loc[id]
        course_dict = course_info.to_dict()
        course_converted_dict = {}
        for key, value in course_dict.items():
            try:
                course_converted_dict[key] = np.asscalar(value)
            except AttributeError:
                course_converted_dict[key] = value
        search_results.append(course_converted_dict)

    return search_results

search_results = cosine_similarity_description(0,5)


#dispplay clean output for serach results
print(clean_json(search_results))


