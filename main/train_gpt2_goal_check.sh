base_folder="gpt2_goal_check"
domain="grippers"

python train_gpt2_goal_check.py \
    --pretrained_model_path ../models/$domain/gpt2_generator/checkpoint-23500 \
    --output_dir ../models/$domain/"$base_folder" \
    --train_file data/$domain/$domain"_goal_check_train.csv" \
    --val_file data/$domain/$domain"_goal_check_val.csv" \
    --per_device_train_batch_size 32 \
    --learning_rate 5e-6 \
    --num_train_epochs 5
