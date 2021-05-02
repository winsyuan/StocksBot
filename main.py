import discord
from decouple import config
import yfinance as yf
from bs4 import BeautifulSoup
import requests

intents = discord.Intents.default()

intents.members = True
client = discord.Client(intents=intents)



@client.event
async def on_member_join(member):
    await member.send("Welcome to the RUhacks stonks server!")
    await member.send("Are you a new to investing?(yes/no)")


# DMS a new client
def valid_stock_check(stock):
    if len(stock.info) == 1:
        return False
    return True


def scrap_yahoo_trending_stocks():
    yahoo_trending_url = "https://finance.yahoo.com/most-active/"
    response = requests.get(yahoo_trending_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        data = soup.select(".simpTblRow")[:6]
        return [
            {
                "ticket": item.select("[aria-label=Symbol]")[0].get_text(),
                "name": item.select("[aria-label=Name]")[0].get_text(),
                "price": item.select("[aria-label*=Price]")[0].get_text(),
                "change_percentage": item.select('[aria-label="% Change"]')[0].get_text(),
            }
            for item in data
        ]
    return []


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


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
    """
        Command that gets more information on a stock
        $ticket [req: symbol]
        ex: $ticket AAPL
    """
    if message.content.startswith("$ticket"):
        input_message = message.content.split(" ")
        length = len(input_message)
        output_message = ""
        if length == 1:
            output_message = "Missing required symbol parameter try `$ticket (SYMBOL)`"
        else:
            ticket = input_message[1]
            stock = yf.Ticker(ticket)
            valid = valid_stock_check(stock)
            if valid:
                if length == 2:
                    output_message = "**Information about " + ticket.upper() + "** \n"
                    data = stock.history(period="1d")
                    output_message += (
                        "Company Name: "
                        + stock.info["longName"]
                        + "\n"
                        + "Opening Stock Price: "
                        + str(round(data["Open"][0], 3))
                        + "\n"
                        + "Closing Stock Price: "
                        + str(round(data["Close"][0], 3))
                        + "\n"
                        + "Stock Volume: "
                        + str(round(data["Volume"][0], 3))
                    )
            else:
                output_message = "Stock not found, try again with a different symbol"
        await message.channel.send(output_message)

    if message.content == "$active":
        output_message = "**Most Active Stocks**```\nCompany Name | Ticket | Stock Price | Percentage Change  \n"
        data = scrap_yahoo_trending_stocks()
        for i in range(len(data)):
            output_message += (
                data[i]["name"]
                + " "
                + data[i]["ticket"]
                + " $"
                + data[i]["price"]
                + " "
                + data[i]["change_percentage"]
                + "\n"
            )
        output_message += "```"
        await message.channel.send(output_message)


client.run(config("DISCORD_TOKEN"))
