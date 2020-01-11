import os
import re
from gensim.models import fasttext as ft
import numpy as np
import nltk
import operator
import nltk
from dataclasses import dataclass
from ftooc import *


class BlankSort:
    """BlankSort Class"""

    __model = None
    __lemmatizer = None
    __windowSize = None
    __stemmer = None
    __stops = set()

    def __init__(self, binary_path):
        self.__loadData(binary_path)

    def __loadData(self, binary_path):
        nltk.download("wordnet")
        nltk.download("stopwords")
        nltk.download("punkt")
        self.__model = FTOOC(
            os.path.join(os.getcwd(), os.path.join(binary_path, "cc.en.300.vec"))
        )
        self.__windowSize = 3
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

    def __buildDictionary(self, tokens):
        dictionary = set(tokens)
        return dictionary

    def rank(self, text):
        tokens = self.__cleanText(text)
        dictionary = self.__buildDictionary(tokens)
        wordCounts = self.__countWords(tokens)
        scores = np.zeros(len(tokens))
        wordScores = dict()
        similarityMatrix = np.full((len(tokens), len(tokens)), np.nan, dtype=float)
        for i in range(len(tokens)):
            leftBound = max(0, i - self.__windowSize)
            rightBound = min(len(tokens) - 1, i + self.__windowSize)
            contextSize = rightBound - leftBound + 1
            for j in range(i + 1, rightBound + 1):
                similarityScore = 0.0
                if np.isnan(similarityMatrix[i][j]):
                    similarityScore = self.__model.similarity(tokens[i], tokens[j])
                    # similarityScore = (similarityScore + 1) / 2.0
                else:
                    similarityScore = similarityMatrix[i][j]
                scores[i] += similarityScore
                scores[j] += similarityScore
                similarityMatrix[i][j] = similarityScore
                similarityMatrix[j][i] = similarityScore
            wordScore = scores[i] / (wordCounts[tokens[i]] * contextSize)
            if tokens[i] not in wordScores:
                wordScores[tokens[i]] = wordScore
            else:
                wordScores[tokens[i]] = min(wordScores[tokens[i]], wordScore)
        scoreList = list(map(list, wordScores.items()))
        scoreList = sorted(scoreList, key=lambda x: x[1])
        return scoreList
