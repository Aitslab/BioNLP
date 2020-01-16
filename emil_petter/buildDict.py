import pickle
import regex as re
from protein import Protein
from mentionindex import MentionIndex

# We could not find the original text file to test the dictionary on.
# Since the test file is split on spaces, you can't be certain where the spaces around symbols should be.
# This method will create an alternate version of words where all symbols have spaces around them


def altVersion(token):
    token = token.replace("(", " ( ")
    token = token.replace(")", " ) ")
    token = token.replace(".", " . ")
    token = token.replace(",", " , ")
    token = token.replace("[", " [ ")
    token = token.replace("]", " ] ")
    token = token.replace("-", " - ")
    token = token.replace("/", " / ")
    token = token.replace("+", " + ")
    token = token.replace("%", " % ")
    token = token.replace(":", " : ")
    token = token.replace(";", " ; ")
    token = token.replace("=", " = ")
    token = token.replace("'", " ' ")
    token = token.replace("`", " ` ")
    token = token.replace("<", " < ")
    token = token.replace(">", " > ")
    token = token.replace("&", " & ")
    token = token.replace("?", " ? ")
    token = token.replace("*", " * ")
    token = re.sub("[ ]+", " ", token)
    return token.strip()


# Creates a unique ID for all proteins based on which species it is found in
def createID(prot, counter):
    species = 0
    if prot.species_id is not None:
        species = int(prot.species_id)
    return "LUGE" + "{:08d}".format(species) + "{:08d}".format(counter)


# Combines the proteins from the 2 dictionaries and removes any overlap
def combineDicts(combined, dataDict):
    for prot in dataDict:
        match = None
        IDs = []

        for ID in prot.uniprot_id:
            IDs.append(ID)
            if ID in combined:
                match = combined[ID]

        for ID in prot.hgnc_id:
            IDs.append(ID)
            if ID in combined:
                match = combined[ID]

        if match is not None:
            match.update(prot)

        for ID in IDs:
            if ID not in combined:
                combined[ID] = prot


def main():
    combinedNoID = {}

    uniprot = pickle.load(open("out/uniprotID.out", "rb"))
    combineDicts(combinedNoID, uniprot)

    hgnc = pickle.load(open("out/hgncID.out", "rb"))
    combineDicts(combinedNoID, hgnc)

    counter = 0
    combined = {}
    for prot in combinedNoID.values():
        if prot.id is None:
            prot.id = createID(prot, counter)
            combined[prot.id] = prot
            counter += 1

    # Creates a tab delimited index with two columns; the protein name and its corresponding ID
    index = open("out/index.txt", "w+")
    for key, entry in combined.items():
        for name in entry.names:
            index.write(name.strip() + "\t" + key + "\n")
            index.write(altVersion(name) + "\t" + key + "\n")
    index.close()

    # Uses Marcus Klang's MentionIndex to generate a tokenized and cleaned up index
    # Can be used later on to run his dictionary tagger
    mi = MentionIndex()
    mi.connect_jvm(6006)
    mi.build_keyed_index("out/index.txt", "out/index.fst")


if __name__ == "__main__":
    main()
