#!/usr/bin/env python
# coding=utf-8
# Copyright 2018 Google AI, Google Brain and Carnegie Mellon University Authors and the HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Conditional text generation with the auto-regressive models of the library (GPT/GPT-2/CTRL/Transformer-XL/XLNet)
"""

import openai
from tqdm import tqdm
import argparse
import logging

import numpy as np
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=str)
    parser.add_argument("--generator", type=str)
    parser.add_argument("--verifier", type=str)
    parser.add_argument("--instances", type=str, default="")
    parser.add_argument("--num_trajectories", type=int, default=10)
    parser.add_argument("--max_trajectory_length", type=int, default=40)
    parser.add_argument("--start_idx", type=int)
    parser.add_argument("--end_idx", type=int)
    parser.add_argument("--length", type=int, default=20)
    parser.add_argument("--stop_token", type=str, default=None, help="Token at which text generation is stopped")

    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="temperature of 1.0 has no effect, lower tend toward greedy sampling",
    )
    parser.add_argument(
        "--repetition_penalty", type=float, default=1.0, help="primarily useful for CTRL model; in that case, use 1.2"
    )
    parser.add_argument("--k", type=int, default=0)
    parser.add_argument("--p", type=float, default=0.9)

    args = parser.parse_args()
    instances = pd.read_csv(args.instances)
    if args.verifier is None:
        out_file = f'results/{args.domain}/{args.generator}_generator.csv'
    else:
        out_file = f'results/{args.domain}/{args.generator}_generator_{args.verifier}_verifier.csv'
    # plans = {'instances': [], 'trajectories': [], 'attempt': [], 'status': []}
    for i in range(args.start_idx, args.end_idx):
        
        if os.path.exists(out_file):
            existing_plans = pd.read_csv(out_file)
            # breakpoint()
            if i in np.array(existing_plans['instances']):
                print(f"Instance {i} already exists")
            # if os.path.exists(f'results/{args.domain}/{i}.csv'):
                continue
        print(f"Trying instance {i}")
        instance = instances['instances'][i]
        plan_found = False
        for j in range(args.num_trajectories):
            candidate = [instance]
            goal_attained = False
            for k in tqdm(range(args.max_trajectory_length), desc='transition'):
                prev_state = candidate[-1]
                
                goal = prev_state.split("GOAL:\n")[1].split("\n\nSTATE:")[0].strip()
                if len(candidate) == 1:
                    state = prev_state.split("STATE:\n")[1].strip()
                else:
                    try:
                        state = prev_state.split("NEXT STATE:\n")[1].split("\nEND")[0]
                    except: 
                        # breakpoint()
                        break
                prompt = f"GOAL:\n{goal}\n\nSTATE:\n{state}\n\nACTION:"
                # prompts.append(prompt_text)
                response = openai.Completion.create(
                    model=args.generator,
                    prompt=prompt,
                    max_tokens=150,
                    temperature=1,
                    stop="END"
                )
                transition = prompt + response['choices'][0]['text']
                candidate.append(transition)
                try:
                    if goal_reached(transition):
                        print("Goal reached")
                        goal_attained = True
                        break
                except:
                    break
            
            if goal_attained:
                if args.verifier is None:
                    print("Checking plan validity")
                    status = is_valid(candidate, i, args.domain)
                    print(f"Instance {i}: Status {status}")
                    plan_found = True        
                    break
                else:
                    print("Verifying plan...")
                    verifier_rejection = False
                    for transition in candidate[1:]:
                        state = transition.split("STATE:")[1].split("ACTION")[0].strip()
                        action = transition.split("ACTION:")[1].split("NEXT")[0].strip()
                        verifier_prompt = f"STATE:\n{state}\n\nACTION:\n{action}\n\nEND"
                        verifier_response = openai.Completion.create(
                            model=args.verifier,
                            prompt=verifier_prompt,
                            max_tokens=1,
                            temperature=0
                        )
                        if verifier_response['choices'][0]['text'].strip() != 'yes':
                            print(verifier_prompt)
                            print(f"This transition was rejected by the verifier saying {verifier_response['choices'][0]['text'].strip()}")
                            verifier_rejection = True
                            # breakpoint()
                            break
                    if verifier_rejection:
                        print("Plan rejected by verifier. Finding a new one...")
                    else:
                        print("Plan accepted by verifier!")
                        print("Checking plan validity...")
                        status = is_valid(candidate, i, args.domain)
                        print(f"Instance {i}: Status {status}")
                        plan_found = True        
                        break
            else:
                print("Goal not reached")
        
        plans = {'instances': [], 'trajectories': [], 'attempt': [], 'status': []}
        plans['instances'].append(i)
        if plan_found:
            plans['trajectories'].append(candidate)
            plans['attempt'].append(j+1)
            plans['status'].append(status)
        else:
            plans['trajectories'].append([])
            plans['attempt'].append(-1)
            plans['status'].append(("False", "no plan found"))
        
        if os.path.exists(out_file):
            existing_plans = pd.read_csv(out_file)
            existing_plans = pd.concat([existing_plans, pd.DataFrame(plans)])
            existing_plans = existing_plans.sort_values(by=['instances'])
        else:
            existing_plans = plans    
        pd.DataFrame(existing_plans).to_csv(out_file, index=False)

        

if __name__ == "__main__":
    main()
