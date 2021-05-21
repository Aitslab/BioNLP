# Written by oskarjonszon.
#   Takes a folder as input and combines all the conll files into one file specified as output.
#   To compile the output file to jsonlines for eval/prediction/training use the minimize.py script 
#   from mandarjoshi's coref repository. 

import os

output = "./data/test.english.v4_gold_conll"
input = "../CRAFT-conll/test"

# Clears the current file from data.
open(output, 'w').close()

for file in [f for f in os.listdir(input) if f.endswith('.conll')]:
  with open(input + "/" + file) as f_in:
      with open(output, "a") as f_out:
        f_out.write(f_in.read())
