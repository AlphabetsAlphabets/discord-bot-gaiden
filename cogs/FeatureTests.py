import discord
from discord.ext import commands


class FeatureTests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def embed_test(self, ctx):
        # Creates an instance of discord.Embed, and set the title, and description
        embed = discord.Embed(
            title = "Title",
            description = "Description"
        )

        # Stores the emojis that I want
        emojis = ["◀️", "➡️", "✅"]

        message = await ctx.send(embed=embed)
        for emoji in emojis:
            # Reacts to the previously sent message with emojis from the emojis list
            await message.add_reaction(emoji)

    @commands.command()
    async def get_emoji_id(self, ctx):
        channel = ctx.channel

        msg_id = 829226619859763211
        msg = await channel.fetch_message(msg_id)

        print("Getting reactions from latest message.\n")
        reactions = msg.reactions
