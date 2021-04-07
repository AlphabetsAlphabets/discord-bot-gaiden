import time

import discord
from discord.ext import commands

import cogs
from cogs.MessageHandler import MessageHandler
from cogs.Engine import Engine
from cogs.FeatureTests import FeatureTests

prefix = "<"
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    t0 = time.time()
    print("Gaiden is online!")
    t1 = time.time()
    print(f"Gaiden took {t0-t1}s to startup.")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

with open("token.txt") as f:
    token = f.readline()

if __name__ == "__main__":
    # Adding cogs
    bot.add_cog(MessageHandler(bot))
    bot.add_cog(Engine(bot))
    bot.add_cog(FeatureTests(bot))

    # running the bot
    bot.run(token)
