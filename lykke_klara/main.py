import json

from scripts import add_custom_labels
from scripts import build_art_corpus
from scripts import bert_finetune
from scripts import evaluation
from scripts import plot

# add custom labels (chemprot) / build corpus
def run_add_custom_labels(add_custom_labels_config: dict, ignore: bool):
  if ignore:
    print("Ignoring script: add custom labels.")
    return

  print("Running add custom labels script.")

  add_custom_labels.run(add_custom_labels_config["input_path"], add_custom_labels_config["output_path"]) 

  print("Finished running add custom labels script.")

def run_build_art_corpus(build_art_corpus_config: dict, ignore: bool):
  if ignore:
    print("Ignoring script: build art corpus.")
    return

  print("Running build art corpus script.")

  build_art_corpus.run(build_art_corpus_config["input_path"], build_art_corpus_config["train_path"], build_art_corpus_config["train_class_size"])
  build_art_corpus.run(build_art_corpus_config["input_path"], build_art_corpus_config["dev_path"], build_art_corpus_config["dev_class_size"])

  print("Finished running build corpus script.")

# bert finetune
def run_bert_finetune(bert_finetune_config: dict, ignore: bool):
  if ignore:
    print("Ignoring script: BERT finetune.")
    return

  print("Running BERT finetune script.")

  bert_finetune.run(bert_finetune_config["train_path"],
   bert_finetune_config["dev_path"], bert_finetune_config["model_path"],
   bert_finetune_config["metrics_path"], 
   bert_finetune_config["oversample"],
   bert_finetune_config["epochs"]
   ) 

  print("Finished running BERT finetune script.")

# evaluation
def run_eval(eval_config: dict, ignore: bool):
  if ignore:
    print("Ignoring script: eval.")
    return

  print("Running eval script.")

  evaluation.run(eval_config["train_path"], eval_config["model_path"], eval_config["metrics_path"]) 
  evaluation.run(eval_config["dev_path"], eval_config["model_path"], eval_config["metrics_path"])

  print("Finished running eval script.")

# plot
def run_plot(plot_config: dict, ignore: bool):
  if ignore:
    print("Ignoring script: plot.")
    return

  print("Running plot script.")

  plot.run(plot_config["train_path"], plot_config["dev_path"], plot_config["metrics_path"], plot_config["output_path"]) 

  print("Finished running plot script.")


if __name__ == "__main__":
    print("Please see config.json for configuration!")

    with open("/content/drive/MyDrive/edan70/config.json", "r") as f:
        config = json.loads(f.read())

    print("Loaded config:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print()

    ignore = config["ignore"]

    run_build_art_corpus(config["build_art_corpus"], ignore=ignore["build_art_corpus"])
    print()

    run_add_custom_labels(config["add_custom_labels"], ignore=ignore["add_custom_labels"])
    print()

    run_bert_finetune(config["bert_finetune"], ignore=ignore["bert_finetune"])
    print()

    run_eval(config["evaluation"], ignore=ignore["evaluation"])
    print()

    run_plot(config["plot"], ignore=ignore["plot"])
    print()
