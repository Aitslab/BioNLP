import torch

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig

# running in google colab, bert-finetune directory contains the model files
output_dir = 'bert-finetune'
if torch.cuda.is_available():

    device = torch.device("cuda")

    print('\n\nFound %d available GPU(s).' % torch.cuda.device_count())
    print('Using GPU:', torch.cuda.get_device_name(0))

else:
    print("\n\nNo GPU(s) available, switching to CPU.")
    device = torch.device("cpu")

# 404 Client Error: Not Found for url: https://huggingface.co/bert-finetune/resolve/main/config.json
model = BertForSequenceClassification.from_pretrained(output_dir)
tokenizer = BertTokenizer.from_pretrained(output_dir)
model.to(device)

model.eval()

print("model evaluated", model)

# add prediction on the chemprot training and dev sets
