# serve.py
import re
import os
from os import listdir
from os.path import isfile, join
import sys
import pprint
from flask import Flask, redirect, url_for, request,render_template,jsonify
path = 'demo'
import glob
import json
import base64
global_data=list()
# creates a Flask application, named app
app = Flask(__name__,static_url_path='', 
            static_folder='/root/static',
            template_folder='/root/templates')

# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():  
    message = "Hello, World"
    """ return jsonify({
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}) """
    return render_template('index.html', message=message)

@app.route('/refreshsingle', methods=['GET'])
def refreshingle():
    global global_data
    all_data=list()

    filename = os.path.join('/','root', 'static','data',"refresh.json")
    with open(filename) as f:
    	global_data=json.load(f)
    return jsonify({"succes":"true"})

@app.route('/refresh', methods=['GET'])
def refresh():
    global global_data
    all_data=list()

    path_to_files = os.path.join('/','root', 'static','data',"*","*.json")
    for filename in sorted(glob.glob(path_to_files)):
        with open(filename) as f:
            print(filename)
            data = json.load(f)
            data['path']=filename
            #print(data)
            all_data.append(data)
    global_data=all_data
    return jsonify(all_data)

@app.route('/search/<word>', methods=['GET'])
def search(word):
    global global_data
    if request.method == 'GET':
        print(word)
        results=[]
        print(len(global_data))
        for paper in global_data:
            title = paper['metadata']['title']
            x = re.search(word.lower(), title.lower())
            print(x)
            if(x):
                result={
                    "title":paper['metadata']['title'],
                    "path":paper['path']
                }
                results.append(result)
        return jsonify(results)

@app.route('/searchmultipleor/<words>', methods=['GET'])
def searchmultipleor(words):
    global global_data
    if request.method == 'GET':
        word = words.split(" ")
        print(word)
        results={}
        for item in word:
            results[item]=[]
            for paper in global_data:
                title = paper['metadata']['title']
                x = re.search(item.lower(), title.lower())
                print(x)
                if(x):
                    result={
                        "title":paper['metadata']['title'],
                        "path":paper['path']

                    }
                    results[item].append(result)
    
        return jsonify(results)

@app.route('/searchmultipleand/<words>', methods=['GET'])
def searchmultipleand(words):
    global global_data
    if request.method == 'GET':
        word = words.split(" ")
        print(word)
        results=[]
        for paper in global_data:
            title = paper['metadata']['title']
            flag=1
            for item in word:
                x = re.search(r"\b"+item.lower()+r"\b", title.lower())
                if(x):
                    pass
                else:
                    flag=0
            if(flag==1):   
                message_bytes = paper['path'].encode('ascii')
                base64_bytes=base64.b64encode(message_bytes)
                base64_message = base64_bytes.decode('ascii')

 
                result={
                    "title":paper['metadata']['title'],
                    "path":base64_message,
                }
                results.append(result)
        return jsonify(results)

@app.route('/getdetail/<path>', methods=['GET'])
def getdetail(path):
    if request.method == 'GET':
        return render_template('getdetail.html', message=path)

@app.route('/contact', methods=['GET'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')

@app.route('/getdetailapi/<path>', methods=['GET'])
def getdetailapi(path):
    if request.method == 'GET':

        base64_bytes = path.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        filepath = message_bytes.decode('ascii')
        with open(filepath) as f:
            #print(filename)
            paper = json.load(f)
            abs_txt=""
            for abs in paper['abstract']:
                abs_txt=abs_txt+" "+ abs['text']
            body_txt=""
            for body in paper['body_text']:
                body_txt=body_txt+" "+ body['text']
            
            result= {
                    "title":paper['metadata']['title'],
                    "path":filepath,
                    "abs":abs_txt
                }
                
        return jsonify(result)



@app.route('/searchmultiplecountry/<words>', methods=['GET'])
def searchmultiplecountry(words):
    global global_data
    country={}
    if request.method == 'GET':
        word = words.split(" ")
        print(word)
        results=[]
        for paper in global_data:
            title = paper['metadata']['title']
            flag=1
            for item in word:
                x = re.search(r"\b"+item.lower()+r"\b", title.lower())
                if(x):
                    pass
                else:
                    flag=0
            if(flag==1):    
                try:

                    if paper['metadata']['authors'][0]['affiliation']['location']['country'] in country.keys():
                        country[paper['metadata']['authors'][0]['affiliation']['location']['country']]=country[paper['metadata']['authors'][0]['affiliation']['location']['country']] + 1
                    else:
                        country[paper['metadata']['authors'][0]['affiliation']['location']['country']]=1
                except:
                    pass
        return jsonify(country)



# run the application
if __name__ == "__main__":
    global_data=[]  
    app.run(host= '0.0.0.0',debug=True)