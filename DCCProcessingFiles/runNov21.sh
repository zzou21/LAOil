#!/bin/bash
#SBATCH --output=outputNov21.out
#SBATCH --error=errorNov21.err
#SBATCH --mem=7G
#SBATCH --partition=common

srun --cpu-bind=none python /hpc/home/zz341/test4/testLOCExtract.py