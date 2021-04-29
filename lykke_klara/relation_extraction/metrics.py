import torch
import json

from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import multilabel_confusion_matrix as cm

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from sklearn.metrics import confusion_matrix

for i in range(4):
  input_dir = '/content/drive/MyDrive/EDAN70/bert-finetuned-{}'.format(i)
  train_file = open("/content/drive/MyDrive/nlp_2021_alexander_petter/utils/chemprot/custom_label_datasets/train.txt", "r")
  # dev_file = open("/content/drive/MyDrive/nlp_2021_alexander_petter/utils/chemprot/custom_label_datasets/dev.txt", "r")

  train_list = train_file.read().split("\n")
  # dev_list = dev_file.read().split("\n")

  #print("--------------------------------Iteration: ------------------", i)

  if torch.cuda.is_available():

      device = torch.device("cuda")

      print('\n\nFound %d available GPU(s).' % torch.cuda.device_count())
      print('Using GPU:', torch.cuda.get_device_name(0))

  else:
      print("\n\nNo GPU(s) available, switching to CPU.")
      device = torch.device("cpu")

  # to load the model later:
  model = BertForSequenceClassification.from_pretrained(input_dir, local_files_only=True, cache_dir=None)
  tokenizer = BertTokenizer.from_pretrained(input_dir)
  model.to(device)

  classes = ["NOT", "PART-OF", "INTERACTOR", "REGULATOR-POSITIVE", "REGULATOR-NEGATIVE", "OTHER"]

  predictions = []
  true_classes = []

  correct_predictions = 0
  #row_counter = 0

  for seq in train_list:
    #row_counter += 1
    #print(row_counter, "\n")
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
  print("Accuracy: ", correct_predictions / len(train_list))
  #print("Accuracy: ", correct_predictions / len(dev_list)) # Accuracy:  0.5174825174825175

  precision, recall, fscore, support = score(true_classes, predictions)

  print(set(true_classes) - set(predictions))
  print(cm(true_classes, predictions))

  print("Precision: ", precision)
  print("Recall: ", recall)
  print("F1-score: ", fscore)

