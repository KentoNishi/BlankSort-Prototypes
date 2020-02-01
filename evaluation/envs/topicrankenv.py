import pke
import string
from nltk.corpus import stopwords


class TopicRankEnv:
    def __init__(self):
        pass

    def rank(self, text, **args):
        self.tr = pke.unsupervised.TopicRank()
        listSize = args["listSize"] if "listSize" in args else 5
        self.tr.load_document(input=text, language="en")
        self.tr.candidate_selection()
        self.tr.candidate_weighting()
        wordList = []
        for item in self.tr.get_n_best(n=listSize):
            string = item[0]
            tokenized = string.split()
            for word in tokenized:
                wordList.append(word)
        return wordList[:listSize]
