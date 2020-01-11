import os
import re
from gensim.models import fasttext as ft
import numpy as np
import nltk
import operator
import nltk
from dataclasses import dataclass
from ftmmap import *


class BlankSort:
    """BlankSort Class"""

    __model = None
    __lemmatizer = None
    __window_size = None
    __stemmer = None
    __stops = set()

    def __init__(self, binary_path):
        self.__loadData(binary_path)

    def __loadData(self, binary_path):
        nltk.download("wordnet")
        nltk.download("stopwords")
        self.__model = FTmmap(
            os.path.join(os.getcwd(), os.path.join(binary_path, "cc.en.300.vec"))
        )
        self.__window_size = 3
        self.__lemmatizer = nltk.WordNetLemmatizer()
        self.__stemmer = nltk.stem.porter.PorterStemmer()
        # https://github.com/Alir3z4/stop-words
        self.__stops = set(
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
        lemmatizedWords = [self.__lemmatizer.lemmatize(word) for word in tokens]
        stemmedWords = [
            token
            for token in lemmatizedWords
            if self.__stemmer.stem(token) not in self.__stops
            and token not in self.__stops
        ]
        return stemmedWords

    def rank(self, text):
        text = self.__cleanText(text)
