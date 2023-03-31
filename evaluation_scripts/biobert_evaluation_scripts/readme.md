## BioBERT Prediction Script
Created 19th Jan, 2023 by Rafsan Ahmed

The biobert_prediction_script.sh script is used to run predictions on test sets of a corpora (IOB2 format) with a pre-trained or fine-tuned (both are ok) BioBERT model. The scripts predicts tags using the specified model and saves them into the given SAVE_DIR folder, while calculating precision, recall and F1 scores. It uses an updated run_ner.py script from the original BioBERT repository (https://github.com/dmis-lab/biobert-pytorch). While the original BioBERT script is used to fine-tune models, evaluate and run predictions; the updated script only keeps the part of the script that is used to run predictions (--do_predict).

