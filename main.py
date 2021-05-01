import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$hello"):
        await message.channel.send('Hello!')

    if message.content.startswith("$bob"):
            await message.channel.send('Bob!')

client.run(os.getenv('DISCORD_TOKEN'))
