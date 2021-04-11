import discord
from typing import List
from discord.ext import commands

from discord.ext.commands import context

import pytube
from pytube import YouTube

class User:
    def __init__(self, ctx: context.Context, stream: pytube.Stream, url: str):
        """ctx: The context at which the command was invoked.
        stream: The audio stream of the song
        url: Url to the video"""

        author = ctx.author
        self.id = author.id

        self.song = stream.title
        self.song_url = url
        self.queue = None

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

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

    def better_kbps(self, streams: List[pytube.Stream]):
        """Filter a list of streams to find the stream with the highest audio quality.
        streams: A list of `pytube.Stream`."""
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

    def filter_streams(self, url: str, streams: List[pytube.Stream]) -> pytube.Stream:
        """filters `pytube.Stream` with helper functions to find the highest quality
        of streams

        url: The url to the song,
        streams: A list of `pytube.Stream`"""
        streams = filter(self.audio_only, streams)
        streams = list(filter(self.hq_kbps, streams))
        if len(streams) > 1:
            stream = self.better_kbps(streams)
        else: 
            stream = streams

        return stream[0]

    def prepare_audio_file(self, ctx: context.Context, url: str):
        """Prepares the audio file, by filtering streams, and downloading the one with
        highest quality, then making a folder for each user.

        ctx: The context in which this command was invoked
        url: Url to the song."""
        streams = YouTube(url).streams
        stream = self.filter_streams(url, streams)

        user = User(ctx, stream, url)
        self.users[user.id] = user

        title = stream.title
        self.users[user.id] = user
        stream.download(f"streaming/{user.id}", filename = f"{title}.mp3")
        print("Download complete.")


    @command.commands()
    async def play(self, ctx: context.Context, url: str):
        self.prepare_audio_file(ctx, url)
