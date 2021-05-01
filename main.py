import discord
import os
from decouple import config


class DiscordBot(discord.Client):
    async def on_ready(self):
        print("Logged in as {0.user}".format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith(""):
            await message.channel.send("")


client = DiscordBot()
client.run(config("DISCORD_TOKEN"))
