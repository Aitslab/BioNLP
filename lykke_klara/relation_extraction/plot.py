import sys
import json
import matplotlib.pyplot as plt

# Plot the training and validation metrics
def plot_loss_acc(data, indices, output_dir):  
  x = list(indices)
  plt.xticks(indices)

  plt.plot(x, data['average training loss'],     color="blue")
  plt.plot(x, data['average validation loss'],   color="red")
  plt.plot(x, data['average training accuracy'], color="green")
  plt.plot(x, data['train.txt']['accuracy'],     color="orange") # accuracies returned by the eval.py script

  plt.legend(['avg. training loss', 'avg. validation loss', 
              'avg. training accuracy', 'avg. validation accuracy'], 
              loc="upper center", bbox_to_anchor=(0.5, 1.23),
              fancybox=True, ncol=2)

  plt.xlabel('epoch')
  plt.tight_layout()
  plt.savefig(output_dir + '/training_validation.png')
  plt.show()

# Plot the metrics (f1-score, recall and precision) for the models
def plot_metrics(train_data, dev_data, indices, output_dir):
  x = list(indices)

  for metric in train_data:
    plt.xticks(indices)
  
    plt.plot(x, train_data[metric], color="blue")
    plt.plot(x, dev_data[metric], color="red")

    plt.legend(["train", "dev"], loc="upper center", bbox_to_anchor=(0.5, 1.15),
          fancybox=True, ncol=2)

    plt.xlabel('epoch')
    plt.ylabel(metric)
    plt.savefig(output_dir + '/{}.png'.format(metric))
    plt.show()

def read_data(filename):
  print("File: ", filename)
  with open(filename) as json_file:
    data = json.loads(json_file.read())
  
    return data

# Pass the result file and output dir for the plots
if __name__ == "__main__":
  filename   = sys.argv[1]
  output_dir = sys.argv[2]
  data = read_data(filename)
  indices = range(1, len(data['average training loss']) + 1) 
  plot_loss_acc(data, indices, output_dir)
  plot_metrics(data['train.txt'], data['dev.txt'], indices, output_dir)