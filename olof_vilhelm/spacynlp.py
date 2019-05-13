import spacy
import neuralcoref
import time
from math import floor
from scrape_abstracts import get_abstracts
from entity_relations_model import *
import gui


def find_prep(root, tokens, depth):  # unfinished
    children = root.children
    newtokens = []
    for child in children:
        """
        (child.dep_ == 'compound' or child.dep_ == 'nmod' or child.dep_ == 'amod' or child.dep_ == 'pobj'
                or child.dep_ == 'nummod' or child.dep_ == 'punct')
        """
        if child.dep_ != 'prep' and depth != 0:
            newtokens.append(child)
            newtokens = find_prep(child, newtokens, depth + 1)

        if child.dep_ == 'prep':
            newtokens.append(child)
            newtokens = find_prep(child, newtokens, depth + 1)

    tokens.extend(newtokens)
    return tokens


if __name__ == '__main__':
    print("Loading spacy...")
    # spacy.prefer_gpu()
    nlp = spacy.load("en_core_web_sm")
    neuralcoref.add_to_pipe(nlp)
    filename = 'corpus/pubmed19n0195.xml'
    print("Scraping abstracts from " + filename + "...")
    unfiltered_abstracts = get_abstracts(filename)
    keywords = {'activates', 'activate', 'activated', 'induces', 'induce', 'induced', 'impairs', 'impair', 'impaired',
                'inhibits', 'inhibit', 'inhibitors', 'inhibitor', 'inhibited', 'promotes', 'promote', 'promoted',
                'localizes', 'localized', 'localize', 'leading', 'lead', 'leads', 'enhances', 'enhance', 'enhancing',
                'enhanced', 'activator', 'stabilizes', 'stabilize', 'stabilized', 'agonist', 'increase', 'increases',
                'increased', 'mediates', 'mediate', 'mediator', 'executes', 'execute', 'causes', 'cause', 'inactivate',
                'executed', 'caused', 'inactivated', 'blocked', 'repressed', 'reduced', 'disrupted', 'prevented',
                'inactivates', 'block', 'blocks', 'repress', 'represses', 'antagonist', 'reduces', 'reduce',
                'disrupts', 'disrupt', 'prevents', 'prevent', 'participates', 'contributes', 'contributed'
                'participate', 'contribute', 'participated'}  # should contain all keywords?

    print("Filtering abstracts...")
    abstracts = dict()
    for pmid in unfiltered_abstracts:
        text = unfiltered_abstracts[pmid]
        for word in text.split():
            if word in keywords:
                abstracts[pmid] = text
                break
    cnt = 0
    actualkeycnt = 0
    s = time.time()
    print("Analyzing abstracts...")
    entities = list()
    relations = list()

    for abstract in abstracts:
        text = abstracts[abstract]
        doc = nlp(text)
        #print(text, "\n")
        for token in doc:
            if token.text in keywords:
                actualkeycnt += 1
        for chunk in doc.noun_chunks:
            nsubjstring = ""
            dobjstring = ""
            keyword = chunk.root.head
            keywordlist = [chunk.root.head]
            if (chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'nsubjpass') and chunk.root.head.text in keywords:
                # print(text, "\n")
                nsubjtokenlist = []
                for i in range(len(chunk)):
                    nsubjtokenlist.append(chunk[i])
                norigin = chunk.text
                nsubjtokenlist = find_prep(chunk.root, nsubjtokenlist, 0)
                for chunk2 in doc.noun_chunks:
                    if chunk2.root.dep_ == 'dobj' and chunk2.root.head.text == keyword.text:
                        dobjtokenlist = []
                        for i in range(len(chunk2)):
                            dobjtokenlist.append(chunk2[i])
                        dobjtokenlist = find_prep(chunk2.root, dobjtokenlist, 0)
                        nsubjtokenlist = sorted(nsubjtokenlist, key=lambda tok: tok.i)
                        for token in nsubjtokenlist:
                            nsubjstring += token.text + " "

                        dobjtokenlist = sorted(dobjtokenlist, key=lambda tok: tok.i)
                        for token in dobjtokenlist:
                            dobjstring += token.text + " "

                        """
                        sentencelist = nsubjtokenlist
                        sentencelist.extend(keywordlist)
                        sentencelist.extend(dobjtokenlist)
                        sentencelist = list(dict.fromkeys(sentencelist)) # removes duplicates
                        """
                        if nsubjstring != "" or dobjstring != "":
                            print(nsubjtokenlist, keywordlist, dobjtokenlist)
                            print("{", nsubjstring, "} {",  keyword.text, "} {",  dobjstring, "}\n")

                        e1 = Entity(nsubjstring)
                        e1_i_e = len(doc[0:nsubjtokenlist[-1].i + 1].text)
                        e1_i_s = e1_i_e - len(nsubjstring)

                        e2 = Entity(dobjstring)
                        e2_i_e = len(doc[0:dobjtokenlist[-1].i + 1].text)
                        e2_i_s = e2_i_e - len(dobjstring)

                        r_i_e = len(doc[0:keyword.i + 1].text)
                        r_i_s = r_i_e - len(keyword.text)

                        entities += [e1, e2]
                        relation = Relation(Source(doc.text, "id=???"), keyword.text, r_i_s, r_i_e)
                        relation.from_(e1, e1_i_s, e1_i_e).to_(e2, e2_i_s, e2_i_e)
                        relations.append(relation)

                cnt += 1
    print("seconds: ", floor((time.time()-s)))
    print("keywords with nsubj found: ", cnt)
    print("Abstracts with keywords in them: ", len(abstracts))
    print("actual keywords found: ", actualkeycnt)
    gui.Gui(entities, relations)
