base_folder="gpt2_verifier"
model_folder="checkpoint-3500"
domain="blocksworld-4ops"

python evaluate_plans.py \
    --pretrained_model_path ../models/"$base_folder"/"$model_folder"\
    --plans_file ../results/0.csv \
    --num_trajectories_to_consider 50 \
    --batch_size 20