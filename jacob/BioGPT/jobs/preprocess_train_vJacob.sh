#!/usr/bin/env bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# Modified by Jacob Krucinski on 2023-04-21
# ** This script also calls the pre-process script

#SBATCH --gpus 1
#SBATCH -t 8:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ja6750kr-s@student.lu.se

# Show GPU Info
nvidia-smi

# Load Anaconda
ml Anaconda/2021.05-nsc1
conda activate biogpt

# Call pre-process script
export FASTBPE=../../fastBPE/fastBPE
export MOSES=../../mosesdecoder
echo $MOSES
./preprocess.sh

SAVE_DIR=../../checkpoints/RE-BC5CDR-BioGPT
mkdir -p ${SAVE_DIR}

echo START TRAINING...
fairseq-train \
    ../../data/BC5CDR/relis-bin --save-dir ${SAVE_DIR} \
    --user-dir ../../src \
    --finetune-from-model ../../checkpoints/Pre-trained-BioGPT/checkpoint.pt \
    --task language_modeling_prompt \
    --arch transformer_lm_prompt_biogpt \
    --share-decoder-input-output-embed --decoder-learned-pos \
    --optimizer adam --adam-betas '(0.9, 0.98)' \
    --weight-decay 0.01 --clip-norm 0.0 \
    --lr 1e-5 --lr-scheduler inverse_sqrt --warmup-updates 100 --warmup-init-lr 1e-07 \
    --tokens-per-sample 1024 --max-source-positions 640 --max-target-positions 1024 \
    --max-tokens 1024 --update-freq 32 \
    --skip-invalid-size-inputs-valid-test \
    --max-epoch 100 --keep-last-epochs 5 \
    --learned-prompt 9