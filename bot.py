import os
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if(str(message.author) != 'test-bot#8872'):
        channel = message.channel
        print(str(message.author) + ': ' + message.content)
        if(is_toxic(message.content.lower())):
            await channel.send(str(message.author) + ' is being toxic! he said: ' + message.content )
            await message.delete()
        if(should_kick(message.content.lower())):
            await channel.send(str(message.author) + ' is kicked for being ultra toxic! he said: ' + message.content )
            await message.author.kick()

def is_toxic(x):
    if "fuck" in x :
        return True
    return False

def should_kick(x):
    if "rithik" in x:
        return True
    return False

client.run(token)
