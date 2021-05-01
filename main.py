import discord
import os
import random
from decouple import config


class DiscordBot(discord.Client):
    async def on_ready(self):
        print("Logged in as {0.user}".format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return

        numbers = ['1','2','3','4','5']
        if message.content == ("$number"):
            response = random.choice(numbers)
               await message.channel.send(response)
client = DiscordBot()
client.run(config("DISCORD_TOKEN"))
