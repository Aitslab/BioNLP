import glob
### I had separate gold files that could be merged
### This is for Disease evaluation and could be changed for Protein or chemical as well
gold_files = glob.glob('../data/evaluation_flair/Gold_corpus_tsv/*.tsv')
flair_disease_files = glob.glob('../data/evaluation_flair/Modified_Flair_tagged_disease/*.tsv')
flair_protein_files = glob.glob('../data/evaluation_flair/Modified_Flair_tagged_protein/*.tsv')

path = '../data/evaluation_flair/'
### I just initialized TP, TN, and FP, FN
True_pos_disease = 0
True_neg_disease = 0
False_pos_disease = 0
False_neg_disease = 0


True_pos_protein = 0
True_neg_protein = 0
False_pos_protein = 0
False_neg_protein = 0



################################################################################
for g_file in gold_files:
    g_lines = []
    f_lines = []
    with open(g_file,'r') as g_f:
        with open(path+'Modified_Flair_tagged_disease/'+ g_file.split('/')[-1],'r') as f_f:
            for i in g_f:
                if i:
                    g_lines.append(i.strip().split())
            for j in f_f:
                if j:
                    f_lines.append(j.strip().split())
            #print(g_lines)
            if len(g_lines)!=len(f_lines):
                print("The number of tokens are not the same!!!!!!!! in {}".format(g_file))
                break
            for k in range(len(g_lines)):
                if g_lines[k]:
                    if 'B-Disease' in g_lines[k][1] and f_lines[k][1]=='<B>' or \
                       'I-Disease' in g_lines[k][1] and f_lines[k][1]=='<I>':
                        True_pos_disease += 1
                    elif 'B-Disease' in g_lines[k][1] and f_lines[k][1]!='<B>' or \
                            'I-Disease' in g_lines[k][1] and f_lines[k][1]!='<I>':
                        False_neg_disease+=1
                    elif 'B-Disease' not in g_lines[k][1] and f_lines[k][1]=='<B>' or \
                            'I-Disease' not in g_lines[k][1] and f_lines[k][1]=='<I>':
                        False_pos_disease+=1
                    elif 'B-Disease' not in g_lines[k][1] and f_lines[k][1]!='<B>' or \
                            'I-Disease' not in g_lines[k][1] and f_lines[k][1]!='<I>':
                        True_neg_disease+=1
                    
print('TN is {}'.format(True_neg_disease))
print('TP is {}'.format(True_pos_disease))
print('FP is {}'.format(False_pos_disease))
print('FN is {}'.format(False_neg_disease))

Precision = True_pos_disease / (True_pos_disease+False_pos_disease)
Recall   = True_pos_disease / (True_pos_disease+False_neg_disease)
print('Precsion is {}'.format(Precision))
print('Recall is {}'.format(Recall))
##################################################################################################

F1_score = 2 * (Precision*Recall/(Precision+Recall))
print('F1-score is {}'.format(F1_score))
