import sys
import torch
import json
import csv

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig

# Predict classes
def predict(model_dir, articles):

  # Load model
  model = BertForSequenceClassification.from_pretrained(model_dir, local_files_only=True, cache_dir=None)
  tokenizer = BertTokenizer.from_pretrained(model_dir)
  device = torch.device("cuda")
  model.to(device)

  classes     = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE"]
  predictions = []

  for article in articles.values():
    sentences = article["sentences"]

    for sentence in sentences:
      text     = sentence["text"]
      entities = sentence["entities"]

      # Only predict if two entities
      if len(entities) == 2:
        input_ids  = torch.tensor(tokenizer.encode(text)).unsqueeze(0).to(device)
        outputs    = model(input_ids)
        pred_class = classes[torch.softmax(outputs.logits, dim=1).argmax()]

        predictions.append({"entities": entities, "relation": pred_class, "text": text})
 
  return predictions


def read_corpus(corpus):

  with open(corpus, "r", encoding="utf-8") as f:
    articles = json.loads(f.read())
  
  return articles


def write_predictions(predictions, file_path):

 with open(file_path, "w") as tsv_file:
    writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')

    for prediction in predictions:
      entities = prediction["entities"]
      writer.writerow([entities[0], prediction["relation"], entities[1], prediction["text"]])

    
if __name__ == "__main__":
  model     = sys.argv[1]
  corpus    = sys.argv[2]
  file_path = sys.argv[3]

  articles    = read_corpus(corpus)
  predictions = predict(model, articles)
  write_predictions(predictions, file_path)