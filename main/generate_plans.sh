base_folder="gpt2_generator"
model_folder="checkpoint-23000"
domain="grippers"

python generate_plans.py \
    --model_type gpt2 \
    --model_name_or_path ../models/"$domain"/"$base_folder"/"$model_folder"\
    --instances data/"$domain"/"$domain"_test.csv \
    --num_trajectories 50 \
    --max_trajectory_length 40 \
    --domain $domain \
    --length 250 \
    --temperature 1.0 \
    --stop_token "END" \
    --repetition_penalty 1.0 \
    --p 0.99 \
    --start_idx 150 \
    --end_idx 200
