import spacy
import datetime
from xml.etree import cElementTree as ET

if __name__ == '__main__':
    print("1")
    # spacy.require_gpu()
    nlp = spacy.load("en_core_web_sm")


    print("2")
    tree = ET.parse('pubmed19n0195.xml')
    root = tree.getroot()
    print("3")
    abstracts = {}
    for article in root:
        pmid = ""
        abstract = ""
        for xid in article.iter("PMID"):
            pmid = xid.text
        for txt in article.iter("AbstractText"):
            abstract = txt.text
        if abstract != "" and pmid != "":
            abstracts[pmid] = abstract

    keywords = {'activates', 'activate', 'activating', 'induces', 'induce', 'inducing', 'impairs', 'impair', 'impairing',
                'inhibits', 'inhibit', 'inhibitors', 'inhibitor', 'inhibiting', 'promotes', 'promote', 'promoting',
                'localizes', 'localize', 'localizing', 'leading', 'lead', 'leads', 'enhances', 'enhance', 'enhancing',
                'activator', 'stabilizes', 'stabilize', 'stabilizing', 'agonist', 'increase', 'increases', 'increasing',
                'mediates', 'mediate', 'mediator', 'executes', 'execute', 'causes', 'causing', 'cause', 'inactivate',
                'inactivates', 'block', 'blocks', 'repress', 'represses', 'antagonist', 'reduces', 'reduce', 'reducing',
                'disrupts', 'disrupt', 'disrupting', 'prevents', 'prevent', 'preventing', 'participates', 'contributes',
                'participate', 'contribute'}  # should contain all keywords?
    # could use lemma instead to skip all other forms of words

    # large file holds 3960 files, small file only 21
    cnt = 0
    print("4")
    print(str(datetime.datetime.now()).split('.')[0])
    for abstract in abstracts:
        text = abstracts[abstract]
        doc = nlp(text)  # break down an abstract to sentences




        # chunking strategy - take one sentence at a time, chunk, and match nsubj and dobj with the keyword
        for s in doc.sents:
            sent = nlp(s.text)  # break down a sentence into deprels, POS, NEr etc
            nsubjstring = ""
            keyword = ""
            dobjstring = ""
            for chunk in sent.noun_chunks:
                if chunk.root.dep_ == 'nsubj' and chunk.root.head.text in keywords:
                    nsubjstring = chunk.text
                    keyword = chunk.root.head.text
                    cnt += 1
                if chunk.root.dep_ == 'dobj' and chunk.root.head.text in keywords:
                    dobjstring = chunk.text
                    keyword = chunk.root.head.text

            if nsubjstring != "" and dobjstring != "":
                print(nsubjstring, keyword, dobjstring)

    print(str(datetime.datetime.now()).split('.')[0])
    print("keywords found: ", cnt)
