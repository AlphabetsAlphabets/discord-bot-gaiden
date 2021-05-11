import time
import sys
import os

sys.path.append("./module/")

import discord
from discord.ext import commands

import cogs
from cogs.MessageHandler import MessageHandler
from cogs.Engine import Engine
from cogs.FeatureTests import FeatureTests
from cogs.Music import Music

prefix = "<"
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    t0 = time.time()
    print("Gaiden is online!")
    t1 = time.time()
    time_taken = (t1 - t0) * 1000
    print(f"Gaiden took {time_taken}s to startup.")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

try:
    with open("token.txt") as f:
        token = f.readline()
except FileNotFoundError:
    token = os.environ["API_KEY"]

if __name__ == "__main__":
    # Adding cogs
    bot.add_cog(MessageHandler(bot))
    bot.add_cog(Engine(bot))
    bot.add_cog(FeatureTests(bot))
    bot.add_cog(Music(bot))

    # running the bot
    bot.run(token)
    
