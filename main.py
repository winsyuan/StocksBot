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
        if message.content.startswith("$buy"):
            userMessage = message.content.split()
            try:
                stock = userMessage[1]
            except:
                await message.channel.send("No stock entered")
            try:
                money = userMessage[2]
            except:
                await message.channel.send("Amount of money not entered")
            try:
                floatMoney = float(money)
            except:
                await message.channel.send("Please enter a valid number")
            try:
                stockPrice = current_price(stock)
            except:
                await message.channel.send("Not a valid stock")
            stockAmount = int(floatMoney//float(stockPrice))
            moneyLeftover = "{:.2f}".format(floatMoney%float(stockPrice))
            if(stockAmount == 0):
                await message.channel.send("```You cannot buy a full share of " + stock + " with $" + money + "```")
            elif(stockAmount == 1):
                await message.channel.send("```You can buy " + str(stockAmount) + " share of " + stock + " with $" + moneyLeftover + " leftover```")
            else:
                await message.channel.send("```You can buy " + str(stockAmount) + " shares of " + stock + " with $" + moneyLeftover + " leftover```")
            stock = yf.Ticker("AMZN") 
            #hist = stock.history(period="max")
            #print(current_price('AAPL'))
            await message.channel.send(stock.sustanability)
            
client = DiscordBot()
client.run(config("DISCORD_TOKEN"))
