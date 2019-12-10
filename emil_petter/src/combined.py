import pickle


def createID(data, counter):
    species = 0
    if data["speciesID"] is not None:
        species = int(data["speciesID"])
    return "LUGE" + "{:08d}".format(species) + "{:08d}".format(counter)


def combineDicts(combined, dataDict, idKey):
    for ID, entry in dataDict.items():
        if ID in combined.setdefault(idKey, {}):
            newIDs = combineEntries(combined[idKey][ID], entry)
            for newID in newIDs:
                combined.setdefault(newID[0], {})[newID[1]] = combined[idKey][ID]
        else:
            for key in entry:
                if key.endswith("ID") and key != "speciesID":
                    for ID in entry[key]:
                        combined.setdefault(key, {})[ID] = entry


def combineEntries(combined, new):
    keys = set(combined.keys())
    keys.update(new.keys())
    newIDs = []

    for key in keys:
        if key in combined and key in new:
            if isinstance(combined[key], set):
                combined[key].update(new[key])
            else:
                if key == "name" and combined[key] != new[key]:
                    combined.setdefault("altNames", set()).add(new[key])
        elif key in new:
            if key.endswith("ID") and key != "speciesID":
                for ID in new[key]:
                    newIDs.append((key, ID))
            combined[key] = new[key]

    if "name" in combined and combined["name"] in combined["altNames"]:
        combined["altNames"].remove(combined["name"])

    return newIDs


def main():
    f = open("out/uniprot.out", "rb")
    uniprot = pickle.load(f)
    f.close()

    f = open("out/hgnc.out", "rb")
    hgnc = pickle.load(f)
    f.close()

    combinedNoID = {}

    combineDicts(combinedNoID, uniprot, "uniprotID")
    del uniprot

    combineDicts(combinedNoID, hgnc, "hgncID")
    del hgnc

    combined = {}
    counter = 0
    for idkey in combinedNoID:
        for entry in combinedNoID[idkey].values():
            if "skip" not in entry:
                entry["skip"] = True
                ID = createID(entry, counter)
                combined[ID] = entry
                counter += 1
    del combinedNoID

    f = open("out/combined.out", "wb")
    pickle.dump(combined, f)
    f.close()


if __name__ == "__main__":
    main()
