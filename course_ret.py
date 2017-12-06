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
print(title_list[:5])

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
	print("Everything is going okay!")
	inverted_index = makeInvertedIndex(title_list)
	results_layer1 = {}
	results_layer1 = search_input(inverted_index,'artificial intelligence')
	filter_test = {}
	list_test = []
	for i in range(len(results_layer1)):
		filter_test['Title'] = results_layer1[i]['Title']
		filter_test['Subject'] = results_layer1[i]['Subject']
		list_test.append(filter_test)
	print(list_test)
	json_str = clean_json(list_test)
	print (json_str)

	#writing json data to file
	text_file = open("data.js", "w")
	text_file.write("var courses = ")
	text_file.close()
	with open('data.js', 'a') as outfile:
		#json.dump(json_str, outfile)
		outfile.write(list_test)

	#keys = ['Title', 'Subject']
	#filter_test = {x:results_layer1[x] for x in keys}
	#print(filter_test)




def combining_results(query):
	print(query)
