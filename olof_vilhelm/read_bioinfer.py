import sys
import xml.etree.cElementTree as ET

""" Part of a 'gist', retrieved at 2019-06-06, from https://gist.github.com/cbare/4678963 made by Christopher Bare (cbare)
at https://cbare.github.io/ or https://github.com/cbare """
class Dynamic(dict):
    """Dynamic objects are just bags of properties, some of which may happen to be functions"""
    def __init__(self, **kwargs):
        self.__dict__ = self
        self.update(kwargs)

    def __setattr__(self, name, value):
        import types
        if isinstance(value, types.FunctionType):
            self[name] = types.MethodType(value, self)
        else:
            super(Dynamic, self).__setattr__(name, value)


class BioInfer:
    NEGATIVE_CLASSES = {"INHIBIT", "DOWNREGULATE", "SUPPRESS"}
    POSITIVE_CLASSES = {"MEDIATE", "UPREGULATE", "STIMULATE", "ACTIVATE", "CATALYZE"}

    def __init__(self, filename):
        self.__sentences = dict()

        self.__t_id_t_index_dict = dict()
        self.__st_id_st_index_dict = dict()
        self.__e_id_e_index_dict = dict()

        root = ET.parse(filename).getroot()
        if root.tag == "bioinfer":
            sentences = root.find("sentences")
            for sntnc in sentences.findall("sentence"):
                s_id = sntnc.attrib["id"]
                s_text = sntnc.attrib["origText"]
                s = {"text": s_text, "id": s_id}
                self.__sentences[s_id] = s

                self.__sentences[s_id]['tokens'] = list()
                self.__sentences[s_id]['subtokens'] = list()
                self.__t_id_t_index_dict[s_id] = dict()
                self.__st_id_st_index_dict[s_id] = dict()
                t_counter = 0
                st_counter = 0
                for tkn in sntnc.findall("token"):
                    t_id = tkn.attrib["id"]
                    t_text = ""

                    for subtoken in tkn.findall("subtoken"):
                        t_text += subtoken.attrib["text"]
                        st_id = subtoken.attrib["id"]
                        st_text = subtoken.attrib["text"]
                        sbtkn = {"text": st_text, "id": st_id}
                        self.__sentences[s_id]['subtokens'].append(sbtkn)
                        self.__st_id_st_index_dict[s_id][st_id] = st_counter
                        st_counter += 1

                    t = {"text": t_text, "id": t_id}
                    self.__sentences[s_id]['tokens'].append(t)
                    self.__t_id_t_index_dict[s_id][t_id] = t_counter
                    t_counter += 1

                self.__sentences[s_id]['dependencies'] = list()
                links = None
                for lnkg in sntnc.find("linkages").findall("linkage"):
                    if lnkg.attrib["type"] == "stanford":
                        links = lnkg
                        break

                for link in links.findall("link"):
                    t_id_1 = link.attrib["token1"]
                    t_id_2 = link.attrib["token2"]
                    deprel = link.attrib["type"]
                    if deprel == "None":
                        continue
                    head_id = None
                    word_id = None
                    if "<" in deprel:
                        head_id = t_id_2
                        word_id = t_id_1
                    elif ">" in deprel:
                        head_id = t_id_1
                        word_id = t_id_2

                    deprel = deprel.replace("<", "").replace(">", "")
                    head_index = self.__t_id_t_index_dict[s_id][head_id]
                    word_index = self.__t_id_t_index_dict[s_id][word_id]
                    dpndncy = {
                        "deprel": deprel,
                        "head": head_index,
                        "word": word_index,
                        "head_id": head_id,
                        "word_id": word_id
                    }
                    self.__sentences[s_id]['dependencies'].append(dpndncy)

                self.__sentences[s_id]['entities'] = list()
                self.__e_id_e_index_dict[s_id] = dict()
                e_counter = 0
                for entity in sntnc.findall("entity"):
                    e_id = entity.attrib["id"]
                    e_type = entity.attrib["type"]
                    e_st_ids = list()
                    for e_sbtkns in entity.findall("nestedsubtoken"):
                        e_st_ids.append(e_sbtkns.attrib["id"])
                    e_text = ""
                    for i in range(len(e_st_ids)):
                        e_st_id = e_st_ids[i]
                        e_st_index = self.__st_id_st_index_dict[s_id][e_st_id]
                        e_text += self.__sentences[s_id]['subtokens'][e_st_index]["text"]
                        if i+1 in range(len(e_st_ids)):
                            e_st_id_prev = e_st_ids[i-1]
                            if not BioInfer.__from_same_token(e_st_id, e_st_id_prev):
                                e_text += " "

                    ntty = {
                        "id": e_id,
                        "type": e_type,
                        "text": e_text,
                        "st_ids": e_st_ids
                    }
                    self.__sentences[s_id]['entities'].append(ntty)
                    self.__e_id_e_index_dict[s_id][e_id] = e_counter
                    e_counter += 1

                self.__sentences[s_id]['relations'] = list()
                for formula in sntnc.find("formulas").findall("formula"):
                    rel_e = formula.find("relnode")
                    if "entity" in rel_e.attrib:
                        rel_e_id = rel_e.attrib["entity"]
                    rel_bioinfer_class = rel_e.attrib["predicate"]

                    rel_entities = rel_e.findall("entitynode")
                    if len(rel_entities) == 2:
                        source_entity_id = rel_entities[0].attrib["entity"]
                        target_entity_id = rel_entities[1].attrib["entity"]
                        source_entity_index = self.__e_id_e_index_dict[s_id][source_entity_id]
                        target_entity_index = self.__e_id_e_index_dict[s_id][target_entity_id]
                        source_text = self.__sentences[s_id]["entities"][source_entity_index]["text"]
                        target_text = self.__sentences[s_id]["entities"][target_entity_index]["text"]
                        rel_class = "OTHER"
                        if rel_bioinfer_class in BioInfer.NEGATIVE_CLASSES:
                            rel_class = "NEGATIVE"
                        elif rel_bioinfer_class in BioInfer.POSITIVE_CLASSES:
                            rel_class = "POSITIVE"

                        rel_fine_class = ""
                        rel_e_index = -1
                        if "entity" in rel_e.attrib:
                            rel_e_index = self.__e_id_e_index_dict[s_id][rel_e_id]
                            rel_fine_class = self.__sentences[s_id]['entities'][rel_e_index]["text"]
                        rltnshp = {
                            "source": {
                                "index": source_entity_index,
                                "id": source_entity_id,
                                "text": source_text,
                            },
                            "target": {
                                "index": target_entity_index,
                                "id": target_entity_id,
                                "text": target_text
                            },
                            "relation": {
                                "index": rel_e_index,
                                "id": rel_e_id,
                                "text": rel_fine_class,
                                "class": rel_class,
                                "fine_class": rel_fine_class,
                                "bioinfer_class": rel_bioinfer_class,
                                "bioinfer_rel_entity_index": rel_e_index
                            }
                        }
                        self.__sentences[s_id]['relations'].append(rltnshp)

        else:
            print("File \'" + filename + "\' is not a bioinfer corpus.")
            exit(1)

    @staticmethod
    def __from_same_token(st1_id, st2_id):
        type_1 = st1_id.split(".")[0]
        type_2 = st2_id.split(".")[0]
        if type_1 == "st" and type_2 == "st":
            s_id_1 = st1_id.split(".")[1]
            s_id_2 = st2_id.split(".")[1]
            t_id_1 = st1_id.split(".")[2]
            t_id_2 = st2_id.split(".")[2]
            if s_id_1 == s_id_2 and t_id_1 == t_id_2:
                return True

        return False

    def sentences(self):
        return self.__sentences


