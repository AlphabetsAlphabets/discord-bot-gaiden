import discord
from discord.ext.commands import context

from enum import Enum

class EmbedType(Enum):
    SearchAPI = 1
    MusicControl = 2

class User:
    def __init__(self, ctx: context.Context, url: str,
            message: discord.Message = None, embed: discord.Embed = None):
        self.user_id = ctx.author.id
        self.currently_listening_to = url
        self.song_title = ""

        self.message = message
        self.embed = embed
