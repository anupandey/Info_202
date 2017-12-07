import time
import course_ret as pt
import json
from flask import Flask, request, redirect, render_template, jsonify

app = Flask(__name__,static_url_path="/static")

search_results = []
inverted_index = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def showData():
    result = request.form['query']
    query = json.loads(result)
    print(query)
    pt.combining_results(query)
    time.sleep(3)  
    return render_template('result.html', title = "Kaush")

if __name__ == "__main__":
    app.run(debug=True)