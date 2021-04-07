import discord
from discord.ext import commands

import requests

class Engine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='search')
    async def instant_answers_api(self, ctx, *args):
        # The message content
        text = ctx.message.content

        # split it by spaces then take the list starting from the first index,
        # because the 0th index is the command itself
        search_query = text.split(" ")[1:]
        search_query = (" ").join(search_query)

        # Replaces all spaces with %20 since spaces are represented that way
        # in a url
        search_query = search_query.replace(" ", "%20") 

        uri = f"https://api.duckduckgo.com/{search_query}?q=&format=json"

        # Make a request, and get the data behind the key RelatedTopics
        response = requests.get(uri)
        data = response.json()["RelatedTopics"]

        # Keeps the max amount of results to 8
        barrier = 4 

        # If there are more than 8 results, then it'll remove everything else
        # after the 8th index position
        if barrier > len(data):
            data = data[:barrier]

        # I only want results with the "Text" key in them

        map(remove_text, data))

        results = []
        for result in data:
            for key in result.keys():
                if "Text" not in key:
                    continue

                results.append(result)
        
        embed = discord.Embed(title = f"You searched for '{search_query}'")

        embed.set_author(name=ctx.author.name)

        for count, result in enumerate(results, start=1):
            # Extracting the text description, and url
            desc = result["Text"]
            url = result["FirstURL"]

            # Setting up the output text
            return_result = f"{desc}\nFor more information checkout: {url}\n"
            embed.add_field(name=f"Result {count}", value=return_result, inline=False)
 
        # Emoji detection
        await ctx.send(embed=embed)

    @staticmethod
    def remove_text(data: dict):
        value, key = data.items()
        if "Text" in key:
            return data
