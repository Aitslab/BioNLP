import json

from collections import defaultdict
from typing import DefaultDict, List

directory = "/content/drive/MyDrive/nlp_2021_alexander_petter/utils/chemprot/processed/"
directory_out = "/content/drive/MyDrive/nlp_2021_alexander_petter/utils/chemprot/custom_label_datsets/"

def make_data_dict(filename):

    entry_set: DefaultDict[str, list()] = defaultdict(lambda: list())

    with open(directory + filename, "r", encoding='utf8') as f:
        data_list = f.readlines()

        for line in data_list:
            entry = json.loads(line)
            entry_set[entry["label"]].append(entry)

    return entry_set

def map_chemprot_labels_to_custom_labels(cpl_set):
    '''
    Maps ChemProt relation-labels to Custom relation-labels

    cid   Custom class                  cpr     ChemProt
    -------------------------------------------------------------------------------------
    0   NOT                             10      NOT

    1   PART-OF                         1       PART-OF

    2   INTERACTOR                      2       REGULATOR
                                        2       DIRECT-REGULATOR
                                        2       INDIRECT-REGULATOR
                                        5       AGONIST
                                        7       MODULATOR
                                        8       CO-FACTOR
                                        9       SUBSTRATE

    3   REGULATOR-POSITIVE              3       UPREGULATOR
                                        3       ACTIVATOR
                                        3       INDIRECT-UPREGULATOR
                                        5       AGONIST-ACTIVATOR
                                        7       MODULATOR-ACTIVATOR

    4   REGULATOR-NEGATIVE              4       DOWNREGULATOR
                                        4       INHIBITOR
                                        4       INDIRECT-DOWNREGULATOR
                                        6       ANTAGONIST
                                        7       MODULATOR-INHIBITOR
                                        5       AGONIST-INHIBITOR

    5   OTHER                                   all labels not included above
    '''

    cl_to_cid = {"NOT":                 "0",
                 "PART-OF":             "1",
                 "INTERACTOR":          "2",
                 "REGULATOR-POSITIVE":  "3",
                 "REGULATOR-NEGATIVE":  "4",

                 "OTHER":               "5"
                 }

    cpl_to_cl = {"PART-OF":                 "PART-OF",

                 "REGULATOR":               "INTERACTOR",
                 "DIRECT-REGULATOR":        "INTERACTOR",
                 "INDIRECT-REGULATOR":      "INTERACTOR",
                 "MODULATOR":               "INTERACTOR",
                 "COFACTOR":                "INTERACTOR",
                 "SUBSTRATE":               "INTERACTOR",
                 "SUBSTRATE_PRODUCT-OF":    "INTERACTOR",
                 "PRODUCT-OF":              "INTERACTOR",
                 "AGONIST":                 "INTERACTOR",

                 "UPREGULATOR":             "REGULATOR-POSITIVE",
                 "ACTIVATOR":               "REGULATOR-POSITIVE",
                 "INDIRECT-UPREGULATOR":    "REGULATOR-POSITIVE",
                 "AGONIST-ACTIVATOR":       "REGULATOR-POSITIVE",
                 "MODULATOR-ACTIVATOR":     "REGULATOR-POSITIVE",

                 "DOWNREGULATOR":           "REGULATOR-NEGATIVE",
                 "INHIBITOR":               "REGULATOR-NEGATIVE",
                 "INDIRECT-DOWNREGULATOR":  "REGULATOR-NEGATIVE",
                 "ANTAGONIST":              "REGULATOR-NEGATIVE",
                 "MODULATOR-INHIBITOR":     "REGULATOR-NEGATIVE",
                 "AGONIST-INHIBITOR":       "REGULATOR-NEGATIVE",

                 "NOT":                     "NOT",

                 "UNDEFINED":               "OTHER"
                 }

    cl_set: DefaultDict[str, list()] = defaultdict(lambda: list())

    for label in cpl_set:
        for entry in cpl_set[label]:
            chemprot_label = entry["label"]
            custom_label = cpl_to_cl[chemprot_label]
            custom_id = cl_to_cid[custom_label]

            entry["cid"] = custom_id
            entry["custom_label"] = custom_label

            cl_set[custom_label].append(entry)


    counter = {
        "PART-OF": 0,
        "INTERACTOR": 0,
        "REGULATOR-POSITIVE": 0,
        "REGULATOR-NEGATIVE": 0,
        "NOT": 0,
        "OTHER": 0
    }

    return cl_set

def write_files(entry_set, filename):
  result_set = list()

  master_set: DefaultDict[str, list()] = defaultdict(lambda: list())

  for custom_label in entry_set:
      for i, entry in enumerate(entry_set[custom_label]):
          master_set[custom_label].append(entry)

      label_list = master_set[custom_label]
      result_set += label_list

  with open(directory_out + filename, "w", encoding='utf8') as out_file: #, \
      
      for entry in result_set:
          out_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

io_files = [("chemprot_training_processed.txt", "train.txt"), ("chemprot_development_processed.txt", "dev.txt"), ("chemprot_test_processed.txt", "test.txt")]

for i, o in io_files:
  entry_set = make_data_dict(i)
  custom_entry_set = map_chemprot_labels_to_custom_labels(entry_set)
  write_files(custom_entry_set, o)