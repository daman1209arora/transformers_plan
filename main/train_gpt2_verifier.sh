base_folder="gpt2_verifier"
domain="blocksworld-4ops"

python train_gpt2_verifier.py \
    --pretrained_model_path ../models/gpt2_generator/checkpoint-17500 \
    --output_dir ../models/"$base_folder" \
    --train_file data/$domain"_verifier_train.csv" \
    --val_file data/$domain"_verifier_val.csv" \
    --per_device_train_batch_size 8 \
    --learning_rate 5e-6 \
    --num_train_epochs 1
