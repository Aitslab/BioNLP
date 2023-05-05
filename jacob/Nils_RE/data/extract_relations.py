from tqdm import tqdm
import json
from collections import defaultdict
from typing import DefaultDict, List
import nltk
nltk.download('punkt')
from nltk import tokenize

p_dev = "development/drugprot_development_"
#p_sample = "sample/chemprot_sample_"
p_test = "test-background/test_background_"         # NOTE: This dir has no relations
p_train = "training/drugprot_training_"

# test "_gs", else ""
extra = ""
p = "drugprot/" + p_train

entity_markers = True

def read_entities(entities):
    entities_data: DefaultDict[str, DefaultDict[str, str]] = defaultdict(lambda: defaultdict(str))

    for line in entities:
        data = line.split("\t")
        entities_data[data[0]][data[1]] = {"type": data[2], "start_offset": int(data[3]),\
                                           "end_offset": int(data[4]), "name": data[5].strip()}

    return entities_data

def read_abstracts(abstracts):
    abstracts_data: DefaultDict[str, DefaultDict[str, str]] = defaultdict(lambda: defaultdict(str))

    for line in abstracts:
        data = line.split("\t")
        abstracts_data[data[0]] = {"title": data[1], "text": data[2]}

    return abstracts_data

def read_relations(relations):
    relations_data: DefaultDict[str, list()] = defaultdict(lambda: list())

    for line in relations:
        data = line.split("\t")
        relations_data[data[0]].append({"label": data[1],\
                                        "arg1": data[2].split(":")[1], "arg2": data[3].split(":")[1].strip()})

    return relations_data

def add_entity_markers(text, arg1_so, arg1_eo, arg2_so, arg2_eo):

    if arg1_so > arg2_so:
        tmp_arg_so = arg1_so
        tmp_arg_eo = arg1_eo
        arg1_so = arg2_so
        arg1_eo = arg2_eo
        arg2_so = tmp_arg_so
        arg2_eo = tmp_arg_eo

    text_with_entity_markers = text[:arg1_so] + "<< " + text[arg1_so:arg1_eo] + " >>" \
                                   + text[arg1_eo:arg2_so] + "[[ " + text[arg2_so:arg2_eo] \
                                   + " ]]" + text[arg2_eo:]

    text_with_entity_markers = text_with_entity_markers.replace(">>[[", ">> [[")

    return text_with_entity_markers

def extract_relevant_sentence(text, a_o, b_o):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)

    a_has_idx = False
    b_has_idx = False

    a_i = 0
    b_i = 0

    offset = 0

    for i, sentence in enumerate(sentences):
        offset += len(sentence)

        if a_o < offset and not a_has_idx:
            a_i = i
            a_has_idx = True

        if b_o < offset and not b_has_idx:
            b_i = i
            b_has_idx = True

        # Spaces are removed at the start of sentences
        offset += 1

    reappend = sentences[min(a_i, b_i): max(a_i, b_i) + 1]
    extracted = ""

    for sentence in reappend:
        extracted += " " + sentence

    return extracted.strip(), len(reappend), a_i, b_i



with open(p + "abstracts" + extra + ".tsv", "r", encoding='utf8') as f_abs,\
        open(p + "entities" + extra + ".tsv", "r", encoding='utf8') as f_ent,\
        open(p + "relations" + extra + ".tsv", encoding='utf8') as f_rel:

    abstracts = f_abs.readlines()
    entities = f_ent.readlines()
    relations = f_rel.readlines()

    abstracts_data = read_abstracts(abstracts)
    entities_data = read_entities(entities)
    relations_data = read_relations(relations)

    formatted_data = []

    for pmid in tqdm(abstracts_data):
        title = abstracts_data[pmid]["title"]
        abstract = abstracts_data[pmid]["text"]

        for relation in relations_data[pmid]:

            arg1 = relation["arg1"]
            arg2 = relation["arg2"]

            arg1_so = entities_data[pmid][arg1]["start_offset"]
            arg1_eo = entities_data[pmid][arg1]["end_offset"]
            arg2_so = entities_data[pmid][arg2]["start_offset"]
            arg2_eo = entities_data[pmid][arg2]["end_offset"]

            in_title = False

            if arg1_so < len(title):
                in_title = True
                text = title

            else:
                text = abstract

                arg1_so = arg1_so - len(title) - 1
                arg1_eo = arg1_eo - len(title) - 1
                arg2_so = arg2_so - len(title) - 1
                arg2_eo = arg2_eo - len(title) - 1

            if entity_markers:
                text = add_entity_markers(text, arg1_so, arg1_eo, arg2_so, arg2_eo)
                # adjust other offsets if they are to be used beyond this point
                arg2_so += 6

            # if-else might be unnecessary as title shouldn't have any splitting applied to it
            if not in_title:
                text, length, a_i, b_i = extract_relevant_sentence(text, arg1_so, arg2_so)
                formatted_data.append({"text": text, "metadata": [], "label": relation["label"]})

            else:
                formatted_data.append({"text": text, "metadata": [], "label": relation["label"]})

        with open("processed/" + p.split("/")[2] + "processed.txt", "w", encoding="utf8") as out:
            for item in formatted_data:
                out.write(json.dumps(item, ensure_ascii=False) + "\n")
