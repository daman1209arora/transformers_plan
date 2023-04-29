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

    output_train_file = f'{domain}/{domain}_action_applicability_train.csv'
    output_val_file = f'{domain}/{domain}_action_applicability_val.csv'
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
               
    X, y = [], []
    for i, gold in enumerate(tqdm(df_gold['transitions'])):
        state = gold.split("STATE:")[1].split("ACTION:")[0].strip()
        action = gold.split("ACTION:")[1].split("NEXT STATE:")[0].strip()
        if random.random() < 0.5:
            y.append("1")
        else:
            action = random.choice(all_actions)
            y.append("0")
        X.append(f"STATE:\n{state}\n\nACTION:\n{action}")
            
                    
    # def give(i):
    #     print(X[i], y[i], sep='\n---\n')
    # breakpoint()
    total_df = pd.DataFrame({'transition': X, 'label': y})

    train_df = total_df.sample(frac=0.95)
    val_df = total_df.drop(train_df.index)

    train_df.to_csv(output_train_file, index=False)
    val_df.to_csv(output_val_file, index=False)


if __name__ == '__main__':
    main()
