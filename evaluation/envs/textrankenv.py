import spacy
import pytextrank


class TextRankEnv:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.tr = pytextrank.TextRank()
        self.nlp.add_pipe(self.tr.PipelineComponent, name="textrank", last=True)

    def rank(self, text, **args):
        listSize = args["listSize"] if "listSize" in args else 5
        doc = self.nlp(text)
        wordList = []
        for item in doc._.phrases:
            string = item.text
            tokenized = string.split()
            for word in tokenized:
                wordList.append(word)
        return wordList[:listSize]
