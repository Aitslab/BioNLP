import sys, os, pathlib, json
from os import listdir
from os.path import isfile, join
import time

def update_scoredict(scoredict, dict_denot, dict_gold):
    cats = list(scoredict.keys())
    for denot in dict_denot["denotations"]:
        this_cat = denot["id"]
        if this_cat in cats:
            scoredict[this_cat]["ent_ret"] += 1
            
            for gold_denot in dict_gold["denotations"]:
                if gold_denot["span"] == denot["span"] and gold_denot["id"] == this_cat:
                    scoredict[this_cat]["real_ent_ret"] += 1
     

    for gold_denot in dict_gold["denotations"]:
        this_cat = gold_denot["id"]
        if this_cat in cats:
            scoredict[this_cat]["real_ent"] += 1
    
def get_recall(real_entities, real_entities_retrieved):
    if real_entities == 0:
        recall = '0 real ent'
    else:
        recall = real_entities_retrieved/real_entities
    return recall

def get_precision(real_entities_retrieved, entities_retrieved):
    if entities_retrieved == 0:
        precision = '0 ent ret'
    else:
        precision = real_entities_retrieved/entities_retrieved
    return precision

def get_dicts(folder_path):
    papers = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    dicts = []

    for filename in papers:
        with open(folder_path + filename, 'r') as f:
            one_dict = json.load(f)
            dicts.append(one_dict)
    dicts = sorted(dicts, key=lambda i: i['text'])
    return dicts

def main():
    #setting up gold dicts
    gold_folder_path = os.path.abspath("gold_standard_corpus_splitted_title_abstract") + "/"
    gold_dicts = get_dicts(gold_folder_path)

    #setting up our dicts
    denot_folder_path = os.path.abspath("gold_papers_tagged") + "/"
    denot_dicts = get_dicts(denot_folder_path)

    #setting up cats and dict for separate class scoring
    cats = ["Virus_SARS-CoV-2", "Disease_COVID-19", "Symptom_COVID-19"]
    entlist = ["real_ent_ret", "real_ent", "ent_ret"]
    entdict = dict(zip(entlist, [0 for i in range(len(cats))]))
    scoredict = dict(zip(cats, [entdict.copy() for i in range(len(cats))]))

    #evaluation
    for dict_gold, dict_denot in zip(gold_dicts, denot_dicts):
        update_scoredict(scoredict, dict_denot, dict_gold)

    rec_prec = ["recall", "precision"]
    rec_prec_init = dict(zip(rec_prec, [0 for i in range(len(rec_prec))]))
    rec_prec_dict = dict(zip(cats, [rec_prec_init.copy() for i in range(len(cats))]))
    for cat in scoredict:
        rec_prec_dict[cat]["recall"] = get_recall(scoredict[cat]["real_ent"], scoredict[cat]["real_ent_ret"])
        rec_prec_dict[cat]["precision"] = get_precision(scoredict[cat]["real_ent_ret"], scoredict[cat]["ent_ret"])
   
    tot_prec, tot_rec, tot_tp, tot_fp, tot_fn = 0, 0, 0, 0, 0
    for cat in cats:
        tot_prec += rec_prec_dict[cat]["precision"]
        tot_rec += rec_prec_dict[cat]["recall"]
        tp = scoredict[cat]["real_ent_ret"]
        fp = scoredict[cat]["ent_ret"] - scoredict[cat]["real_ent_ret"]
        fn = scoredict[cat]["real_ent"] - scoredict[cat]["real_ent_ret"]

        tot_tp += tp
        tot_fp += fp
        tot_fn += fn

        print(cat + " precision: " + str(rec_prec_dict[cat]["precision"]))
        print(cat + " recall: " + str(rec_prec_dict[cat]["recall"]))
        print(cat + " true positives: " + str(tp))
        print(cat + " false positives: " + str(fp))
        print(cat + " false negatives: " + str(fn))
        print()

    
    macro_prec = tot_prec/len(cats)
    macro_rec = tot_rec/len(cats)
    micro_prec = tot_tp/(tot_tp+tot_fp)
    micro_rec = tot_tp/(tot_tp+tot_fn)
    macro_f1 = 2*macro_prec*macro_rec/(macro_prec + macro_rec)
    micro_f1 = 2*micro_prec*micro_rec/(micro_prec + micro_rec)

    print("macro precision:" + str(macro_prec) + "\n"
    "macro recall: " + str(macro_rec) + "\n"
    "micro precision :" + str(micro_prec) + "\n"
    "micro recall: " + str(micro_rec) + "\n"
    "macro F1: " + str(macro_f1) + "\n"
    "micro F1: " + str(micro_f1) + "\n")


if __name__ == '__main__':
    t0 = time.clock()
    main()
    print(time.clock() - t0)