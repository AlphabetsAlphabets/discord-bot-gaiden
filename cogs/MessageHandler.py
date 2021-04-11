import discord
from discord.ext import commands

class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        invoke = message.content

        if invoke.startswith("reply"):
            # Sending a reply to the user
            text = invoke.split(" ")[1:]
            text = (" ").join(text)

            await message.reply(text)

        if invoke.startswith("gaiden say"):
            # await message.delete()
            text = message.content.split(" ")
            text = text[2:]
            text = " ".join(text) + "."

            channel = message.channel
            await message.delete()
            await channel.send(text)

        if invoke.startswith("<search"):
            await message.delete()
