import discord

import module
from module.consts import EmbedType
from module.consts import User

class TypeVerifier:
    @staticmethod
    def embed_variant(embed: discord.Embed) -> EmbedType: 
        if "currently listening to" in embed.title.lower():
            return EmbedType.MusicControl

        elif "search result" in embed.title.lower():
            return EmbedType.SearchAPI

    @staticmethod
    async def check_embed_variant(message: discord.Message, user: User):
        reactions = user.message.reactions 
        embeds = user.message.embeds

        variant = ""
        relevant_embed = ""
        for embed in embeds:
            variant = self.embed_variant(embed)
            relevant_embed = embed
            break

        if variant == EmbedType.MusicControl:
            await self.music_control(reactions, message, relevant_embed)

