from flask import Flask,request
import uuid
import subprocess
import os
app = Flask(__name__)

@app.route('/scss',methods=["POST"])
def scss():
    data = request.get_json()
    scss = data['scss']
    filename = str(uuid.uuid4()) + '.scss'
    f = open(filename, "x")
    f.write(scss)
    f.close()
    status, output = subprocess.getstatusoutput("node-sass " + filename)
    os.remove(filename)
    print(output)
    return output

@app.route('/js',methods=["POST"])
def js():
    data = request.get_json()
    js = data['js']
    filename = str(uuid.uuid4()) 

    f = open(filename + '.coffee', "x")
    f.write(js)
    f.close()
    name = filename + '.coffee'
    status, output = subprocess.getstatusoutput("coffee -c " + name)
    os.remove(filename + '.coffee')

    jsfilename = open(filename + '.js',mode='r')
    jsfilestr = jsfilename.read()
    jsfilename.close()
    os.remove(filename + '.js')
    print(jsfilestr)
    return jsfilestr