"""
oskarjonszon

  Takes a folder as input and combines all the conll files into one file specified as output.
  To compile the output file to jsonlines for eval/prediction/training use the minimize.py script 
  from mandarjoshi's coref repository. 

  The script splits the CoNLL arcitles into parts with the same ID. The split condition is N.
"""

import os

output = "./data/dev.english.v4_gold_conll"
input = "../CRAFT-conll/dev"

# Number of sentences to split on.
N = 200

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Clears the current file from data.
open(output, 'w').close()

for file in [f for f in os.listdir(input) if f.endswith('.conll')]:

  with open(input + "/" + file) as f_in:
    
    first_line = f_in.readline()

    paragraphs = [line.split('\n') for line in f_in.read().split('\n\n') if line]

    chs = chunks(paragraphs, N)

    with open(output, "a") as f_out:
      
      for idx, ch in enumerate(chs):
        
        f_out.write(first_line[0:-2] + str(idx) + "\n")
        
        for paragraph in ch:
          for line in paragraph:
            parts = line.split()
            parts[1] = idx
            f_out.write(' '.join([str(p) for p in parts[0:2]]) + ' ' + '\t'.join([str(p) for p in parts[2:]]) + "\n")
          f_out.write('\n')
        f_out.write('\n')


