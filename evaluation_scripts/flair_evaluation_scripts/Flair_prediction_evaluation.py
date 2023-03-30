#!/usr/bin/env python
# coding: utf-8



from flair.data import Corpus
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings, ELMoEmbeddings
from typing import List
import torch

# 1. get the corpus
from flair.data import Corpus
from flair.datasets import ColumnCorpus

# define columns
columns = {0: 'text', 1: 'ner'}

# this is the folder in which train, test and dev files reside
data_folder = '../20230328_RA_nlpeng_craft_4.0.0_processed/PR_gene_spacy_custom/'  ## This could be any .tsv format data

# init a corpus using column format, data folder and the names of the train, dev and test files
corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file='train.tsv',
                              test_file='test.tsv',
                              dev_file='devel.tsv')   ## This could be only test.tsv file

### If gpu was available
device = None
if torch.cuda.is_available():
	device = torch.device('cuda:0')
	print('gpu')
else:
	device = torch.device('cpu')
	print('cpu')                                


from flair.data import Sentence
from flair.models import SequenceTagger
# load tagger
tagger = SequenceTagger.load('hunflair-gene')  ## This model could be any model from Flair repos listed in flair/models/sequence_tagger_model.py from https://nlp.informatik.hu-berlin.de/resources/models/

## The result of prediction will be saved in prediction_gene.txt file and evaluated by flair scrip.
result = tagger.evaluate(corpus.test, mini_batch_size=4, out_path=f"predictions_gene.txt", gold_label_type="ner")
print(result.detailed_results)