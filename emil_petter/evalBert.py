import pickle
from corpus import getCorpus

def getMatches():
    result = open("in/NER_result_conll.txt", "r")

    matches = []
    prot = False

    # Since we keep track of matches as indexes of their start and end characters
    # we use counter as a representation of that
    counter = 0
    for line in result:
        line = line.strip()

        # +1 to counter to represent newline
        if not line:
            counter += 1
            continue

        # +1 to counter to represent space
        if counter:
            counter += 1

        line = line.split(" ")
        if prot:
            if line[2] == "B-MISC":
                matches.append((start, stop))
                start = counter
            elif line[2] == "O-MISC":
                matches.append((start, stop))
                prot = False
        else:
            if line[2] == "B-MISC":
                start = counter
                prot = True
        
        counter += len(line[0])
        stop = counter
    
    return matches


def main():
    _, entities = getCorpus()
    matches = getMatches()

    nTruePositives = len(set(matches) & entities)

    nEntities = len(entities)
    nPositives = len(matches)

    recall = nTruePositives / nEntities
    precision = nTruePositives / nPositives
    f1 = (2*recall*precision) / (recall + precision)

    print("--Dictionary--")
    print("Recall:\n" + str(recall))
    print("Precision:\n" + str(precision))
    print("F1-score:\n" + str(f1))

    pickle.dump(matches, open("out/bertMatches.out", "wb"))


if __name__ == "__main__":
    main()