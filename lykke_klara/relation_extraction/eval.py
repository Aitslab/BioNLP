import sys
import torch
import json

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from sklearn.metrics import multilabel_confusion_matrix as cm
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import classification_report

# Predict classes and calculate metrics
def evaluate(input_dir, corpus, metrics):
  classes = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE"]
  predictions = []
  true_classes = []
  correct_predictions = 0

  data_file = open(corpus, "r")
  data_list = data_file.read().split("\n")
  device = torch.device("cuda")

  # Load model
  model = BertForSequenceClassification.from_pretrained(input_dir, local_files_only=True, cache_dir=None)
  tokenizer = BertTokenizer.from_pretrained(input_dir)
  model.to(device)

  # Predict classes
  for seq in data_list:
    text = json.loads(seq)["text"]
    true_class = json.loads(seq)["custom_label"]
    input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0).to(device)
    outputs = model(input_ids)

    pred_class = classes[torch.softmax(outputs.logits, dim=1).argmax()]
   
    if pred_class == true_class:
      correct_predictions += 1
  
    predictions.append(pred_class)
    true_classes.append(true_class)

  precision, recall, fscore, _ = score(true_classes, predictions, average='macro')
  
  # Print the classification report and confusion matrices
  print(classification_report(true_classes, predictions))
  print(cm(true_classes, predictions, labels=["INTERACTOR", "NOT", "PART-OF", "REGULATOR-NEGATIVE", "REGULATOR-POSITIVE"]))

  metrics["f1-score"].append(fscore)
  metrics["recall"].append(recall)
  metrics["precision"].append(precision)
  metrics["accuracy"].append(correct_predictions / len(data_list))

  return metrics


# Pass a model and one or more corpuses 
# Appends the metrics to the result file
if __name__ == "__main__":
  model = sys.argv[1]
  corpus = sys.argv[2]
  output_file = sys.argv[3]

  with open(output_file) as infile:
    data = infile.read()

  metrics = json.loads(data)
  filename = corpus.split("/")[-1]

  if filename in metrics.keys():
    metrics[filename] = evaluate(model, corpus, metrics[filename])
  else:
    metrics[filename] = evaluate(model, corpus, {"f1-score": [], "recall": [], "precision": [], "accuracy": []})
  
  with open(output_file, "w") as outfile:
    json.dump(metrics, outfile)
