#!/usr/bin/env bash

#SBATCH --gpus 1
#SBATCH -t 00:30:00

# Show GPU Info
nvidia-smi

# Load Anaconda
ml Anaconda/2021.05-nsc1
conda activate biogpt

# Script path
python covid_19_example.py > covid_19_example_OUT.txt