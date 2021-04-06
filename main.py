import time

import discord
from discord.ext import commands

import cogs
from cogs.hello import MessageHandler

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

@bot.command()
async def say(ctx, *args):
    words = list(args)
    words = " ".join(words) + "."

    await ctx.send(words)

with open("token.txt") as f:
    token = f.readline()

if __name__ == "__main__":
    bot.add_cog(MessageHandler(bot))
    bot.run(token)
