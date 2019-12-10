import pickle

combined = pickle.load(open("out/combined.out", "rb"))

dictBySpecies = {}
for key in combined:
    dictByName = {}
    if "speciesName" in combined[key]:
        dictBySpecies.setdefault(combined[key]["speciesName"], dictByName)
    else:
        dictBySpecies.setdefault("-1", dictByName)

    if "altNames" in combined[key]:
        altNames = combined[key]["altNames"]

        for altName in altNames:
            dictByName.setdefault(altName, set()).add(key)

        if "name" in combined[key]:
            dictByName.setdefault(combined[key]["name"], set()).add(key)

counter = 0
for species in dictBySpecies:
    dictByName = dictBySpecies[species]

    for key in dictByName:
        altNames = dictByName[key]
        if len(altNames) > 1:
            counter += 1

print(len(dictBySpecies))
print(counter)
print(len(combined))
