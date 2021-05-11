## Scripts
* [`add_custom_labels.py`](relation_extraction/add_custom_labels.py) replaces labels in datafiles with custom labels
* [`bert_finetune.py`](relation_extraction/bert_finetune.py) trains the models and saves them
* [`eval.py`](relation_extraction/eval.py) saves evaluation metrics in result file
* [`plot.py`](relation_extraction/plot.py) plots the metrics


## Setup

First you need to follow the [`setup`](https://github.com/Aitslab/nlp_2021_alexander_petter#setup-using-conda-anaconda--miniconda) guide using Conda. Thereafter follow [`step 1`](https://github.com/Aitslab/nlp_2021_alexander_petter/tree/master/utils/chemprot#step-1-reformatting-the-chemprot-corpus) to process your data.

## How to run the program

[`add_custom_labels.py`](relation_extraction/add_custom_labels.py):

```shell
python add_custom_labels.py <processed_dir> <output_dir>
```
`processed_dir` is the directory with the proccessed corpus from the setup. 

[`bert_finetune.py`](relation_extraction/bert_finetune.py):

```shell
python bert_finetune.py <model_dir> <output_metrics_dir>
```
Outputs the trained models to `model_dir` and the training and validation metrics to `output_metrics_file` in the `output_metrics_dir`.

[`eval.py`](relation_extraction/eval.py):

```shell
python eval.py <model_dir> <corpus>*
```
Appends metrics to `output_metrics_file`.

<sub> \* one or more <sub>

[`plot.py`](relation_extraction/plot.py):

```shell
python plot.py <output_metrics_file> <output_plot_dir>
```
