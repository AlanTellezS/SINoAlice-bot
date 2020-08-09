import discord
import os
import asyncio
from enum import Enum
from common_embed import generic_embed
from datetime import datetime
from discord.ext import commands
import mysql.connector as mysql

client = commands.Bot(command_prefix = "+")

db = {
    'user': os.getenv('db_user'),
    'dbName': os.getenv('db_name'),
    'password': os.getenv('db_pass'),
    'host': os.getenv('db_host'),
    'port': os.getenv('db_port')
}

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
    print("Remind started")
    while True:
        found = False
        time = datetime.utcnow()
        await checkRemind(channel, found, time, guild)

async def checkRemind(channel, found, time, guild):
    for listener in listeners:
        if (found): break
        for t in listener['times']:
            if (t['time'].minute == time.minute and t['time'].hour == time.hour and t['time'].second == time.second):
                role = discord.utils.find(lambda r : r.name == t['role'], guild.roles)
                await channel.send(role.mention+" has started")
    await asyncio.sleep(1)

@client.event
async def on_ready():
    print("Ygdrasil bot started")
    print("--------------------")
    for channel in client.guilds[0].channels:
        if channel.name == "bot":
            botChannel = channel
    await startReminders(botChannel)

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

@client.command(aliases = ["cq", "createquote", "cquote"])
async def createq(context, quotename=None, quote=None):
    if(quotename==None): await context.send("No arguments given")
    elif(quote==None): await context.send("No quote given")
    else:
        con = mysql.connect(user = db['user'], password = db['password'], host = db['host'], database = db['dbName'], port = db['port'])
        query = f'INSERT INTO quotes(name, quote, user) VALUES ("{quotename}","{quote}","{context.author.name}")'
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
        await context.send(f"Quote {quotename} added!")

@client.command(aliases = ["q"])
async def quote(context, quotename=None):
    if quotename == None: await context.send("No quote name given")
    else:
        channel = context.channel
        con = mysql.connect(user = db['user'], password = db['password'], host = db['host'], database = db['dbName'], port = db['port'])
        cursor = con.cursor()
        query = f'select name, quote from quotes where name = "{quotename}"'
        cursor.execute(query)
        result = cursor.fetchall()
        if (len(result)==0):
            await channel.send( f"Quote {quotename} not found")
        else:
            await channel.send(result[0][1])

@client.command(aliases = ["dq"])
async def delete_quote(context, quotename=None):
    if quotename == None: await context.send("No quote name given")
    else:
        con = mysql.connect(user = db['user'], password = db['password'], host = db['host'], database = db['dbName'], port = db['port'])
        cursor = con.cursor()
        query = f'delete from quotes where name = {quotename} and user = {context.author.name}'
        cursor.execute(query)
        if cursor.rowcount() == 0: await context.send(f"Quote {quotename} by user {context.author.name} doesn't exists")
        else: context.send(f'Quote deleted')

@client.command(aliases = ["lq", "listquotes", "lquotes", "qlist"])
async def list_quotes(context):
    channel = context.channel
    msg = ""
    con = mysql.connect(user = db['user'], password = db['password'], host = db['host'], database = db['dbName'], port = db['port'])
    cursor = con.cursor()
    query = f'select name, user from quotes'
    cursor.execute(query)
    result = cursor.fetchall()
    for name, user in result:
        msg = msg + f'{name} by {user}\n'
    await channel.send(embed = generic_embed("List of quotes", msg, "", ""))

@client.command()
async def t(message,arg1,arg2):
    print (f'arg1 {arg1}')
    print (f'arg2 {arg2}')

client.run(os.getenv('TOKEN'))