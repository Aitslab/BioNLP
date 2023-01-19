export MAX_LENGTH=192
export ENTITY=disease
export SEED=1
export SAVE_DIR=/path/to/save/predictions
export DATA_DIR=/path/to/test_file/

#remove cached_file from test set, create save directory if it doesn't exist
rm ${DATA_DIR}/cached_test*
mkdir -p ${SAVE_DIR}

# run the run_ner.py script form BioBERT pytorch repo: https://github.com/dmis-lab/biobert-pytorch
# an updated run_ner.py script is provided with this script. However, it is relevant only for training.
# the following tokenizer argument can be added to the prediction script, if user wants to predict with a specific tokenizer
#--tokenizer_name /path/to/tokenizer/folder/ 

python /path/to/ner/folder/run_ner.py \
    --data_dir ${DATA_DIR}/ \
    --labels ${DATA_DIR}/labels.txt \
    --model_name_or_path /path/to/model/folder/ \
    --output_dir ${SAVE_DIR}\
    --max_seq_length ${MAX_LENGTH} \
    --seed ${SEED} \
    --do_predict \
    --overwrite_output_dir
