import xml.etree.cElementTree as xmlET
import os


def parse_training_set(file_name):
    tree = xmlET.parse(file_name)
    root = tree.getroot()

    inputs = list()
    #  print(root.tag, root.attrib)
    for sentence_list in root.findall('sentences'):
        #  print(sentence_list.tag, sentence_list.attrib)
        for sentence in sentence_list.findall('sentence'):
            entry = dict()
            entry['text'] = sentence.get('origText')
            #  print(sentence.tag, sentence.attrib)
            #  print(entry['text'])

            tokens = list()
            for token in sentence.findall("token"):
                tkn = ""
                for sub in token.findall("subtoken"):
                    tkn += sub.get("text")
                tokens.append(tkn)
            entry['tokens'] = tokens

            entities = [None] * len(tokens)
            for entity in sentence.findall("entity"):
                token_indices = list()
                if entity.get("type") != "RELATIONSHIP_TEXTBINDING":
                    for subtoken in entity.findall("nestedsubtoken"):
                        token_indices.append(int(subtoken.get("id").split(".")[2]))
                        # "st.2.6.0" where the 6 is the token index in the sentence
                    #  print(int(entity.get("id").split(".")[2]))
                    entities[int(entity.get("id").split(".")[2])] = token_indices
            entry['entities'] = entities

            interactions = list()
            predicates = list()
            for formulas in sentence.findall("formulas"):
                for formula in formulas.findall("formula"):
                    for relnode in formula.findall("relnode"):
                        entity_indices = list()
                        for node in relnode.findall("entitynode"):
                            entity_indices.append(int(node.get("entity").split(".")[2]))
                        interactions.append(entity_indices)
                        predicates.append(relnode.get('predicate').split('_'))
            entry["interactions"] = interactions
            entry['predicates'] = predicates
            inputs.append(entry)
    return inputs


# inp = parse_training_set("trainingFiles\BioInfer_corpus_1.2.0b.binarised.xml")
#  inp = parse_all_files("trainingFiles/")
#  print(inp[140])
#  print(inp[len(inp) - 1])
#  print(len(inp))