import torch
import json

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from sklearn.metrics import confusion_matrix

for i in range(3):
  input_dir = '/content/drive/MyDrive/EDAN70/bert-finetuned-{}'.format(i)
  #train_file = open("/content/drive/MyDrive/EDAN70/custom_label_datasets/train.txt", "r")
  dev_file = open("/content/drive/MyDrive/EDAN70/custom_label_datasets/dev.txt", "r")

  # train_list = train_file.read().split("\n")
  dev_list = dev_file.read().split("\n")

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
  correct_predictions = 0

  for seq in dev_list:
    #print(train_list.index(seq), "\n")
    text = json.loads(seq)["text"]
    actual_class = json.loads(seq)["custom_label"]
    input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0).to(device)
    outputs = model(input_ids)
    pred_class = classes[torch.softmax(outputs.logits, dim=1).argmax()]

    if (pred_class == actual_class):
      correct_predictions += 1
    
    predictions.append(pred_class)

  # # predict on the chemprot training and dev sets
  print("Accuracy: ", correct_predictions / len(train_list))
  # #print("Accuracy: ", correct_predictions / len(dev_list)) # Accuracy:  0.5174825174825175