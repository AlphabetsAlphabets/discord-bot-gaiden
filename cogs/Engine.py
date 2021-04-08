import discord
from typing import List
from discord.ext import commands

import requests

class Engine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.emojis = ["◀️", "➡️", "✅"]

    async def next_page(self, message: discord.Message, embed: discord.Embed):
        channel = message.channel
        await message.delete()

        secondary_page = self.search_pages["secondary page"]
        message = await channel.send(embed=secondary_page)

        prev_arrow = self.emojis[0]
        done = self.emojis[2]

        await message.add_reaction(prev_arrow)
        await message.add_reaction(done)

    async def previous_page(self, message: discord.Message, embed: discord.Embed):
        channel = message.channel
        await message.delete()

        front_page = self.search_pages["front page"]
        message = await channel.send(embed=front_page)

        next_arrow = self.emojis[1]
        done = self.emojis[2]

        await message.add_reaction(next_arrow)
        await message.add_reaction(done)

    def embed_type(self, embed: discord.Embed) -> str: 
        if "search result" in embed.title.lower():
            return "search result"

    async def navigation(self, message: discord.Message):
        """message: The embed"""

        reactions = message.reactions 
        # The bot adds it's own reactions which also triggers this function.
        # This is to prevent an IndexError
        embeds = message.embeds

        variant = ""
        relevant_embed = ""
        for embed in embeds:
            variant = self.embed_type(embed)
            relevant_embed = embed
            break


        channel = message.channel 
        if variant == "search result":
            for reaction in reactions:
                count = reaction.count
                if count < 2:
                    continue

                emoji = reaction.emoji

                # left
                if emoji == self.emojis[0]:
                    await self.previous_page(message, relevant_embed)

                # right
                if emoji == self.emojis[1]:
                    await self.next_page(message, relevant_embed)

                # remove
                if emoji == self.emojis[2]:
                    # Where `done` is the check mark emoji if there is 2 or more of them,
                    # it'll delete the message because, well the person has finished looking at them.
                    await message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        channel = await self.bot.fetch_channel(channel_id)

        message_id = payload.message_id
        message = await channel.fetch_message(message_id)
        embeds = message.embeds
        if len(embeds) != 0:
            title = embeds[0].title.lower()
            if "search" in title or "second page" in title:
                await self.navigation(message)


    @commands.command(name='search')
    async def instant_answers_api(self, ctx, *args):
        text = ctx.message.content
        author = ctx.author.name

        # split it by spaces then take the list starting from the first index,
        # because the 0th index is the command itself
        search_query = text.split(" ")[1:]
        search_query = (" ").join(search_query)

        uri = f"https://api.duckduckgo.com/{search_query}?q=&format=json" 

        response = requests.get(uri)
        data = response.json()

        # Sometimes the key "Abstract" isn't just a blank string, if it is, then
        # the embed's description is blank, if it isn't then the description will be
        # the content behind the key "Abstract"
        embed_desc = ""

        self.search_pages = dict()

        front_page = discord.Embed(
                title = f"{author}'s search result for '{search_query}'",
                description = data["Abstract"]
        )

        data = data["RelatedTopics"][:10]

        # I only want results with the "Text" key in them
        results = []
        for result in data:
            for key in result.keys():
                if "Text" not in key and "Abstract" not in key:
                    continue

                results.append(result)
        
        # create the embed from the results taken by the API response of ddg's instant answer api
        midpoint = round(len(results) / 2)
        front_page = self.format_embed(results[:midpoint], front_page)

        self.search_pages["front page"] = front_page

        secondary_page = discord.Embed(title = "Search result: second page")
        secondary_page = self.format_embed(results[midpoint:], secondary_page)
        self.search_pages["secondary page"] = secondary_page


        message = await ctx.send(embed=front_page)

        next_arrow = self.emojis[1]
        done = self.emojis[2]

        await message.add_reaction(next_arrow)
        await message.add_reaction(done)

    def format_embed(self, results: List[dict], embed: discord.Embed) -> discord.Embed:
        """
        Populates the embed with information from the DDG api

        results: An array of JSON response of the api
        embed: The discord embed
        """
        for result in results:
            desc = result["Text"]
            url = result["FirstURL"]

            return_result = f"{desc}\nFor more information checkout the [source]({url})\n"
            embed.add_field(name="==="*10, value=return_result, inline=False)

        return embed
