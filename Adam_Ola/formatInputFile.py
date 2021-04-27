# This is a python script to convert Hunflair corpora to the same format as that of biobert input.

import csv
import re

plus = r"( O \+)"
minus = r"( O \-)"
b = r"(B-[A-Za-z]+ [\+ \-]?)"
isub = r"(I-[A-Za-z]+ [\+ \-]?)"

#Takes a string as input and change to the IOB format
def convert_iob(t):
    t = re.sub(plus,  "\tO", t)
    t = re.sub(minus, "\tO", t)
    t = re.sub(b, "\tB", t)
    t = re.sub(isub,  "\tI", t)
    return t

#Converts string to list
def convert_to_list(string):
    li = list(string.split())
    return li

#Converts list to tsv
def list_to_tsv(list_to_convert):
    with open('output.tsv', 'w', newline='') as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        for i in range(0,len(list_to_convert),2):
            tsv_output.writerow([list_to_convert[i] , list_to_convert[i+1]])



c = open("SciSpacySentenceSplitter_core_sci_sm_0.2.5_SciSpacyTokenizer_core_sci_sm_0.2.5_dev.conll", "r")
text = c.read()
text = convert_iob(text)
l = convert_to_list(text)
list_to_tsv(l)
