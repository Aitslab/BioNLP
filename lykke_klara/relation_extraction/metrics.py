import torch
import json

import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import multilabel_confusion_matrix as cm
from sklearn.metrics import classification_report

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from sklearn.metrics import confusion_matrix

def get_avg_metrics(filename):
  avg_metrics = {"f1-score": [], "recall": [], "precision": []}

  for i in range(4):
    input_dir = '/content/bert-finetuned-{}'.format(i)
    data_file = open("/content/drive/MyDrive/nlp_2021_alexander_petter/utils/chemprot/custom_label_datasets/" + filename, "r")
    data_list = data_file.read().split("\n")

    if torch.cuda.is_available():
        device = torch.device("cuda")

        print('\n\nFound %d available GPU(s).' % torch.cuda.device_count())
        print('Using GPU:', torch.cuda.get_device_name(0))

    else:
        print("\n\nNo GPU(s) available, switching to CPU.")
        device = torch.device("cpu")

    # loading model
    model = BertForSequenceClassification.from_pretrained(input_dir, local_files_only=True, cache_dir=None)
    tokenizer = BertTokenizer.from_pretrained(input_dir)
    model.to(device)

    classes = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE"]

    predictions = []
    true_classes = []

    correct_predictions = 0
    # row_counter = 0

    for seq in data_list:
      # row_counter += 1
      # print(row_counter, "\n")
      text = json.loads(seq)["text"]
      true_class = json.loads(seq)["custom_label"]
      input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0).to(device)
      outputs = model(input_ids)
      pred_class = classes[torch.softmax(outputs.logits, dim=1).argmax()]

      if (pred_class == true_class):
        correct_predictions += 1
      
      predictions.append(pred_class)
      true_classes.append(true_class)

    # # predict on the chemprot training and dev sets
    print("Accuracy: ", correct_predictions / len(data_list))
    #print("Accuracy: ", correct_predictions / len(dev_list)) # Accuracy:  0.5174825174825175

    precision, recall, fscore, _ = score(true_classes, predictions, average='macro')

    print(set(true_classes) - set(predictions))

    # confusion matrix
    # print(cm(true_classes, predictions))
    avg_metrics["f1-score"].append(fscore)
    avg_metrics["recall"].append(recall)
    avg_metrics["precision"].append(precision)

  return avg_metrics

def plot_metrics(train_metrics, dev_metrics):
  x = [1, 2, 3, 4]

  for metric in train_metrics:
    plt.plot(x, train_metrics[metric])
    plt.plot(x, dev_metrics[metric])

    # Add a legend
    plt.legend(["blue", "green"], loc ="lower right")

    # Show the plot
    plt.show()

train_metrics = get_avg_metrics("train.txt")
dev_metrics = get_avg_metrics("dev.txt")
print(train_metrics)

dev_metrics = {'f1-score': [0.26785459023697816, 0.4121827289387582, 0.4570745103451218, 0.460782566931896], 'recall': [0.3085636200716846, 0.39810885339799, 0.45981603842253743, 0.4625136730319368], 'precision': [0.3895275120053049, 0.526763678261067, 0.5538414932259105, 0.5690672606323701]}

plot_metrics(train_metrics, dev_metrics)