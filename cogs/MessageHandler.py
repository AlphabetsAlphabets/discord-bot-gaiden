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

        message_content = message.content.lower()

        if message_content.startswith("gaiden say"):
            # await message.delete()
            text = message.message_content.split(" ")
            text = text[2:]
            text = " ".join(text)

            channel = message.channel
            await message.delete()
            await channel.send(text)

        if self.git:
            key_word_in_message = ("help" in message_content or "i suck" in invoke)
            length_of_message = len(message_content)

            if key_word_in_message and length_of_message > 50:
                await message.reply("Lmao git gud")

    @commands.command()
    async def toggle_git(self, ctx):
        message = ctx.message.content.lower()
        message = message.split(" ")[-1]
        
        if message == "disable":
            self.git = False
        else:
            self.git = True
