import torch
import re
import json
import random
import numpy as np
import pandas as pd
import os
import time
import datetime
import sys
import argparse

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from transformers import get_linear_schedule_with_warmup
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from imblearn.over_sampling import RandomOverSampler

parser = argparse.ArgumentParser()
parser.add_argument("--oversample", action="store_true")
parser.add_argument('files', nargs='*')
args = parser.parse_args()

oversample = args.oversample
files = args.files

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
data_dir = files[1]
exclude_label = {"OTHER"}
torch.cuda.empty_cache()

if torch.cuda.is_available():

    device = torch.device("cuda")

    print('\n\nFound %d available GPU(s).' % torch.cuda.device_count())
    print('Using GPU:', torch.cuda.get_device_name(0))

else:
    print("\n\nNo GPU(s) available, switching to CPU.")
    device = torch.device("cpu")

# Oversample parameters
os_params = {"NOT":                  {"cid": 0, "support": 241, "factor": 5},
             "PART-OF":              {"cid": 1, "support": 308, "factor": 3},
             "INTERACTOR":           {"cid": 2, "support": 2583,"factor": 3},
             "REGULATOR-POSITIVE":   {"cid": 3, "support": 799, "factor": 3},
             "REGULATOR-NEGATIVE":   {"cid": 4, "support": 2505,"factor": 3}
            }

def read_data(file_path, oversample=False):
  with open(file_path, "r", encoding="utf-8") as f:
      input = f.readlines()

      sentences   = []
      labels      = []

      for line in input:
          entry = json.loads(line)

          if not entry["custom_label"] in exclude_label:
              sentences.append(entry["text"])
              labels.append(int(entry["cid"]))

      # Oversampling
      if oversample:
        not_params     = os_params["NOT"]
        part_of_params = os_params["PART-OF"]
        reg_pos_params = os_params["REGULATOR-POSITIVE"]

        # Define oversampling strategy
        os_strategy = {not_params["cid"]    : not_params["support"]     * not_params["factor"], 
                       part_of_params["cid"]: part_of_params["support"] * part_of_params["factor"], 
                       reg_pos_params["cid"]: reg_pos_params["support"] * reg_pos_params["factor"]
                      }

        oversample = RandomOverSampler(sampling_strategy=os_strategy)
        sentences_over, labels_over = oversample.fit_resample(np.array([sentences]).T, labels)

        return sentences_over.flatten(), labels_over

      return sentences, labels

train_sentences, train_labels   = read_data(data_dir + "train.txt", oversample)
dev_sentences, dev_labels       = read_data(data_dir + "dev.txt")
test_sentences, test_labels     = read_data(data_dir + "test.txt")

assert len(train_sentences)     == len(train_labels)
assert len(dev_sentences)       == len(dev_labels)
assert len(test_sentences)      == len(test_labels)

print('\nLoading BERT-tokenizer')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
print('\nBERT-tokenizer loaded. Running example:\n')

print("Original: ",  train_sentences[0])
print("Tokenized: ", tokenizer.tokenize(train_sentences[0]))
print("Token IDs: ", tokenizer.convert_tokens_to_ids(tokenizer.tokenize(train_sentences[0])))

max_seq_length = 128
longest_sequence = 0
over_max = 0
under_max = 0

print("\n")
for sentence in train_sentences:

    input_ids = tokenizer.encode(sentence, add_special_tokens=True)
    longest_sequence = max(longest_sequence, len(input_ids))

    if len(input_ids) > max_seq_length:
        over_max += 1
    else:
        under_max += 1

print("\nLongest sequence: " + str(longest_sequence) + " tokens")
print("Sequences over " + str(max_seq_length) + ": " + str(over_max))
print("Sequences under " + str(max_seq_length) + ": " + str(under_max))


def get_encodings(sentences, labels):
    '''
    encode_plus will:
        (1) Tokenize the sentence
        (2) Prepend the [CLS] token to the start
        (3) Append the [SEP] token to the end
        (4) Map tokens to their IDs
        (5) Pad or truncate the sentence to max_length
        (6) Create attention masks for [PAD] tokens
    '''

    input_ids = []
    attention_masks = []

    for i, sentence in enumerate(sentences):
        encoded = tokenizer.encode_plus(sentence,
                                             add_special_tokens = True,
                                             max_length = max_seq_length,
                                             pad_to_max_length = True,
                                             return_attention_mask = True,
                                             truncation = True,
                                             return_tensors = 'pt'
                                        )

        input_ids.append(encoded["input_ids"])
        attention_masks.append(encoded["attention_mask"])

    input_ids       = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    labels          = torch.tensor(labels)

    return input_ids, attention_masks, labels

