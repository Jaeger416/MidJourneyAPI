import json
import Levenshtein as lev
with open("./hps_training_prompts.json", 'r') as f:
    data = json.load(f)
    
with open("/media/caesar/Expansion/new_1.json", 'r') as f:
    exist_prompts = json.load(f)
exist_prompts = [d['prompt'] for d in exist_prompts]

used = []
for p in exist_prompts:
    if p in data:
        used.append(p)
    else:
        dist = [lev.ratio(p,d) for d in data]
        max_index = max(enumerate(dist), key=lambda x: x[1])[0]
        matched_prompt = data[max_index]
        used.append(matched_prompt)
        # print(p)
        # print(matched_prompt)
        # print('==============================================')
        assert matched_prompt in data

unused = [p for p in data if p not in used]
l = len(unused) // 5
for i in range(5):
    with open(f'prompts/split_{i}.json', 'w') as f:
        json.dump(unused[i * l : (i + 1) * l], f)

        