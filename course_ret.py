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

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

courses= pd.read_csv("courses_list_final.csv")

title_list= courses['Title'].tolist()

ps = PorterStemmer() #for stemming - taking care of mistakes etc.
stopWords = set(stopwords.words('english')) #set of stop words 


#inverted index
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

#inverted_index = makeInvertedIndex(title_list)


def orSearch(invertedIndex, query):
    result_set= set()
    for item in query:
        if item not in stopWords:
            item = ps.stem(item)
            doc_set = invertedIndex.get(item.lower(), set())
            result_set = result_set.union(doc_set)
        
    return result_set

#orSearch(inverted_index, ['machine', 'structure'])




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


#andSearch(inverted_index, ['machine', 'structure'])




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


if __name__ == "__main__":
    print("Things are going okay!")

    #keys = ['Title', 'Subject']
    #filter_test = {x:results_layer1[x] for x in keys}
    #print(filter_test)


# Filter search_results by enrollment
def filter_result_by_language(search_results, language):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:%s' %(language)]:
            filtered_search_results.append(search_result)
    return filtered_search_results


def filter_result_by_institute(search_results, institute):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:Offered by %s' %(institute)]:
            filtered_search_results.append(search_result)
    return filtered_search_results


def filter_result_by_shortduration(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:ShortDuration']:
            filtered_search_results.append(search_result)
    return filtered_search_results

def filter_result_by_highworkload(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:HighWorkload']:
            filtered_search_results.append(search_result)
    return filtered_search_results

def filter_result_by_enrollment(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:Enroll']:
            filtered_search_results.append(search_result)
    return filtered_search_results

def filter_result_by_paid_certification(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:PaidCertification']:
            filtered_search_results.append(search_result)
    return filtered_search_results

def filter_result_by_highrating(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:HighRating']:
            filtered_search_results.append(search_result)
    return filtered_search_results


def filter_result_by_selfpace(search_results):
    filtered_search_results = []
    for search_result in search_results:
        if search_result['f:Self Paced Courses']:
            filtered_search_results.append(search_result)
    return filtered_search_results

def filter_result_by_pricing(search_results, pricing):
    filtered_search_results = []
    if pricing == 'Free':
        for search_result in search_results:
            if search_result['f:Free']:
                filtered_search_results.append(search_result)
    else:
        for search_result in search_results:
            if not search_result['f:Free']:
                filtered_search_results.append(search_result)
    return filtered_search_results




def combining_results(query):

    #obtaining search criteria
    searchText = query['searchText']
    print(searchText)

    language = query['language']
    print(language)

    provider = query['provider']
    print(provider)

    institute = query['institute']
    print(institute)

    pricing = query['pricing']
    print(pricing)

    

    #print(query.items())
    #value = query['checkboxes[]']
    #print(value)


    inverted_index = makeInvertedIndex(title_list)
    if searchText != "":
        results_layer1 = search_input(inverted_index,searchText)
    else:
        print("Search is empty!")

    print("This is layer one : \n")
    #print (len(results_layer1))

    if language !="":
        results_layer2 = filter_result_by_language(results_layer1,language)
    else:
        results_layer2 = results_layer1
    

    if provider !="":
        results_layer3 = filter_result_by_institute(results_layer2,provider)
    else:
        results_layer3 = results_layer2


    if pricing != "":
        results_layer4 = filter_result_by_pricing(results_layer3, pricing)
    else:
        results_layer4 = results_layer3


    if institute !="":
        results_layer5 = filter_result_by_institute(results_layer4,institute)
    else:
        results_layer5 = results_layer4

    for key,value in query.items():
        print("kay" + key)
        print("values" + value)

    search_results = results_layer5

    for key,value in query.items():
        if(key == "shortduration"):
            search_results = filter_result_by_shortduration(search_results)
        if(key == "easy"):
            search_results = filter_result_by_highworkload(search_results)
        if(key == "enrollnow"):
            search_results = filter_result_by_enrollment(search_results)
        if(key == "paidcert"):
            search_results = filter_result_by_paid_certification(search_results)
        if(key == "rating"):
            search_results = filter_result_by_highrating(search_results)
        if(key == "pacing"):
            search_results = filter_result_by_selfpace(search_results)

    print(len(search_results))

    courses_str = "var courses = ["
    for result in search_results:
        courses_str += "{ Title: '" + result['Title'] + "' , Subject: '" + result['Subject'] + "' },"
    courses_str = courses_str[:-1] + "]"    
   
    #print(courses_str)

    #writing json data to file
    text_file = open("courses.js", "w")
    text_file.write(courses_str)
    text_file.close()
