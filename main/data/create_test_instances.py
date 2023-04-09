import pandas as pd
import argparse
import os, random
from tqdm import tqdm
import numpy as np
import json
import pandas as pd
import subprocess
from lifted_pddl import Parser

CONFIG_FOLDER = "../../configs/generator_config/"
GENERATOR_FOLDER = "../../generators/"

def generate_trajectory(domain, instance):
    
    parser = Parser()
    parser.parse_domain(os.path.join(GENERATOR_FOLDER, f'{domain}/domain.pddl'))
    parser.parse_problem(f"instances/{domain}/{i}.pddl")
    
    states, actions = [], []
    states.append(parser.encode_atoms_as_pddl(parser.atoms, 'str'))
    for j in range(trajectory_length):
        
        applicable_actions = parser.get_applicable_actions()
        applicable_actions_list = []
        for template in applicable_actions.keys():
            for grounding in applicable_actions[template]:
                applicable_actions_list.append((template, grounding))
        
        random.shuffle(applicable_actions_list)
        found_action = False
        for action in applicable_actions_list:
            state = parser.get_next_state(*action)
            all_different = True
            for prev_state in states:
                if parser.encode_atoms_as_pddl(state, 'str') - prev_state == set():
                    all_different = False
                    break
            if all_different:
                found_action = True
                break
        
        if not found_action:
            break
        action_dict = {action[0]: ([action[1]])}
        actions.append(list(parser.encode_ground_actions_as_pddl(action_dict, 'str'))[0])
        parser.atoms = state
        states.append(parser.encode_atoms_as_pddl(parser.atoms, 'str'))
    
    assert len(np.unique(states)) == len(states)
    return states, actions
    
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', type=str)
    parser.add_argument('--num_instances', type=int)
    parser.add_argument('--trajectory_length', type=int)
    parser.add_argument('--mode')
    args = parser.parse_args()
    domain, num_instances, trajectory_length, mode = args.domain, args.num_instances, args.trajectory_length, args.mode
   
    config_file = os.path.join(CONFIG_FOLDER, f'{domain}.config')
    generator = os.path.join(GENERATOR_FOLDER, f'{domain}/{domain}')
    generator_configs = json.load(open(config_file))['arguments']
    
    transitions = []
    i = 0
    while i < num_instances:
        print(i)
        try:
            generator_args = [f"./{generator}"]
            for conf in generator_configs:
                conf_name = list(conf.keys())[0]
                min_value, max_value = conf[conf_name][f'{mode}_min'], conf[conf_name][f'{mode}_max']
                generator_args.append(str(random.randint(min_value, max_value)))
            
            with open(f"instances/{domain}/{i}.pddl", 'w') as outfile:
                subprocess.run(generator_args, stdout=outfile, stderr=None)
                
            states, actions = generate_trajectory(domain, i)
            end = random.randint(len(states)//2, len(states)-1)
            transitions.append((states[0], states[end]))
            i += 1
        except Exception as e:
            print(e)
            pass
    
    inputs = {"instances":[]}
    for t in transitions:
        s = "\n".join(sorted(list(t[0])))
        g = "\n".join(sorted(list(t[1])))
        combined = f"GOAL:\n{g}\n\nSTATE:\n{s}"
        inputs['instances'].append(combined)
    
    breakpoint()
    pd.DataFrame(inputs).to_csv(f'{domain}_{mode}.csv', index=False)
        
        
    
    

