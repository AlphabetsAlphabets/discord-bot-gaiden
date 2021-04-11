import discord
from discord.ext import commands
from discord.ext.commands import context

from typing import List
import time
import shutil

from pytube import YouTube, Stream

class User:
    def __init__(self, ctx: context.Context, stream: Stream, url: str):
        """ctx: The context at which the command was invoked.
        stream: The audio stream of the song
        url: Url to the video"""

        author = ctx.author
        self.id = author.id

        self.current_song = stream.title
        self.song_url = url
        self.path = f"streaming/{author.id}"


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.connected = False

        """
        The point of self.users is to store which user is currently using the bot. The current song,
        and what songs the user has queued up.
        """
        self.users = dict()
        print(len(self.users))

    def audio_only(self, stream):
        mime_type = stream.mime_type

        has_audio_type = mime_type == "audio/webm"
        has_audio = stream.includes_audio_track
        has_no_video = stream.includes_video_track

        is_audio = has_audio_type and has_audio and not has_no_video

        if (is_audio):
            return stream


    def hq_kbps(self, stream):
        abr = stream.abr[:-4]
        if int(abr) > 70:
            return stream

    def better_kbps(self, streams: List[Stream]):
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
        streams = list(filter(self.hq_kbps, streams))
        if len(streams) > 1:
            stream = self.better_kbps(streams)
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

        user = User(ctx, stream, url)
        self.users[user.id] = user

        title = stream.title
        title = title.replace(".", "")
        title = title.replace("|", "")

        self.users[user.id] = user
        stream.download(f"streaming/{user.id}", filename = title)

        return title

    @commands.command()
    async def play(self, ctx: context.Context, url: str = None):
        user_id = ctx.author.id
        if user_id in self.users:
            user = self.users[user_id]
            if user.song_url == url:
                await ctx.reply("That song is already playing.")
                return

        if url is None:
            url = "https://www.youtube.com/watch?v=ylwckvS0YHw"

        title = self.prepare_audio_file(ctx, url)

        # Among Us Medley  Super Smash Bros Ultimate.webm
        # Among Us Medley  Super Smash Bros. Ultimate.webm

        user = self.users[user_id]
        path = user.path + f"/{title}.webm"

        voice_client = self.bot.voice_clients[0]
        audio = discord.FFmpegPCMAudio(path)
        voice_client.play(audio)

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            await ctx.send("Not playing.")
        else:
            voice.pause()

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Not paused.")


    @commands.command(name="connect")
    async def connect_test(self, ctx: context.Context, voice_channel):
        """use this function to test if the bot can connect a vc"""
        if self.connected:
            await ctx.reply("Sorry, but Gaiden is already connected to another voice channel.")

        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=voice_channel)
        voice_protocol = await voice_channel.connect()
        self.connected = True

    @commands.command(name="dc")
    async def disconnect(self, ctx: context.Context):
        self.connected = False
        voice_client = self.bot.voice_clients[0]
        await voice_client.disconnect()

        user_id = ctx.author.id
        if False:
            if user_id in self.users:
                path = "streaming/" + user_id
                shutil.rmtree(path)


