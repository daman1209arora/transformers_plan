#/bin/bash
domain="grippers"
python create_test_instances.py --domain $domain --num_instances 200 --trajectory_length 30 --mode test
