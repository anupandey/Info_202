
import course_ret as pt
from flask import Flask, request, redirect, render_template, jsonify
#del course_search 
app = Flask(__name__)

search_results = []
inverted_index = {}

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/ajax', methods = ['GET','POST'])
def ajax_request():
    form_data = request.form
    form_data['searchText']
    pt.combining_results(form_data)
    #return jsonify({'data': form_data['searchText']})
    #return redirect('/result.html')
    return render_template('result.html')


#Getting the search query

#@app.route('/search', methods = ['POST'])
#def search():
    #query = request.form['searchInput']
    #print("The search is '" + query + "'")

    #lang = request.form['langSelected']
    #print("The language is '" + lang + "'")
    #Understanding attributes
    #print (dir(pt))

    #pt.combining_results(query)
    #search_results = pt.search_input(inverted_index, query)
    #search_results = course_search.search_input(inverted_index, query)
    #print(search_results)


    #return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)