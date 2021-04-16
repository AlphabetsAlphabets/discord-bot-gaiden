import discord
from discord.ext.commands import context

from enum import Enum

class EmbedType(Enum):
    SearchAPI = 1
    MusicControl = 2

class User:
    """The user class is used to store a variety of information that can help
    identify a user's current status, guild, and specific voice channel he/she is
    in."""
    def __init__(self, ctx: context.Context, url: str,
            message: discord.Message = None, embed: discord.Embed = None):

        # Storing the user information of the user who invoked a command, and 
        # which guild it is called from
        self.user_id = ctx.author.id
        self.name = ctx.author.name
        self.guild_id = ctx.guild.id
        self.voice_channel_id = ctx.author.voice.channel.id

        # Audio playback related settings
        self.currently_listening_to = url
        self.song_title = ""

        self.message = message
        self.embed = embed


        
