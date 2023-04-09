import pandas as pd
import pdb
from tqdm import tqdm
import random
import argparse

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', type=str)
    args = parser.parse_args()
    domain = args.domain

    gold_plan_file = f'{domain}_train.csv'    

    output_train_file = f'{domain}_verifier_train.csv'
    output_val_file = f'{domain}_verifier_val.csv'
    df_gold = pd.read_csv(gold_plan_file)
    '''
    Negative samples can be:
    1. Wrong action, correct state: Choose any action randomly randomly.
    2. Correct action, wrong state: Remove some atoms, sample some other state.
    3. Wrong action, wrong state: Do both.
    '''
    
    all_actions = []
    for gold in tqdm(df_gold['transitions']):
        choose_next = False
        for line in gold.split("\n"):
            if choose_next:
               all_actions.append(line.strip())
               break
            if "ACTION:" in line:
               choose_next = True
    all_states = []
    for gold in tqdm(df_gold['transitions']):
        all_states.append(gold.split("NEXT STATE:\n")[1].split("GOAL")[0].strip())
    
    X, y, cause = [], [], []
    for i, gold in enumerate(tqdm(df_gold['transitions'])):
        
        cause.append("")
        if "GOAL NOT REACHED" in gold:
            if random.random() < 0.5:
                X.append(gold)
                y.append("1")
                cause[i] += "[correct_no_goal]"
            else:
                goal = gold.split("GOAL:\n")[1].split("\n\nSTATE:")[0]
                state = gold.split("STATE:\n")[1].split("\n\nACTION:")[0]
                action = gold.split("ACTION:\n")[1].split("\n\nNEXT STATE:")[0]
                next_state = gold.split("NEXT STATE:\n")[1].split("\nGOAL")[0]
                
                if random.random() < 0.5:
                    action = random.choice(all_actions)
                    cause[i] += "[wrong_action]"
                if random.random() < 0.5:
                    if random.random() < 0.5:
                        next_state = next_state.split('\n')
                        while True:
                            next_state_dummy = []
                            for atom in next_state:
                                if random.random() > 0.2:
                                    next_state_dummy.append(atom)
                            if len(next_state) != len(next_state_dummy):
                                next_state = "\n".join(next_state_dummy)    
                                cause[i] += "[missing_atoms]"
                                break
                    if random.random() < 0.5:
                        next_state = random.choice(all_states)
                        cause[i] += "[wrong_next_state]"
                
                transition = f'GOAL:\n{goal}\n\nSTATE:\n{state}\n\nACTION:\n{action}\n\nNEXT STATE:\n{next_state}\nGOAL NOT REACHED'
                X.append(transition)
                if cause[i] == "":
                    y.append("1")
                    cause[i] = "[correct_no_goal]"
                else:
                    y.append("0")
        else:
            if random.random() < 0.5:
                X.append(gold)
                y.append("1")
                cause[i] += "[correct_goal]"
            else:
                gold.replace("GOAL REACHED", "GOAL NOT REACHED")
                X.append(gold)
                y.append("0")
                cause[i] += "[wrong_goal]"
                        
    # def give(i):
    #     print(X[i], y[i], cause[i], sep='\n---\n')
    # pdb.set_trace()
    total_df = pd.DataFrame({'transition': X, 'label': y, 'cause': cause})

    train_df = total_df.sample(frac=0.95)
    val_df = total_df.drop(train_df.index)

    train_df.to_csv(output_train_file, index=False)
    val_df.to_csv(output_val_file, index=False)


if __name__ == '__main__':
    main()
