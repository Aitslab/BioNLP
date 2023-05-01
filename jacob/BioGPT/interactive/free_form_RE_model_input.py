# free_form_RE_text_gen_model_input.py
# Written by Jacob Krucinski on 2023-04-27
# 
# Run Relation Extraction (RE) on free_form text from --in_file
# and peform true model inference using my trained RE model from 2023-04-27

# Imports
import os
import json
import string
import argparse
from fairseq.models.transformer_lm import TransformerLanguageModel

# Define argparser
parser = argparse.ArgumentParser()
parser.add_argument("--in_file", type=str, default="")
parser.add_argument("--out_file", type=str, default="")
args, _ = parser.parse_known_args()

# Read in_file
print("Reading input...")
free_form_text = ""
with open(args.in_file, 'r') as f:
    free_form_text += f.readline()
#free_form_text = free_form_text.translate(str.maketrans('', '', string.punctuation))     # remove punctuation
print(free_form_text)

# Pre-process free-form text: Apply tokenization and BPE
# Tokenization
moses
raw_data_dir
prefix = "free_form"
os.popen(f"perl ${MOSES}/scripts/tokenizer/tokenizer.perl -l en -a -threads 8 < {args.in_file}.txt > {args.out_file}.tok.txt")
# NOTE: Check if this needs to be in .x or .y file format (because the data is just plain text)


# Run inference.py script
data_dir    = ""
model_dir   = ""
model       = ""
src_file    = ""
output_file = ""
temp = os.popen(f"python ../../inference.py --data_dir={data_dir} --model_dir={model_dir} \
                --model_file={model} --src_file={src_file} --output_file={output_file}").read()

# Find REs in BC5CDR form
print("\n\n")
print("Relation Extraction...")
out_file = open(args.out_file, 'a')
for c in found_chemicals:
    for d in found_diseases:
        # TODO: Consider directionality of relation
        prompt = f"The relation between {c} and {d} is "
        print(f"Prompt: {prompt}")
        src_tokens = m.encode(prompt)
        generate = m.generate([src_tokens], beam=5)[0]
        output = m.decode(generate[0]["tokens"])

        # Append RE to out_file
        out_file.write(output)
        out_file.write("\n\n")

out_file.close()

