# Standard library imports

# Third party imports
import spacy

# Local application imports
import sv_pipeline

 
def load_nlp():
    """Load a spacy object trained with"""
    nlp = spacy.load("sv_pipeline")
    return nlp
    # nlp = spacy.load("/home/callebalik/projects/BioNLP/carl/spaCy/journalparser.py")
    
load_nlp()
