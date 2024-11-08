base_folder="gpt2_generator"
domain="grippers"

python transformers/examples/pytorch/language-modeling/run_clm.py \
    --model_name_or_path gpt2 \
    --overwrite_output_dir \
    --output_dir "../models/"$domain"/"$base_folder \
    --do_train \
    --do_eval \
    --do_predict \
    --evaluation_strategy steps \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 8 \
    --gradient_accumulation_steps 1 \
    --learning_rate 5e-6 \
    --num_train_epochs 20 \
    --warmup_steps 50 \
    --logging_strategy steps \
    --logging_dir "../models/"$domain"/"$base_folder"/tb_logs/" \
    --logging_steps 20 \
    --save_total_limit 2 \
    --eval_steps 250 \
    --metric_for_best_model loss \
    --greater_is_better False \
    --train_file "data/"$domain"/"$domain"_train.csv" \
    --validation_file "data/"$domain"/"$domain"_val.csv"
