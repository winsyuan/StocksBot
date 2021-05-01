import discord
import os
from decouple import config


class DiscordBot(discord.Client):


    async def on_go():
        print('Bot is ready')
    async def on_ready(self):
        print("Logged in as {0.user}".format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("hello"):
            await message.channel.send("bye")


    async def new_member(self, member):
        await message.channel.send(f'(member) has joined the server.')


    async def member_removed(self, member):
        await message.channel.send(f'(member) has left')

client = DiscordBot()
client.run(config("DISCORD_TOKEN"))