print("\nEncoding datasets...")
train_input_ids, train_attention_masks, train_labels    = get_encodings(train_sentences, train_labels)
dev_input_ids, dev_attention_masks, dev_labels          = get_encodings(dev_sentences, dev_labels)
test_input_ids, test_attention_masks, test_labels       = get_encodings(test_sentences, test_labels)
print("\nEncoding done. Running example:")
print("Original:\t", train_sentences[1])
print("Token IDs:\t", train_input_ids[1])

print("\n\nDatasets:")
print(str(len(train_sentences)) + " training samples")
print(str(len(dev_sentences)) + " development samples")
print(str(len(test_sentences)) + " test samples")

train_dataset   = TensorDataset(train_input_ids, train_attention_masks, train_labels)
dev_dataset     = TensorDataset(dev_input_ids, dev_attention_masks, dev_labels)
test_dataset    = TensorDataset(test_input_ids, test_attention_masks, test_labels)

batch_size = 32

train_dataloader    = DataLoader(train_dataset,
                                sampler = RandomSampler(train_dataset),     # Sample randomly
                                batch_size = batch_size
                                 )

dev_dataloader      = DataLoader(dev_dataset,
                                 sampler = SequentialSampler(dev_dataset),  # Sample sequentially
                                 batch_size = batch_size
                                 )

test_dataloader     = DataLoader(test_dataset,
                                 sampler = SequentialSampler(test_dataset),
                                 batch_size = batch_size
                                 )


# Will raise warnings since we initialize new weights
model = BertForSequenceClassification.from_pretrained("allenai/scibert_scivocab_uncased",
                                                      num_labels = 5,
                                                      output_attentions = False,
                                                      output_hidden_states = False
                                                      )
model.to(device)

params = list(model.named_parameters())

print('BERT model has {:} different named parameters.\n'.format(len(params)))
print('==== Embedding Layer ====\n')
for param in params[0:5]:
    print("{:<55} {:>12}".format(param[0], str(tuple(param[1].size()))))

print('\n==== First Transformer ====\n')
for param in params[5:21]:
    print("{:<55} {:>12}".format(param[0], str(tuple(param[1].size()))))

print('\n==== Output Layer ====\n')
for param in params[-4:]:
    print("{:<55} {:>12}".format(param[0], str(tuple(param[1].size()))))


optimizer = AdamW(model.parameters(),
                  lr = 2e-5,# Learning rate
                  eps = 1e-8 # epsilon parameter is a very small number to prevent any division by zero in the implementation
                  )

# Starts overfitting after 2 epochs
epochs = 5
# [number of batches] x [number of epochs]. Note that it is not the same as the number of training samples
total_steps = len(train_dataloader) * epochs

# Learning rate scheduler
scheduler = get_linear_schedule_with_warmup(optimizer,
                                            num_warmup_steps = 0,
                                            num_training_steps = total_steps
                                            )

# Calculates the accuracy of our predictions vs labels
def flat_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    return np.sum(pred_flat == labels_flat) / len(labels_flat)

def format_time(elapsed):
    '''
    Takes time in seconds and returns string in format hh:mm:ss
    '''
    elapsed_rounded = int(round(elapsed))
    return str(datetime.timedelta(seconds=elapsed_rounded))



seed_val = 113
random.seed(seed_val)
np.random.seed(seed_val)
torch.manual_seed(seed_val)
torch.cuda.manual_seed_all(seed_val)

total_t0 = time.time()

# Metrics: training loss, training accuracy, validation loss and validation accuracy.
model_metrics = {"average training loss": [], "average validation loss": [], "average training accuracy": []}

