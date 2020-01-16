import pickle
import regex as re
from corpus import getCorpus
from mentionindex import MentionIndex
from docria import Document, DataTypes as T


mi = MentionIndex()
mi.connect_jvm(6006)

index = mi.load_keyed_index("out/index.fst")
corpus, entities = getCorpus()

doc = Document()
doc.maintext = corpus
doc = mi.process(index, doc)

matches = [(match["text"].start, match["text"].stop) for match in doc["matches"]]

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

pickle.dump(matches, open("out/dictMatches.out", "wb"))