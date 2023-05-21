# free_form_RE_text_gen.py
# Written by Jacob Krucinski on 2023-04-27
# 
# Run Relation Extraction (RE) on free_form text from stdin
# using the text generation capability of 

# Imports
import sys
import torch
from fairseq.models.transformer_lm import TransformerLanguageModel

# Read stdin
print("Reading stdin...")
free_form_text = ''.join([line for line in sys.stdin])
print(free_form_text)

# Load the model
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

# Engineer a prompt for RE from the stdin and apply BioGPT text generation
prompt = f"List all chemicals and diseases in the following text: {free_form_text}"
src_tokens = m.encode(prompt)
generate = m.generate([src_tokens], beam=5)[0]
output = m.decode(generate[0]["tokens"])
print("\n" + output, file=sys.stdout)