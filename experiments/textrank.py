import spacy
import pytextrank
from collections import OrderedDict

def rankText(text):
    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("en_core_web_sm")

    # add PyTextRank to the spaCy pipeline
    tr = pytextrank.TextRank()
    nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    doc = nlp(text)

    # examine the top-ranked phrases in the document
    """
    for p in doc._.phrases:
        print("{:.4f} {:5d}  {}".format(p.rank, p.count, p.text))
        print(p.chunks)
    """
    phrases=[[p.text,p.rank] for p in doc._.phrases]
    return phrases