import discord
from typing import List
from discord.ext import commands

import requests

class Engine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.emojis = ["◀️", "➡️", "✅"]

    def structure_embed(self, embed: discord.Embed, result: List[dict], stop: int):
        for count, result in enumerate(results[:stop], start = 1):
            desc = result["Text"]
            url = result["FirstURL"]

            # Setting up the output text
            return_result = f"{desc}\nFor more information checkout the [source]({url})\n"
            embed.add_field(value=return_result, inline=False)

        return embed

    async def search(self, message: discord.Message):
        reactions = message.reactions

        # The bot adds it's own reactions which also triggers this function.
        # This is to prevent an IndexError
        if len(reactions) >= 3:
            view_previous = reactions[0]
            view_next = reactions[1]
            done = reactions[2]

            if view_next.count == 2:
                channel = message.channel
                await message.delete()

                mid_page = self.search_pages["mid_embed"]
                await channel.send(embed=mid_page)

            if view_previous.count == 2:
                author = message.author
                channel = message.channel

                await message.delete()

                await channel.send(embed=embed)

            if done.count == 2:
                await message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        channel = await self.bot.fetch_channel(channel_id)

        message_id = payload.message_id
        message = await channel.fetch_message(message_id)
        embeds = message.embeds
        if len(embeds) != 0:
            title = embeds[0].title
            if "search" in title.lower():
                await self.search(message)


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

        abstract_desc = data["Abstract"]
        if abstract_desc != "":
            embed_desc = abstract_desc

            front_embed = discord.Embed(
                    title = f"{author}'s search result(s) for '{search_query}'",
                    description=embed_desc
            )

            search_results.append(font_embed)

        data = data["RelatedTopics"][:10]

        # I only want results with the "Text" key in them
        results = []
        for result in data:
            for key in result.keys():
                if "Text" not in key:
                    continue

                results.append(result)
        

        mid_embed = discord.Embed(title = "Page two")

        final_embed = discord.Embed(title = "Page three")

        midpoint = len(results)
        mid_embed = self.structure_embed(mid_embed, results, midpoint)
        final_embed = self.structure_embed(final_embed, results, len(results) - midpoint)

        self.search_pages["mid_embed"] = mid_embed
        self.search_pages["final_embed"] = final_embed

        message = await ctx.send(embed=embed)
        for emoji in self.emojis:
            await message.add_reaction(emoji)
