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
        nltk.download("punkt")
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
        tokens = [
            word for word in tokens if word not in self.__stops and word.isalpha()
        ]
        tokens = [word.strip() for word in tokens]
        lemmatizedWords = [self.__lemmatizer.lemmatize(word) for word in tokens]
        stemmedWords = [
            token
            for token in lemmatizedWords
            if self.__stemmer.stem(token) not in self.__stops
            and self.__model.inVocab(token)
        ]
        return stemmedWords

    def __countWords(self, tokens):
        wordCounts = dict()
        for i in range(len(tokens)):
            if tokens[i] in wordCounts:
                wordCounts[tokens[i]] += 1
            else:
                wordCounts[tokens[i]] = 1
        return wordCounts

    def rank(self, text):
        tokens = self.__cleanText(text)
        print(tokens)
        wordCounts = self.__countWords(tokens)
        scores = np.zeros(len(tokens))

