import spacy
import neuralcoref
import time
from math import floor
from scrape_abstracts import get_abstracts
from keywords import *
from entity_relations_model import *
import docria
import pickle

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

    """
    print("Scraping abstracts from " + filename + "...")
    unfiltered_abstracts = get_abstracts(filename)
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
    dcnt = 0
    icnt = 0
    actualkeycnt = 0
    s = time.time()
    print("Analyzing abstracts...")
    entities = RelationalSet()
    relations = list()
    output = {}
    filename = 'corpus/out_json_pubmed19n0001.xml.txt.docria'
    docria_reader = docria.DocumentIO.read(filename)

    for docria in docria_reader:
        dcnt += 1
        if dcnt % 10 == 0:
            print(dcnt)
        text = docria.text['main'].text  # reads text directly from
        doc = nlp(text)
        # print(text, "\n")

        output[docria.props['id']] = {'text': text, 'tokens': [], 'entities': [], 'relations': []}
        text_tokens = []
        for token in doc:
            text_tokens.append(token.text)
            if token.text in keywords:
                actualkeycnt += 1
        j = 0
        output[docria.props['id']]['tokens'] = text_tokens
        for chunk in doc.noun_chunks:

            nsubjstring = ""
            dobjstring = ""
            keyword = chunk.root.head
            keywordlist = [chunk.root.head]

            e = []

            for i in range(len(chunk)):
                e.append(chunk[i].i)
            output[docria.props['id']]['entities'].append(e)
            # finds chunks where both nsubj and dobj point to a keyword
            if (chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'nsubjpass') and keyword.text in keywords:
                # print(text, "\n")
                nsubjtokenlist = []
                for i in range(len(chunk)):
                    nsubjtokenlist.append(chunk[i])
                norigin = chunk.text
                nsubjtokenlist = find_prep(chunk.root, nsubjtokenlist, 0)  # adds prepositions for context
                k = 0
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
                            pass
                            #print(nsubjtokenlist, keywordlist, dobjtokenlist, "\n")
                        else:
                            break
                        matches = list()  # adds allmatches from the docria document into one list
                        for prot in docria.layer['protmatches']:
                            matches.append(str(prot['text']))
                        for lys in docria.layer['lysomatches']:
                            matches.append(str(lys['text']))
                        interesting = False
                        sentencelist = nsubjtokenlist
                        sentencelist.extend(dobjtokenlist)
                        for n in sentencelist:       # checks if any of the found words in either nsubj or dobj
                            if n.text in matches:    # are a detected protein or lysosome word. if so, proceed
                                interesting = True
                                break
                        if interesting and doc[keyword.i-1].dep_ != 'neg':
                            icnt += 1
                            if keyword.text in positive_kw:
                                output[docria.props['id']]['relations'].append((j, k, 'P'))
                            else:
                                output[docria.props['id']]['relations'].append((j, k, 'N'))

                            e1 = Entity(nsubjstring)
                            e2 = Entity(dobjstring)

                            entities += [e1, e2]
                            src = Source(doc.text, filename + "\nPMID=" + docria.props['id'])
                            relation = Relation(src, keyword.text, inverse_keywords[keyword.text], *gen_indices(doc, keywordlist))
                            relation.from_(e1, *gen_indices(doc, nsubjtokenlist)).to_(e2, *gen_indices(doc, dobjtokenlist))
                            relations.append(relation)
                        nsubjstring = ""
                        dobjstring = ""
                    k += 1
                cnt += 1
            j += 1
    print("seconds: ", floor((time.time()-s)))
    print("keywords with nsubj found: ", cnt)
    print("documents in docria: ", dcnt)
    print("actual keywords found: ", actualkeycnt)
    print("interesting keywords found: ", icnt)
    # print(output)
    """
    for r in output:
        if len(output[r]['relations']) > 0:
            rel = output[r]['relations'][0][0]  # första relationen, och så tar man 'from'
            print(rel)
            ent = output[r]['entities'][rel][0]  # första ordet i entityn.
            print(ent)
            tok = output[r]['tokens'][ent]  # har bara ett värde så då tar vi det
            print(tok)
    """
    pickle.dump(output, open("relations.p", "wb"))
    gui.Gui(sorted(entities.list()), relations)









"""
dict av PMID   
    varje PMID har {text, [tokens], [entities], [relations]} där entity är [token_i1, token_i2...]

"""
