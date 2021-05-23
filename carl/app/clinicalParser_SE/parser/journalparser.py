from .spacyloader import load_nlp

file = open("", "r")
doc = file.read()

load_nlp()

nlp_doc = nlp(doc)


width = 15
for token in nlp_doc:
    print(f"{token.text: <{width}} {token.tag_: <{width}} {token.dep_: <{width}}")
    
for ent in nlp_doc.ents:
    print(ent.text, ent.label_)

