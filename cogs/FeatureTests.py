import discord
from discord.ext import commands


class FeatureTests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def embed_test(self, ctx):
        embed = discord.Embed(
            title = "Title",
            description = "Description"
        )

        emoji = "✅"

        for e in ctx.guild.emojis:
            print(e.name)
            print(e.id)
            print()

        emojis = ["◀️", "➡️", "✅"]

        message = await ctx.send(embed=embed)
        for emoji in emojis:
            await message.add_reaction(emoji)

    @commands.command()
    async def get_emoji_id(self, ctx):
        channel = ctx.channel

        msg_id = 829226619859763211
        msg = await channel.fetch_message(msg_id)

        print("Getting reactions from latest message.\n")
        reactions = msg.reactions
