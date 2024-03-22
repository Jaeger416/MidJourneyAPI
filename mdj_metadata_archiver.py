import discord
import requests
import os
import json
import asyncio

intents = discord.Intents.default()
intents.messages = True  # Enables receiving messages
intents.dm_messages = True  # Enables receiving DM messages

client = discord.Client(intents=intents, proxy="http://127.0.0.1:7890/")

# Open the JSON file and load its content
with open('./bot_config.json', 'r') as file:
    config = json.load(file)
# Configuration
#YOUR_CHANNEL_ID = 980108517929283604
#YOUR_CHANNEL_ID = 1089358474426712224  # Replace with your channel ID
YOUR_CHANNEL_ID = config["channel_id"]
START_MESSAGE_ID = 0  # Set to 0 to start from the beginning, or specific message ID to start from that message
MESSAGE_QUANTITY = config["message_quantity"] # Number of messages to examine
DELAY_SECONDS = config["delay_secs"]
LOOP_COUNTER = 50  # Number of loops after which to introduce a delay
LOOP_DELAY_SECONDS = config["loop_delay_secs"]

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(YOUR_CHANNEL_ID)
    channel_dir = config['image_dir_root']
    # Ensure the directory to save images exists
    os.makedirs(channel_dir, exist_ok=True)  # Replace with your save path

    # Fetch the most recent message ID
    async for last_message in channel.history(limit=1):
        last_message_id = last_message.id if last_message else None

    first_message_id = 0
    # Fetch the earliest message ID
    async for first_message in channel.history(limit=1, oldest_first=True):
        first_message_id = first_message.id if first_message else None

    print(f"First message ID in the channel: {first_message_id}")
    print(f"Last message ID in the channel: {last_message_id}")
    # Start processing messages
    reached_start = START_MESSAGE_ID == 0
    message_count = 0
    earliest_message_id = 0 #first_message_id
    loop_count = 0
    count = 0
    while True:
        messages_fetched = 0

        async for message in channel.history(limit=100, before=discord.Object(id=earliest_message_id) if earliest_message_id else None):
            messages_fetched += 1
            count += 1
            timestamp = message.created_at.strftime('%m/%d/%Y @ %H:%M:%S')
            #print(f"{timestamp}")
            
            if message_count >= MESSAGE_QUANTITY:
                break
            
            formatted = "{:03d}".format(count)
            fetched_count = "{:03d}".format(messages_fetched)
            print(f"{fetched_count}.{formatted}.{timestamp}.({len(message.attachments)})")
            for attachment in message.attachments:
                if any(attachment.filename.endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']):
                    response = requests.get(attachment.url)
                    
                    timestamp = message.created_at.strftime('%Y%m%d_%H%M')
                    formatted_filename = f"{timestamp}_{attachment.filename}"


                    file_path = os.path.join(channel_dir, formatted_filename)  # Replace with your save path
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f'Downloaded {attachment.filename}')

            if message_count >= MESSAGE_QUANTITY:
                break

            earliest_message_id = message.id

            # if messages_fetched < 100:
            # # Break the loop if there were less than 100 messages in the last fetch,
            # # indicating we have reached the beginning of the channel history
            #     break

            # Delay after every 100 loops
            if loop_count >= LOOP_COUNTER:
                print(f"Pausing for {DELAY_SECONDS} seconds...")
                await asyncio.sleep(DELAY_SECONDS)
                loop_count = 0  # Reset the loop counter
            await asyncio.sleep(LOOP_DELAY_SECONDS)


client.run(config['token'])  # Replace with your bot token
