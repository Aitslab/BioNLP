import sys
import torch
import json
import csv

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig

# Write predictions to file
def predict_all(articles):
  global model, tokenizer, device

  model     = BertForSequenceClassification.from_pretrained(model_dir, local_files_only=True, cache_dir=None)
  tokenizer = BertTokenizer.from_pretrained(model_dir)
  device    = torch.device("cuda")
  model.to(device)

  with open(file_path, "w") as tsv_file:
    writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')

    for article in articles.values():
      sentences = article["sentences"]

      for sentence in sentences:

        # Only predict if two entities
        if sentence["entitycount"] == 2:
          tagged   = sentence["tagged"]
          text     = sentence["text"]
          entities = sentence["entities"]
          pred_rel = predict_relation(tagged)

          writer.writerow([entities[0], pred_rel, entities[1], text])


# Predict classes
def predict_relation(text):
  classes    = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE"]
  input_ids  = torch.tensor(tokenizer.encode(text)).unsqueeze(0).to(device)
  outputs    = model(input_ids)
  pred_rel   = classes[torch.softmax(outputs.logits, dim=1).argmax()]
  return pred_rel


def read_corpus(corpus_path):

  with open(corpus_path, "r", encoding="utf-8") as f:
    articles = json.loads(f.read())
  
  return articles

    
if __name__ == "__main__":
  model_dir   = sys.argv[1]
  corpus_path = sys.argv[2]
  file_path   = sys.argv[3]

  articles = read_corpus(corpus_path)
  predict_all(articles)
