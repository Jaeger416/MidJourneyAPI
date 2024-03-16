import requests
import json
import numpy as np
import time
import pandas as pd
import os
import re
from datetime import datetime
import glob
import argparse
import sys
import hashlib

class Receiver:

    def __init__(self, 
                 params,
                 local_path,
                 task_name):
        
        self.params = params
        self.local_path = local_path
        self.task_name = task_name
        self.json_path = f'{task_name}.json'
        os.makedirs(self.local_path, exist_ok=True)
        
        with open('hps_training_prompts.json', 'r') as f:
            self.all_prompts = json.load(f)

        self.sender_initializer()
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as f:
                self.df = json.load(f) 
        else:
            self.df = []
            # pd.DataFrame(columns = ['prompt', 'url', 'filename', 'is_downloaded'])

    
    def sender_initializer(self):

        with open(self.params, "r") as json_file:
            params = json.load(json_file)

        self.channelid=params['channelid']
        self.authorization=params['authorization']
        self.headers = {'authorization' : self.authorization}

    def retrieve_messages(self):
        r = requests.get(
            f'https://discord.com/api/v10/channels/{self.channelid}/messages?limit={100}', headers=self.headers)

        jsonn = json.loads(r.text)
        return jsonn


    def collecting_results(self):
        message_list  = self.retrieve_messages()
        self.awaiting_list = pd.DataFrame(columns = ['prompt', 'status'])
        for i,message in enumerate(message_list):

            if (message['author']['username'] == 'Midjourney Bot') and ('**' in message['content']):
                
                if len(message['attachments']) > 0:

                    if (message['attachments'][0]['filename'][-4:] == '.png') or ('(Open on website for full quality)' in message['content']):
                        id = message['id']
                        prompt = message['content'].split('**')[1].split(' --')[0]
                        url = message['attachments'][0]['url']
                        exists_prompts = [d['prompt'] for d in self.df]
                        if prompt not in exists_prompts:
                            filename = hashlib.sha256(prompt.encode()).hexdigest() + ".png"
                            info = {
                                "prompt":prompt,
                                "url":url,
                                "filename":filename,
                                "is_downloaded":0
                            }
                            self.df.append(info)
                        else:
                            filename = self.df[exists_prompts.index(prompt)]['filename']

                    else:
                        id = message['id']
                        prompt = message['content'].split('**')[1].split(' --')[0]
                        if ('(fast)' in message['content']) or ('(relaxed)' in message['content']):
                            try:
                                status = re.findall("(\w*%)", message['content'])[0]
                            except:
                                status = 'unknown status'
                        self.awaiting_list.loc[id] = [prompt, status]

                else:
                    id = message['id']
                    prompt = message['content'].split('**')[1].split(' --')[0]
                    if '(Waiting to start)' in message['content']:
                        status = 'Waiting to start'
                    self.awaiting_list.loc[id] = [prompt, status]
                    
    
    def outputer(self):
        if len(self.awaiting_list) > 0:
            print(datetime.now().strftime("%H:%M:%S"))
            print('prompts in progress:')
            print(self.awaiting_list)
            print('=========================================')

        waiting_for_download = [d["prompt"] for d in self.df if d["is_downloaded"] == 0]
        if len(waiting_for_download) > 0:
            print(datetime.now().strftime("%H:%M:%S"))
            print('waiting for download prompts: ', waiting_for_download)
            print(f"total {len(waiting_for_download)} prompts")
            print('=========================================')
        
        print(f"total {len(os.listdir(self.local_path))} images has been downloaded")
        print('=========================================')

    def downloading_results(self):
        processed_prompts = []
        for i in range(len(self.df)):
            if self.df[i]["is_downloaded"] == 0:
                response = requests.get(self.df[i]["url"])
                with open(os.path.join(self.local_path, self.df[i]["filename"]), "wb") as req:
                    req.write(response.content)
                self.df[i]["is_downloaded"] = 1
                processed_prompts.append(self.df[i]["prompt"])
        if len(processed_prompts) > 0:
            print(datetime.now().strftime("%H:%M:%S"))
            print('processed prompts: ', processed_prompts)
            print('=========================================')

    def save_result(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.df, f)

  
    def main(self):
        while True:
            try:
                self.collecting_results()
                self.outputer()
                self.downloading_results()
                self.save_result()
                time.sleep(2)
            except:
                self.save_result()

def parse_args(args):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--params',help='Path to discord authorization and channel parameters', default="sender_params.json")
    parser.add_argument('--local-path',help='Path to output images', required=True)
    parser.add_argument('--task-name',help='task name',default='mdj')
        
    return parser.parse_args(args)


if __name__ == "__main__":

    args = sys.argv[1:]
    args = parse_args(args)
    params = args.params
    local_path = args.local_path #'/Users/georgeb/discord_api/images/'
    task_name = args.task_name

    print('=========== listening started ===========')
    receiver = Receiver(params, local_path, task_name)
    receiver.main()