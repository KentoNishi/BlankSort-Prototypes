import os
import re
from gensim.models import fasttext as ft
import numpy as np
import nltk
import operator
import nltk
from dataclasses import dataclass
import ftmmap


class BlankSort:
    """BlankSort Class"""

    __model = None
    __lemmatizer = None
    __window_size = None
    __stemmer = None
    __stops = set()

    def ___init__(self, binary_path):
        self.__loadData(binary_path)

    def __loadData(self, binary_path):
        nltk.download("wordnet")
        nltk.download("stopwords")
        if "__model" not in dir(type(self)):
            # https://fasttext.cc/docs/en/crawl-vectors.html
            type(self).__model = os.path.join(
                os.getcwd(), os.path.join(binary_path, "cc.en.300.bin")
            )
        type(self).__window_size = 3
        type(self).__lemmatizer = nltk.WordNetLemmatizer()
        type(self).__stemmer = nltk.stem.porter.PorterStemmer()
        # https://github.com/Alir3z4/stop-words
        type(self).__stops = set(
            line.strip()
            for line in open(
                os.path.join(
                    os.getcwd(), os.path.join(binary_path, "stopwords-en.txt")
                ),
                encoding="utf8",
            )
        )

    def __cleanText(self, text):
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        lemmatizedWords = [type(self).__lemmatizer.lemmatize(word) for word in tokens]
        stemmedWords = [
            token
            for token in lemmatizedWords
            if type(self).__stemmer.stem(token) not in type(self).__stops
            and token not in type(self).__stops
        ]
        return stemmedWords

    def rank(self, text):
        text = self.__cleanText(text)
