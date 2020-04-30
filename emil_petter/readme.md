This is the repository for a student project at LU in Fall term 2019

It contains the following code:


protein.py: A datastructure used to represent a protein

buildUniprot.py: Reads the xml representation of the UniprotKB/Swiss-Prot database and parses all the data into a list which is then saved using pickle as /out/uniprot.out

buildHGNC.py: Reads the json representation of the HGNC database and parses all the data into a list which is then saved using pickle as /out/hgnc.out

buildDict.py: Combines the the two file outputed by the above scripts and combines them into a unified dictionary, assigning all proteins a unique ID. This dictionary is then used to create an index that can be used in conjuntion with Marcus Klang's dictionary tagger. !NOTICE! This script requires the server from Marcus Klang's dictionary tagger to be running. The code for this can be found here: https://github.com/Aitslab/BioNLP/tree/master/marcus/dictionarytagger

corpus.py: Reads through the corpus file /in/test.tsv to create a list of all entitites found in the text.

evalDict.py: Runs Marcus Klang's dictionary tagger with the previouslt generated index file and finds all matches. It then evalues these matches and prints precision, recall and F1-score. !NOTICE! This script also requires the server from Marcus Klang's dictionary tagger to be running.

evalBert.py: Evaluates the BioBERT results and prints precision, recall and F1-score.

evalCombined.py: Creates a union and an intersection of the dictionary and BioBERT results and evalueates them. Prints precision, recall and F1-score

The mentionindex folder is part of Marcus Klang's code.

All necessary files except for the Uniprot xml and the HGNC json can be found here. This is due to file size constraint on github. These can be downloaded here:

Uniprot - ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz

HGNC - ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/json/hgnc_complete_set.json

