import os
import discord
from discord.ext import commands

client = discord.Client()
notified_users = set()

# your token
TOKEN = os.getenv('DISCORD_TOKEN') 

# channel id for message forwarding, thats where the incoming messages will be redirected
FORWARD_CHANNEL_ID = 000000000000000000 

# message to send to the user that messaged you before forwarding
NOTIFY_MESSAGE = "I'm unavailable right now, but I've been notified of your message!" 

# user id's to exclude from sending the NOTIFY_MESSAGE to (optional)
excluded_users = {
    000000000000000000,
}

@client.event
async def on_ready():
    print(f"logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if isinstance(message.channel, discord.DMChannel):
        if message.author.id not in excluded_users and message.author.id not in notified_users:
            await message.channel.send(NOTIFY_MESSAGE)
            notified_users.add(message.author.id)
    
        forward_channel = client.get_channel(FORWARD_CHANNEL_ID)
        if forward_channel:
            await forward_channel.send(f"incoming message from **{message.author}**:```\n{message.content}```")
        else:
            print(f"error: could not find channel with id: {FORWARD_CHANNEL_ID}")

client.run(TOKEN)