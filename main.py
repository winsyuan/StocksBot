import discord
from decouple import config
import yfinance as yf
import math


def valid_stock_check(stock):
    if len(stock.info) == 1:
        return False
    return True


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


client = DiscordBot()
client.run(config("DISCORD_TOKEN"))
