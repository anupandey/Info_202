"""
@author: Rohan Kapuria
"""
from flask import Flask, request, render_template
import analysis_interface
import plotgraphs as pt
# import gmplot

app = Flask(__name__,static_url_path="/static")

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/topskills.html', methods=['GET'])
def topskills():
    return render_template("topskills.html")

@app.route('/degreespez.html', methods=['GET'])
def degreespez():
    return render_template("degreespez.html")

@app.route('/pubcerti.html', methods=['GET'])
def pubcerti():
    return render_template("pubcerti.html")

'''
@app.route('/maps.html', methods=['GET'])
def maps():
    # heat_lats = [37.773972, 37.773972, 37.468319, 19.07283, 19.07283, 19.07283, 12.9716]
    # heat_longs = [-122.431297, -122.431297, -122.143936, 72.88261, 72.88261, 72.88261, 72.88261, 77.5946]
    # gmap = gmplot.GoogleMapPlotter.heatmap(heat_lats, heat_lngs)
    # gmap.draw("maps.html")
    return render_template("maps.html")
'''

@app.route('/', methods=['POST'])
def showData():
    role = request.form.get("roleSelected")
    #the function call to the plotgraphs.py file will go here. Please import the plotgraphs.py file here
    pt.plotting_publication(role)
    pt.plotting_highest_degree(role)
    pt.plotting_specialization(role)
    pt.plotting_certifications(role)
    # list = analysis_interface.skills_analysis(role)
    # return render_template("topskills.html", role=list)
    return render_template("topskills.html")