import spacy
import neuralcoref
import time
from math import floor
from scrape_abstracts import get_abstracts
from entity_relations_model import *
import docria

import gui


def gen_indices(doc, tokenlist):
    indices = list()
    i = 0
    while i < len(tokenlist):
        c_index_start = len(doc[0:tokenlist[i].i + 1].text) - len(tokenlist[i].text)
        while i < len(tokenlist) - 1 and tokenlist[i+1].i == tokenlist[i].i + 1:
            i += 1
        c_index_end = len(doc[0:tokenlist[i].i + 1].text)
        indices += [c_index_start, c_index_end]
        i += 1
    return tuple(indices)


def find_prep(root, tokens, depth):
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

    """
    print("Scraping abstracts from " + filename + "...")
    unfiltered_abstracts = get_abstracts(filename)
    """
    keywords = {'activates', 'activate', 'activated', 'induces', 'induce', 'induced', 'impairs', 'impair', 'impaired',
                'inhibits', 'inhibit', 'inhibitors', 'inhibitor', 'inhibited', 'promotes', 'promote', 'promoted',
                'localizes', 'localized', 'localize', 'leading', 'lead', 'leads', 'enhances', 'enhance', 'enhancing',
                'enhanced', 'activator', 'stabilizes', 'stabilize', 'stabilized', 'agonist', 'increase', 'increases',
                'increased', 'mediates', 'mediate', 'mediator', 'executes', 'execute', 'causes', 'cause', 'inactivate',
                'executed', 'caused', 'inactivated', 'blocked', 'repressed', 'reduced', 'disrupted', 'prevented',
                'inactivates', 'block', 'blocks', 'repress', 'represses', 'antagonist', 'reduces', 'reduce',
                'disrupts', 'disrupt', 'prevents', 'prevent', 'participates', 'contributes', 'contributed'
                'participate', 'contribute', 'participated'}  # should contain all keywords?
    """
    print("Filtering abstracts...")
    abstracts = dict()
    for pmid in unfiltered_abstracts:
        text = unfiltered_abstracts[pmid]
        for word in text.split():
            if word in keywords:
                abstracts[pmid] = text
                break
    """
    cnt = 0
    actualkeycnt = 0
    s = time.time()
    print("Analyzing abstracts...")
    entities = EntitySet()
    relations = list()

    docria_reader = docria.DocumentIO.read('pubmed1905_0_.docria')
    for docria in docria_reader:
        text = docria.text['main'].text  # reads text directly from
        doc = nlp(text)
        # print(text, "\n")
        for token in doc:
            # print(token.text, token.dep_, token.head.text, token.pos_,
                  # [child for child in token.children])
            if token.text in keywords:
                actualkeycnt += 1

        for chunk in doc.noun_chunks:
            nsubjstring = ""
            dobjstring = ""
            keyword = chunk.root.head
            keywordlist = [chunk.root.head]
            if (chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'nsubjpass') and keyword.text in keywords:
                # print(text, "\n")
                nsubjtokenlist = []
                for i in range(len(chunk)):
                    nsubjtokenlist.append(chunk[i])
                norigin = chunk.text
                nsubjtokenlist = find_prep(chunk.root, nsubjtokenlist, 0)
                for chunk2 in doc.noun_chunks:
                    if chunk2.root.dep_ == 'dobj' and chunk2.root.head == keyword:
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

                        if nsubjstring != "" or dobjstring != "":
                            print(nsubjtokenlist, keywordlist, dobjtokenlist, "\n")
                        else:
                            break
                        matches = list()  # adds allmatches from the docria document into one list
                        for prot in docria.layer['protmatches']:
                            matches.append(str(prot['text']))
                        for lys in docria.layer['lysomatches']:
                            matches.append(str(lys['text']))
                        print(matches)
                        interesting = False
                        sentencelist = nsubjtokenlist
                        sentencelist.extend(dobjtokenlist)
                        for n in sentencelist:  # checks if any of the found words in either nsubj or dobj
                            if n.text in matches:    # are a detected protein or lysosome word. if so, proceed
                                interesting = True
                                break

                        if interesting:
                            e1 = Entity(nsubjstring)
                            e2 = Entity(dobjstring)

                            entities += [e1, e2]
                            relation = Relation(Source(doc.text, "PMID=" + docria.props['id']),
                                                keyword.text, *gen_indices(doc, keywordlist))
                            relation.from_(e1, *gen_indices(doc, nsubjtokenlist)).to_(e2, *gen_indices(doc, dobjtokenlist))
                            relations.append(relation)
                        nsubjstring = ""
                        dobjstring = ""

                cnt += 1
    print("seconds: ", floor((time.time()-s)))
    print("keywords with nsubj found: ", cnt)
    print("actual keywords found: ", actualkeycnt)
    gui.Gui(sorted(entities.list()), relations)
