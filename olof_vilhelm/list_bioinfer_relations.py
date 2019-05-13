import sys
from read_bioinfer import BioInfer

if __name__ == "__main__":
    fn = "corpus/BioInfer_corpus_1.1.1.xml"
    bioinfer = BioInfer(fn)
    long = False
    if len(sys.argv) > 1:
        if "s" in sys.argv[1]:
            long = True
    posneg_relations = 0
    other_relations = 0
    for sentence in bioinfer.sentences():
        interesting_sentence = False
        s_id = sentence["id"]
        for relation in bioinfer.relationships(s_id):
            if relation["class"] != "OTHER":
                interesting_sentence = True
                break

        if interesting_sentence:
            relationships = bioinfer.relationships(s_id)
            entities = bioinfer.entities(s_id)
            print("\nSentence id:", s_id)
            print("  " + sentence["text"])
            if long:
                print("\nEntities:")
                for entity in bioinfer.entities(s_id):
                    print("  " + entity["text"] + "\t" + entity["type"] + "\t(" + entity["id"] + ")")

                print("\nRelationships:")
                if len(relationships) == 0:
                    print("No relationships.")
                for relation in relationships:
                    src_index = relation["source"]
                    src_text = entities[src_index]["text"]
                    src_id = relation["source_id"]
                    tgt_index = relation["target"]
                    tgt_text = entities[tgt_index]["text"]
                    tgt_id = relation["target_id"]

                    rel_class = relation["class"]
                    fine_rel_class = relation["fine_class"]
                    print("  " + src_text + " [" + src_id + "]\t" + rel_class + "(" + fine_rel_class + ")" + "\t" + tgt_text + " [" + tgt_id + "]")

                print("\n######################################################")
            else:
                for relation in relationships:
                    if relation["class"] != "OTHER":
                        posneg_relations += 1
                        src_index = relation["source"]
                        src_text = entities[src_index]["text"]
                        tgt_index = relation["target"]
                        tgt_text = entities[tgt_index]["text"]
                        rel_class = relation["class"]
                        fine_rel_class = relation["fine_class"]
                        print(
                            "  " + src_text + "\t" + rel_class + "(" + fine_rel_class + ")" + "\t" + tgt_text)
                    else:
                        other_relations += 1

    print()
    print(posneg_relations, "POSITIVE/NEGATIVE relations found.")
    print(other_relations, "OTHER relations discarded.")
