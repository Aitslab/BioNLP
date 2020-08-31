# BINP37, Bioinformatics: Research Project

This repository contains the code used in my short Research Project during the Spring semester of 2020, as a part of my master's in Bioinformatics at Lund University. A detailed explanation of the project can be found in the Project Report inside the repo.

# Contents

The formatting scripts do the following:

eval_to_pubannot.py: converts 'NER_results_conll.txt' file to PubAnnotation format. Requires reference file.
gold_to_test.py: converts PubAnnotation format Gold Standard Corpus to BioBERT test.tsv file.
json_to_txt.py: converts CORD-19 Kaggle JSON file to plain text. Also produces reference files.
pubannot_to_tsv.py: Converts PubAnnotation format JSON file to BioBERT test.tsv file. Produces reference.
rename_gold.py: Script used to rename the Gold Standard Corpus.
text_to_tsv.py: Converts plain text to BioBERT test.tsv format.
gold_to_text.py: Converts PubAnnotation format Gold Standard Corpus to plain text.

The sripts in utils do the following:

bioBERT.ipynb: Jupyter Notebook file containing a (not very good) guide to BioBERT I wrote. 
pubannotationevaluator.py: Script that compares PubAnnoation files. Written by Annie and Sofi.
use_evaluator.py: Script used to run Annie and Sofi's evaluator.
split_traindev.py: Splits BioBERT traindev.tsv file into train and dev files.
fuse_tsvs.py: Merges BioBERT tsv files into one.

Specific usage instructions inside each script.

# Data

Most of the Data used in this project can be found here: https://drive.google.com/file/d/1L3Bsn2m7vZN8ge52PqseRY2URBqDDwsZ/view?usp=sharing

# Results

Most of the files related to the results of the project can be found here: https://drive.google.com/file/d/1f-v5r4T9yWGxUqhQl4-5OAhCwYXsCTlm/view?usp=sharing

# References

The template for this README.md file was obtained [here](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2).

[BioBERT](https://github.com/dmis-lab/biobert) is a biomedical language representation model based on BERT.

## Author

**Antton Lamarca** - [AnttonLA](https://github.com/AnttonLA)
Contact me at anttonlamarca@gmail.com

## Acknowledgments

* Thanks to professor Sonja Aits for her guidance and help during this project.
* Thanks to Prof. Pierre Nugues, Dr. Marcus Klang and to Salma Kazemi Rashed for their time and help.
* Thanks to Emil, Peter, William, Annie, Sofi, Viktor and Rasmus.
* Hat tip to anyone else whose code was used.
