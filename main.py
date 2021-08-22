import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "bad", "blue", "brokenhearted", "cast down", "crestfallen", "dejected", "depressed", "despondent",
             "depressing" "disconsolate", "doleful", "down", "downcast", "downhearted", "down in the mouth", "droopy",
             "forlorn", "gloomy", "glum", "hangdog", "heartbroken", "heartsick", "heartsore", "heavyhearted",
             "inconsolable", "joyless", "low", "low-spirited", "melancholic", "melancholy", "miserable", "mournful",
             "saddened", "sorrowful", "sorry", "unhappy", "woebegone", "woeful", "wretched"]

starter_encouragements = ["Cheer Up!", "Hang in there", "You're freakin' awesome", "You can open up to me."]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("http://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = '"' + json_data[0]['q'] + '"' + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_messages]


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if (len(encouragements)) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print('I have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('#pp'):
        await message.channel.send('Hello there...')

    msg = message.content

    if message.content.startswith('#motivate_me'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + list(db['encouragements'])
    # if any(word in msg for word in sad_words):
    # await message.channel.send(random.choice(starter_encouragements))

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("#newmotivate"):
        encouraging_message = msg.split("#newmotivate ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("#delmotivate"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("#delmotivate", 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("#list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("#responding"):
        value = msg.split("#responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")


keep_alive()
client.run(os.getenv('TOKEN'))
# my_secret = os.environ['TOKEN']

