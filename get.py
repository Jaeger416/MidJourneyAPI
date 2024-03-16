import json
with open("/media/caesar/Expansion/HPD/train.json", 'r') as f:
    data = json.load(f)
data = [d['prompt'] for d in data]
data = list(set(data))
with open("./hps_training_prompts.json", 'w') as f:
    json.dump(data, f)