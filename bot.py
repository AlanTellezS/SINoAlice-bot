import discord
import os
from common_embed import generic_embed
from datetime import datetime
from discord.ext import commands

client = commands.Bot(command_prefix = "$")

times = [
    [
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Guerrilla 1"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Guerrilla 2"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Guerrilla 3"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Guerrilla 4"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Guerrilla 5"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Guerrilla 6"}
    ],
    [
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Conquest 1"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Conquest 2"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Conquest 3"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Conquest 4"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Conquest 5"},
        {'time':datetime(2020, 1, 1, 0, 30), 'role':"Conquest 6"}
    ],
    [
        {'time':datetime(2020, 1, 1, 21, 00), 'role':"Guerrilla 1"}
    ]
]

#Image that can be added to embeds
icon_img = "https://pht.qoo-static.com/sLUUkCD39IWR7sHHpjHlJlIm0ft6sCkMQB5aZc4AyLtFt44lEUdqso3nFUb4x-PFQw=w512"

#Listeners to reactions
#1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣
#I wanted to do this with a json but handling the emojis was annoying so RIP
#if no base_rolename is given then emoji value will be the name of the role
listeners = [
    {
        'message_id': 737050303991382127,
        'base_rolename':"Guerrilla ",
        'emojis_allowed':[
            {'name':"1️⃣", 'value':"1"},
            {'name':"2️⃣", 'value':"2"},
            {'name':"3️⃣", 'value':"3"},
            {'name':"4️⃣", 'value':"4"},
            {'name':"5️⃣", 'value':"5"},
            {'name':"6️⃣", 'value':"6"}
        ]
    },
    {
        'message_id': 0,
        'base_rolename':"Conquest",
        'emojis_allowed':[
            {'name':"1️⃣", 'value':"1"},
            {'name':"2️⃣", 'value':"2"},
            {'name':"3️⃣", 'value':"3"}
        ]
    }
]

async def startReminders(channel):
    guild = client.guilds[0]
    await channel.send("Reminders started")
    while True:
        time = datetime.utcnow()
        print(datetime.minute)
        for t1 in times:
            for t2 in t1:
                if (t2['time'].minute == time.minute and t2['time'].hour == time.hour):
                    print("wut")
                    role = discord.utils.find(lambda r : r.name == t2['role'], guild.roles)
                    await channel.send(role.mention+" Guerrilla event has started")
                    break

@client.event
async def on_ready():
    print("Ygdrasil bot started")
    print("--------------------")

@client.event
async def on_raw_reaction_add(payload):
    for listener in listeners:
        if listener['message_id'] == payload.message_id:
            for emoji in listener['emojis_allowed']:
                if (payload.emoji.name == emoji["name"]):
                    rolename = listener["base_rolename"] + emoji["value"]
                    guild = client.guilds[0]
                    role = discord.utils.find(lambda r : r.name == rolename, guild.roles)
                    member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                    print("Adding "+role.name+" to "+ member.name)
                    await member.add_roles(role)
                    print("Role "+rolename+" added")

@client.event
async def on_raw_reaction_remove(payload):
    for listener in listeners:
        if listener['message_id'] == payload.message_id:
            for emoji in listener['emojis_allowed']:
                if (payload.emoji.name == emoji["name"]):
                    rolename = listener["base_rolename"] + emoji["value"]
                    guild = client.guilds[0]
                    role = discord.utils.find(lambda r : r.name == rolename, guild.roles)
                    member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                    await member.remove_roles(role)
                    print("Role "+rolename+" removed")

@client.command()
async def guerilla_message(context):
    msg = """If you want to get notified when Guerilla goes live, use one or more of the reactions
to this message.
The reactions relate to the following timeslots (UTC) of the Events: 
\n1️⃣ 00:30
2️⃣ 02:30
3️⃣ 11:30
4️⃣ 18:30
5️⃣ 20:00
6️⃣ 22:30"""
    message = await context.send(msg)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")
    await message.add_reaction("6️⃣")

@client.command()
async def hello(message):
    guild = client.guilds[0]
    role = discord.utils.find(lambda r : r.name == "Guerrilla 1", guild.roles)
    channel = message.channel
    await channel.send("Hello "+role.mention)

@client.command()
async def start_reminders(context):
    channel = context.message.channel
    await startReminders(channel)

client.run(os.getenv('TOKEN'))