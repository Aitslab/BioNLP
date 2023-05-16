#!/usr/bin/env bash

#SBATCH --gpus 1
#SBATCH -t 00:30:00

# Status check
pwd
nvidia-smi

# Load Anaconda
ml Anaconda/2021.05-nsc1
conda activate biogpt

# For debugging
export CUDA_LAUNCH_BLOCKING=1

# Script path
python interactive.py --model_dir=../../checkpoints/Pre-trained-BioGPT --data_dir=../../data > jacob_test.txt
