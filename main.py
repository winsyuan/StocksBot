import discord
from decouple import config

intents = discord.Intents.default()

intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("hello"):
        await message.channel.send("bye")


@client.event
async def on_member_join(member):
    await member.send("Welcome to the RUhacks stonks server!")
    await member.send("Are you a new to investing?(yes/no)")


# DMS a new client
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.guild:
        # Answer yes output
        if message.content.startswith("yes") or message.content.startswith("Yes"):
            await message.channel.send(
                "How you can get started:"
                "\n1. You should open an account with a stocks brokerage("
                "ex. Wealthsimple, Investing through your bank, Questrade, etc"
                "\n2. Open a Tax Free Savings Account(TFSA), this will save you from paying any "
                "taxes on the profits you make."
                "\n3. Research companies and find stocks you are interested"
                "\n4. When you you find a good entry point use your TFSA and start investing"
                "\n\n Now that you are ready, this server will help you find stocks, the prices and "
                "trends in the market"
            )
            await message.channel.send(
                'Enter "$help" to find commands you can use in this server for analyzing stock'
            )
        # Answer with no
        elif message.content.startswith("no") or message.content.startswith("No"):
            await message.channel.send(
                'Enter "$help" to find commands you can use in this server for analyzing stock'
            )
        # Invalid input
        elif (
            len(message.content) > 1
            and not message.content.startswith("$help")
            and not message.content.startswith("$active")
            and not message.content.startswith("$buy")
            and not message.content.startswith("$graph")
        ):
            await message.channel.send("Invalid input, please enter a valid input.")


client.run(config("DISCORD_TOKEN"))
