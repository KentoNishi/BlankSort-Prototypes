from flask import Flask
import glob
import os
import urllib
import zipfile, re, io
app = Flask(__name__)


def maybe_download(filename, url):
    if not os.path.exists(os.path.join(os.getcwd(),filename)):
        filename, _ = urllib.request.urlretrieve(url, os.path.join(os.getcwd(),filename))
    statinfo = os.stat(os.path.join(os.getcwd(),filename))
    print('Found and verified', filename)
    return filename


def extract(filename):
    with zipfile.ZipFile(filename,"r") as zip_ref:
        zip_ref.extractall("")


maybe_download("binaries.zip","https://blanksortbinaries.blob.core.windows.net/binaries/binaries.zip")
extract("binaries.zip")

"""
@app.route("/")
def hello():
    os.chdir(os.getcwd())
    x = [file for file in glob.glob("**/*.*")]
    return "Hello World!\n"+str(x)

"""