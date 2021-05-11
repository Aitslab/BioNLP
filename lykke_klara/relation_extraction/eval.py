import sys
import torch
import json

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from sklearn.metrics import multilabel_confusion_matrix as cm
from sklearn.metrics import precision_recall_fscore_support as score

from sklearn.metrics import classification_report

def evaluate(input_dir, corpora, metrics):
  data_file = open(corpora, "r")
  data_list = data_file.read().split("\n")

  device = torch.device("cuda")

  # loading model
  model = BertForSequenceClassification.from_pretrained(input_dir, local_files_only=True, cache_dir=None)
  tokenizer = BertTokenizer.from_pretrained(input_dir)
  model.to(device)

  classes = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE"] #["INTERACTOR", "NOT", "PART-OF", "REGULATOR-NEGATIVE", "REGULATOR-POSITIVE"]

  predictions = []
  true_classes = []

  correct_predictions = 0

  # predict class
  for seq in data_list:
    text = json.loads(seq)["text"]
    true_class = json.loads(seq)["custom_label"]
    input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0).to(device)
    outputs = model(input_ids)

    pred_class = classes[torch.softmax(outputs.logits, dim=1).argmax()]

    # if pred_class == 'NOT':
    #   print("------- PREDICTED NOT --------")
    #   print(seq)
    #   print("Predicted: ", pred_class)

    # evaluate prediction
    if pred_class == true_class:
      correct_predictions += 1
  
    predictions.append(pred_class)
    true_classes.append(true_class)

  precision, recall, fscore, _ = score(true_classes, predictions, average='macro')
  
  print("Model: ", input_dir)
  print("Corpora: ", corpora)
  print(classification_report(true_classes, predictions))

  print(cm(true_classes, predictions, labels=["INTERACTOR", "NOT", "PART-OF", "REGULATOR-NEGATIVE", "REGULATOR-POSITIVE"]))

  print(precision, recall, fscore)
  metrics["f1-score"].append(fscore)
  metrics["recall"].append(recall)
  metrics["precision"].append(precision)
  metrics["accuracy"].append(correct_predictions / len(data_list))

  return metrics


if __name__ == "__main__":
  model = sys.argv[1]

  for filepath in sys.argv[2:]:
    with open("drive/MyDrive/nlp_2021_alexander_petter/utils/chemprot/output_metrics.txt") as infile:
      data = infile.read()

    metrics = json.loads(data)
    filename = filepath.split("/")[-1]

    print("Filepath: ", filepath)
    if filename in metrics.keys():
      metrics[filename] = evaluate(model, filepath, metrics[filename])
    else:
      metrics[filename] = evaluate(model, filepath, {"f1-score": [], "recall": [], "precision": [], "accuracy": []})
    
    print("Metrics dict: ")
    print(metrics)
    with open("drive/MyDrive/nlp_2021_alexander_petter/utils/chemprot/output_metrics.txt", "w") as outfile:
      json.dump(metrics, outfile)