# SEE HERE FOR USAGE OF BioInfer CLASS
if __name__ == "__main__":

    # JUST SOME COMMAND-LINE OPTIONS
    sentence_nr = 0
    sentence_id = ""
    if len(sys.argv) > 1:
        try:
            sentence_nr = int(sys.argv[1])
        except ValueError:
            if sys.argv[1] == "id" and len(sys.argv) > 2:
                sentence_id = sys.argv[2]
            else:
                print("Incorrect input. Exiting...")
                exit()

    # MAIN USE OF BioInfer CLASS
    fn = "corpus/BioInfer_corpus_1.2.0b.binarised.xml"
    print("Reading file: '" + fn + "'.")
    bioinfer = BioInfer(fn)
    sentence = None
    s_cnt = 0
    for s_id in bioinfer.sentences():
        if sentence_nr == s_cnt:
            sentence = bioinfer.sentences()[s_id]
            break
        s_cnt += 1

    if sentence_id != "":
        sentence = bioinfer.sentences()[sentence_id]
    else:
        sentence_id = sentence['id']

    tokens = sentence['tokens']
    dependencies = sentence['dependencies']
    entities = sentence['entities']
    relations = sentence['relations']

    print("\nSentence " + str(sentence_nr) + " of " + str(len(bioinfer.sentences())) + " sentences, id:", sentence_id)
    print(sentence["text"])

    print("\nEntities:")
    for i in range(len(entities)):
        entity = entities[i]
        print(str(i) + "\t" + entity["text"] + "\t" + entity["type"] + "\t(" + entity["id"] + ")")

    print("\nRelations:")
    if len(relations) == 0:
        print("No relations.")
    for relation in relations:
        src = relation["source"]
        tgt = relation["target"]
        rel = relation["relation"]
        print(src['text'] + " [" + src['id'] + "]\t" + rel['text'] + " [" + rel['bioinfer_class'] + "]" + "\t" + tgt['text'] + " [" + tgt['id'] + "]")

    print("\nTokens:")
    for i in range(len(tokens)):
        token = tokens[i]
        print(str(i) + "\t" + token["text"] + "\t(" + token["id"] + ")")

    print("\nDependencies:")
    for dependency in dependencies:
        h_index = dependency["head"]
        w_index = dependency["word"]
        h_text = tokens[h_index]["text"]
        w_text = tokens[w_index]["text"]
        print(dependency["deprel"] + "\t" + h_text + " [" + str(h_index) + "]\t" + w_text + " [" + str(w_index) + "]")
