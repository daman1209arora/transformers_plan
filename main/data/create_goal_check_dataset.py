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

    gold_plan_file = f'{domain}/{domain}_train.csv'    

    output_train_file = f'{domain}/{domain}_goal_check_train.csv'
    output_val_file = f'{domain}/{domain}_goal_check_val.csv'
    df_gold = pd.read_csv(gold_plan_file)
    
    all_states = []
    for gold in tqdm(df_gold['transitions']):
        all_states.append(gold.split("NEXT STATE:")[1].split("GOAL")[0].strip())
               
    X, y = [], []
    for i, gold in enumerate(tqdm(df_gold['transitions'])):
        goal = gold.split("GOAL:")[1].split("STATE:")[0].strip()
        state = gold.split("STATE:")[1].split("ACTION:")[0].strip()
        action = gold.split("ACTION:")[1].split("NEXT STATE:")[0].strip()
        next_state = gold.split("NEXT STATE:")[1].split("GOAL")[0].strip()
        success = "GOAL REACHED" in gold 
        if success:
            part = random.random()
            if part < 0.25:
                X.append(f"GOAL:\n{goal}\n\nNEXT STATE:\n{next_state}\nGOAL REACHED")
                y.append(1)
            elif part < 0.5:
                X.append(f"GOAL:\n{goal}\n\nNEXT STATE:\n{random.choice(all_states)}\nGOAL REACHED")
                y.append(0)
            elif part < 0.75:
                X.append(f"GOAL:\n{goal}\n\nNEXT STATE:\n{random.choice(all_states)}\nGOAL NOT REACHED")
                y.append(1)
            else:
                X.append(f"GOAL:\n{goal}\n\nNEXT STATE:\n{next_state}\nGOAL NOT REACHED")
                y.append(0)
    def give(i):
        print(X[i], y[i], sep='\n---\n')
    breakpoint()
    total_df = pd.DataFrame({'transition': X, 'label': y})

    train_df = total_df.sample(frac=0.95)
    val_df = total_df.drop(train_df.index)

    train_df.to_csv(output_train_file, index=False)
    val_df.to_csv(output_val_file, index=False)


if __name__ == '__main__':
    main()
