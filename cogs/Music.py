import discord
from discord.ext import commands
from discord.ext.commands import context

import module
from module.consts import EmbedType
from module.consts import User
from module.type_verification import TypeVerifier

from typing import List
import time
import shutil

from pytube import YouTube, Stream

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        """
        Keeps track of each user's voice protocol, so when they call a function to 
        disconnect from it, it won't cause gaiden to disconnect across all vc's he is 
        currently connected to.
        """
        self.voice_protocols = dict()
        self.emojis = {"play_pause": "⏯️", "stop": "🚫", "leave": "👋"}

        """
        The point of self.users_listening is to store and keep track of which
        user is currently using the bot.
        """
        self.users_listening = dict()

    def audio_only(self, stream):
        mime_type = stream.mime_type

        has_audio_type = mime_type == "audio/webm"
        has_audio = stream.includes_audio_track
        has_video = stream.includes_video_track

        is_audio = has_audio_type and has_audio and not has_video

        if (is_audio):
            return stream

    def get_kbps_over_70(self, stream):
        abr = stream.abr[:-4]
        if int(abr) > 70:
            return stream

    def get_best_kbps(self, streams: List[Stream]):
        """Filter a list of streams to find the stream with the highest audio quality.
        streams: A list of `Stream`."""
        current = None
        previous = None
        highest_abr = None

        for stream in streams:
            if previous is None:
                previous = stream
                continue

            current = stream
            current_abr = int(current.abr[:-4])
            previous_abr = int(previous.abr[:-4])

            if current_abr > previous_abr:
                highest_abr = current
            else:
                highest_abr = previous

        return highest_abr

    def filter_streams(self, url: str, streams: List[Stream]) -> Stream:
        """filters `Stream` with helper functions to find the highest quality
        of streams

        url: The url to the song,
        streams: A list of `Stream`"""

        streams = filter(self.audio_only, streams)
        streams = list(filter(self.get_kbps_over_70, streams))
        if len(streams) > 1:
            stream = self.get_best_kbps(streams)
        else: 
            stream = streams

        return stream[0]

    def prepare_audio_file(self, ctx: context.Context, url: str) -> str:
        """Prepares the audio file, by filtering streams, and downloading the one with
        highest quality, then making a folder for each user.

        ctx: The context in which this command was invoked
        url: Url to the song."""
        streams = YouTube(url).streams
        stream = self.filter_streams(url, streams)

        user_id = ctx.author.id

        # All replace calls are because those characters are not allowed in the
        # file names on Ubuntu
        title = stream.title
        title = title.replace(".", "")
        title = title.replace("|", "")
        title = title.replace("\"", "")

        stream.download(f"streaming/{user_id}", filename = title)

        return title

    @commands.command()
    async def play(self, ctx: context.Context, url: str = None):
        """It first connects to the voice channel, the caller is in, prepares an audio file
        then starts audio playback."""
        await self.connect(ctx, url)

        title = self.prepare_audio_file(ctx, url)
        
        user_id = ctx.author.id
        user = self.users_listening[user_id]
        user.song_title = title
        path = f"streaming/{user_id}/{title}.webm"

        # There is only one voice client anyways to just get the first one.
        voice_client = self.bot.voice_clients[0]
        try:
            audio = discord.FFmpegPCMAudio(path)
            voice_client.play(audio)
        except discord.opus.OpusNotLoaded as onlEx:
            msg = "Sorry but this command is currently unavailable, because FFmpeg is not available. DM/ping Aurelius#6698 with this exact message."
            await ctx.reply(msg)

    @commands.command()
    async def pause(self, ctx: context.Context):
        """Pauses the audio playback
        ctx: The context in which this command is invoked."""

        # TODO: Make this part of an embed system
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Not playing.")

    @commands.command()
    async def resume(self, ctx):
        """Resumes the audio playback
        ctx: The context in which this command is invoked."""

        # TODO: Make this part of an embed system
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Not paused.")


    async def connect(self, ctx: context.Context, url: str):
        """use this function to test if the bot can connect a vc"""
        # TODO: Find a way to add a check, to make sure you can use this in multiple servers
        voice_channel = ctx.author.voice.channel
        try:
            voice_protocol = await voice_channel.connect()
            self.voice_protocols[ctx.author.id] = voice_protocol

        except discord.ClientException:
            voice_protocol = self.voice_protocols[ctx.author.name]
            await voice_protocol.disconnect()

            voice_protocol = await voice_channel.connect()
            self.voice_protocols[ctx.author.id] = voice_protocol

        user = User(ctx, url)
        self.users_listening[ctx.author.id] = user

    @commands.command(name="dc")
    async def disconnect(self, ctx: context.Context):
        """Disconnects from the voice chat, and clears the audio streaming cache for the current user"""

        # TODO: Make clearing the cache song specfic, and a few seconds right after the song stops output.
        # TODO: Make this part of an embed system
        user_id = ctx.author.id
        if user_id not in self.voice_protocols:
            ctx.reply("You aren't in a voice channel.")
            return

        voice_protocol = self.voice_protocols[user_id]
        await voice_protocol.disconnect()
        del self.voice_protocols[user_id]

        user_id = ctx.author.id
        if user_id in self.users_listening:
            path = "streaming/" + str(user_id)
            shutil.rmtree(path)

            del self.users_listening[user_id]

