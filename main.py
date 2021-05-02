import discord
from decouple import config

intents = discord.Intents.default()

intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("hello"):
        await message.channel.send("bye")


@client.event
async def on_member_join(member):
    await member.send('user joined')


@client.event
async def on_member_remove(member):
    await member.send('user left')


client.run(config("DISCORD_TOKEN"))
