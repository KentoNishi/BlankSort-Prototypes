# https://github.com/codingMJ/Using-pretrained-FastText-model/blob/master/search%20word_vectors%20model%20(out-of-core).py
from gensim.models.wrappers import FastText
from gensim.matutils import cossim
import numpy as np
from numpy import dot
from numpy.linalg import norm
from operator import itemgetter
from scipy import spatial


class FTOOC:

    __vocabulary = set()
    savedVectors = dict()

    def __init__(self, path):
        self.__modelPath = path
        self.__getVocab()

    def __cos_sim(self, a, b):
        return spatial.distance.cosine(a, b)

    def inVocab(self, search_token):
        return search_token in self.__vocabulary

    def __getVocab(self):
        with open(self.__modelPath, "rb") as infile:
            for line in infile:
                line_decoded = line.decode("utf-8")
                word, vec_s = line_decoded.strip().split(" ", 1)
                self.__vocabulary.add(word)
        return False

    def loadVectors(self, dictionary):
        if(len(dictionary)==0):
            return
        with open(self.__modelPath, "rb") as infile:
            for line in infile:
                line_decoded = line.decode("utf-8")
                word, vec_s = line_decoded.strip().split(" ", 1)
                if word not in self.savedVectors and word in dictionary:
                    vector = np.array([float(v) for v in vec_s.split(" ")])
                    self.savedVectors[word] = vector

    def getVector(self, search_token):
        return self.savedVectors[search_token]

    def similarity(self, a, b):
        return self.__cos_sim(self.getVector(a), self.getVector(b))

