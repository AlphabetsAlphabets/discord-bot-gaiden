import discord
from typing import List
from discord.ext import commands

from module.consts import EmbedType
from module.type_verification import TypeVerifier

import requests

class Engine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.emojis = ["◀️", "➡️", "✅"]

    def format_embed(self, results: List[dict], embed: discord.Embed) -> discord.Embed:
        """
        Populates the embed with information from the DDG api

        results: An array of JSON response of the api
        embed: The discord embed
        """
        for result in results:
            desc = result["Text"]
            url = result["FirstURL"]

            return_result = (
                f"{desc}\nFor more information checkout the [source]({url})\n"
            )
            embed.add_field(name="===" * 10, value=return_result, inline=False)

        return embed

    async def next_page(self, message: discord.Message, embed: discord.Embed):
        """
        Cycles to the next page in the search result.

        message: The message to delete
        embed: The embed to be sent in place of the previous message.
        """
        channel = message.channel
        await message.delete()

        secondary_page = self.search_pages["secondary page"]
        message = await channel.send(embed=secondary_page)

        prev_arrow = self.emojis[0]
        done = self.emojis[2]

        await message.add_reaction(prev_arrow)
        await message.add_reaction(done)

    async def previous_page(self, message: discord.Message, embed: discord.Embed):
        """
        Cycles to the previous page in the search result.

        message: The message to delete
        embed: The embed to be sent in place of the previous message.
        """
        channel = message.channel
        await message.delete()

        front_page = self.search_pages["front page"]
        message = await channel.send(embed=front_page)

        next_arrow = self.emojis[1]
        done = self.emojis[2]

        await message.add_reaction(next_arrow)
        await message.add_reaction(done)

    def embed_variant(self, embed: discord.Embed) -> EmbedType:
        if "search result" in embed.title.lower():
            return EmbedType.SearchAPI

    async def check_embed_variant(self, message: discord.Message):
        """message: The embed"""

        reactions = message.reactions
        embeds = message.embeds

        variant = ""
        relevant_embed = ""
        for embed in embeds:
            variant = TypeVerifier.embed_variant(embed)
            relevant_embed = embed
            break

        if variant == EmbedType.SearchAPI:
            await self.navigate_search_results(reactions, message, relevant_embed)

        channel = message.channel

    async def navigate_search_results(
        self,
        reactions: List[discord.Reaction],
        message: discord.Message,
        relevant_embed: discord.Embed,
    ):
        """
        Helps to navigate through the search results

        reactions: A list of reactions
        message: the message to delete
        relevant_embed: the embed to be sent in place of the deleted message.
        """
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
                # The 'search result' message is deleted as the search results
                # can get really long, and this is to avoid filling up the screen
                # with search results
                await message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        channel = await self.bot.fetch_channel(channel_id)

        message_id = payload.message_id
        message = await channel.fetch_message(message_id)

        # This check is put in place to make sure that only embeds go through
        # furthermore, the embeds must be a variant of the enum EmbedType
        # this is the avoid confusion between normal embeds, and command generated ones.
        embeds = message.embeds
        if len(embeds) != 0 or embeds != None:
            await self.check_embed_variant(message)

    @commands.command(name="search")
    async def instant_answers_api(self, ctx, *args):
        """The main feature of this cog. The search function, powered by the DuckDuckGo InstantAnswerAPI"""
        message = ctx.message
        # Text is the text content that invoked this commands
        text = message.content

        # The person who invoked the commands
        author = ctx.author.name
        self.search_pages = dict()

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

        front_page = discord.Embed(
            title=f"{author}'s search result for '{search_query}'",
            description=data["Abstract"],
        )

        data = data["RelatedTopics"][:10]

        # I only want results with the "Text" key in them
        results = []
        for result in data:
            for key in result.keys():
                if "Text" not in key and "Abstract" not in key:
                    continue

                results.append(result)

        # create the embed from the results taken by the API response of ddg's
        # instant answer api
        midpoint = round(len(results) / 2)
        front_page = self.format_embed(results[:midpoint], front_page)

        self.search_pages["front page"] = front_page

        secondary_page = discord.Embed(title="Search result: second page")
        secondary_page = self.format_embed(results[midpoint:], secondary_page)
        self.search_pages["secondary page"] = secondary_page

        message = await ctx.send(embed=front_page)

        next_arrow = self.emojis[1]
        done = self.emojis[2]

        await message.add_reaction(next_arrow)
        await message.add_reaction(done)

