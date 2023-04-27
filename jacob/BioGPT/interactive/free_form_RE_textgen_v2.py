# free_form_RE_text_gen_v2.py
# Written by Jacob Krucinski on 2023-04-27
# 
# Run Relation Extraction (RE) on free_form text from stdin
# using the text generation capability of 
#
# v2 update: Since NER prompt seems to fail, manually perform NER via a lookup table 

# Imports
import json
import string
import argparse
from fairseq.models.transformer_lm import TransformerLanguageModel

# Define argparser
parser = argparse.ArgumentParser()
parser.add_argument("--in_file", type=str, default="")
parser.add_argument("--out_file", type=str, default="")
args, _ = parser.parse_known_args()

# Read stdin
print("Reading input...")
free_form_text = ""
with open(args.in_file, 'r') as f:
    free_form_text += f.readline()
free_form_text = free_form_text.translate(str.maketrans('', '', string.punctuation))     # remove punctuation
print(free_form_text)

# Load the model
print("Loading model...")
model_dir   = "../checkpoints/Pre-trained-BioGPT"
model_name  = "checkpoint.pt"
m = TransformerLanguageModel.from_pretrained(
        model_dir, 
        model_name, 
        "../../data",
        tokenizer='moses', 
        bpe='fastbpe', 
        bpe_codes="../data/bpecodes",
        min_len=100,
        max_len_b=1024)
m.cuda()

# NER_v1
# print("Performing NER...")
# prompt = f"List all chemicals and diseases in the following text: {free_form_text}"
# src_tokens = m.encode(prompt)
# generate = m.generate([src_tokens], beam=5)[0]
# output = m.decode(generate[0]["tokens"])
# with open(args.out_file, 'w') as f:
#     f.write(output)

# NER_v2
print("Performing NER...")
with open("../data/BC5CDR/raw/train.entities.json", 'r') as f:
    entity_data = json.loads(f.read())
    chemicals = set(entity_data["chemical2id"].keys())
    diseases = set(entity_data["disease2id"].keys())

found_chemicals = []
found_diseases  = []
for word in free_form_text.split():
    if (word in chemicals):
        found_chemicals.append(word)

    if (word in diseases):
        found_diseases.append(word)

print(f"Found chemicals: {found_chemicals}")
print(f"Found diseases: {found_diseases}")

# Find REs in rel-is form
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

