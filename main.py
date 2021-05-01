import discord
import os
from decouple import config


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(""):
            await message.channel.send('')

client.run(config('DISCORD_TOKEN'))
