#!/usr/bin/env bash

# Written by Jacob Krucinski on 2023-05-10
# This 

#SBATCH -A SNIC2022-22-707
#SBATCH --gpus-per-node 1
#SBATCH -t 3:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ja6750kr-s@student.lu.se

# Show GPU Info
nvidia-smi

# Load Anaconda
ml Anaconda3
conda init bash
#./$(basename $0) && exit      # Restart bash
conda activate /mimer/NOBACKUP/groups/snic2022-22-707/jacob/conda_envs/roberta

# Call pipeline script
python main.py > jacob_edits/2023_05_10_roberta_finetune_merged.txt