from gensim.models import fasttext as ft
import numpy as np
import os
import nltk
import operator
import re
import nltk
import numpy
from dataclasses import dataclass


class BlankSort:
    """BlankSort Class"""
    _model = None
    _lemmatizer = None
    _window_size = None
    _stemmer = None
    _stops = set()

    def __init__(self, binary_path):
        self._loadData(binary_path)

    def _loadData(self, binary_path):
        nltk.download('wordnet')
        nltk.download('stopwords')
        if "model" not in dir(type(self)):
            # https://fasttext.cc/docs/en/crawl-vectors.html
            type(self)._model = ft.load_facebook_vectors(
                os.path.join(os.getcwd(), os.path.join(binary_path, "cc.en.300.bin")))
        type(self)._window_size = 3
        type(self)._lemmatizer = nltk.WordNetLemmatizer()
        type(self)._stemmer = nltk.stem.porter.PorterStemmer()
        # https://github.com/Alir3z4/stop-words
        type(self)._stops = set(line.strip() for line in open(os.path.join(
            os.getcwd(), os.path.join(binary_path, "stopwords-en.txt")), encoding='utf8'))

    def _cleanText(self, text):
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        lemmatizedWords = [type(self)._lemmatizer.lemmatize(word)
                           for word in tokens]
        stemmedWords = [token for token in lemmatizedWords if
                        type(self)._stemmer.stem(
                            token) not in type(self)._stops
                        and token not in type(self)._stops]
        return stemmedWords

    def rank(self, text):
        text = self._cleanText(text)
