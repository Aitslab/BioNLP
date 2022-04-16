import sys
import torch
import json
import os

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from sklearn.metrics import confusion_matrix
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import classification_report

# Predict classes and calculate metrics
def evaluate(input_dir, input_path, metrics):
  classes = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE"]
  predictions = []
  true_classes = []
  correct_predictions = 0

  data_file = open(input_path, "r", encoding='utf-8')
  data_list = data_file.read().split("\n")
  device = torch.device("cuda")

  # Load model_path
  model_path = BertForSequenceClassification.from_pretrained(input_dir, local_files_only=True, cache_dir=None)
  tokenizer = BertTokenizer.from_pretrained(input_dir)
  model_path.to(device)

  # Predict classes
  for seq in data_list:
    text = json.loads(seq)["text"]
    true_class = json.loads(seq)["custom_label"]
    input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0).to(device)
    outputs = model_path(input_ids)

    pred_class = classes[torch.softmax(outputs.logits, dim=1).argmax()]
   
    if pred_class == true_class:
      correct_predictions += 1
  
    predictions.append(pred_class)
    true_classes.append(true_class)

  # precision, recallmacro, fscore, _ = score(true_classes, predictions, average='macro')
  precision_macro, recall_macro, fscore_macro, _ = score(true_classes, predictions, average='macro')
  precision_micro, recall_micro, fscore_micro, _ = score(true_classes, predictions, average='micro')
  precision_weighted, recall_weighted, fscore_weighted, _ = score(true_classes, predictions, average='weighted')
  
  # Print the classification report and confusion matrices
  print(classification_report(true_classes, predictions))
  print(multilabel_confusion_matrix(true_classes, predictions, labels=["INTERACTOR", "NOT", "PART-OF", "REGULATOR-NEGATIVE", "REGULATOR-POSITIVE"]))
  print(confusion_matrix(true_classes, predictions))


  metrics["f1-score"]["macro"].append(fscore_macro)
  metrics["recall"]["macro"].append(recall_macro)
  metrics["precision"]["macro"].append(precision_macro)
  metrics["f1-score"]["micro"].append(fscore_micro)
  metrics["recall"]["micro"].append(recall_micro)
  metrics["precision"]["micro"].append(precision_micro)
  metrics["f1-score"]["weighted"].append(fscore_weighted)
  metrics["recall"]["weighted"].append(recall_weighted)
  metrics["precision"]["weighted"].append(precision_weighted)
  # metrics["f1-score"].append(fscore)
  # metrics["recall"].append(recall)
  # metrics["precision"].append(precision)
  metrics["accuracy"].append(correct_predictions / len(data_list))
  metrics["confusion matrices"].append(confusion_matrix(true_classes, predictions).tolist())

  return metrics


# Pass a directory with models and a corpus
# Appends the metrics to the result file
def run(input_path, model_path, output_path):
  for model in os.listdir(model_path):

    with open(output_path) as infile:
      data = infile.read()

    metrics = json.loads(data)
    print(input_path)
    filename = input_path.split("/")[-1]

    if filename in metrics.keys():
      metrics[filename] = evaluate(model_path + model, input_path, metrics[filename])
    else:
      # metrics[filename] = evaluate(model_path + model, input_path, {"f1-score": [], "recall": [], "precision": [], "accuracy": []})
      metrics[filename] = evaluate(model_path + model, input_path, 
                                  {"f1-score": {"macro" : [], "micro" : [], "weighted" : []}, 
                                  "recall": {"macro" : [], "micro" : [], "weighted" : []}, 
                                  "precision": {"macro" : [], "micro" : [], "weighted" : []}, 
                                  "accuracy": [], 
                                  "confusion matrices": []})

    with open(output_path, "w") as outfile:
      json.dump(metrics, outfile, indent=4)