for epoch_i in range(0, epochs):
    torch.cuda.empty_cache()
    '''
    ==============================================
                Our training-loop
    ==============================================
    '''

    # Perform one full pass over the training set.

    print("")
    print('======== Epoch {:} / {:} ========'.format(epoch_i + 1, epochs))

    t0 = time.time()

    # Reset loss for this epoch
    total_train_loss = 0

    # Set model into training mode. 'dropout' and 'batchnorm' layers behave differently during training
    model.train()

    for step, batch in enumerate(train_dataloader):

        if step % 10 == 0 and not step == 0:
            elapsed = format_time(time.time() - t0)
            print(' Batch {:>5,} of {:>5,}.     Elapsed: {:}'.format(step, len(train_dataloader), elapsed))


        # Unpack training batch from dataloader
        #   [0]:    input_ids
        #   [1]:    attention_masks
        #   [2]:    labels
        batch_input_ids         = batch[0].to(device)
        batch_attention_mask    = batch[1].to(device)
        batch_labels            = batch[2].to(device)

        # Clear any previously calculated gradients before performing a backward pass
        model.zero_grad()

        # Perform a forward pass (evaluate model on this training batch)
        outputs = model(batch_input_ids,
                             token_type_ids=None,
                             attention_mask=batch_attention_mask,
                             labels=batch_labels
                             )
        loss, logits = outputs['loss'], outputs['logits']

        total_train_loss += loss.item()

        # Perform a backward pass to calculate the gradients
        loss.backward()

        # Clip the norm of the gradients to 1.0
        # This helps prevent the "exploding gradients" problem
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        # Update parameters and take a step using the computed gradient
        # The optimizer dictates the "update rule" - how the parameters are
        # modified based on their gradients, the learning rate, etc.
        optimizer.step()

        # Update the learning rate
        scheduler.step()

    avg_train_loss = total_train_loss / len(train_dataloader)

    training_time = format_time(time.time() - t0)


    print("")
    print("     Average training loss: {0:.2f}".format(avg_train_loss))
    print("     Training epoch took: {:}".format(training_time))

    '''
    ==============================================
                    Validation
    ==============================================
    '''

    print("")
    print("Running validation")

    t0 = time.time()

    # Put the model in evaluation mode - the dropout layers behave differently during evaluation
    model.eval()

    total_eval_accuracy = 0
    total_eval_loss     = 0
    nb_eval_steps       = 0


    for batch in dev_dataloader:

        # Unpack validation batch from dataloader
        #   [0]:    input_ids
        #   [1]:    attention_masks
        #   [2]:    labels
        batch_input_ids         = batch[0].to(device)
        batch_attention_mask    = batch[1].to(device)
        batch_labels            = batch[2].to(device)

        # Tells pytorch to not construct the compute graph during the forward pass
        # since it's only needed for backpropagation in training
        with torch.no_grad():

            # Forward pass
            output = model(batch_input_ids,
                                 token_type_ids = None,
                                 attention_mask = batch_attention_mask,
                                 labels = batch_labels
                                 )
            loss = output.loss
            logits = output.logits

        # Moves logits and labels to CPU
        logits      = logits.detach().cpu().numpy()
        label_ids   = batch_labels.to('cpu').numpy()

        total_eval_accuracy += flat_accuracy(logits, label_ids)

        total_eval_loss += loss.item()

    # Report final accuracy for this validation run
    avg_val_accuracy = total_eval_accuracy / len(dev_dataloader)
    print("     Accuracy: {0:.2f}".format(avg_val_accuracy))

    # Calculate average loss over all of the batches
    avg_val_loss = total_eval_loss / len(dev_dataloader)

    validation_time = format_time(time.time() - t0)

    print("     Validation Loss: {0:.2f}".format(avg_val_loss))
    print("     Validation took: {:}".format(validation_time))

    # Save the metrics
    model_metrics['average training loss'].append(avg_train_loss)
    model_metrics['average validation loss'].append(avg_val_loss)
    model_metrics['average training accuracy'].append(avg_val_accuracy)

    print("")
    print("Training complete!")
    print("Total training took {:} (h:mm:ss)".format(format_time(time.time()-total_t0)))
    model_dir = files[0] + 'bert-finetuned-{}/'.format(epoch_i)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    print("Saving model to %s" % model_dir)

    model_to_save = model.module if hasattr(model, 'module') else model
    model_to_save.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)

# Write metrics to result file
with open(files[2] + 'output_metrics.txt', 'w') as outfile:
    json.dump(model_metrics, outfile)