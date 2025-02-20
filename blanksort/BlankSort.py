import os
import re
import numpy as np
import nltk
from ftooc import *
import time


class BlankSort:
    """BlankSort Class"""

    __model = None
    __lemmatizer = None
    __windowSize = None
    __stemmer = None
    __stops = set()
    __similarityDict = dict()
    __lemmatizedDict = dict()

    def __init__(self, binary_path, preloadVectors=False, saveGeneratedVectors=False):
        self.__loadData(binary_path)
        if preloadVectors:
            self.__model.preloadVectors()
        self.__model.saveGeneratedVectors = saveGeneratedVectors

    def __loadData(self, binary_path):
        nltk.download("wordnet")
        nltk.download("stopwords")
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        # https://fasttext.cc/docs/en/crawl-vectors.html
        self.__model = FTOOC(os.path.join(binary_path, "cc.en.300.vec"))
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

    def lemmatize(self, word):
        if word in self.__lemmatizedDict:
            return self.__lemmatizedDict[word]
        self.__lemmatizedDict[word] = self.__lemmatizer.lemmatize(word)
        return self.__lemmatizedDict[word]

    def cleanText(self, text):
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        tokens = [word.strip() for word in tokens]
        tokens = [word for word in tokens if len(word) > 2 and word.isalpha()]
        lemmatizedWords = [self.lemmatize(word) for word in tokens]
        lemmatizedWords = [
            word
            for word in lemmatizedWords
            if word not in self.__stops and len(word) > 2
        ]
        return lemmatizedWords

    def processText(self, text):
        tokens = lemmatizedWords = self.cleanText(text)
        stemmedWords = [
            token
            for token in lemmatizedWords
            if token not in self.__stops
            and self.__stemmer.stem(token) not in self.__stops
            # and self.__model.inVocab(token)
        ]
        posTagList = nltk.pos_tag(tokens)
        posTags = dict()
        for word in posTagList:
            posTags[word[0]] = word[1]
        return stemmedWords, posTags

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

    def getSimilarity(self, wordA, wordB):
        similarityScore = 0.0
        if (wordA + " " + wordB) not in self.__similarityDict:
            similarityScore = self.__model.similarity(wordA, wordB)
        else:
            similarityScore = self.__similarityDict[(wordA + " " + wordB)]
        self.__similarityDict[(wordA + " " + wordB)] = similarityScore
        self.__similarityDict[(wordB + " " + wordA)] = similarityScore
        return similarityScore

    def __filterResults(self, scoreList, posTags, listSize, similarityThreshold):
        finalList = []
        index = 0
        while index < len(scoreList) and len(finalList) < listSize:
            if (
                posTags[scoreList[index][0]][:2] == "NN"
                or posTags[scoreList[index][0]][:2] == "JJ"
            ):
                canAdd = True
                for word in finalList:
                    if (
                        self.getSimilarity(word, scoreList[index][0])
                        > similarityThreshold
                    ):
                        canAdd = False
                        break
                if canAdd:
                    finalList.append(scoreList[index][0])
            index += 1
        return finalList

    def rank(self, text, **args):
        """
        Extracts keywords from the given text.

        Parameters
        ----------
        text : str
            The input text.

        listSize : int, optional
            The number of keywords to extract.

        Returns
        -------
        list
            A list of strings, which are keywords.
        """
        # defaults to selecting top 5 keywords
        listSize = args["listSize"] if "listSize" in args else 5
        # sets default similarity removal threshold to 0.75
        similarityThreshold = (
            args["similarityThreshold"] if "similarityThreshold" in args else 0.8
        )
        # processes text and generates tokens (words)
        # and position tags (noun, verb, adjective, etc.)
        tokens, posTags = self.processText(text)
        # counts the number of occurrences of each word
        wordCounts = self.__countWords(tokens)
        # initializes local word scores array to zeros
        scores = np.zeros(len(tokens))
        # creates a dictionary to hold global word scores
        wordScores = dict()
        # for each word in the input text
        for i in range(len(tokens)):
            # find left boundary based on the window size
            leftBound = max(0, i - self.__windowSize)
            # find right boundary based on the window size
            rightBound = min(len(tokens) - 1, i + self.__windowSize)
            # calculate the total context size
            contextSize = rightBound - leftBound + 1
            # for each word in the right window
            for j in range(i + 1, rightBound + 1):
                # calculate the similarity score
                similarityScore = self.getSimilarity(tokens[i], tokens[j])
                # add the score to this word and the other word
                scores[i] += similarityScore
                scores[j] += similarityScore
            # average the word score and scale it inversely by the
            # number of occurrences of this word
            wordScore = scores[i] / (wordCounts[tokens[i]] * contextSize)
            # if the word does not yet have a global word score
            if tokens[i] not in wordScores:
                # store the word score
                wordScores[tokens[i]] = wordScore
            # if the global word score has been assigned previously
            else:
                # set the global word score to the minimum local word score
                wordScores[tokens[i]] = min(wordScores[tokens[i]], wordScore)
        # convert the dictionary to a list
        scoreList = list(map(list, wordScores.items()))
        # sort the list of candidate keywords
        scoreList = sorted(scoreList, key=lambda x: x[1])
        # filter out results that are too similar and return the keywords
        return self.__filterResults(scoreList, posTags, listSize, similarityThreshold)

    def loadVector(self, word):
        self.__model.loadVector(word)

    def getVector(self, word):
        return self.__model.getVector(word)
