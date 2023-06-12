import pandas as pd
import json
import random

df = pd.read_csv('finetune_data/finetune_data.csv')
frac = 0.25
original_len = 2000
data = []
all_actions = []
for elem in df['transitions'][:int(original_len*frac)]:
    all_actions.append(elem.split("ACTION:")[1].split("NEXT")[0].strip())
    
for elem in df['transitions'][:int(original_len*frac)]:
    state = elem.split("STATE:")[1].split("ACTION")[0].strip()
    action = elem.split("ACTION:")[1].split("NEXT")[0].strip()
    if random.random() < 0.5:
        prompt = f"STATE:\n{state}\n\nACTION:\n{action}\n\nEND"
        data.append({'prompt': prompt, 'completion': 'yes'})
    else:
        action = random.sample(all_actions, k=1)[0]
        prompt = f"STATE:\n{state}\n\nACTION:\n{action}\n\nEND"
        data.append({'prompt': prompt, 'completion': 'no'})

json.dump(data, open(f'finetune_data/verifier_data_{frac}.json', 'w'), indent=4)