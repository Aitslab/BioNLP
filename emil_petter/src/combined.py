import pickle


def createID(data, counter):
    if data["speciesID"] is not None:
        return "LUGE" + "{:08d}".format(int(data["speciesID"])) + "{:08d}".format(counter)
    else:
        return "LUGE00000000" + "{:08d}".format(counter)


def combine(main, other):
    combinedAltNames = set()
    combinedAltNames.update(main["altNames"])
    combinedAltNames.update(other["altNames"])
    combined = {**other, **main}
    combined["altNames"] = combinedAltNames
    return combined


uniprot = pickle.load(open("uniprot.out", "rb"))
hgnc = pickle.load(open("hgnc.out", "rb"))

hgncIDset = set()
for uniprotID, data in uniprot.items():
    if "hgncID" in data:
        hgncID = data["hgncID"]
        if hgncID in hgnc:
            uniprot[uniprotID] = combine(data, hgnc[hgncID])
            hgncIDset.add(hgncID)

hgncNoDuplicate = {}
for hgncID, hgncData in hgnc.items():
    if hgncID in hgncIDset:
        continue
    else:
        if "uniprotID" in hgncData:
            uniprotID = hgncData["uniprotID"]
            hgncData = combine(uniprot[uniprotID], hgncData)
        hgncNoDuplicate[hgncID] = hgncData

combinedDict = {}
counter = 0

for data in uniprot.values():
    ID = createID(data, counter)
    counter += 1
    combinedDict[ID] = data

for data in hgncNoDuplicate.values():
    ID = createID(data, counter)
    counter += 1
    combinedDict[ID] = data

pickle.dump(combinedDict, open("combined.out", "wb"))
