
import course_ret as pt
from flask import Flask, request, redirect, render_template
#del course_search 
app = Flask(__name__)

search_results = []
inverted_index = {}

@app.route('/')
def hello_world():
    return render_template('index.html')
    print("This function works")


#Getting the search query
@app.route('/search', methods = ['POST'])
def search():
    query = request.form['searchInput']
    print("The search is '" + query + "'")

    #Understanding attributes
    print (dir(pt))

    pt.combining_results(query)
    #search_results = pt.search_input(inverted_index, query)
    #search_results = course_search.search_input(inverted_index, query)
    #print(search_results)
    return redirect('/')

if __name__ == "__main__":
    app.run()