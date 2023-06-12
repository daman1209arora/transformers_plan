import pandas as pd
import json
import random

df = pd.read_csv('finetune_data/finetune_data.csv')
frac = 0.25
original_len = 2000
data = []
for elem in df['transitions'][:int(original_len*frac)]:
    split = elem.split("ACTION:")
    prompt, completion = split[0], split[1]
    prompt += "ACTION:"
    # breakpoint()
    data.append({'prompt': prompt, 'completion': completion})

json.dump(data, open(f'finetune_data/finetune_data_{frac}.json', 'w'), indent=4)