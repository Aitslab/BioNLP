##This script takes a .txt file and changes it to a tsv file of the structure:
#word + '\t' + 'O' + '\n'

import sys
import re

def removeall_replace(x, l):
    t = [y for y in l if y != x]
    del l[:]
    l.extend(t)
    return l

def sentence_to_tokens(text): # Inspired by https://github.com/spyysalo/standoff2conll/blob/master/common.py
    """Return list of tokens in given sentence using NERsuite tokenization."""
    tok = [t for t in re.compile(r'([^\W_]+|.)').split(text) if t]
    tok_nospace = removeall_replace(' ', tok)
    return tok_nospace

with open(sys.argv[1], "r") as text_file: # Open the text file
    with open('generated_test.tsv', 'w') as out_file:  # Define the output file
        for line in text_file:
            if line is '\n': #Respect newlines to keep sentences separate.
                out_file.write('\n')
            else:
                line = sentence_to_tokens(line) #Tokenized
                for word in line:
                    if word != '\n': out_file.write(word + '\t' + 'O' + '\n')
        out_file.write('\n') #VERY IMPORTANT
