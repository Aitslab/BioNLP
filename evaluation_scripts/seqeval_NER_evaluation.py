# author: Sonja Aits


import pandas as pd
from seqeval.metrics import f1_score, precision_score, recall_score

def seqeval_NER_evaluation(true_file, pred_file, output_file, separator): 
  # the input files should be in IOB2 format (one token per line, tags in the second column)
  # the separator can be anything, e.g. comma, tab or whitespace ('\s+')

    # read TSV files with gold standard and predictions
    true = pd.read_csv(true_file, sep=separator, header=None)
    pred = pd.read_csv(pred_file, sep=separator, header=None)

    # convert column with tags to nested list
    y_true = [true.iloc[:, 1].tolist()]
    y_pred = [pred.iloc[:, 1].tolist()]

    # print seqeval metrics to output_file
    with open(output_file, 'w') as f:
        f.write('seqeval metrics'+'\n')
        f.write('Precision: '+str(precision_score(y_true, y_pred))+'\n')
        f.write('Recall: '+str(recall_score(y_true, y_pred))+'\n')
        f.write('F1: '+str(f1_score(y_true, y_pred))+'\n')