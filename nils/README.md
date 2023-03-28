# EDAN70 NLP Project 2022
Author: Nils Broman

## Description
This project was part of the course EDAN70 Project in Computer Science at Lund University, in collaboration with the "Cell Death, Lysosomes and Artificial Intelligence" research group at Lund Biomedical Centre (BMC). In this project, I continued the work of prior students, to improve training of BERT-based language models for classifying relations between chemicals and proteins found in scientific articles. For more info, read the full report found in this repo. Instructions on how to use the code to train models of your own can be found below. 

## Files

* **[root](https://github.com/Aitslab/BioNLP/blob/master/nils/)**
    - [`main.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/main.py): The main script used to run the pipeline.
    - [config.json](https://github.com/Aitslab/BioNLP/blob/master/nils/config.json): Configuration file, specifying paths for models, corpora, metrics, and plots as well as details for training and construction of corpora.
    - [`plotting_notebook.ipynb`](https://github.com/Aitslab/BioNLP/blob/master/nils/plotting_notebook.ipynb): Due to making many small changes in the plots while analyzing the data, i opted for using a notebook. If you want to use the [`plot.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/scripts/plot.py) in the scripts folder in the main pipeline, you must first update it with with the functions in this notebook.
    - [`log.ipynb`](https://github.com/Aitslab/BioNLP/blob/master/nils/log.ipynb): Worklog, though not fully all-inclusive
    

* **[scripts](https://github.com/Aitslab/BioNLP/blob/master/nils/scripts)**
    - [`add_custom_labels.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/scripts/add_custom_labels.py): Adds the custom labels to the corpus. Updated to also add custom labels to the sample and test set.
    - [`bert_finetune.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/scripts/bert_finetune.py): Fine-tunes the BERT model on the ChemProt corpus and saves as a new model after each epoch. Updated to use the correct tokenizer for SciBERT.
    - [`build_art_corpus.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/scripts/build_art_corpus.py): Constructs the artificial corpora using randomized building blocks. Creates a separate file for each label, then combines them into one file. Updated to use the artificial chem-prot interactions.
    - [build_mixed_corpus.py](https://github.com/Aitslab/BioNLP/blob/master/nils/build_mixed_corpus.py): Combines the baseline corpora and a percentage of artificial data (with the option of adding weighted support for the labels).
    - [`evaluation.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/scripts/evaluation.py): Loads and evaluates the models saved after every epoch from bert_finetune, and saves the statistics of precision, recall, f-score as well as confusion matrices to a file. Updated metrics path to fit my machine. Added micro and weighted averages as well as confusion matrices to the list of metrics.
    - [`plot.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/scripts/plot.py): Plots f-score, precision, recall, accuracy-loss curves over epochs. **NOTE: Outdated due to the use of a notebook** 

* **[data](https://github.com/Aitslab/BioNLP/blob/master/nils/data)**:
    - [artificial-building-blocks](https://github.com/Aitslab/BioNLP/blob/master/nils/data/artificial-building-blocks) Text files with the builing blocks for artificially constructing sentences, using ChemProt labels
    - [artificial-custom-labeled](https://github.com/Aitslab/BioNLP/blob/master/nils/data/artificial-custom-labeled) Custom labeled artifically constructed sentences used to make artificial corpora
    - [chemprot](https://github.com/Aitslab/BioNLP/blob/master/nils/data/chemprot) Raw [ChemProt data](https://biocreative.bioinformatics.udel.edu/news/corpora/chemprot-corpus-biocreative-vi/)
    - [`extract_relations.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/data/extract_relations.py): Processes the ChemProt data to a line-by-line format that can be fed to the BERT models (from [Alexander and Petter](https://github.com/Aitslab/nlp_2021_alexander_petter/tree/master/utils/chemprot/)).
    - [extract_chemical_names.py](https://github.com/Aitslab/BioNLP/blob/master/nils/data/extract_chemical_names.py): Extracts the names of the chemicals in the ChemProt train set.


* [corpora](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora): The processed corpora used for training and evaluating models

    - [`chemprot_train.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/chemprot_train.txt): ChemProt training set.
    - [`chemprot_dev.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/chemprot_dev.txt): ChemProt development set.
    - [`chemprot_sample.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/chemprot_sample.txt): ChemProt sample set.
    - [`chemprot_test.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/chemprot_test.txt): ChemProt test set.
    - [`artificial_pp_train.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/artificial_pp_train.txt): Artificial training set with 5000 protein-protein interactions, 1000 of each class.
    - [`artificial_pp_dev.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/artificial_pp_dev.txt): Artificial development set with 2500 protein-protein interactions, 500 of each class.
    - [`artificial_cp_train.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/artificial_cp_train.txt): Artificial training set with 5000 chemical-protein interactions, 1000 of each class.
    - [`artificial_cp_dev.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/artificial_cp_dev.txt): Artificial development set with 2500 chemical-protein interactions, 500 of each class.
    - [`mixed_train_10.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/mixed_train_10.txt): Mixed training set consisting of ChemProt training set with an additional 10% artificial data, using chemical-protein interactions.
    - [`mixed_train_25.txt`](https://github.com/Aitslab/BioNLP/blob/master/nils/corpora/mixed_train_25.txt): Mixed training set consisting of ChemProt training set with an additional 25% artificial data, using chemical-protein interactions.

*   **[test-environments](https://github.com/Aitslab/BioNLP/tree/master/nils/test-environments)**
    - [`pytorch_env_test.ipynb`](https://github.com/Aitslab/BioNLP/blob/master/nils/test-environments/pytorch_env_test.ipynb): Checks that pytorch is working correctly and with GPU utilization enabled
    - [`tensorflow_env_test.ipynb`](https://github.com/Aitslab/BioNLP/blob/master/nils/test-environments/tensorflow_env_test.ipynb): Checks that tensorflow is working correctly and with GPU utilization enabled. Though tensorflow is not used in this project, it is part of the major pipeline.


## Setup

As this project is part of a [larger pipeline](https://github.com/Aitslab/nlp_2021_alexander_petter), it is easiest to use the same environment and packages (with some additions) to ensure compatibility, even though some of them will not be used in this project. I used my own hardware for training, and to do so you must ensure you're using the correct versions of CUDA and cuDNN (I used PyTorch: 1.8.1+cu111 CUDA: 11.1, cuDNN: 8005).

### Setup using Conda (Anaconda / Miniconda)

It's best to create a custom environment first:

```
conda create -n ENV_NAME
conda activate ENV_NAME
conda install python==3.7
```

This will create an empty environment and install Python 3.7 together with
the corresponding version of pip. We will then use _that_ version of pip
to install the requirements.

Clone this repo using git, navigate to the folder. Then run:

```
pip install -r requirements.txt
```

It's important to get this right, since BERT requires TensorFlow 1.15,
which in its turn requires Python/pip 3.7 (not 3.8). If you get an error for tensorflow (ERROR: Could not find a version that satisfies the requirement tensorflow==1.15.0
ERROR: No matching distribution found for tensorflow==1.15.0) check if you are inside the environment you made.

## Usage

The main pipeline is run using [`main.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/main.py) file and controlled by altering the parameters in [config.json](https://github.com/Aitslab/BioNLP/blob/master/nils/config.json). By setting the parameters accordingly, all steps (other than preprocessing and plotting) of choice can be run in succession.

#### Step 0.5: Preprocessing data and building the corpora (Optional)

### Preprocessing
Since I've already created these files, you may skip this step, but if you want to recreate, follow the instructions for extracting relations found in [the data folder](https://github.com/Aitslab/BioNLP/tree/master/nils/data), but skip the part for building datasets. 

#### Build corpora
In [the config file](https://github.com/Aitslab/BioNLP/blob/master/nils/config.json) under `ignore`, set `create_custom_labels` to `false`, and change the paths if needed, before running the [main script](https://github.com/Aitslab/BioNLP/blob/master/nils/main.py)

Similarly, to construct the artificial sets, change the parameters under `build_art_corpus` and/or `build_mixed_corpus` as needed in [the config file](https://github.com/Aitslab/BioNLP/blob/master/nils/config.json) and set the ignore status to `false`. 


### Step 1: Training the model

In [the config file](https://github.com/Aitslab/BioNLP/blob/master/nils/config.json), change the paths to the training and development set of choice, as well as where you want to save the model and model metrics. Additionally, pick the number of epochs to train and if you want to use oversampling. 

### Step 2: Running evaluation

Again, alter the paths for model, metrics, train and development set and enable evaluation in [the config file](https://github.com/Aitslab/BioNLP/blob/master/nils/config.json).

### Step 3: Create plots

Use the [plotting notebook](https://github.com/Aitslab/BioNLP/blob/master/nils/plotting_notebook.ipynb) to create the plots. As of writing, the notebook includes plots for accuracy/loss, F1-score, precision, recall as well as confusion matrices. If you'd rather want to make it part of the pipeline, you may simply update [`plot.py`](https://github.com/Aitslab/BioNLP/blob/master/nils/scripts/plot.py) with the functions from the notebook.
