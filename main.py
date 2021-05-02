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
    await member.send('Welcome to the RUhacks stonks server!')
    await member.send('Are you a new to investing?')

   # if member.content.startswith("yes"):
    #    await member.send('You can start by making an account an online broker')
@client.event
async def on_message(message):

    if not message.guild:
        if message.content.startswith('yes') or message.content.startswith('Yes'):
            await message.channel.send('')

        elif message.content.startswith('no') or message.content.startswith('No'):
            await message.channel.send('Enter "$help" to find commands you can use in this server for analyzing stock')

        else (len(message.content) > 0)
            await message.channel.send('Invalid input')



@client.event
async def on_member_remove(member):

    await member.send('user left')


client.run(config("DISCORD_TOKEN"))
