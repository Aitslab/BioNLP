## File structure

* root:
  - [`config.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/config.json) configuration parameters to the pipeline
  - [`main.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/main.py) runs the pipeline

* scripts: 
  - [`add_custom_labels.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/add_custom_labels.py) replaces labels in datafiles with custom labels
  - [`build_art_corpus.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/build_art_corpus.py) creates an artificial corpus
  - [`bert_finetune.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/bert_finetune.py) trains the models and saves them
  - [`evaluation.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/evaluation.py) saves evaluation metrics in result file
  - [`plot.py`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/scripts/plot.py) plots the metrics

* corpora: 
  - ChemProt [`training`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/corpora/chemprot_train.txt) and [`development`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/corpora/chemprot_dev.txt) set
  - [`statistics`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/corpora/statistics.txt) which specifies the distribution of the classes in the ChemProt training and development sets
  - Artificial corpus [`training`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/corpora/artificial_train.txt) and [`development`](https://github.com/Aitslab/BioNLP/blob/master/lykke_klara/corpora/artificial_dev.txt) set

## artificial building blocks
The files used to build the artificial corpus can be found [`here`](https://drive.google.com/drive/folders/1REtDAAx6rfL2JkO0FLCg3xIQOT9xJCkS). The protein entities were extracted from the [`Uniprot database`](https://www.uniprot.org/) by previous students and the cell line names in the start phrases were taken from the [`cell line ontology`](http://www.obofoundry.org/ontology/clo.html) by our  biomedically trained supervisor Sonja Aits. Aits then compiled start phrases and replaced different verbs, adjectives, adverbs and nouns with synonyms.

## Models
Since the models are too big to upload on git, the best model from each configuration can be found:
  - [`baseline model`](https://drive.google.com/drive/folders/1_jNQFYvr4TrU4mEZenR6IlKv3qsTBSPy?usp=sharing)
  - [`oversampled model`](https://drive.google.com/drive/folders/1RA080Eoy1Q7gYiqutxYQtZf-cDKLTCEw?usp=sharing)
  - [`artificial model`](https://drive.google.com/drive/folders/1u8bAsUDlGkY6GOtKzxJn7Sf8LXRl9vs7?usp=sharing)
  - [`artifical model trained one epoch on ChemProt corpus`](https://drive.google.com/drive/folders/1zshZodHcMGN2URyv4T4T8KPCL1D08NPt?usp=sharing)


## Visualisation of the pipeline

<img width="1098" alt="method" src="https://user-images.githubusercontent.com/46992305/121548522-5d156180-ca0d-11eb-8302-8eba64b548e9.png">

## How to run 

### Step 1: Setup

This setup is tested on Google Colabratory using GPU on both MacOS Catalina and Windows 10.

First you need to follow the [`setup`](https://github.com/Aitslab/nlp_2021_alexander_petter#setup-using-conda-anaconda--miniconda) guide using Conda. Thereafter follow [`step 1: extracting relations`](https://github.com/Aitslab/nlp_2021_alexander_petter/tree/master/utils/chemprot#extracting-relations) to process your data. Do not continue to the `Building dataset` step as we don't want to change the data splits.

### Step 2: Run the pipeline
Change parameters in the config-file. And choose whether you want to run with the ChemProt corpus or the artifical corpus. The input and output for each script can be found in the config file.

#### Step 2a: With the ChemProt corpus

`add_custom_labels:`

set `input_path` to the directory of the processed ChemProt files

#### Step 2b: With the artifical corpus

`build_copus:`

set `input_path` to the directory of your building blocks 
choose the amount of sentences for each class for both the training and development set by setting the `train_class_size` and `dev_class_size` 

### Step 3: Train and save models

`bert_finetune`:

choose whether or not you want to `oversample` and state the classes and their respective factors on line `36`
the script outputs training loss, validation loss and training accuracy to the file specified in `metrics_path`

### Step 4: Evaluate

`evaluate`: 

change the `model_path` to the diectory of your models. `metrics_path` is the same as the `metrics_path` from step 3. 

### Step 5: Plot

saves the plots in the specified output directory

## Run the NLP pipline

The relation extraction step written by us is integrated into a [`NLP pipeline`](https://github.com/Aitslab/nlp_2021_alexander_petter) written by previous students. The implementation of the relation extraction can be found [`here`](https://github.com/Aitslab/nlp_2021_alexander_petter/blob/master/scripts/re.py).
