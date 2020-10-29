# Built-in packages
import random
import os, sys

# Web related
import requests
import json

# Discord
import discord
from discord.ext import commands

# Bot & Owner setup: prefix, who is the owner, etc.
prefix = "g."
bot = commands.Bot(command_prefix=prefix)
owner = 'å¶å®¶ç…Œ(Jia Hong)#8464' # The text is messed up because part of my discord username is in chinese. 

channelPath = os.getcwd() + "\\tokens & APIs\\channels.txt"
tokenPath = os.getcwd() + "\\tokens & APIs\\tokens.txt"

# Start up
@bot.event
async def on_ready():
    print()
    print(f"{bot.user} has connected to Discord!")
    print("-" * 20)
    print("\n")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=prefix))

# Welcome/Leave system
channels = []
with open(channelPath) as f:
    for line in f.readlines():
        channels.append(line.strip("\n"))

bot_pit = channels[1]
general = channels[4]
welcome = channels[7]

@bot.event
async def on_member_join(member):
    thumbnail = member.avatar_url
    channel = member.guild.get_channel(welcome)

    EMBED = discord.Embed(
        title='A new member has joined!'
    )

    EMBED.set_thumbnail(url=thumbnail)
    EMBED.add_field(
        name="Welcome!",
        value=f"Welcome {member.mention}, we hope you enjoy your stay here, at {member.guild}!",
        inline=True
    )

    EMBED.add_field(
        name='Things you should do first.',
        value="You should go ahead and check out <#719416884876935228>. If you don't, nothing will happen, however, if you are penalized for something it will be your fault.",
        inline=True
    )

    await channel.send(embed=EMBED)

@bot.event
async def on_member_remove(member):
    thumbnail = member.avatar_url
    channel = member.guild.get_channel(welcome)

    EMBED = discord.Embed(
        title='A traitor amongst our midst!'
    )

    EMBED.set_thumbnail(url=thumbnail)

    EMBED.add_field(
        name="Traitor! Don't come back!",
        value=f"{member.mention} has left {member.guild}. Traitor.",
        inline=True
    )

    await channel.send(embed=EMBED)

# CSE API (Google)
tokens = []
with open(tokenPath) as f:
    for line in f.readlines():
        tokens.append(line.strip("\n"))

token = tokens[0]
EngineAPI = tokens[-1]
EngineID = tokens[-2]

@bot.command()
async def ddg(ctx, *args):
    EMBED = discord.Embed(
        title = 'Your search result'
        )

    titles = []
    links = []
    snippets = []

    query = list(args)
    query = "+".join(query)
    url = f"https://www.googleapis.com/customsearch/v1?key={EngineAPI}&cx={EngineID}&q={query}&start=1"
    r = requests.get(url).json()

    items = r['items']
    for item in r['items']:
        title = item['title']
        link = item['link']
        snippet = item['snippet']

        titles.append(title)
        links.append(link)
        snippets.append(snippet)

    EMBED.add_field(
        name=titles[0],
        value=f"{snippets[0]}\nIf you wish to know more visit the [source]({links[0]})",
        inline=False
        )

    EMBED.add_field(
        name=titles[1],
        value=f"{snippets[1]}\nIf you wish to know more visit the [source]({links[1]})",
        inline=False
        )

    EMBED.add_field(
        name=titles[2],
        value=f"{snippets[2]}\nIf you wish to know more visit the [source]({links[2]})",
        inline=False
        )

    await ctx.send(embed=EMBED)
# Chat bot
annoying = [
    'Is it now?', 'Nope', 'Not really', 'I say not', 'lol git gud', 'Naaaa'
]

query = ['Yes that is correct.', f"""I agree with which was last said""", "That's correct",
         "I'm not sure, you tell me.", "Oh please you're smarter than that.", "Figure it out.",
         "I'm not google.", "You think I know everything?",
         "I'm not going to say it, now that you want me to say it.",
         "lol good luck figuring it out on your own", "why would I know.",
         "Sure. If that's what you wanna think."]

what_is = [
    "I'm not sure, you tell me.", "Oh please you're smarter than that.",
    "Figure it out.", "I'm not google.", "You think I know everything?",
    "I'm not going to say it, now that you want me to say it.",
    "lol good luck figuring it out on your own",
    "why would I know.", "Sure. If that's what you wanna think."
]

# Chat bot
bot_name = 'gaiden'

@bot.event
async def on_message(message):
    varA = 0
    count = 0
    if message.author == bot.user:
        return

    elif f"isn't that right {bot_name}" in message.content.lower() or f"what do you think {bot_name}" in message.content.lower():
        await message.channel.send(random.choice(query))

    elif f'{bot_name} is' in message.content.lower() or f'{bot_name} what' in message.content.lower():
        await message.channel.send(random.choice(what_is))

    elif f'{bot_name} why' in message.content.lower() or f'{bot_name} will' in message.content.lower():
        await message.channel.send(random.choice(what_is))

    elif f'{bot_name} who' in message.content.lower():
        await message.channel.send(random.choice(what_is))

    elif 'bitch please' in message.content.lower():
        await message.channel.send("Nuh ah, don't bitch please me.")

    elif varA >= 30:
        await message.channel.send(random.choice(annoying))
        varA = 0

    varA += 1
    await bot.process_commands(message)

# Administrator commands
@bot.command()
async def test(ctx):
    await ctx.send("This bot is working")

bot.run(token)
