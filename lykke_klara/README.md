## Scripts
* [`add_custom_labels.py`](relation_extraction/add_custom_labels.py) replaces labels in datafiles with custom labels
* [`bert_finetune.py`](relation_extraction/bert_finetune.py) trains the models and saves them
* [`eval.py`](relation_extraction/eval.py) saves evaluation metrics in result file
* [`plot.py`](relation_extraction/plot.py) plots the metrics
* [`run_re.py`](relation_extraction/run_re.py) predicts relation and outputs the result in a tsv file (integrated in the [`main.py`](https://github.com/Aitslab/nlp_2021_alexander_petter/blob/master/main.py))


## Setup

First you need to follow the [`setup`](https://github.com/Aitslab/nlp_2021_alexander_petter#setup-using-conda-anaconda--miniconda) guide using Conda. Thereafter follow [`step 1: extracting relations`](https://github.com/Aitslab/nlp_2021_alexander_petter/tree/master/utils/chemprot#extracting-relations) to process your data. Do not continue to the `Building dataset` step as we don't want to change the data splits.

## How to train and evaluate SciBERT on Chemprot corpus

#### 1. Add custom labels:

```shell
python add_custom_labels.py <processed_dir> <output_dir>
```
`processed_dir` is the directory with the proccessed corpus from the setup. 

#### 2. Train and save the models:

```shell
python bert_finetune.py [--oversample] <model_dir> <processed_dir> <output_metrics_dir>
```
Outputs the trained models to `model_dir` and the training and validation metrics to `output_metrics_file` in the `output_metrics_dir`.

#### 3. Evaluate a model:

Pass a model from your `model_dir` together with one corpus file

```shell
python eval.py <model> <corpus> <output_metrics_file> 
```
Appends f1-score, precision and recall to `output_metrics_file`.

#### 4. Plot the metrics:

```shell
python plot.py <output_metrics_file> <output_plot_dir>
```
Saves plots in `output_plot_dir`.

## How to use your trained models to predict on output from NER

Continue to follow the [`setup`](https://github.com/Aitslab/nlp_2021_alexander_petter#setup-using-conda-anaconda--miniconda) guide and run the pipeline with the downloader, sentencer, NER and add_tags.

To the `re` in [`config`](https://github.com/Aitslab/nlp_2021_alexander_petter/blob/master/config.jsonof) add:

* the path to the directory of your pre-trained SciBERT model e.g. `models/scibert/<model>/`
* the path to the predictions file
* the path to the statistics file

The output fron `re` is:
* predictions file which is a tab separated file with output on the format: `entity1 relation entity2 sentence`
* statistics  file which is a tab separated file with output on the format: `entity1 entity2 relation frequency`
