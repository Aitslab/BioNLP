import random
import json
import numpy as np

# read files in artificial-custom-labeled/chemical-protein, 
# create new file with chemprot_train + chosen parts of above (set weights on each class)

relations = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE"]

# train_path = "corpora/chemprot_train.txt"
# artificial_custom_class_folder= "data/artificial-custom-labeled/chemical-protein/"
# output_path = "corpora/mixed-train-v1.txt"

# artificial_ratio = 0.25


#Creates list of examples from artificial data for each class using the files created in build_art_corpus.py
def create_artificial_class_list(artificial_custom_class_folder):
    artificial_class_lists = {}
    for relation in relations:
        artificial_class_lists[relation] = []
        with open(artificial_custom_class_folder+'corpus_PC-{}-PC_1-2.txt'.format(relation), encoding = 'utf-8') as file:  
            for line in file:
                artificial_class_lists[relation].append(line.replace('\n',''))
    return artificial_class_lists


def write_corpus(train_path, artificial_class_lists, artificial_ratio, output_path):
    with open(output_path, 'x', encoding='utf-8') as outfile:
        num_lines = sum(1 for line in open(train_path, encoding='utf-8'))
        with open(train_path, 'r', encoding='utf-8') as real_corp:
            contents=real_corp.read()
            outfile.write(contents)
        for relation in relations:
            #replace int(num_lines*artificial_ratio/5) with artificial_ratio[relation] if dictionary with individual weights for each class 
            for line in random.sample(artificial_class_lists[relation], int(num_lines*artificial_ratio/5)):
                outfile.write("\n" + line)

def run(train_path, artificial_path, artificial_ratio, output_path):
    artificial_class_lists = create_artificial_class_list(artificial_path)
    write_corpus(train_path, artificial_class_lists, artificial_ratio, output_path)
