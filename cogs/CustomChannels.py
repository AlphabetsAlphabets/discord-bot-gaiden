import discord
from discord.ext import commands

class CustomChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    
    @commands.command(name="room")
    async def room(self, ctx, command, *args):
        commands = ["new", "delete"]
        if command not in commands:
            string = commands.pop(0)
            for command in commands:
                string += f", {command}"

            await ctx.send(f"Valid commands for room are {string}")

        if command == "new":
            name = " ".join(args)
            await self.create_new_room(ctx, name)

            # TODO
            # Assign create and assign a new role to the person who created this
            # room, and allow that person only to make edits to who can and cannot join.

        if command == "delete":
            pass
            

    async def create_new_room(self, ctx, name):
        guild = ctx.guild

        categories = guild.categories
        category_name = ""
        for category in categories:
            if category.name == "Rooms":
                category_name = category
                break

        topic = f"{ctx.author.name} would like to discuss about {name}."
        await guild.create_text_channel(name, topic=topic, category=category_name)
