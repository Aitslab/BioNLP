import pickle

combined = pickle.load(open("combined.out", "rb"))

dictByName = {}
for key in combined:
    altNames = combined[key]["altNames"]
    
    for altName in altNames:
        dictByName.setdefault(altName, set()).add(key)

    if "name" in combined[key]:
        dictByName.setdefault(combined[key]["name"], set()).add(key)

ambiguous = {}
for key in dictByName:
    altNames = dictByName[key]
    if len(altNames) > 1:
        ambiguous[key] = dictByName[key]

print(len(dictByName))
print(len(ambiguous))
print(len(combined))
