# Creates a text string from the corpus as well as a set of character ranges that contain all the entities found in the corpus
def getCorpus():
    corpus = ""
    entities = set()

    test = open("in/test.tsv", "r")

    prot = False
    for line in test:
        line = line.strip()

        if not line:
            corpus += "\n"
            continue

        # Just to avoid leading space
        if corpus:
            corpus += " "

        line = line.split("\t")
        if prot:
            if line[1] == "B":
                entities.add((start, stop))
                start = len(corpus)
            elif line[1] == "O":
                entities.add((start, stop))
                prot = False
        else:
            if line[1] == "B":
                start = len(corpus)
                prot = True
        corpus += line[0]
        stop = len(corpus)

    return corpus, entities
