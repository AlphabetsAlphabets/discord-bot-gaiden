import discord
from typing import List
from discord.ext import commands

from pytube import YouTube

class User:
    def __init__(self, ctx: discord.commands.Context, stream: pytube.Stream, url: str):
        """ctx: The context at which the command was invoked.
        stream: The audio stream of the song
        url: Url to the video"""

        author = ctx.author
        self.name = author.name 
        self.id = author.id

        self.song = stream.title
        self.song_url = url
        self.queue = None

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        """
        self.users = {"Dex#1234": {"song": "My Way", queue: "Don't stop me now", "I'm still standing"}}
        The point of self.users is to store which user is currently using the bot. The current song,
        and what songs the user has queued up.
        """
        self.users = dict()

    def audio_only(self, stream):
        mime_type = stream.mime_type

        has_audio_type = mime_type == "audio/webm"
        has_audio = stream.includes_audio_track
        has_no_video = !stream.includes_video_track

        is_audio = has_audio_type and has_audio and has_no_video

        if (is_audio):
            return stream


    def hq_kbps(self, stream):
        abr = stream.abr[:-4]
        if int(abr) > 70:
            return stream

    def better_kbps(self, streams: List[pytube.Stream]):
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

    def filter_streams(self, url, streams):
        streams = filter(self.audio_only, streams)
        streams = list(filter(self.hq_kbps, streams))
        if len(streams) > 1:
            stream = self.better_kbps(streams)
        else: 
            stream = streams

        return stream
        

    def add_listener(self, user: User):
        pass

    @commands.command
    async def play(self, ctx, url):
        streams = YouTube(url).streams
        stream = self.filter_streams(url, streams)

        user = User(ctx, stream, url)
        self.users[user.name] = user

        title = stream.title
        # stream.download(f"streaming/{user.name}", filename = f"{title}.mp3")
