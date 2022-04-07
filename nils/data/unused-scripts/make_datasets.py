import json
import os
import random
from collections import defaultdict
from typing import DefaultDict, List

directory = "processed/"
directory_out = "datasets/"

# add up to 1
r_train = 0.8
r_dev = 0.1
r_test = 0.1



def make_data_dict():

    entry_set: DefaultDict[str, list()] = defaultdict(lambda: list())

    for filename in os.listdir(directory):
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

    print("\nlabel" + " "*25 + "count\n" + "-"*40)
    for label in cl_set:
        for entry in cl_set[label]:
            counter[entry["custom_label"]] += 1

        print(label + " "*(30-len(label)) + str(counter[label]))
    print()

    return cl_set

def format_dataset(dataset, scaling_factor: int, balance: bool):
    '''
    Can be useful for experimentation

        - scaling_factor:       percentage of which the dataset will be scaled down to
        - balance:              make label sets of equal cardinality

        Function contains exclude_set, and will exclude labels in this set from the dataset
    '''

    master_set: DefaultDict[str, list()] = defaultdict(lambda: list())
    master_list = list()

    # Exclude labels with small size
    exclude_set = {"OTHER"}

    for entry in dataset:
        if not entry["custom_label"] in exclude_set:
            master_set[entry["custom_label"]].append(entry)


    trunc_value = min([len(master_set[label]) for label in master_set])

    for label in master_set:
        if not balance:
            trunc_value = len(master_set[label])

        master_set[label] = master_set[label][:int(trunc_value*scaling_factor)]
        master_list += master_set[label]

    random.shuffle(master_list)
    return master_list


# Takes output from make_data_dict()
def make_datasets(entry_set):

    assert r_train + r_dev + r_test == 1.0

    statistics: DefaultDict[str, defaultdict()] = defaultdict(lambda: defaultdict(int))
    master_set: DefaultDict[str, list()] = defaultdict(lambda: list())

    train_set       = list()
    dev_set         = list()
    test_set        = list()

    for custom_label in entry_set:
        for i, entry in enumerate(entry_set[custom_label]):
            master_set[custom_label].append(entry)

        label_list = master_set[custom_label]
        length = len(label_list)

        e_train = int(length*r_train)
        e_dev = int(length*(r_train+r_dev))

        train_set   += label_list[0:e_train]
        dev_set     += label_list[e_train: e_dev]
        test_set    += label_list[e_dev:]

        statistics["train"][custom_label]   = e_train
        statistics["train"]["total"]       += e_train

        statistics["dev"][custom_label]     = e_dev - e_train
        statistics["dev"]["total"]         += e_dev - e_train

        statistics["test"][custom_label]    = length - e_dev
        statistics["test"]["total"]        += length - e_dev

    # shuffle partitioned data (not needed when format_dataset is called)
    # random.shuffle(train_set)
    # random.shuffle(dev_set)
    # random.shuffle(test_set)

    # Format and truncate label sets to be of equal size for experimentation
    train_set   = format_dataset(train_set, 1.0, False)
    dev_set     = format_dataset(dev_set, 1.0, False)
    test_set    = format_dataset(test_set, 1.0, False)

    with open(directory_out + "train.txt", "w", encoding='utf8') as train, \
        open(directory_out + "dev.txt", "w", encoding='utf8') as dev, \
        open(directory_out + "test.txt", "w", encoding='utf8') as test, \
        open(directory_out + "statistics.txt", "w", encoding='utf8') as stats:

        for entry in train_set:
            train.write(json.dumps(entry, ensure_ascii=False) + "\n")

        for entry in dev_set:
            dev.write(json.dumps(entry, ensure_ascii=False) + "\n")

        for entry in test_set:
            test.write(json.dumps(entry, ensure_ascii=False) + "\n")

        for set in statistics:
            stats.write(set + "_set\n" + "-"*50 + "\n")
            stats.write("label" + " "*25 + "count" + "\t" + "%\n")
            stats.write("- "*25 + "\n")
            stats.write("total" + " "*25 + str(statistics[set]["total"]) + "\t" +
                        str(round(100*statistics[set]["total"]/statistics[set]["total"], 2)) + "\n")

            for custom_label in statistics[set]:
                if custom_label == "total":
                    continue

                stats.write(custom_label + " "*(30-len(custom_label)) + str(statistics[set][custom_label]) + "\t" +
                            str(round(100*statistics[set][custom_label]/statistics[set]["total"], 2)) + "\n")
            stats.write("-"*50 + "\n\n")

entry_set = make_data_dict()
custom_entry_set = map_chemprot_labels_to_custom_labels(entry_set)

make_datasets(custom_entry_set)




