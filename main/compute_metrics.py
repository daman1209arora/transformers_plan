import pandas as pd
from lifted_pddl import Parser
import os
import argparse
from tqdm import tqdm
import random
import json

GENERATOR_FOLDER = "../generators/"

def goal_reached(transition):
    goal = transition.split("GOAL:")[1].split("STATE")[0].strip()
    state = transition.split("STATE:")[1].split("ACTION:")[0].strip()
    next_state = transition.split("NEXT STATE:")[1].split("END")[0].strip()
    return next_state == goal

def is_valid(plan, instance, domain):
    parser = Parser()
    parser.parse_domain(os.path.join(GENERATOR_FOLDER, f'{domain}/domain.pddl'))
    try:
        parser.parse_problem(f"data/test_instances/{domain}/{instance}.pddl")
    except:
        return False, "error in parsing pddl"
    start_state = parser.encode_atoms_as_pddl(parser.atoms, 'str')
    goal = plan[0].split("GOAL:")[1].split("STATE:")[0].strip()
    for transition in plan[1:]:
        applicable_actions = parser.get_applicable_actions() 
        applicable_actions_list = list(parser.encode_ground_actions_as_pddl(applicable_actions, 'str'))
        
        action = transition.split("ACTION:")[1].split("NEXT STATE")[0].strip()
        # breakpoint()
        if action not in applicable_actions_list:
            return False, "bad action"
        
        # breakpoint()
        action_template = action[1:-1].split(" ")[0]
        action_args = action[1:-1].split(" ")[1:]
        action_args_numeric = [parser.object_names.index(arg) for arg in action_args]
        action_repr = [action_template, action_args_numeric]
        
        next_state = parser.get_next_state(*action_repr)
        next_state_pred = transition.split("NEXT STATE:")[1].split("END")[0].strip()
        next_state_atoms = parser.encode_atoms_as_pddl(next_state, 'str')
        next_state_atoms_str = "\n".join(list(sorted(next_state_atoms)))
        # breakpoint()
    
        if next_state_atoms_str != next_state_pred:
            return False, "bad next state"
        if goal == next_state_pred:
            return True, "success"
        parser.atoms = next_state
    return False, "goal not reached"
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain")
    parser.add_argument("--planner")
    parser.add_argument("--max_trajectories", required=False, type=int)
    args = parser.parse_args()
    planner = args.planner
    domain = args.domain
    
    if planner == "first_traj":
        results = {
            "success": 0,
            "bad action": 0,
            "goal not reached": 0, 
            "bad next state": 0,
            "error in parsing pddl": 0,
            "no_valid_found": 0
        }
        for i in tqdm(range(200)):
            trajs = pd.read_csv(f'../results/{domain}/{i}.csv')['trajectories']
            results[is_valid(eval(trajs[0]), i, domain)[1]] += 1
        with open(f'metrics/{domain}/{planner}.json', 'w') as out_file:
            json.dump(results, out_file, indent=4)
        
    elif planner == "multiple_traj_with_verifier":
        total_metrics = []
        for num_traj_to_consider in tqdm(range(1, args.max_trajectories+1)):
            results = {
                "num_trajectories": num_traj_to_consider,
                "success": 0,
                "bad action": 0,
                "goal not reached": 0, 
                "bad next state": 0,
                "error in parsing pddl": 0,
                "no_valid_found": 0
            }
            for i in tqdm(range(200)):
                trajs = pd.read_csv(f'../results/{domain}/{i}.csv')['trajectories']
                action_preds = pd.read_csv(f'../results/{domain}/{i}_pred.csv')['action_model_preds']
                accepted_traj = None
                for j in range(num_traj_to_consider):
                    action_pred = eval(action_preds[j])
                    traj = eval(trajs[j])
                    bad_step = False
                    for k in range(40):
                        try:
                            if action_pred[k] == 0:
                                bad_step = True
                                break
                            if goal_reached(traj[k+1]):
                                accepted_traj = traj[:k+2]
                                break 
                        except:
                            continue
                    if accepted_traj:
                        break        
                # breakpoint()
                if accepted_traj is not None:
                    results[is_valid(accepted_traj, i, domain)[1]] += 1
                else:
                    results["no_valid_found"] += 1
            total_metrics.append(results)
            
        with open(f'metrics/{domain}/{planner}.json', 'w') as out_file:
            json.dump(total_metrics, out_file, indent=4)
    
        
    elif planner == "random_with_restart":
        total_metrics = []
        for num_traj_to_consider in tqdm(range(1, args.max_trajectories+1)):
            
            results = {
                "num_trajectories": num_traj_to_consider,
                "success": 0,
                "goal not reached": 0,
                "error in parsing pddl": 0
            }
            
            for i in tqdm(range(200)):
                trajs = pd.read_csv(f'../results/{domain}/{i}.csv')['trajectories']
                goal = eval(trajs[0])[0].split("GOAL:")[1].split("STATE")[0].strip()
                pddl_parser = Parser()
                pddl_parser.parse_domain(os.path.join(GENERATOR_FOLDER, f'{domain}/domain.pddl'))
                try:
                    pddl_parser.parse_problem(f"data/test_instances/{domain}/{i}.pddl")
                except:
                    results["error in parsing pddl"] += 1
                    continue
                for j in range(num_traj_to_consider):
                    goal_found = False
                    pddl_parser = Parser()
                    pddl_parser.parse_domain(os.path.join(GENERATOR_FOLDER, f'{domain}/domain.pddl'))
                    pddl_parser.parse_problem(f"data/test_instances/{domain}/{i}.pddl")
                    
                    for k in range(40):
                        
                        applicable_actions = pddl_parser.get_applicable_actions() 
                        applicable_actions_list = list(pddl_parser.encode_ground_actions_as_pddl(applicable_actions, 'str'))
                        random_action = random.choice(applicable_actions_list)
                        action_template = random_action[1:-1].split(" ")[0]
                        action_args = random_action[1:-1].split(" ")[1:]
                        action_args_numeric = [pddl_parser.object_names.index(arg) for arg in action_args]
                        action_repr = [action_template, action_args_numeric]
                        
                        next_state = pddl_parser.get_next_state(*action_repr)
                        next_state_atoms = pddl_parser.encode_atoms_as_pddl(next_state, 'str')
                        next_state_atoms_str = "\n".join(list(sorted(next_state_atoms)))
                        if next_state_atoms_str == goal:
                            goal_found = True
                            break
                        pddl_parser.atoms = next_state
                    if goal_found:
                        results["success"] += 1
                        break
                    
                if not goal_found:
                    results["goal not reached"] += 1
            total_metrics.append(results)
        
        with open(f'metrics/{domain}/{planner}.json', 'w') as out_file:
            json.dump(total_metrics, out_file, indent=4)
        
    # else:
    #     first_traj_correct = 0
    #     num_total_traj = 0
    #     num_accepted_traj = 0
    #     num_accepted_and_valid_traj = 0
        
    #     for i in range(200):
    #         trajs = pd.read_csv(f'../results/{domain}/{i}.csv')['trajectories']
    #         action_preds = pd.read_csv(f'../results/{domain}/{i}_pred.csv')['action_model_preds']
    #         # goal_preds = pd.read_csv(f'../results/{i}_pred.csv')['goal_model_preds']
            
    #         accepted_traj = None
    #         for j in range(min(len(trajs), len(action_preds))):
    #             action_pred = eval(action_preds[j])
    #             # goal_pred = eval(goal_preds[j])
    #             traj = eval(trajs[j])
    #             breakpoint()
    #             bad_step = False
    #             for k in range(40):
    #                 try:
    #                     if action_pred[k] == 0:
    #                         bad_step = True
    #                         break
    #                     # if goal_pred[k] == 0:
    #                     #     bad_step = True
    #                     #     break
    #                     if goal_reached(traj[k+1]):
    #                         accepted_traj = traj[:k+2]
    #                         break 
    #                 except:
    #                     continue
    #             if accepted_traj:
    #                 break        
    #         # breakpoint()
    #         if accepted_traj is not None:
    #             result = is_valid(accepted_traj, i)
    #             if result[0]:
    #                 num_accepted_and_valid_traj += 1
    #             else:
    #                 actions = []
    #                 start_state = accepted_traj[0].split("STATE:")[1].strip()
    #                 goal = accepted_traj[0].split("GOAL:")[1].split("STATE:")[0].strip()
    #                 for tr in accepted_traj[1:]:
    #                     actions.append(tr.split("ACTION:")[1].split("NEXT STATE")[0].strip())
    #                 # print(start_state)
    #                 # print(actions)
    #                 # print(goal)
    #                 print(result[1])
    #                 # breakpoint()
    #             num_accepted_traj += 1
                
    #         num_total_traj += 1
    #         first_traj_correct += is_valid(eval(trajs[0]), i)[0]
    #         print(num_total_traj, num_accepted_traj, num_accepted_and_valid_traj, j, first_traj_correct)
    
if __name__ == '__main__':
    main()
