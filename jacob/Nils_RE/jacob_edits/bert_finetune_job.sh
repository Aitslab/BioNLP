#!/usr/bin/env bash

# Written by Jacob Krucinski on 2023-05-04
# This 

#SBATCH --gpus 1
#SBATCH -t 16:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ja6750kr-s@student.lu.se

# Show GPU Info
nvidia-smi

# Load Anaconda
ml Anaconda/2021.05-nsc1
conda activate /proj/berzelius-2021-21/users/jacob/conda_envs/nilsre

# Call pipeline script
python main.py > jacob_edits/2023_05_05_bert_finetune_merged.txt
