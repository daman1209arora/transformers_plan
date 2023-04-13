base_folder="gpt2_generator"
model_folder="checkpoint-17500"
domain="blocksworld-4ops"

python generate_plans.py \
    --model_type gpt2 \
    --model_name_or_path ../models/"$base_folder"/"$model_folder"\
    --instances data/"$domain"_test.csv \
    --num_trajectories 100 \
    --max_trajectory_length 40 \
    --output_file responses_"$domain"_test.csv \
    --length 150 \
    --temperature 1.0 \
    --stop_token "REACHED" \
    --repetition_penalty 1.0 \
    --p 0.99 \
    --start_idx 175 \
    --end_idx 250
