import requests
import json
import time
import re
import argparse
import sys

class Sender:

    def __init__(self, 
                 params):
        
        self.params = params
        self.sender_initializer()

    def sender_initializer(self):

        with open(self.params, "r") as json_file:
            params = json.load(json_file)

        self.channelid=params['channelid']
        self.authorization=params['authorization']
        self.application_id = params['application_id']
        self.guild_id = params['guild_id']
        self.session_id = params['session_id']
        self.version = params['version']
        self.id = params['id']
        self.flags = params['flags']
        
        
    def send(self, prompt):
        header = {
            'authorization': self.authorization
        }
        
        # prompt = prompt.replace('_', ' ')
        # prompt = " ".join(prompt.split())
        # prompt = re.sub(r'[^a-zA-Z0-9\s]+', '', prompt)

        payload = {'type': 2, 
        'application_id': self.application_id,
        'guild_id': self.guild_id,
        'channel_id': self.channelid,
        'session_id': self.session_id,
        'data': {
            'version': self.version,
            'id': self.id,
            'name': 'imagine',
            'type': 1,
            'options': [{'type': 3, 'name': 'prompt', 'value': str(prompt) + ' ' + self.flags}],
            'attachments': []}
            }
        
        r = requests.post('https://discord.com/api/v9/interactions', json = payload , headers = header)
        while r.status_code != 204:
            r = requests.post('https://discord.com/api/v9/interactions', json = payload , headers = header)

        print('prompt [{}] successfully sent!'.format(prompt))

def parse_args(args):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--params', help='Path to discord authorization and channel parameters', default="sender_params.json")
    parser.add_argument('--prompt',help='prompt to generate', default='a little papi')
    parser.add_argument('--from-file',type=str,default="hps_training_prompts.json")
    parser.add_argument('--resume', type=int, default=0)
    parser.add_argument("--task", type=str)
        
    return parser.parse_args(args)


if __name__ == "__main__":

    args = sys.argv[1:]
    args = parse_args(args)
    params = args.params
    prompt = args.prompt
    from_file = args.from_file
    sender = Sender(params)

    if from_file is not None:
        with open(from_file, 'r') as f:
            data = json.load(f)

        idx = args.resume   
        while idx < len(data):
            try:
                prompt = data[idx]
                sender.send(prompt)
                time.sleep(4.5)
                idx += 1
                print(f" finished [{idx}/{len(data)}  ")
            except ConnectionResetError or requests.exceptions.ProxyError:
                time.sleep(1)
            except Exception as e:
                with open(f'{args.task}/finished_idx.json', 'w') as f:
                    json.dump(idx, f)
    else:   
        sender.send(prompt)