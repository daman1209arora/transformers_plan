import pandas as pd

df = pd.read_csv('data/blocksworld-4ops/blocksworld-4ops_train.csv')
df = df.sample(n=7)
for x in df['transitions']:
    print(x)
