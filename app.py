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