import discord
from discord.ext import commands

class CustomChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command(name="room")
    async def room(self, ctx, command, *args):
        args = list(args)
        commands = ["new", "delete"]
        if command not in commands:
            string = commands.pop(0)
            for command in commands:
                string += f", {command}"

            await ctx.reply(f"Valid commands for room are {string}")
            return

        if command == "new":
            # TODO
            # Assign create and assign a new role to the person who created this
            # room, and allow that person only to make edits to who can and cannot join.
            make_private = False
            if args[-1].lower() == "true":
                make_private = bool(args.pop(-1))

            if args[-1].lower() == "false":
                make_private = False

            name = " ".join(args)
            channel = await self.create_new_room(ctx, name)
            role = await self.make_room_owner(ctx, channel)

            if make_private:
                # Make `channel` visible to only users with role `role`
                pass

        if command == "delete":
            can_delete = False
            for role in ctx.author.roles:
                if ctx.author.name in role.name:
                    await role.delete()
                    can_delete = True
                    break

            if can_delete:
                await ctx.channel.delete(reason=f"{ctx.author.name}'s discussion has ended.")

            else: 
                await ctx.reply("You are not the owner of this room.")

    async def create_new_room(self, ctx, name):
        category = ""
        for category in ctx.guild.categories:
            if category.name == "Rooms":
                category_name = category
                break

        topic = f"{ctx.author.name} would like to discuss about {name}."
        channel = await ctx.guild.create_text_channel(name, topic=topic, category=category)
        return channel

    async def make_room_owner(self, ctx, channel):
        owner = ctx.author.name
        reason = channel.topic
        role = await ctx.guild.create_role(name=f"Room for {owner}", reason=reason)

        await ctx.author.add_roles(role, reason=reason)
        return role
