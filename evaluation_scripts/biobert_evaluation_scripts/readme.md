## BioBERT Prediction Script
Created 19th Jan, 2023 by Rafsan Ahmed

The biobert_prediction_script.sh script is used to run predictions on test sets of a corpora with a pre-trained or fine-tuned (both are ok) BioBERT model. The scripts gets predictions and saves them into the given SAVE_DIR folder, while calculating precision, recall and F1 scores. It uses an updated run_ner.py script from the original BioBERT repository (https://github.com/dmis-lab/biobert-pytorch) is included. This is however only for fine-tuning models and not necessarity for predictions. The update only includes addition of early stopping callback of 50 epochs.

