This is the README for the BioGPT Hyperparameter Tuning
and Free-form Relation Extraction (RE) sub-projects
---
# Introduction
## Hyperparameter Tuning
Hyperparameter tuning is the process of adjusting model "hyperparameters"
to optimize a specific performance metric of the model. Hyperparameters 
include: learning rate, dropout, hidden layer sizes, and number of attention heads. In this sub-project, I adjusted the learning rate (and associated parameters) and dropout to try to decrease the BioGPT validation loss.

## Free-form Relation Extraction
A problem with many Natural Language Processing (NLP) deep learning models is 
that they have been trained on specific corpora. As a result, it is hard for a
non-technical end-user to apply such a model to new data which is not in that
corpus' format. Therefore, I worked on adding BioGPT inference capability
on free-form text contained in a standard `.txt` file. This allows the BioGPT
model to perform RE on any text. Such a capability can then
be integrated with other NLP RE pipelines, such as the [Aits Labs 
pipeline](https://github.com/Aitslab/BioNLP/tree/master/lykke_klara).
To implement the free-form text RE, I used the following 3 approaches
1. End-to-end RE using modified [inference](examples/RE-BC5CDR/infer_free_form.sh) script
2. Text generation for Named Entity Recognition (NER), then RE
3. Text generation for NER via look-up table


# Setup
## Development Environment
To setup the environment, you can use the following command (called from this
directory) to create a new Anaconda virtual environment with the necessary
packages.
```
conda env create -f ../envs/biogpt_environment.yml
```
Once created, activate the environment with
```
conda activate biogpt
```

If installation fails, create a new environment manually
with Python 3.10 and PyTorch 2.0.0, and install other missing
dependencies via `pip install`. **Please note** that a GPU
is required to run inferences with the BioGPT model.

## Model Checkpoint
Due to model checkpoint files being very large, they are not part of the GitHub repository and instead can be
downloaded from this **link**.

# Key Files
Please note, this repository is a clone of the 
[BioGPT](https://github.com/microsoft/BioGPT) repository and contains 
many unnecessary files/folder related to my research.
The files/folders I worked on are described below.

## Data
* [data/BC5CDR/raw](data/BC5CDR/raw): Raw data from the [BC5CDR](https://biocreative.bioinformatics.udel.edu/tasks/biocreative-v/track-3-cdr/) corpus
* [free_form_RE](free_form_RE): Input and output `.txt` files for free-form text RE with the 3 methods described above
  * [in](free_form_RE/in) folder: Input `.txt` files, specifically 2 PubTator abstracts, and one custom file
  * [out](free_form_RE/out) folder: Output `.txt` files. The number after the `v` in the file denotes which method was used. `RE` only prefix files denote no NER was used (even by manual annotations) and `RE_NER` denotes manual NER annotations were added.
  * [temp](free_form_RE/temp/) folder: Stores temporary files in the inference process, including tokenized and BPE-encoded text files

## Scripts and Results
* [examples/RE-BC5CDR](examples/RE-BC5CDR/) folder: Main folder for hyperparameter tuning and the end-to-end RE method for free form text.
  * `.out` files: Log files from training or inference scripts run as batch jobs
  * [infer_free_form.sh](examples/RE-BC5CDR/infer_free_form.sh): Bash script that takes an input `.txt` file, per
  * [infer_vJacob.sh](examples/RE-BC5CDR/infer_vJacob.sh): Modification of initial infer script to work on my machine
  * [preprocess_train_vJacob.sh](examples/RE-BC5CDR/preprocess_train_vJacob.sh): Bash script used to preprocess BC5CDR data and start a training job, in particular one of the hyperparameter tuning experiments
* [interactive](interactive) folder: Main folder for my free-form text RE subproject.
  * [free_form_RE_textgen_NER_lookup.py](free_form_RE/free_form_RE_textgen_NER_lookup.py): Runs free-form text RE using Method 3 from above, where each word in the input file is scanned and compared with a lookup table to see if it is a chemical or disease. Then a prompt in the form of `The relation between {chemical} and {disease} is` is passed to BioGPT and the result for each chemical/disease pair is saved in the output file.
* [train_eval](train_eval) folder: Scripts and figures related to hyperparameter tuning of BioGPT for RE using the `BC5CDR` corpus
  * [results](train_eval/results) folder: Figures from 3 training runs of BioGPT, the [2023_04_27](train_eval/results/BioGPT_TrainValid_Loss_2023_04_27.png) file correspondings to the first hyperparameter tuning experiment in the paper, and the [2023_05_17](train_eval/results/BioGPT_TrainValid_Loss_2023_05_17.png) file is the second hyperparameter tuning experiment
  * [biogpt_loss_curves.ipynb](train_eval/biogpt_loss_curves.ipynb) A Jupyter notebook adapted from  Salma Kazemi Rashed to parse the `.out` file from training, extracting the training/validation loss metrics and plotting them.

# Usage
To ensure relative paths in scripts work properly, 
run all scripts from the folder they reside in.
## Hyperparameter Tuning
To start a new hyperparameter tuning experiment, modify the 
[preprocess_train_vJacob.sh](examples/RE-BC5CDR/preprocess_train_vJacob.sh) script to activate your Anaconda
environment and change the `SAVE_DIR` directory if desired.
To run the script, use:
```
./preprocess_train_vJacob.sh
```

## Free-form Text RE
To use Method 1 from above, modify the `MODEL_DIR` and `MODEL` variables in the [infer_free_form.sh](examples/RE-BC5CDR/infer_free_form.sh) script and Anaconda environment and run the script with the following format:
```
./infer_free_form.sh INPUT_FILE OUTPUT_FILE
```

To use Method 2 from above, use the [free_form_RE_textgen.py](free_form_RE/free_form_RE_textgen.py) script with the input and output files specified as pipes. Please note that
this method did **NOT** work well and that Method 3 should
be used instead.
```
python free_form_RE_textgen.py < INPUT_FILE > OUTPUT_FILE
```

To use Method 3 from above, use the [free_form_RE_textgen_NER_lookup.py](free_form_RE/free_form_RE_textgen_NER_lookup.py) script with the input
and output files specified as follows:
```
python free_form_RE_textgen_NER_lookup.py --in_file INPUT_FILE --out_file OUTPUT_FILE
```
