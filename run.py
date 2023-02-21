import openai
import discord
from discord.ext import commands 
import requests
import os
from dotenv import load_dotenv

#Load the environment variables from the .env file
load_dotenv()

#OpenAI API key
openai_key = os.environ.get("OPENAI")
token = os.environ.get("DISCORD")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message: any):
    if message.author == bot.user:
        return
    if "bad word" in message.content:
        await message.channel.send(f" No bad words {message.author}")
        #deleting bad words
        await message.delete()
    await bot.process_commands(message)

@bot.command(name="start")
async def send_hello(ctx):
    response = 'Hello'
    await ctx.send(response)

@bot.command(name="crypto")
async def send_price_crypto(ctx, crypto: str, base: str):
    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={crypto.upper()}{base.upper()}")
        data = response.json()  
        price = data.get("price")
        if price:
            price = float(price)
            embed = discord.Embed(
            title=f"Price of {crypto.upper()}/{base.upper()}", 
            description=f"The current price of {crypto.upper()}/{base.upper()} is **${price:.2f}**.", 
            color=0x00ff00
            )

            await ctx.send(embed=embed)
        
        else:
            await ctx.send('Invalid pair')
    except:
        await ctx.send('Error')

@bot.command(name="private")
async def message_private(ctx):
    """send messages in private"""
    try:
        await ctx.author.send("Private message")
    except discord.errors.forbbiden:
        await ctx.send('Error sending message, enable receive messages from any server')

bot.run(token)
