from flask import Flask
from flask import request
from flask import render_template

from mainProcessor import *
app = Flask(__name__)

@app.route('/')
def my_form():
    return open("my-form.html").read()

@app.route('/<query>')
def queryService(query):
	#return query
	query = query.split("=")[1]
	print query
	mp = MainProcessor(query)
	result = "<br>Social Media Score: {} <br>Press Coverage Score: {}<br>Search Popularity Score: {}<br><b>M-Score: {}</b>".format(mp.twitterScore, mp.apScore, mp.trendsScore, mp.powerScore)
	return result

@app.route('/about.html')
def about():
	return open("about.html").read()

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    mp = MainProcessor(text)
    result = "<br>Social Media Score: {} <br>Press Coverage Score: {}<br>Search Popularity Score: {}<br><b>M-Score: {}</b>".format(mp.twitterScore, mp.apScore, mp.trendsScore, mp.powerScore)
    return result

if __name__ == '__main__':
    app.run(host= '0.0.0.0')