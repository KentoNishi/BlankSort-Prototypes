from rake_nltk import Rake


class RakeEnv:
    def __init__(self):
        self.r = Rake()

    def rank(self, text, **args):
        listSize = args["listSize"] if "listSize" in args else 5
        self.r.extract_keywords_from_text(text)
        wordList=[]
        for string in self.r.get_ranked_phrases():
            tokenized=string.split()
            for word in tokenized:
                wordList.append(word)
        return wordList[:listSize]
