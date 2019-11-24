#!/usr/bin/env python
# coding: utf-8

# In[37]:


import os
from keras.models import load_model
import pickle
import re
import numpy as np
import nltk
from nltk.corpus import stopwords


# In[ ]:


def inNB():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


# In[39]:


def beforeStartup():
    if(inNB()):
        maybe_download("binaries.zip",
                    "https://blanksortbinaries.blob.core.windows.net/binaries/binaries.zip")
        extract("binaries.zip")
    globals()["model"] = load_model(os.path.join(os.path.join(os.path.abspath(
        './binaries'), "models"), "classification_model.h5"))
    model.summary()
    names = ["window_size", "vocab_size", "dictionary"]
    for name in names:
        with open(os.path.join(os.path.join(os.path.abspath('./binaries'), "pickles"), name+".pickle"), "rb") as f:
            globals()[name] = pickle.load(f)
    nltk.download("stopwords")
    globals()["stopWords"] = set(stopwords.words("english"))


# In[41]:


def removeStopWords(rankedWords):
    return [word for word in rankedWords if word[0] not in stopWords]


# In[42]:


def removeNumbers(rankedWords):
    return  [word for word in rankedWords if not any(char.isdigit() for char in word[0])]


# In[43]:


def generateInverseCounts(wordSequence):
    countDict=dict()
    for word in wordSequence:
        if word not in countDict:
            countDict[word]=1
        else:
            countDict[word]+=1
    return [1/countDict[word] for word in wordSequence]


# In[44]:


def findWordScores(wordSequence,tokenized):
    wordScores=np.zeros(len(wordSequence))
    contextCounts=np.zeros(len(wordSequence))
    inverseCounts=generateInverseCounts(wordSequence)
    for i in range(len(wordSequence)):
        leftBound=max(0,i-window_size)
        rightBound=min(len(wordSequence)-1,i+window_size)
        contextCounts[i]=rightBound-leftBound+1
        for k in range(i+1,rightBound+1):
            confidence=model.predict([[wordSequence[i]],[wordSequence[k]]])
            wordScores[i]+=confidence[0][0]
            wordScores[k]+=confidence[0][0]
    return ([tokenized[i],inverseCounts[i]*wordScores[i]/contextCounts[i]] for i in range(len(wordSequence)))


# In[45]:


def formatData(string):
    string=re.sub(r"[^\w\s]", ' ', string)
    string=string.lower()
    tokenized=string.split()
    wordSequence=[]
    for word in tokenized:
        if word in dictionary:
            wordSequence.append(dictionary[word])
        else:
            wordSequence.append(dictionary["UNK"])
    return wordSequence,tokenized,string


# In[46]:


def generateRankedList(string,**attributes):
    string=" ".join(string.split())
    noNumbers=attributes["noNumbers"] if "noNumbers" in attributes else True
    noStopWords=attributes["noStopWords"] if "noStopWords" in attributes else True
    wordSequence,tokenized,string=formatData(string)
    wordScores=findWordScores(wordSequence,tokenized)
    wordBank={}
    for word in wordScores:
        if word[0] in wordBank:
            wordBank[word[0]]=min(wordBank[word[0]],word[1])
        else:
            wordBank[word[0]]=word[1]
    sortedList=sorted(wordBank.items(), key=lambda x: x[1])
    rankedWords=[[x,y] for x,y in sortedList]
    if noStopWords:
        rankedWords=removeStopWords(rankedWords)
    if noNumbers:
        rankedWords=removeNumbers(rankedWords)
    return rankedWords


# In[47]:


def printList(testCase,num=None,**attributes):
    noNumbers=attributes["noNumbers"] if "noNumbers" in attributes else True
    noStopWords=attributes["noStopWords"] if "noStopWords" in attributes else True
    rankedWords=generateRankedList(testCase,noNumbers=noNumbers,noStopWords=noStopWords)
    print(testCase)
    if(num==None):
        num=len(rankedWords)
    else:
        num=min(len(rankedWords),num)
    print()
    for i in range(num):
        print(str(i+1)+". "+rankedWords[i][0]+": "+str(round(rankedWords[i][1],3)))
    print()


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
    statinfo = os.stat(os.path.join(os.getcwd(), filename))
    print('Found and verified', filename)
    return filename


def extract(filename):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall("")

def returnRanks(testCase, num=None, **attributes):
    noNumbers = attributes["noNumbers"] if "noNumbers" in attributes else True
    noStopWords = attributes["noStopWords"] if "noStopWords" in attributes else True
    rankedWords = generateRankedList(
        testCase, noNumbers=noNumbers, noStopWords=noStopWords)
    return rankedWords


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
