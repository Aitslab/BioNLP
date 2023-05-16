#!/usr/bin/env bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# Modified by Jacob Krucinski on 2023-04-24

#SBATCH interactive --gpus 1 -t 0:30:00

# Set up path variables
MODEL_DIR=../../checkpoints/RE-BC5CDR-BioGPT/paper_model
MODEL=checkpoint_avg.pt
DATA_DIR=${PWD}/../../data/BC5CDR/relis-bin
BASE_DATA_DIR=${DATA_DIR%/*}
BIN_DATA_DIR=${DATA_DIR##*/}
DATA_PREFIX=${BIN_DATA_DIR%-*}
RAW_DATA_DIR=${BASE_DATA_DIR}/raw
OUTPUT_FILE=infer_${MODEL}

INPUT_FILE=${RAW_DATA_DIR}/${DATA_PREFIX}_test.tok.bpe.x
OUTPUT_FILE=${MODEL_DIR}/${OUTPUT_FILE}
GOLD_FILE=${RAW_DATA_DIR}/CDR_Data/CDR.Corpus.v010516/CDR_TestSet.PubTator.txt
ENTITY_FILE=${RAW_DATA_DIR}/test.entities.json
PMID_FILE=${RAW_DATA_DIR}/${DATA_PREFIX}_test.pmid

# Export paths to libraries too
export FASTBPE=../../fastBPE/fastBPE
export MOSES=../../mosesdecoder

# Show GPU Info
nvidia-smi

# Load Anaconda
ml Anaconda/2021.05-nsc1
conda activate biogpt

# average checkpoints
echo "*** AVERAGE CHECKPOINTS ***"
if [ ! -f "${MODEL_DIR}/${MODEL}" ]; then
    python ../../scripts/average_checkpoints.py --inputs=${MODEL_DIR} --output=${MODEL_DIR}/${MODEL} --num-epoch-checkpoints=5
fi


# inference
echo "*** INFERENCE ***"
echo $OUTPUT_FILE
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Begin inferencing ${INPUT_FILE} using ${MODEL_DIR}/${MODEL}"
    python ../../inference.py --data_dir=${DATA_DIR} --model_dir=${MODEL_DIR} --model_file=${MODEL} --src_file=${INPUT_FILE} --output_file=${OUTPUT_FILE}
fi

# debpe
echo "*** DEBPE ***"
sed -i "s/@@ //g" ${OUTPUT_FILE}
# detok
echo "*** DETOKENIZATION ***"
perl ${MOSES}/scripts/tokenizer/detokenizer.perl -l en -a < ${OUTPUT_FILE} > ${OUTPUT_FILE}.detok
# postprocess
echo "*** POST PROCESS ***"
python postprocess.py ${OUTPUT_FILE}.detok ${ENTITY_FILE} ${PMID_FILE}
# eval
echo "*** EVALUATION ***"
echo $OUTPUT_FILE
cd ${RAW_DATA_DIR}/BC5CDR_Evaluation-0.0.3
bash eval_relation.sh PubTator ${GOLD_FILE} ${OUTPUT_FILE}.detok.extracted.PubTator
cd ${OLDPWD}