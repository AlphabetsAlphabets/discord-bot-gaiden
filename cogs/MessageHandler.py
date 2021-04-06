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
            if message.author.name != "Dex":
                await message.reply("Lol fuck off.")
                return

            # Sending a reply to the user
            await message.reply("replied")

        if invoke.startswith("gaiden say"):
            # await message.delete()
            text = message.content.split(" ")
            text = text[2:]
            text = " ".join(text) + "."

            channel = message.channel
            await channel.send(text)
