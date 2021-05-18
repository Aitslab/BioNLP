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

![image](https://user-images.githubusercontent.com/21019121/116400197-0e7b8180-a82a-11eb-83d3-755737162880.png)

Confusion matrices for the 1st model:

![image](https://user-images.githubusercontent.com/21019121/116403398-ccecd580-a82d-11eb-959a-bf722340ad87.png)

* TODO 1/5: calculate the recall, f-score and precision for the models. Plot graphs for these metrics for the dev and train sets, create table with the statistics of the size of your dataset, write in the report

### 1/5
* Removed "OTHER" label from the data (and bert_finetune.py)
* Added code to retreive all metrics from the models and put it in the report (we will change the screenshots to tables later)

* We still get the error:

![image](https://user-images.githubusercontent.com/21019121/116787160-e77bb480-aaa2-11eb-90f3-123b7ab9eee9.png)

* Wrote code to plot the f1-score, precision and recall. We could not save them since our time on Google Colab ran out.

* TODO 3/5: 
* Run the script to get the plots
* Fix script to plot the training metrics
* Fill in the statistics table
* Figure out which confusion matrix maps to which class and put it in the report
* Write corpus & tools section in report

### 2/5
* Wrote the section about code and code changes

### 3/5
* generated plots for f1-score, precision and recall for the models for dev and train
* generated plot for avg. training loss, avg. validation loss and avg. training accuracy for the training set
* created the statistics table (will fill in the values tomorrow)
* started writing on the corpus section in the report

TODO 4/5:
* modify add_custom_labels to count statistics and fill in values in table
* Figure out which confusion matrix maps to which class and put it in the report
* Write corpus & tools section in report

### 4/5:
* edited the metrics plots
* generated statistics for our custom label datasets
* figured out which confusion matrix maps to which class


### 5/5
* Meeting: decided to try to oversample the data for the classes NOT and PART-OF
* started refactoring the code: created a new eval.py file which should take in the corpora and a model and then return all the metrics. Our goal is to also create a seperate plot file and another one that outputs the confusion matrices

### 6/5
* continuing refactorization, although our precision for "NOT" class in model 2 all of a sudden got a value of 1. We need to look into that.

### 8/5
* Tried to debug the unexpected behaviour in our metrics. No luck :)
* Generated all metrics for 5 epochs from the old code. However, sometimes we get extra graphs in our plots which don't correspond to any of our data. 

### 10/5
* Our refactored code seems to work without any changes, it's unclear why it generated weird results before. We created two new files, eval and plot, from our old script metrics. They are now availabe on git. 
* We generated new plots and metrics for the 5 ecpohs, they are under the section "Appendix" at the moment, but will replace our old results shortely. 

TODO 11/5:
* write manual on how to run our program
* add code comments
* add the new data to the report
* start to look at oversampling

### 11/5
* Wrote a README with instructions on how to run our scripts
* Cleaned up our code and added some comments
* Started writing code to oversample data before training

### 12/5
* Finished the code for oversampling the train.txt file
* Trained all the models on the oversampled data and evaluated
* Saved the results in the report
* Attended a meeting with the other groups

### 13/5 (Lykke)
* Created the run_re script which takes as input the output from NER and outputs a tsv file with the entities, relation and sentence

### 16/5 (Lykke)
* integrated the code from run_re to the main.py in the pipeline. moved the code to a separate script in the script directory
* updated README to fit the changes
* updated code changes in report

### 17/5
* added code to the re.py script to output a file with statistics for the relations
* started looking at the visualization in cytoscape
* started working on the presentation

### 18/5
* Used Sonja's script to create artificial train and dev corpora
* Trained new models using the artificial train corpus
* Attempted to evaluate the models using the artificial train, the artificial dev and the original dev corpus. Ran into major issues with Google Colab, we are currently unable to save our evaluation metrics :(
