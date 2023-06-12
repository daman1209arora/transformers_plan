domain="blocksworld-4ops"

python generate_plans_gpt3.py \
    --instances data/"$domain"/"$domain"_test.csv \
    --generator "ada:ft-academics-arizona:gen-0-25-2023-05-30-19-14-19" \
    --verifier "ada:ft-academics-arizona:ver-0-25-2023-06-04-11-10-16" \
    --num_trajectories 25 \
    --max_trajectory_length 40 \
    --domain $domain \
    --length 250 \
    --temperature 1.0 \
    --stop_token "END" \
    --repetition_penalty 1.0 \
    --p 0.99 \
    --start_idx $1 \
    --end_idx $2


# --verifier "ada:ft-academics-arizona:ver-2-0-2023-06-04-04-26-15" \
# --generator "ada:ft-academics-arizona:gen-2-0-2023-06-03-20-51-25" \
# --verifier "ada:ft-academics-arizona:ver-2-0-2023-06-04-04-26-15" \
# --verifier "ada:ft-academics-arizona:ver-0-25-2023-06-04-11-10-1" \
# --verifier "ada:ft-academics-arizona:ver-1-0-2023-06-03-09-16-45" \
# --verifier "ada:ft-academics-arizona:ver-0-5-2023-06-03-10-00-12" \
# --model "ada:ft-academics-arizona:gen-1-0-2023-05-30-19-27-28" \
# --model "ada:ft-academics-arizona:gen-0-25-2023-05-30-19-14-19" \

# Experiment plan
# 25% - v, v+g
# 50% - v, v+g
# 75% - v, v+g
# 100% - v, v+g
# Two modes: 
# Restart, resample action