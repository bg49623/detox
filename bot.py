import os
import discord
#from dotenv import load_dotenv
import InferenceScript
import pickle
import json

with open('users.json', 'r') as f:
    users = json.load(f)

with open('curse-translation.pickle', 'rb') as f:
    T = pickle.load(f)

#load_dotenv()
token = 'NjgzNDc0NDY2ODE0MTY1MDM1.XlsiiQ.uQd23lR-kZqJPy3o6nkfcW1r6bw'

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if(str(message.author) != 'detoxbot#2304'):
        channel = message.channel
        print(str(message.author) + ': ' + message.content)
        if(is_toxic(translate(message.content.lower()))):
            if(str(message.author)) in users.keys():
                users[str(message.author)] = int(users[str(message.author)]) + 1
            else:
                users[str(message.author)] = "1"

            await channel.send("Hello {}, your message has been deleted for using language that is considered harassing or toxic. You've been reported to the moderators.".format(str(message.author)))
            await message.delete()

            with open('users.json', 'w') as f:
                json.dump(users, f)

def is_toxic(x):
    return InferenceScript.infer(x) > 0.6

def translate(x):
    all = x.replace('\n', ' ').split(' ')
    for i in range(len(all)):

        word = all[i]
        puncf = ""
        puncl = ""

        try:
            if(word[-1] == '.' or word[-1] == '!' or word[-1] == ',' or word[-1] == '?' or word[-1] == '"' or word[-1] == "'"):
                puncl = word[-1]
                word = word[:-1]

            if(word[0] == '.' or word[0] == '!' or word[0] == ',' or word[0] == '?' or word[0] == '"' or word[0] == "'"):
                puncf = word[0]
                word = word[1:]
        except:
            continue

        if word in T.keys():
            all[i] = puncf + T[word] + puncl

    return ' '.join(all)

client.run(token)
