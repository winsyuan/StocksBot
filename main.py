import discord
import os
import random
import matplotlib.pyplot as plt
import mplfinance as mpf
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
        if message.content.startswith("$buy"): # The bot outputs the amount of shares that can be bought
            buyMessage = message.content.split()
            try:
                stock = buyMessage[1]
            except:
                await message.channel.send("No stock entered")
            try:
                money = buyMessage[2]
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
        if message.content.startswith("$graph"): # The bot outputs a graph
            graphMessage = message.content.split() #  The format is $graph StockName startdate enddate
            try:
                stockName = graphMessage[1]
                startDate = graphMessage[2]
                endDate = graphMessage[3]
                interval = graphMessage[4]
            except:
                await message.channel.send("Please enter the correct format: ```$graph StockName YYYY-MM-DD YYYY-MM-DD 1m/1h/1d/1wk/1mo```")
            stock = yf.Ticker(stockName) 
            hist = stock.history(start=startDate, end=endDate,interval = interval,actions=False)
            mpf.plot(hist,type='candle',volume=True,style='yahoo',mav=(20),title=stockName, tight_layout=True,savefig='plot.png')
            await message.channel.send(file=discord.File('plot.png'))
            os.remove('plot.png')
        if message.content.startswith("$help"):
            await message.channel.send("valid commands include `$active`, `$buy`, and `$graph`\n")
            await message.channel.send("> `$active` sends information on the most actively traded stocks\n> **To use $active:** enter *$active*\n")
            await message.channel.send("> `$buy` looks at the stock's price and calculates how many shares you can buy with a given amount of money\n> **To use $buy:** enter *$buy*, the ticker symbol and the amount of money you would like to spend, all separated by spaces \n")
            await message.channel.send("> `$graph` sends a graph of a given stock over a given time interval\n> **To use $graph:** enter *$graph*, the ticker symbol, the start and end date, and the time interval, all separated by spaces \n")


client = DiscordBot()
client.run(config("DISCORD_TOKEN"))
