import random
import pandas as pd

# df = pd.read_csv('data/blocksworld-4ops/blocksworld-4ops_val.csv')
# gen_prompt = []
# df_gen = df.sample(n=4)
# for x in df_gen['transitions']:
#     prompt = "STATE:\n" + x.split("STATE:")[1].strip().split("NEXT")[0].strip()
#     gen_prompt.append(prompt)

# gen_prompt = "\n---\n".join(gen_prompt)
# with open('generator_few_shot_prompt.txt', 'w') as outfile:
#     outfile.write(gen_prompt)

# ver_prompt = []
# df_ver = df.sample(n=4)
# for x in df_ver['transitions']:
#     if random.random() < 0.5:
#         prompt = "STATE:\n" + x.split("STATE:")[1].strip().split("NEXT")[0].strip() + "\nCORRECT"
#         ver_prompt.append(prompt)
#     else:
#         action = df.sample(n=1)['transitions'].iloc[0].split("ACTION:")[1].strip().split("NEXT")[0].strip()
#         prompt = "STATE:\n" + x.split("STATE:")[1].strip().split("ACTION")[0].strip() + f"\n\nACTION:\n{action}" + "\nINCORRECT"
#         ver_prompt.append(prompt)


# breakpoint()
# ver_prompt = "\n---\n".join(ver_prompt)
# with open('verifier_few_shot_prompt.txt', 'w') as outfile:
#     outfile.write(ver_prompt)

import openai

openai.organization = 'org-FmY4LUtUMYuCSZZXmUD5s3wG' # Rao's org asu
openai.api_key = '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' # rao's key

prompt = open('description.txt', 'r').read()
prompt += "\nWhat all actions can I take in this state?"
# prompt += "\nGive an example of an action that can I take in this state."
# prompt += "\nIn this state can I uproot the blue block?"
# breakpoint()
response = openai.ChatCompletion.create(
    model='gpt-4',
    messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": prompt}
    ],
    max_tokens=200,
    temperature=1,
    n=1,
)
print(response)
breakpoint()