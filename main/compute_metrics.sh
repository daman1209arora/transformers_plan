domain="grippers"
max_trajectories=25
echo "-------------------first_traj------------------"
python compute_metrics.py --domain $domain --planner "first_traj"
# echo "-------------------random_with_restart------------------"
# python compute_metrics.py --domain $domain --planner "random_with_restart" --max_trajectories $max_trajectories
echo "-------------------multiple_traj_with_verifier------------------"
python compute_metrics.py --domain $domain --planner "multiple_traj_with_verifier" --max_trajectories $max_trajectories