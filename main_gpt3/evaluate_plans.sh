action_model="gpt2_action_applicability"
action_model_ckpt="checkpoint-10000"
domain="grippers"

python evaluate_plans.py \
    --domain $domain \
    --action_model ../models/"$domain"/"$action_model"/"$action_model_ckpt" \
    --plans_file ../results/0.csv \
    --num_trajectories_to_consider 50 \
    --batch_size 20
