import discord
from discord.ext import commands
from discord.ext.commands import context

from typing import List
import time
import shutil

from pytube import YouTube, Stream

class User:
    def __init__(self, ctx: context.Context, url: str):
        self.user_id = ctx.author.id
        self.currently_listening_to = url

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.is_connected = False
        self.voice_protocols = dict()

        """
        The point of self.users is to store which user is currently using the bot. The current song,
        and what songs the user has queued up.
        """
        self.users_listening = dict()

    def audio_only(self, stream):
        mime_type = stream.mime_type

        has_audio_type = mime_type == "audio/webm"
        has_audio = stream.includes_audio_track
        has_no_video = stream.includes_video_track

        is_audio = has_audio_type and has_audio and not has_no_video

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

        # Ubuntu doesn't allow chracters in the following replace methods, to appear in the file name.
        # You cannot have multiple instances of . unless it's to specify the file type, and the bar |
        # cannot appear at all.
        title = stream.title
        title = title.replace(".", "")
        title = title.replace("|", "")

        stream.download(f"streaming/{user_id}", filename = title)

        return title

    @commands.command()
    async def play(self, ctx: context.Context, url: str = None):
        await self.connect(ctx, url)

        title = self.prepare_audio_file(ctx, url)
        
        user_id = ctx.author.id
        user = self.users_listening[user_id]
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
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            await ctx.send("Not playing.")
        else:
            voice.pause()

    @commands.command()
    async def resume(self, ctx):
        """Resumes the audio playback
        ctx: The context in which this command is invoked."""
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
        user_id = ctx.author.id
        voice_protocol = self.voice_protocols[user_id]
        await voice_protocol.disconnect()
        del self.voice_protocols[user_id]

        user_id = ctx.author.id
        if user_id in self.users_listening:
            path = "streaming/" + str(user_id)
            shutil.rmtree(path)

            del self.users_listening[user_id]

