import json

from scripts import add_custom_labels
from scripts import build_corpus
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

def run_build_corpus(build_corpus_config: dict, ignore: bool):
  if ignore:
    print("Ignoring script: build corpus.")
    return

  print("Running build corpus script.")

  build_corpus.run(build_corpus_config["input_path"], build_corpus_config["train_path"], build_corpus_config["train_class_size"])
  build_corpus.run(build_corpus_config["input_path"], build_corpus_config["dev_path"], build_corpus_config["dev_class_size"])

  print("Finished running build corpus script.")

# bert finetune
def run_bert_finetune(bert_finetune_config: dict, ignore: bool):
  if ignore:
    print("Ignoring script: BERT finetune.")
    return

  print("Running BERT finetune script.")

  bert_finetune.run(bert_finetune_config["input_path"], bert_finetune_config["model_path"], bert_finetune_config["output_path"], bert_finetune_config["oversample"]) 

  print("Finished running BERT finetune script.")

# eval
def run_eval(eval_config: dict, ignore: bool):
  if ignore:
    print("Ignoring script: eval.")
    return

  print("Running eval script.")

  evaluation.run(eval_config["input_path"], eval_config["model_path"], eval_config["output_path"]) 

  print("Finished running eval script.")

# plot
def run_plot(plot_config: dict, ignore: bool):
  if ignore:
    print("Ignoring script: plot.")
    return

  print("Running plot script.")

  plot.run(plot_config["input_path"], plot_config["output_path"]) 

  print("Finished running plot script.")


if __name__ == "__main__":
    print("Please see config.json for configuration!")

    with open("/content/drive/MyDrive/edan70/config.json", "r") as f:
        config = json.loads(f.read())

    print("Loaded config:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print()

    # os.makedirs("data", exist_ok=True)

    ignore = config["ignore"]

    run_build_corpus(config["build_corpus"], ignore=ignore["build_corpus"])
    print()

    run_add_custom_labels(config["add_custom_labels"], ignore=ignore["add_custom_labels"])
    print()

    run_bert_finetune(config["bert_finetune"], ignore=ignore["bert_finetune"])
    print()

    run_eval(config["eval"], ignore=ignore["eval"])
    print()

    run_plot(config["plot"], ignore=ignore["plot"])
    print()
