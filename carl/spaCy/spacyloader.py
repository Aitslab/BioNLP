import spacy
import sv_pipeline

def load_nlp():
    nlp = spacy.load("sv_pipeline")
    return nlp
    # nlp = spacy.load("/home/callebalik/projects/BioNLP/carl/spaCy/journalparser.py")

load_nlp()