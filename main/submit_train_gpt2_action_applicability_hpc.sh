#!/bin/sh

#PBS -P darpa.ml.cse
#PBS -q high
#PBS -lselect=1:ncpus=1:ngpus=1:centos=skylake
#PBS -lwalltime=04:30:00

echo "==============================="
echo $PBS_JOBID
cat $PBS_NODEFILE
echo $PBS_JOBNAME
echo "==============================="

source /home/apps/anaconda3_2018/4.6.9/etc/profile.d/conda.sh
module load apps/anaconda/3
conda activate ~/plan
module unload apps/anaconda/3
cd /home/cse/dual/cs5180404/scratch/transformers_plan/main

./train_gpt2_action_applicability.sh
