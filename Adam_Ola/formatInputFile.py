# This is a python script to convert Hunflair corpora to the same format as that of biobert input.

import csv
import re

plus = r"( O \+)"
minus = r"( O \-)"
b = r"(B-[A-Za-z]+ [\+ \-]?)"
isub = r"(I-[A-Za-z]+ [\+ \-]?)"
newl = r"(\n\n)"

#Takes a string as input and change to the IOB format
def convert_iob(t):
    t = re.sub(plus,  "\tO", t)
    t = re.sub(minus, "\tO", t)
    t = re.sub(b, "\tB", t)
    t = re.sub(isub,  "\tI", t)
    t = re.sub(newl, "\tnewLine2000\tnewLine2000\t", t)
    return t

#Converts string to list
def convert_to_list(string):
    li = list(string.split())
    return li

#Converts list to tsv
def list_to_tsv(list_to_convert):
    with open('test.tsv', 'w', newline='') as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        s = ''
        for i in range(0,len(list_to_convert),2):
            if list_to_convert[i] == 'newLine2000':
                tsv_output.writerow(s)
            else:
                tsv_output.writerow([list_to_convert[i], list_to_convert[i + 1]])




c = open("TagSentenceSplitter_[__SENT__]_SciSpacyTokenizer_core_sci_sm_0.2.5_test.conll", "r")
text = c.read()
text = convert_iob(text)
l = convert_to_list(text)
print(l[0:100])
list_to_tsv(l)
