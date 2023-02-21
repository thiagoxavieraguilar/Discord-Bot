import requests
crypto = "btc"
base = "usdt"
response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={crypto.upper()}{base.upper()}")
data = response.json()  
price = data.get("price")
print(price)



@bot.command
async def ai_response():
    if message.content.startswith('!openai'):
        try:
            message_without_prefix = message.content[7:]
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=message_without_prefix,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.8,
            )

            response_text = response["choices"][0]["text"].strip()
            await message.channel.send(response_text)

        except:
             await message.channel.send('say !openai and write you question after that, example: !openai who is the president of usa? ')

