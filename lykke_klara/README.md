## Scripts
* [`add_custom_labels.py`](relation_extraction/add_custom_labels.py) replaces labels in datafiles with custom labels
* [`bert_finetune.py`](relation_extraction/bert_finetune.py) trains the models and saves them
* [`eval.py`](relation_extraction/eval.py) saves evaluation metrics in result file
* [`plot.py`](relation_extraction/plot.py) plots the metrics


## Setup

First you need to follow the [`setup`](https://github.com/Aitslab/nlp_2021_alexander_petter#setup-using-conda-anaconda--miniconda) guide using Conda. Thereafter follow [`step 1: extracting relations`](https://github.com/Aitslab/nlp_2021_alexander_petter/tree/master/utils/chemprot#extracting-relations) to process your data. Do not continue to the `Building dataset` step as we don't want to change the data split.

## How to run the program

#### 1. Add custom labels:

```shell
python add_custom_labels.py <processed_dir> <output_dir>
```
`processed_dir` is the directory with the proccessed corpus from the setup. 

#### 2. Train and save the models:

```shell
python bert_finetune.py <model_dir> <output_metrics_dir>
```
Outputs the trained models to `model_dir` and the training and validation metrics to `output_metrics_file` in the `output_metrics_dir`.

#### 3. Evaluate a model:

Pass a model from your `model_dir` together with at lest one corpus file

```shell
python eval.py <model> <corpus>
```
Appends f1-score, precision and recall to `output_metrics_file`.

#### 4. Plot the metrics:

```shell
python plot.py <output_metrics_file> <output_plot_dir>
```
Saves plots in `output_plot_dir`.
