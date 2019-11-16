from flask import Flask
import glob
import os
app = Flask(__name__)

@app.route("/")
def hello():
    os.chdir(os.getcwd())
    x = [file for file in glob.glob("**/*.*")]
    return "Hello World!\n"+str(x)
