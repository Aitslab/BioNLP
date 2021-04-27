### 26/3

* First meeting with our supervisors
* Read the paper "SCIBERT: A Pretrained Language Model for Scientific Text" (https://arxiv.org/pdf/1903.10676.pdf)
* Read about SciBert (https://github.com/allenai/scibert)
* Watched a quick video about BERT: "BERT Neural Network - EXPLAINED!" (https://www.youtube.com/watch?v=xI0HHN5XKDo) 
* Cloned the BioNLP repo

### 1/4

* Tried to set up the environment, had issues with too little memory on Windows and a not compatible GPU with Cuda on Mac

### 6/4

* Meeting, got recommended to try Google Colab

### 13/4

* Meeting
* Set up logbook and the report 

### 19/4: 

* We got the environment to work and trained the SciBert on the Chemprot corpus using Google Colab
* Watched "Lecture 7 – Relation Extraction | Stanford CS224U: Natural Language Understanding | Spring 2019" (https://www.youtube.com/watch?v=pO3Jsr31s_Q)

### 24/4:
* Read the description of the Chemprot corpus
* Started writing a script to evaluate the SciBERT model

### 26/4
* Wrote script to predict the relational class of the Chemprot corups using SciBERT
* Wrote script to calculate the accuracy 

### 27/4
* Meeting with Sonja
* We modified the make_datasets to keep the original splits from the extract_relations to prevent overlapping between the dev and training sets 
* Added code to save the models from each epoch in the bert_finetune 
* Started looking at how to calculate the recall, f-score and precision for the models. However, we got the warning: 

/usr/local/lib/python3.7/dist-packages/sklearn/metrics/_classification.py:1272: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior. _warn_prf(average, modifier, msg_start, len(result)) {'OTHER', 'REGULATOR-POSITIVE', 'NOT', 'PART-OF'} Precision: [0.47938931 0. 0. 0. 0.76012793 0. ] Recall: [0.93037037 0. 0. 0. 0.54761905 0. ] F1-score: [0.63274559 0. 0. 0. 0.63660714 0. ]

* TODO 1/5: calculate the recall, f-score and precision for the models. Plot graphs for these metrics for the dev and train sets, create table with the statistics of the size of your dataset, write in the report
