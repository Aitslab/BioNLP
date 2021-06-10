## File structure

* root:
  - config.py configuration parameters to the pipeline
  - main.py runs the pipeline

* scripts: 
  - [`add_custom_labels.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/add_custom_labels.py) replaces labels in datafiles with custom labels
  - [`build_art_corpus.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/build_art_corpus.py) creates an artificial corpus
  - [`bert_finetune.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/bert_finetune.py) trains the models and saves them
  - [`evaluation.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/evaluation.py) saves evaluation metrics in result file
  - [`plot.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/plot.py) plots the metrics

* corpora: 
  - ChemProt training and development set
  - Ovesampled ChemPot training and development set
  - Artificial corpus training and development set

* models: 
  - best baseline model
  - best oversampled model
  - best artificial model 
  - best artifical model trained one epoch on ChemProt corpus

artifical_building_blocks:
* Create artificial corpus (link to drive)

## Visualisation of the pipeline

<img width="1098" alt="method" src="https://user-images.githubusercontent.com/46992305/121548522-5d156180-ca0d-11eb-8302-8eba64b548e9.png">

## How to run 

### Step 1: Setup

This setup is tested on Google Colabratory  using GPU on both MacOS Catalina and Windows 10.

First you need to follow the [`setup`](https://github.com/Aitslab/nlp_2021_alexander_petter#setup-using-conda-anaconda--miniconda) guide using Conda. Thereafter follow [`step 1: extracting relations`](https://github.com/Aitslab/nlp_2021_alexander_petter/tree/master/utils/chemprot#extracting-relations) to process your data. Do not continue to the `Building dataset` step as we don't want to change the data splits.

### Step 2: Run the pipeline
Change parameters in the config-file. And choose whether you want to run with the ChemProt coprus or the artifical corpus.

#### Step 2a: With the ChemProt corpus

`add_custom_labels:`

set `input_path` to the directory of the pocessed ChemProt files

#### Step 2b: With the artifical corpus

`build_copus:`

set `input_path` to the directorry of your building blocks 
choose the amount of sentences for each class for both the training and development set by setting the `train_class_size` and `dev_class_size` 

### Step 3: Train and save models

`bert_finetune`:

choose whether or not you want to `oversample` and state the classes and their respective factors on line `36`.

### Step 4: Evaluate

`evaluate`: 

change the `model_path` to the diectory of your models. `metrics_path` is the same as the `metrics_path` from step 3. 

### Step 5: Plot

## Run the NLP pipline

The relation extraction step written by us is integrated into a [`NLP pipeline`](https://github.com/Aitslab/nlp_2021_alexander_petter) written by previous students. The implementation of the relation extration can be found [`here`](https://github.com/Aitslab/nlp_2021_alexander_petter/blob/master/scripts/re.py).
