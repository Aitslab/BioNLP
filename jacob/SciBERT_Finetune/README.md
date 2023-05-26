This is the README for the SciBERT fine-tuning project
---
# Introduction
A previous student of the Aits Lab group, Nils Broman, experimented with fine-tuning the [SciBERT](https://arxiv.org/abs/1903.10676) model for relation extraction using the ChemProt and artificial corpora.
To further his work, I created a new corpus to see if performance could be improved from his existing model. This new corpus was a
merged version of the [ChemProt](https://biocreative.bioinformatics.udel.edu/news/corpora/chemprot-corpus-biocreative-vi/) and [DrugProt](https://zenodo.org/record/5119892) corpus.
After careful validation, it was shown that my fine-tuned model
trained on the combined corpus achieved a 5% gain in performance.

# Setup
To setup the environment, you can use the following command (called from this
directory) to create a new Anaconda virtual environment with the necessary
packages.
```
conda env create -f ../envs/scibert_environment.yml
```
Once created, activate the environment with
```
conda activate scibert
```

# Files
## Data
* [corpora](corpora) folder: Contains pre-processed `.txt` files of the corpora training and devlopment sets loaded by the model
*  [data](data) folder: Raw corpora data files
## Scripts
* [jacob_edits](jacob_edits) folder: Contains the main changes I made to Nils' repository
  * [bert_finetune_job.sh](jacob_edits/bert_finetune_job.sh): Bash script to set up SciBERT training jobs on Berzelius (after [config.json](config.json) has been set)
  * [plotting-notebook.ipynb](jacob_edits/plotting-notebook.ipynb): Plots epoch-level loss curves, accuracy, precision/recall/F1 scores, and confusion matrices for the SciBERT fine-tuning with the combined ChemProt and DrugProt corpus
  * [plotting-notebook-os.ipynb](jacob_edits/plotting-notebook-os.ipynb): Plots epoch-level loss curves, accuracy, precision/recall/F1 scores, and confusion matrices for the SciBERT fine-tuning with the *oversampled* combined ChemProt and DrugProt corpus
* [scripts](scripts) folder: Contains the scripts related to each steup in the fine-tuning pipeline
  * [add_custom_labels.py](scripts/add_custom_labels.py): Pre-processing script to map CPR labels to the 5 custom classes: `INTERACTOR`, `NOT`, `PART-OF`, `REGULATOR-NEGATIVE`, and `REGULATOR-POSTIVE`
  * [bert_finetune.py](scripts/bert_finetune.py): Script to perform SciBERT fine- tuning. I added a new oversampling strategy for the combined ChemProt/DrugProt corpus
  * [roberta_finetune.py](scripts/roberta_finetune.py): Script to perform [RoBERTa](https://huggingface.co/AdapterHub/roberta-base-pf-scicite) fine-tuning (work in progress)
* [main.py](main.py): Main script use to run various subtasks of the RE pipeline (pre-processing, training, validation, etc.). I added support for RoBERTa finetune (work in progress)

## Figures/Results
* [jacob_edits/figs](jacob_edits/figs/) folder: Initial training test using the ChemProt corpus. Not used/discussed in the [report](../EDAN70_Project_Report_JacobK.pdf).
* [jacob_edits/merged-figs](jacob_edits/merged-figs/) folder: Loss curves, accuracy plots, epoch-level precision/recall/F1 plots, and 
confusion matrices produced during the `evaluation` of the combined corpus model
* [jacob_edits/merged-os-figs](jacob_edits/merged-os-figs/) folder: Loss curves, accuracy plots, epoch-level precision/recall/F1 plots, and 
confusion matrices produced during the `evaluation` of the *oversampled* combined corpus model (see [report](../EDAN70_Project_Report_JacobK.pdf) for oversampling strategy)

# Configuration File
General details about the [config.json](config.json) file 
can be found in Nils' [repository](https://github.com/Aitslab/BioNLP/tree/master/nils)
* `ignore` section: The boolean flag should be set to `false` for parts of the pipeline you want to run (parts described below)
* `add_custom_labels` section: Converts the CPR codes of the corpus to the 5 classes (see [here](https://github.com/Aitslab/BioNLP/tree/master/nils/data) for more details) 
  * `input_path`: Directory of the processed data (directions on how to process the data can be found [here](https://github.com/Aitslab/BioNLP/tree/master/nils/data))
  * `output_path`: Directory of the [corpora](corpora) folder
* `build_art_corpus` section: See Nils' [repository](https://github.com/Aitslab/BioNLP/tree/master/nils) for details
* `build_mixed_corpus` section: See Nils' [repository](https://github.com/Aitslab/BioNLP/tree/master/nils) for details
* `bert_finetune` section: Paths needed for SciBERT fine-tuning
  * `train_path`: Path to processed training set in the [corpora](corpora) folder
  * `dev_path`: Path to processed development set in the [corpora](corpora) folder
  * `model_path`: Directory to the model checkpoints with each epoch in its own numbered subfolder
  * `metrics_path`: Filename where you want to save epoch-level training/validation loss and accuracy, ideally in a `metrics` folder
  * `oversample`: Boolean whether or not to use the oversampling strategy
  * `epochs`: Number of epochs to train for
* `roberta_finetune` section: Paths needed for RoBERTa fine-tuning (same as `bert_finetune` except no `oversample` option)
* `evaluation` section: Paths needed to perform a more detailed epoch-level analysis of performance using precision/recall/F1
  * `train_path`: Should match `bert_finetune` parameter
  * `dev_path`: Should match `bert_finetune` parameter
  * `model_path`: Should match `bert_finetune` parameter
  * `metrics_path`: Should be a COPY of the `metrics_path` file from `bert_finetune` BUT with a different name (to prevent any results from being overwritten)
* `plot` section: This part of the pipeline has been superceded by the [plotting-notebook](plotting-notebook.ipynb)

# Usage
To ensure relative paths in scripts work properly, run the `main.py` script from this folder after editing the configuration file using the command:
```
python main.py
```