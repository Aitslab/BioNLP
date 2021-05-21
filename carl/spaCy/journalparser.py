from spacyloader import load_nlp

file = open("/home/callebalik/projects/BioNLP/carl/data/corpus/mockup-patient-records/by_Anton/chart1.txt", "r")
doc = file.read()
load_nlp()
nlp_doc = nlp(doc)


width = 15
for token in nlp_doc:
    print(f"{token.text: <{width}} {token.tag_: <{width}} {token.dep_: <{width}}")
    
for ent in nlp_doc.ents:
    print(ent.text, ent.label_)