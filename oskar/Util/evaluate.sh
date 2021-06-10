#!/bin/bash
#SBATCH -A SNIC2021-7-54 -p alvis #add your AI/ML project
#SBATCH -n 4
#SBATCH -J Model15_effnet
#SBATCH --gpus-per-node=V100:2 #You can specify V100:2 if your job isn't as computationally expensive.
#SBATCH --time=04:00:00
#SBATCH --mail-user=os2847jo-s@student.lu.se
#SBATCH --mail-type=END
#SBATCH -o job.out
#SBATCH -e job.errs
python evaluate.py train_spanbert_base
