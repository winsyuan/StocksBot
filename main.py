import discord
import os
import random
from decouple import config
import yfinance as yf


class DiscordBot(discord.Client):

    async def on_ready(self):
        print("Logged in as {0.user}".format(client))

    async def on_message(self, message):
        def current_price(symbol): # function to get current price of stock
            ticket = yf.Ticker(symbol)
            today_data = ticket.history(period='1d')
            return today_data['Close'][0]
        if message.author == client.user:
            return
        if message.content.startswith("$ticket"):
            userMessage = message.content.split()
            try:
                stock = userMessage[1]
            except:
                await message.channel.send("No stock entered")
            try:
                money = userMessage[2]
            except:
                await message.channel.send("Not a valid price")
            try:
                stockPrice = current_price(stock)
            except:
                await message.channel.send("Not a valid stock")
            stockAmount = float(money)//float(stockPrice)
            moneyLeftover = float(money)%float(stockPrice)
            await message.channel.send("You can buy " + str(stockAmount) + " stocks of " + stock + " with $" + str(moneyLeftover) + " leftover")
            #stock = yf.Ticker("AAPL")
            #hist = stock.history(period="max")
            #print(current_price('AAPL'))
            #await message.channel.send(aapl)
client = DiscordBot()
client.run(config("DISCORD_TOKEN"))
