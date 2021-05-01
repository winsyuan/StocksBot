import discord
import os
import random
from decouple import config
import yfinance as yf


class DiscordBot(discord.Client):

    async def on_ready(self):
        print("Logged in as {0.user}".format(client))

    async def on_message(self, message):
        def current_price(symbol):
            ticket = yf.Ticker(symbol)
            today_data = ticket.history(period='1d')
            return today_data['Close'][0]
        if message.author == client.user:
            return
        if message.content == ("$ticket"):
            stock = yf.Ticker("AAPL")
            hist = stock.history(period="max")
            print(current_price('AAPL'))
            #await message.channel.send(aapl)
client = DiscordBot()
client.run(config("DISCORD_TOKEN"))
