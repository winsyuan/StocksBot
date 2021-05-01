import discord
from decouple import config
import yfinance as yf
import math
from bs4 import BeautifulSoup
import requests


def valid_stock_check(stock):
    if len(stock.info) == 1:
        return False
    return True


def scrap_yahoo_trending_stocks():
    yahoo_trending_url = "https://finance.yahoo.com/most-active/"
    response = requests.get(yahoo_trending_url)
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


class DiscordBot(discord.Client):
    async def on_ready(self):
        print("Logged in as {0.user}".format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return

        # wb currency?
        """
            Command that gets more information on a stock and calculates how many stocks able to purchase
            $ticket [req: symbol] [opt: amount to spend: float]
            ex: $ticket AAPL
            ex: $ticket GOOGL 2000
        """
        if message.content.startswith("$ticket"):
            input_message = message.content.split(" ")
            length = len(input_message)
            output_message = ""
            if length == 1:
                # missing symbol required parameter
                output_message = (
                    "Missing required symbol parameter try `$ticket (SYMBOL)`"
                )
            else:
                ticket = input_message[1]
                stock = yf.Ticker(ticket)
                valid = valid_stock_check(stock)
                if valid:
                    if length == 2:
                        # output stock info with stock.info.{w.e}
                        output_message = "Found stock, format the info and print it"
                    else:
                        ticket = input_message[1]
                        stock = yf.Ticker(ticket)
                        valid = valid_stock_check(stock)
                        if valid:
                            try:
                                spend_amount = float(input_message[2])
                                if spend_amount < 0:
                                    output_message = "Invalid input for amount to spend"
                                else:
                                    # amount_stocks = math.floor(spend_amount / stock.info['regularMarketPrice'])
                                    # remaining_amount = spend_amount - amount_stocks * stock.info['regularMarketPrice']
                                    output_message = "Received valid stock ticket and valid number input"
                            except ValueError:
                                output_message = "Invalid input for amount to spend"
                else:
                    output_message = (
                        "Stock not found, try again with a different symbol"
                    )
            await message.channel.send(output_message)

        if message.content == "$active":
            output_message = "**Most Active Stocks**```\n"
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


client = DiscordBot()
client.run(config("DISCORD_TOKEN"))
