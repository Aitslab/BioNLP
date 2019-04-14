from stanfordcorenlp import StanfordCoreNLP
from scrape_abstracts import get_abstracts
from random import randint

STANDARD_DEPENDENCIES_INDICES = 0
STANDARD_DEPENDENCIES_WORDS = 1
SIMPLE_DEPENDENCIES = 2

STANFORD_CORE_NLP_DIR = "libs/stanford-corenlp-full-2018-10-05"

BATCH_SIZE = 1

MODE = SIMPLE_DEPENDENCIES

if __name__ == '__main__':
    sNLP = StanfordCoreNLP(STANFORD_CORE_NLP_DIR)
    filename = 'corpus/pubmed19n0195.xml'
    abstracts = get_abstracts(filename)

    print("Abstracts scraped, running Stanford Core on ", BATCH_SIZE, " random abstracts.")

    text = ""
    pmids = ""
    for i in range(BATCH_SIZE):
        batch_nr = randint(0, len(abstracts))
        pmid, abstract = abstracts[batch_nr]
        text += abstract
        print("\nAbstract PMID:", pmid)
        print(abstract)

    pos_tags = sNLP.pos_tag(text)
    dependencies = sNLP.dependency_parse(text)


    d_words = ["ROOT"]
    for i in range(len(pos_tags)):
        d_words.append(pos_tags[i][0])

    print("\n### SENTENCE HEADS")
    for dependency in dependencies:
        if dependency[0] == "ROOT":
            to_i = dependency[2]
            to_w = d_words[to_i]
            print(to_w +  " (" + str(to_i-1) + ")")


    print("\n### POS TAGS:")
    print("W\tPOS")
    for i in range(len(pos_tags)):
        w = pos_tags[i][0]
        d_words.append(w)
        pos = pos_tags[i][1]
        print(w + "\t" + pos)


    print("\n### DEPENDENCIES:")
    if MODE in(STANDARD_DEPENDENCIES_INDICES, STANDARD_DEPENDENCIES_WORDS):
        print("deprel\tfrom\tto")
    for i in range(len(dependencies)):
        deprel = dependencies[i][0]
        from_i = dependencies[i][1]
        to_i = dependencies[i][2]

        from_w = d_words[from_i]
        to_w = d_words[to_i]
        if MODE == STANDARD_DEPENDENCIES_INDICES:
            print(deprel + "\t" + str(from_i) + "\t" + str(to_i))
        elif MODE == STANDARD_DEPENDENCIES_WORDS:
            print(deprel + "\t" + from_w + "\t" + to_w)
        elif MODE == SIMPLE_DEPENDENCIES:
            print(from_w + "\t--" + deprel + "->\t" + to_w)




    # print("Annotate:", sNLP.annotate(text))
    # tokens = sNLP.word_tokenize(text)

    # sNLP.word_tokenize(text)
    # print("NER:", sNLP.ner(text))
    # print("Parse:", sNLP.parse(text))
    # print(sNLP.dependency_parse(text))
    sNLP.close()
