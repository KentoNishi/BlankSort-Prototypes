# https://github.com/codingMJ/Using-pretrained-FastText-model/blob/master/search%20word_vectors%20model%20(out-of-core).py
from gensim.models.wrappers import FastText
from gensim.matutils import cossim
import numpy as np
import os
from numpy import dot
from numpy.linalg import norm
from operator import itemgetter
from scipy import spatial
from sqlitedict import SqliteDict


class FTOOC:

    __modelPath = ""
    savedVectors = dict()

    def __init__(self, path):
        self.__modelPath = path
        databasePath = os.path.join(
            os.path.dirname(self.__modelPath), "blanksort.database"
        )
        print("Database path: "+databasePath)
        self.savedVectors = SqliteDict(databasePath, autocommit=True)
        self.__loadVectors()

    def __cos_sim(self, a, b):
        return spatial.distance.cosine(a, b)

    def inVocab(self, search_token):
        return search_token in self.savedVectors

    def __loadVectors(self):
        with open(self.__modelPath, "rb") as infile:
            for line in infile:
                line_decoded = line.decode("utf-8")
                word, vec_s = line_decoded.strip().split(" ", 1)
                vector = np.array([float(v) for v in vec_s.split(" ")])
                self.savedVectors[word] = vector

    def getVector(self, search_token):
        return self.savedVectors[search_token]

    def similarity(self, a, b):
        return self.__cos_sim(self.getVector(a), self.getVector(b))
