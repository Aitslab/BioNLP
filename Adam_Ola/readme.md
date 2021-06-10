# NER_200

This is a repository with material for evaluating the Hunflair NER corpora on BioBERT

It provides the following: 
* A filestructure and jupyter notebook adapted to be run on Google Colab.
* The NER corpora from HunFlair converted to a format compatible with BioBERT.
* Fine-tuned models where Hunflair corpora and BioBERT-Base v1.1 (+ PubMED 1M) has been used.
* Evalutations from run models.
* Instructions on how to do your own NER fine tuning or evaluation.

## Background

**BioBERT:**
Please see the paper and git repository for description of BioBERT
* [BioBERT: a pre-trained biomedical language representation model for biomedical text mining](http://doi.org/10.1093/bioinformatics/btz682).
* [DMIS-Lab BioBERT](https://github.com/dmis-lab/biobert/blob/master/README.md)

**HunFlair:**
Please see the paper and git repository for description of HunFlair
* [HunFlair: An Easy-to-Use Tool for State-of-the-Art Biomedical Named Entity Recognition](https://arxiv.org/abs/2008.07347)
* [FlairNLP HunFlair](https://github.com/flairNLP/flair/blob/master/resources/docs/HUNFLAIR.md)


## Setup

Before you can do any evalutaion or fine tuning you must have thie filestructure ready.

1. Download this repository to your local machine.
    ```
    git clone https://github.com/AdamBarvesten/NER_200.git
    ```
2. Copy the NER_200 folder and put it in your Google Drive 
3. Download the wanted verision of BioBERT [here](https://github.com/dmis-lab/biobert/blob/master/README.md#download) to your local machine. Our results was given by BioBERT-Base v1.1 (+ PubMED 1M). _Please note BioBERT-Large is too large for a free verision of Google Colab_
4. Extract the files from the downloaded BioBERT archive and put the files on your Google Drive in the folder named 'biobert_pretrained_weights'.
5. Make sure the files are named accordingly with X replaced with correct number (For BioBERT-Base v1.1 (+ PubMed _**1M**_ ) : X = '1000000')
* bert_config.json 
* model.ckpt-X.data-00000-of-00001
* model.ckpt-X.index
* model.ckpt-X.meta
* vocab.txt


## Fine tuning

***Please note, this may take several hours. The corpora all_chemical and all_disease are too big for the free verision of Google Colab***

1. Run the notebook NER_200.ipynb according to the instructions
2. Make sure you're configuring the input path to the corpora you wish to fine tune with correctly, as noted in the notebook.


## Evaluating

1. Aquire a fine tuned model either by creating your own, or dowload one of our pre computed [here](https://drive.google.com/drive/folders/1TReOc9S4134nS1Verkt9jxlds-eFNOyo?usp=sharing).
2. Put the contents of the folder into the ner_outputs folder.
3. Run the notebook NER_200.ipynb according to the instructions

## Contact

[Adam Barvesten](https://www.linkedin.com/in/adam-varg-b-63908389/), ad2626ba-s@student.lu.se

Ola Olde, elt13oo1@student.lu.se

