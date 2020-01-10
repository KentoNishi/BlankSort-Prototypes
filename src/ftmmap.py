# https://github.com/codingMJ/Using-pretrained-FastText-model/blob/master/search%20word_vectors%20model%20(out-of-core).py
from gensim.models.wrappers import FastText
from gensim.matutils import cossim
import numpy as np
from numpy import dot
from numpy.linalg import norm
from operator import itemgetter


class FTmmap:
    def __init__(self, path):
        self.__modelPath = path

    def cos_sim(self, a, b):
        return dot(a, b) / (norm(a) * norm(b))

    def similarity(self, a, b):
        try:
            return _cos_sim(getVector(a), getVector(b))
        except Exception:
            return None

    def inVocab(self, search_token):
        with open(self.__modelPath, "rb") as infile:
            for line in infile:
                line_decoded = line.decode("utf-8")
                word, vec_s = line_decoded.strip().split(" ", 1)
                if search_token == word:
                    return True
        return False

    def getVector(self, search_token):
        search_token_vec = None
        with open(self.__modelPath, "rb") as infile:
            for line in infile:
                line_decoded = line.decode("utf-8")
                word, vec_s = line_decoded.strip().split(" ", 1)
                if search_token == word:
                    search_token_vec = np.array([float(v) for v in vec_s.split(" ")])
                    break
        return search_token_vec
