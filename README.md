# Running

```shell
# send prompts to discord
python sender.py --params path/to/sender_params.json --from_file path/to/prompts.json --task-name demo

# download images from discord
python receiver.py --params path/to/sender_params.json --task-name demo

# make sure running render and receiver together and use the same param.json and task-name
```

change sending time interval according to MidJourney Server busyness, the default is set to 45.0s for relax mode.

```shell
# for fast mode we recommend
python sender.py --params path/to/sender_params.json --from_file path/to/prompts.json --task-name demo --wait-time 4.5
```
