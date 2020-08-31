# This script runs the evaluator written by Annie and Sofi for their course Edan70.
# The evaluator itself is a script named 'pubannotationevaluator.py'
# The script will generate two files: false_negatives_dict.txt and false_positives_dict.txt

# Usage: the variable 'word_classes_set' will define which tags should be considered by the PubannotationEvaluator
# The variable 'tagger_output_dir_path' is a path to where your output in PubAnnotation format is stored.
# The variable 'true_output_dir_path' is the path to the Gold Standard dataset is located (also in PubAnnotation format)
# Consider that: In both the results and the ground truth there has to be the same amount of files,
# with the same file names and the same tag names. Only the specified tags will be consedered.


from pubannotationevaluator import *
import os

word_classes_set = {'Disease'}
#word_classes_set = {'Protein'}
#word_classes_set = {'Disease_COVID-19', 'Symptom', 'Virus_SARS-CoV-2'}
#word_classes_set = {'Symptom'}

tagger_output_dir_path = '/Users/Tony/Documents/BINP37/data/datasets/WilliamDisease/gold_william_results_pubanot/'
#tagger_output_dir_path = '/Users/Tony/Documents/BINP37/data/datasets/Sofi/gold_sofi_results_pubannot/'

true_output_dir_path = '/Users/Tony/Documents/BINP37/data/datasets/0_Gold_Standard/renamed_gold_corpus/'
#true_output_dir_path = '/Users/Tony/Documents/BINP37/dataset_from_pubannot/renamed_gold_corpus2/'
evaluator = PubannotationEvaluator(tagger_output_dir_path, true_output_dir_path, word_classes_set)
evaluator.evaluate()

for word_class in word_classes_set:
    print(f'CLASS: {word_class}')
    print(f'Total: {evaluator.get_total(word_class)}')
    print(f'True Positives: {evaluator.get_true_positives(word_class)}')
    print(f'False Positives: {evaluator.get_false_positives(word_class)}')
    print(f'False Negatives: {evaluator.get_false_negatives(word_class)}')
    with open('false_positives_dict.txt', 'w') as false_pos:
        false_pos.write(str(evaluator.word_classes_result_dict[word_class]['false_positives']))
    with open('false_negatives_dict.txt', 'w') as false_neg:
        false_neg.write(str(evaluator.word_classes_result_dict[word_class]['false_negatives']))
