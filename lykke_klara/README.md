## Scripts
* [`add_custom_labels.py`](relation_extraction/add_custom_labels.py) replaces labels in datafiles with custom labels
* [`bert_finetune.py`](relation_extraction/bert_finetune.py) trains the models and saves them
* [`eval.py`](relation_extraction/eval.py) saves evaluation metrics in result file
* [`plot.py`](relation_extraction/plot.py) plots the metrics
* [`run_re.py`](relation_extraction/run_re.py) predicts relation and outputs the result in a tsv file


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

### Setup
Continue to follow the [`setup`](https://github.com/Aitslab/nlp_2021_alexander_petter#setup-using-conda-anaconda--miniconda) guide and run the pipeline with the downloader, sentencer and NER. 

#### 1. Add entity markers
The output from NER needs to be tagged. To do that, run [`add_ner_tag.py`](https://github.com/Aitslab/nlp_2021_alexander_petter/blob/master/under_development/add_ner_tags.py) and pass the output file from NER (`text-ner.json`) and path to output file (`text-nertags.json`) as arguments. The script needs the [`util.py`](https://github.com/Aitslab/nlp_2021_alexander_petter/blob/master/scripts/util.py) script as well.

#### 2. Predict relations and save result

Pass a model from your `model_dir` together with the `text-nertags.json` file and path to output file (.tsv format)

```shell
python run_re.py <model> <text-nertags> <output_file> 
```
outputs the predictions in the `output_file` on the format: `entity1 relation entity2 sentence`
