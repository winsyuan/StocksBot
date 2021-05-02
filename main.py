import discord
from decouple import config
import yfinance as yf
from bs4 import BeautifulSoup
import requests
import os
import mplfinance as mpf

intents = discord.Intents.default()

intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_member_join(member):
    await member.send("Welcome to the RUhacks stonks server!")
    await member.send("Are you a new to investing? (yes/no)")


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
                "ticker": item.select("[aria-label=Symbol]")[0].get_text(),
                "name": item.select("[aria-label=Name]")[0].get_text(),
                "price": item.select("[aria-label*=Price]")[0].get_text(),
                "change_percentage": item.select('[aria-label="% Change"]')[
                    0
                ].get_text(),
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

    # DMS a new client
    if not message.guild:
        # Answer yes output
        if message.content.startswith("yes") or message.content.startswith("Yes"):
            await message.channel.send(
                "**How you can get started:**"
                "\n1. You should open an account with a stocks brokerage("
                "ex. Wealthsimple, Investing through your bank, Questrade, etc."
                "\n2. Open a Tax Free Savings Account(TFSA), this will save you from paying any "
                "taxes on the profits you make."
                "\n3. Research companies and find stocks you are interested."
                "\n4. When you you find a good entry point use your TFSA and start investing."
                "\n\nNow that you are ready, this server will help you find stocks, the prices and "
                "trends in the market.\n"
                "Enter `$help` to find commands you can use in this server for analyzing stock."
            )
        # Answer with no
        elif message.content.startswith("no") or message.content.startswith("No"):
            await message.channel.send(
                'Enter "$help" to find commands you can use in this server for analyzing stock.'
            )
        # Invalid input
        elif (
            len(message.content) > 1
            and not message.content.startswith("$help")
            and not message.content.startswith("$active")
            and not message.content.startswith("$buy")
            and not message.content.startswith("$graph")
            and not message.content.startswith("$ticker")
        ):
            await message.channel.send("Invalid input, please enter a valid input.")
    """
        Command that gets more information on a stock
        $ticker [req: symbol]
        ex: $ticker AAPL
    """
    if message.content.startswith("$ticker"):
        input_message = message.content.split(" ")
        length = len(input_message)
        output_message = ""
        if length == 1:
            output_message = (
                "Missing required symbol parameter try `$ticker (TICKER SYMBOL)`"
            )
        else:
            ticker = input_message[1]
            stock = yf.Ticker(ticker)
            valid = valid_stock_check(stock)
            if valid:
                if length == 2:
                    output_message = "**Information about " + ticker.upper() + "** \n"
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

        output_message = "**Most Active Stocks**```\nCompany Name | Ticker | Stock Price | Percentage Change  \n"
        data = scrap_yahoo_trending_stocks()
        for i in range(len(data)):
            output_message += (
                data[i]["name"]
                + " "
                + data[i]["ticker"]
                + " $"
                + data[i]["price"]
                + " "
                + data[i]["change_percentage"]
                + "\n"
            )
        output_message += "```"
        await message.channel.send(output_message)

    def current_price(symbol):  # function to get current price of stock
        ticker = yf.Ticker(symbol)
        today_data = ticker.history(period="1d")
        return today_data["Close"][0]

    if message.content.startswith(
        "$buy"
    ):  # The bot outputs the amount of shares that can be bought
        buyMessage = message.content.split()
        try:
            stock = buyMessage[1]
        except:
            await message.channel.send("No stock entered")
            return
        try:
            money = buyMessage[2]
        except:
            await message.channel.send("Amount of money not entered")
            return
        try:
            floatMoney = float(money)
        except:
            await message.channel.send("Please enter a valid number.")
            return
        try:
            stockPrice = current_price(stock)
        except:
            await message.channel.send("Not a valid stock.")
            return
        stockAmount = int(floatMoney // float(stockPrice))
        moneyLeftover = "{:.2f}".format(floatMoney % float(stockPrice))
        if stockAmount == 0:
            await message.channel.send(
                "```You cannot buy a full share of " + stock + " with $" + money + "```"
            )
        elif stockAmount == 1:
            await message.channel.send(
                "```You can buy "
                + str(stockAmount)
                + " shares of "
                + stock
                + " with $"
                + moneyLeftover
                + " leftover.```"
            )
        else:
            await message.channel.send(
                "```You can buy "
                + str(stockAmount)
                + " shares of "
                + stock
                + " with $"
                + moneyLeftover
                + " leftover.```"
            )
    if message.content.startswith("$graph"):  # The bot outputs a graph
        graphMessage = (
            message.content.split()
        )  #  The format is $graph |StockName| |startdate| |enddate| |time interval|
        try:
            stockName = graphMessage[1]
            startDate = graphMessage[2]
            endDate = graphMessage[3]
            interval = graphMessage[4]
        except:
            await message.channel.send(
                "Please enter the correct format: ```$graph StockName YYYY-MM-DD YYYY-MM-DD 1m/1h/1d/1wk/1mo```"
            )
        stock = yf.Ticker(stockName)
        hist = stock.history(
            start=startDate, end=endDate, interval=interval, actions=False
        )
        mpf.plot(
            hist,
            type="candle",
            volume=True,
            style="yahoo",
            mav=(20),
            title=stockName,
            tight_layout=True,
            savefig="plot.png",
        )
        await message.channel.send(file=discord.File("plot.png"))
        os.remove("plot.png")
    if message.content.startswith("$help"):
        await message.channel.send(
            "Valid commands include `$active`, `$buy`, `$graph`, `$ticker`\n"
        )
        await message.channel.send(
            "> `$active` displays the most actively traded stocks\n> **To use $active:** enter *$active*\n"
        )
        await message.channel.send(
            "> `$buy` looks at the stock's price and calculates how many shares you can buy with a given amount of "
            "money\n> **To use $buy:** enter *$buy*, the ticker symbol and the amount of money you would like to "
            "spend, all separated by spaces \n "
        )
        await message.channel.send(
            "> `$graph` sends a graph of a given stock over a given time interval\n> **To use $graph:** enter "
            "*$graph*, the ticker symbol, the start and end date, and the time interval, all separated by spaces \n "
        )
        await message.channel.send(
            "> `$ticker` displays key information on a chosen stock\n> **To use $ticker:** enter *$ticker*, "
            "and the ticker symbol\n "
        )


client.run(config("DISCORD_TOKEN"))
