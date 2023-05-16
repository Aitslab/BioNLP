#!/usr/bin/env bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# Modified by Jacob Krucinski on 2023-04-24
# 
# NOTE: Run this script in the examples/RE-BC5CDR
# 
# Usage instructions:
# ./infer_free_form.sh {INPUT_FILE} {OUTPUT_FILE}

#SBATCH --gpus 1 -t 0:30:00

# Set up path variables
MODEL_DIR=../../checkpoints/RE-BC5CDR-BioGPT-v2
MODEL=checkpoint_best.pt
DATA_DIR=${PWD}/../../data/BC5CDR/relis-bin
BASE_DATA_DIR=${DATA_DIR%/*}
BIN_DATA_DIR=${DATA_DIR##*/}
DATA_PREFIX=${BIN_DATA_DIR%-*}
RAW_DATA_DIR=${BASE_DATA_DIR}/raw

INPUT_FILE=$1
OUTPUT_FILE=$2
OUTPUT_FILE_NAME=$(basename ${OUTPUT_FILE} .txt)
TEMP_DIR=../../interactive/temp
ENTITY_FILE=${RAW_DATA_DIR}/train.entities.json
PMID_FILE=${RAW_DATA_DIR}/${DATA_PREFIX}_train.pmid

# Export paths to libraries too
export FASTBPE=../../fastBPE/fastBPE
export MOSES=../../mosesdecoder

# Show GPU Info
# nvidia-smi

# Load Anaconda
ml Anaconda/2021.05-nsc1
conda activate /proj/berzelius-2021-21/users/jacob/conda_envs/biogpt

echo $OUTPUT_FILE_NAME

# Pre-process the free-form input
echo "*** PRE-PROCESSING  ***"
# Clear temp directory
if [ -d "${TEMP_DIR}" ]; then
    rm ${TEMP_DIR}/*
fi
# Tokenization - clean up file naming later
echo "*** TOKENIZATION ***"
echo $INPUT_FILE
echo $OUTPUT_FILE
perl ${MOSES}/scripts/tokenizer/tokenizer.perl -l en -a -threads 8 < ${INPUT_FILE} > ${TEMP_DIR}/${OUTPUT_FILE_NAME}.tok.x
# BPE
echo "*** FAST BPE ***"
${FASTBPE}/fast applybpe ${TEMP_DIR}/${OUTPUT_FILE_NAME}.tok.bpe.x  ${TEMP_DIR}/${OUTPUT_FILE_NAME}.tok.x ${RAW_DATA_DIR}/bpecodes
# Binarize
echo "*** BINARIZE ***"
fairseq-preprocess \
    -s x --workers 8 \
    --only-source \
    --validpref ${TEMP_DIR}/${OUTPUT_FILE_NAME}.tok.bpe \
    --destdir ${TEMP_DIR} \
    --srcdict ${RAW_DATA_DIR}/dict.txt

# inference
echo "*** INFERENCE ***"
echo ${TEMP_DIR}/${OUTPUT_FILE_NAME}.txt
echo "Begin inferencing ${INPUT_FILE} using ${MODEL_DIR}/${MODEL}"
python ../../inference.py --data_dir=${DATA_DIR} --model_dir=${MODEL_DIR} --model_file=${MODEL} --src_file=${INPUT_FILE} --output_file=${TEMP_DIR}/${OUTPUT_FILE_NAME}.txt

# debpe
echo "*** DEBPE ***"
sed -i "s/@@ //g" ${TEMP_DIR}/${OUTPUT_FILE_NAME}.txt

# detok
echo "*** DETOKENIZATION ***"
perl ${MOSES}/scripts/tokenizer/detokenizer.perl -l en -a < ${TEMP_DIR}/${OUTPUT_FILE_NAME}.txt > ${TEMP_DIR}/${OUTPUT_FILE_NAME}.detok

# postprocess
echo "*** POST PROCESS ***"
python postprocess.py ${TEMP_DIR}/${OUTPUT_FILE_NAME}.detok ${ENTITY_FILE} ${PMID_FILE}

# Rename output file and move from temp to output dir
mv ${TEMP_DIR}/${OUTPUT_FILE_NAME}.detok.extracted.PubTator ${OUTPUT_FILE}
# #mv ${TEMP_DIR}/${OUTPUT_FILE_NAME}.detok.extracted.PubTator $(dirname ${OUTPUT_FILE})
