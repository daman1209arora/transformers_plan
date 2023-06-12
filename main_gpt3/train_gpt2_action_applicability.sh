base_folder="gpt2_action_applicability"
domain="grippers"

python train_gpt2_action_applicability.py \
    --pretrained_model_path ../models/$domain/gpt2_generator/checkpoint-23000 \
    --output_dir ../models/"$domain"/"$base_folder" \
    --train_file data/$domain/$domain"_action_applicability_train.csv" \
    --val_file data/$domain/$domain"_action_applicability_val.csv" \
    --per_device_train_batch_size 8 \
    --learning_rate 5e-6 \
    --num_train_epochs 1
