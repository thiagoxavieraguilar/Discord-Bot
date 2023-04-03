import openai
import discord
from discord.ext import commands 
import requests
import httpx
import os
from dotenv import load_dotenv

#Load the environment variables from the .env file
load_dotenv()

#OpenAI API key
openai.api_key  = os.environ.get("OPENAI")
#token discord
token = os.environ.get("DISCORD")
#alpha api
alpha_api = os.environ.get("ALPHAVANTAGE_API_KEY")


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message: any):
    #ignore messages from the bot itself
    if message.author == bot.user:
        return
    #check if the message contains a bad word
    if "bad word" in message.content:
        await message.channel.send(f" No bad words {message.author}")
        #deleting bad words
        await message.delete()
    #check if the message contains a '!' to start the bot
    elif not "!" in message.content:
        initial_msg = 'Hello, all comands: !crypto, !private, !chatgpt'
        await message.channel.send(initial_msg)
    await bot.process_commands(message)

@bot.command(name="start")
async def send_hello(ctx):
    response = 'Hello, all comands: !crypto, !private, !chatgpt'
    await ctx.send(response)

@bot.command(name="crypto")
async def send_price_crypto(ctx, crypto=None, base=None):
    """send message with price of crypto"""
    try:
        #send a GET request to the Binance API with the requested crypto and base symbols
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={crypto.upper()}{base.upper()}")
        data = response.json()  
        #extract the current price of the requested crypto and base pair
        price = data.get("price")
        if price:
            #create an embed message to display the price
            price = float(price)
            embed = discord.Embed(
            title=f"Price of {crypto.upper()}/{base.upper()}", 
            description=f"The current price of {crypto.upper()}/{base.upper()} is **${price:.2f}**.", 
            color=0x00ff00)
            #send the embed message to the channel where the command was used
            await ctx.send(embed=embed)

        else:
            #if the requested pair is invalid, send an error message with an example of a valid pair
            await ctx.send('Invalid pair, say !crypto and write the pair of crypto, example: !crypto BTC USDT')
    except:
        #if there is an error, send a error message
        await ctx.send('Error,  say !crypto and write the pair of crypto, example: !crypto BTC USDT')


@bot.command(name="private")
async def message_private(ctx):
    """send messages in private"""
    try:
        await ctx.author.send("Private message")
    except discord.errors.forbbiden:
        await ctx.send('Error sending message, enable receive messages from any server')


@bot.command(name="chatgpt")
async def ai_response(ctx,*args):
    """send message with response for openai"""
    if len(args) == 0:
        await ctx.send('say !chatgpt and write you question after that, example: !chatgpt who is the president of usa? ')
    else:
        try:
            msg = " ".join(args)
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=msg,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.8,
                )
            response_text = response["choices"][0]["text"].strip()
            await ctx.send(response_text)
        except:
            await ctx.send('say !chatgpt and write you question after that, example: !chatgpt who is the president of usa? ')
    
@bot.command(name='stock')
async def stock_price(ctx, symbol_stock=None):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol_stock.upper()}&apikey={alpha_api}")
            data = response.json()
            current_price = float(data["Global Quote"]["05. price"])            
            embed = discord.Embed(
                title=f"Price of {symbol_stock.upper()}", 
                description=f"The current price of {symbol_stock.upper()} is **${current_price:.2f}**.", 
                color=0x00ff00)
                #send the embed message to the channel where the command was used
            await ctx.send(embed=embed)
    except:
            await ctx.send('Error, say !stock and write the symbol of the stock, example: !stock MSFT')


bot.run(token)
