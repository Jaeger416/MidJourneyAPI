# MiDjourneyAPI
This is API for automatic run midjourney image generation in discord

## preparation

1. Sign up discord , invite midjourney bot to your channel and subscribe.
2. Open F12 developer tools of browser, send a prompt. You can find all required params in developer tools --> network --> interactions --> pyload. Put your params in sender_params.json.

## Running

```shell
# send prompts to discord
python sender.py --params path/to/sender_params.json --from_file path/to/prompts.json --task-name demo

# download images from discord
# open another shell
python receiver.py --params path/to/sender_params.json --task-name demo

# make sure running render and receiver together and use the same param.json and task-name
```

change sending time interval according to MidJourney Server busyness, the default is set to 45.0s for relax mode.

```shell
# for fast mode we recommend
python sender.py --params path/to/sender_params.json --from_file path/to/prompts.json --task-name demo --wait-time 4.5
```

## Tips
1. Each IP can only run one MidJourney at the same time
2. In relax mode, the approximated speed is 60 images/hour, 600 images/hour for fast mode.
3. Because discord api can only go back to the latest 100 history of channel, earlier history won't be downloaded by receiver. Please make sure receiver and sender run at the same pace.
4. If you didn't download in time and the image can't be traced back by receiver, invite "Channel Attachments Downloader" bot to your channel. It can trace back about 1000~1500 attachments in channel history. You can also develope a crawler for Midjourney gallery, where all your generated images are stored online.


## To Do
1. Try use pydiscord for more functions.
2.  Midjourney gallery crawler
