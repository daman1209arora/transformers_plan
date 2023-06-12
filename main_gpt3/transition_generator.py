import random
import openai
import pandas as pd
from lifted_pddl import Parser
import os

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
    
def is_valid_transition(transition, instance, domain):
    parser = Parser()
    parser.parse_domain(os.path.join(GENERATOR_FOLDER, f'{domain}/domain.pddl'))
    try:
        parser.parse_problem(f"data/val_instances/{domain}/{instance}.pddl")
    except:
        return False, "error in parsing pddl"
    # breakpoint()
    state = transition.split("STATE:")[1].split("ACTION:")[0].strip().split("\n")
    state = [x.strip("()") for x in state]
    state_atoms = set([(x.split(" ")[0], tuple([parser.object_names.index(y) for y in x.split(" ")[1:]])) for x in state])
    
    parser.atoms = state_atoms
    goal = transition.split("GOAL:")[1].split("STATE:")[0].strip()
    applicable_actions = parser.get_applicable_actions() 
    applicable_actions_list = list(parser.encode_ground_actions_as_pddl(applicable_actions, 'str'))
    
    action = transition.split("ACTION:")[1].split("NEXT STATE")[0].strip()
    # breakpoint()
    print(action, applicable_actions_list)
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
    return True, "success"
    
    
def main():
    openai.organization = 'org-FmY4LUtUMYuCSZZXmUD5s3wG' # Rao's org asu
    openai.api_key = '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' # rao's key
    
    states = pd.read_csv('data/blocksworld-4ops/blocksworld-4ops_val.csv').sample(n=50)
    for state, instance in zip(states['transitions'], states['instances']):
        prompt = state[:state.index("ACTION:")] + "ACTION:"
        response = openai.Completion.create(
            model='ada:ft-academics-arizona-2023-05-27-19-56-44',
            prompt=prompt,
            max_tokens=150,
            temperature=1,
            stop="END"
        )
        generated_transition = state[:state.index("ACTION:")] + "ACTION:" + response['choices'][0]['text'] + "END"
        print(is_valid_transition(generated_transition, instance, 'blocksworld-4ops'))
        # print(generated_transition)
        # breakpoint()
    
if __name__ == '__main__':
    main()