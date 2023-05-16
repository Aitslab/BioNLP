# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

SAVE_DIR=../../checkpoints/DC-HoC-BioGPT
mkdir -p ${SAVE_DIR}

fairseq-train \
    ../../data/HoC/ansis-bin --save-dir ${SAVE_DIR} \
    --user-dir ../../src \
    --finetune-from-model ../../checkpoints/Pre-trained-BioGPT/checkpoint.pt \
    --task language_modeling_prompt \
    --arch transformer_lm_prompt_biogpt \
    --share-decoder-input-output-embed --decoder-learned-pos \
    --optimizer adam --adam-betas '(0.9, 0.98)' \
    --weight-decay 0.01 --clip-norm 0.0 \
    --lr 1e-5 --lr-scheduler inverse_sqrt --warmup-updates 1000 --warmup-init-lr 1e-07 \
    --tokens-per-sample 1024 --max-source-positions 900 --max-target-positions 1024 \
    --max-tokens 1024 --update-freq 32 \
    --skip-invalid-size-inputs-valid-test \
    --max-update 20000 --save-interval-updates 1000 --no-epoch-checkpoints \
    --learned-prompt 1