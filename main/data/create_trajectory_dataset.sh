#/bin/bash

# python create_trajectory_dataset.py --domain blocksworld-4ops --num_instances 10000 --trajectory_length 20 --mode train
python create_trajectory_dataset.py --domain blocksworld-4ops --num_instances 1000 --trajectory_length 20 --mode val
