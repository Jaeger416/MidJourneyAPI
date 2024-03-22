import json
import Levenshtein as lev
with open("./hps_training_prompts.json", 'r') as f:
    data = json.load(f)
    
with open("./new_1.json", 'r') as f:
    exist_prompts = json.load(f)
exist_prompts = [d['prompt'] for d in exist_prompts]

new_prompt = []
for p in exist_prompts:
    if p in data:
        new_prompt.append(p)
    else:
        dist = [lev.ratio(p,d) for d in data]
        min_index = max(enumerate(dist), key=lambda x: x[1])[0]
        new_prompt.append(p)
        