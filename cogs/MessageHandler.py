import discord
from discord.ext import commands

class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.git = True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        invoke = message.content.lower()

        if invoke.startswith("gaiden say"):
            # await message.delete()
            text = message.content.split(" ")
            text = text[2:]
            text = " ".join(text) + "."

            channel = message.channel
            await message.delete()
            await channel.send(text)

        if self.git:
            if "help" in invoke or "i suck" in invoke:
                await message.reply("Lmao git gud")

    @commands.command()
    async def toggle_git(self, ctx):
        if ctx.content.lower() == "disable":
            self.git = False
            return

        self.git = True
