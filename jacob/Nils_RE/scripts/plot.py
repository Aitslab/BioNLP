import sys
import json
import matplotlib.pyplot as plt

# Plot the training and validation metrics
def plot_loss_acc(data, indices, output_dir, train_key):  
  x = list(indices)
  plt.xticks(indices)

  plt.plot(x, data['average training loss'],     color="blue")
  plt.plot(x, data['average validation loss'],   color="red")
  plt.plot(x, data[train_key]['accuracy'],     color="green") # accuracies returned by the eval.py script
  plt.plot(x, data['average validation accuracy'], color="orange")

  plt.legend(['avg. training loss', 'avg. validation loss', 
              'avg. training accuracy', 'avg. validation accuracy'], 
              loc="upper center", bbox_to_anchor=(0.5, 1.23),
              fancybox=True, ncol=2)

  plt.xlabel('epoch')
  plt.tight_layout()
  plt.savefig(output_dir + '/training_validation.png')
  plt.close()

# Plot the metrics (f1-score, recall and precision)
def plot_metrics(train_data, dev_data, indices, output_dir):
  x = list(indices)

  print(f"Metrics: {train_data}")
  for metric in train_data:
    plt.xticks(indices)
  
    plt.plot(x, train_data[metric], color="blue")
    plt.plot(x, dev_data[metric], color="red")

    plt.legend(["train", "dev"], loc="upper center", bbox_to_anchor=(0.5, 1.15),
          fancybox=True, ncol=2)

    plt.xlabel('epoch')
    plt.ylabel(metric)
    plt.savefig(output_dir + '/{}.png'.format(metric))
    plt.close()

def read_data(filename):
  print("File: ", filename)
  with open(filename) as json_file:
    data = json.loads(json_file.read())
  
    return data

# Pass the file path for train and dev sets, 
# result file and output dir for the plots
def run(train_path, dev_path, input_path, output_path):
  data = read_data(input_path)
  train_key = train_path.split("/")[-1]
  dev_key = dev_path.split("/")[-1]

  indices = range(1, len(data['average training loss']) + 1) 
  plot_loss_acc(data, indices, output_path, train_key)
  plot_metrics(data[train_key], data[dev_key], indices, output_path)