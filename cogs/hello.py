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

            # Sending message to the channel
            # await message.channel.send(f"You wrote {content}")

            # Sending a reply to the user
            await message.reply("replied")

        if invoke.startswith("gaiden say"):
            # await message.delete()
            text = message.content.split(" ")
            text = text[2:]
            text = " ".join(text) + "."

            channel = message.channel
            await channel.send(text)

        await self.bot.process_commands(message)

    @commands.command(name='check')
    async def check_permissions(self, ctx):
        for channel in self.bot.get_all_channels():
            member = ctx.author
            perms = member.permissions_in(channel)
            
            print(perms.connect)
            break




            
