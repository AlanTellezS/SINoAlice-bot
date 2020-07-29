import discord
import os
import asyncio
from enum import Enum
from common_embed import generic_embed
from datetime import datetime
from discord.ext import commands

client = commands.Bot(command_prefix = "$")

#Image that can be added to embeds
icon_img = "https://pht.qoo-static.com/sLUUkCD39IWR7sHHpjHlJlIm0ft6sCkMQB5aZc4AyLtFt44lEUdqso3nFUb4x-PFQw=w512"

#Listeners to reactions
#1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣
#I wanted to do this with a json but handling the emojis was annoying so RIP
#if no base_rolename is given then emoji value will be the name of the role
listeners = [
    {
        'message_id': 737829720418287697,
        'base_rolename':"Guerrilla ",
        'emojis_allowed':[
            {'name':"1️⃣", 'value':"1"},
            {'name':"2️⃣", 'value':"2"},
            {'name':"3️⃣", 'value':"3"},
            {'name':"4️⃣", 'value':"4"},
            {'name':"5️⃣", 'value':"5"},
            {'name':"6️⃣", 'value':"6"}
        ],
        'message': "If you want to get notified when Guerilla goes live, use one or more of the reactions to this message.n" +
            "The reactions relate to the following timeslots (UTC) of the Events:\n",
        'times':[
            {'time':datetime(2020, 1, 1, 0, 30, 0), 'role':"Guerrilla 1"},
            {'time':datetime(2020, 1, 1, 2, 30, 0), 'role':"Guerrilla 2"},
            {'time':datetime(2020, 1, 1, 11, 30, 0), 'role':"Guerrilla 3"},
            {'time':datetime(2020, 1, 1, 18, 30, 0), 'role':"Guerrilla 4"},
            {'time':datetime(2020, 1, 1, 20, 30, 0), 'role':"Guerrilla 5"},
            {'time':datetime(2020, 1, 1, 22, 30, 0), 'role':"Guerrilla 6"}
        ]
    },
    {
        'message_id': 737829728743850034,
        'base_rolename':"Conquest",
        'emojis_allowed':[
            {'name':"1️⃣", 'value':" 1"},
            {'name':"2️⃣", 'value':" 2"},
            {'name':"3️⃣", 'value':" 3"},
            {'name':"4️⃣", 'value':" 4"},
            {'name':"5️⃣", 'value':" 5"},
            {'name':"6️⃣", 'value':" 6"}
        ],
        'message': "If you want to get notified when Conquest goes live, use one or more of the reactions to this message.\n" +
            "The reactions relate to the following timeslots (UTC) of the Events:\n",
        'times':[ 
            {'time':datetime(2020, 1, 1, 1, 30, 0), 'role':"Conquest 1"},
            {'time':datetime(2020, 1, 1, 3, 30, 0), 'role':"Conquest 2"},
            {'time':datetime(2020, 1, 1, 12, 0, 0), 'role':"Conquest 3"},
            {'time':datetime(2020, 1, 1, 19, 30, 0), 'role':"Conquest 4"},
            {'time':datetime(2020, 1, 1, 21, 30, 0), 'role':"Conquest 5"},
            {'time':datetime(2020, 1, 1, 23, 30, 0), 'role':"Conquest 6"}
        ]
    },
    {
        'message_id': 737829736864284694,
        'base_rolename':"",
        'emojis_allowed':[
            {'name':"1️⃣", 'value':"Colosseum"}
        ],
        'message': "If you want to get notified when Colosseum goes live, use one or more of the reactions to this message.\n"+
        "The reactions relate to the following timeslots (UTC) of the Events:\n",
        'times':[
            {'time':datetime(2020, 1, 1, 18, 50, 0, 0), 'role':"Colosseum"}
        ]
    }
]

async def startReminders(channel):
    guild = client.guilds[0]
    await channel.send("Reminders started")
    while True:
        found = False
        time = datetime.utcnow()
        for listener in listeners:
            if (found): break
            for t in listener['times']:
                if (t['time'].minute == time.minute and t['time'].hour == time.hour and t['time'].second == time.second):
                    role = discord.utils.find(lambda r : r.name == t['role'], guild.roles)
                    await channel.send(role.mention+" has started")
                    await asyncio.sleep(2)

@client.event
async def on_ready():
    print("Ygdrasil bot started")
    print("--------------------")
    for channel in client.guilds[0].channels:
        if channel.name == "bot":
            botChannel = channel
    await startReminders(channel)

@client.event
async def on_raw_reaction_add(payload):
    print(payload.emoji.name)
    for listener in listeners:
        if listener['message_id'] == payload.message_id:
            for emoji in listener['emojis_allowed']:
                if (payload.emoji.name == emoji["name"]):
                    rolename = listener["base_rolename"] + emoji["value"]
                    guild = client.guilds[0]
                    role = discord.utils.find(lambda r : r.name == rolename, guild.roles)
                    member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                    await member.add_roles(role)
                    print("Role added")

@client.event
async def on_raw_reaction_remove(payload):
    print(payload.emoji.name)
    for listener in listeners:
        if listener['message_id'] == payload.message_id:
            for emoji in listener['emojis_allowed']:
                if (payload.emoji.name == emoji["name"]):
                    rolename = listener["base_rolename"] + emoji["value"]
                    guild = client.guilds[0]
                    role = discord.utils.find(lambda r : r.name == rolename, guild.roles)
                    member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                    await member.remove_roles(role)
                    print("Role added")

@client.command()
async def send_listeners_message(context):
    for listener in listeners:
        emojis = listener['emojis_allowed']
        times = listener['times']
        msg = listener['message']
        for i in range(len(emojis)):
            msg = msg + emojis[i]['name'] + " " + str(times[i]['time'].hour).rjust(2, "0") + ":" + str(times[i]['time'].minute).rjust(2, "0") + "\n"
        message = await context.send(msg)
        for emoji in listener['emojis_allowed']:
            await message.add_reaction(emoji["name"])

@client.command()
async def hello(message):
    """
    guild = client.guilds[0]
    role = discord.utils.find(lambda r : r.name == "Guerrilla 1", guild.roles)"""
    channel = message.channel
    while True:
        await channel.send("Hello")
        await asyncio.sleep(60)

client.run(os.getenv('TOKEN'))