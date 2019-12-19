import subprocess
import os

p = subprocess.Popen("jupyter nbconvert --to python "+os.path.join(os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "notebooks", "runModel.ipynb"))+" --stdout", stdout=subprocess.PIPE)

runModelScript = p.communicate()[0].decode("utf-8")

serverInit = """
from flask import Flask, request, jsonify
import glob
import urllib
import zipfile
import re
import io
import cgi
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def maybe_download(filename, url):
    if not os.path.exists(os.path.join(os.getcwd(), filename)):
        filename, _ = urllib.request.urlretrieve(
            url, os.path.join(os.getcwd(), filename))
    # statinfo = os.stat(os.path.join(os.getcwd(), filename))
    print('Found and verified', filename)
    return filename


def extract(filename):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall("")
"""

serverRun = """

@app.before_first_request
def beforeFirstRequest():
    beforeStartup()


@app.route("/post", methods=['POST'])
def loadPage():
    data = request.json
    result  = {"status": "error"}
    if("text" in data and len(data["text"]) <= 3000):
        try:
            result = {
                "status": "ok",
                "result": returnRanks(data["text"])
            }
        except Exception:
            pass
    return jsonify(result)


@app.route("/")
def loadDefault():
    return "Server running!"
"""

with open(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "application.py")), "w") as file:
    file.write(runModelScript+serverInit+serverRun)
    file.close()
