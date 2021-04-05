import discord
import time
from discord.ext import commands


class Gaiden(discord.Client):
    def __init__(self):
        self.prefix = "g."
        self.bot = commands.Bot(command_prefix=self.prefix)
        super().__init__()

    async def on_ready(self):
        t0 = time.time()
        print("Gaiden is online!")
        t1 = time.time()
        print(f"Gaiden took {t0-t1}s to startup.")

    async def on_message(self, message):
        if message.author == self.user:
            return

        invoke = message.content

        if invoke.startswith("reply"):
            if message.author.display_name != "Dex":
                await message.reply("lol fuck off.")
                return

            # Sending message to the channel
            # await message.channel.send(f"You wrote {content}")

            # Sending a reply to the user
            await message.reply("replied")

        if invoke.startswith("channels"):
            print("Someone said 'channels'")
            # channels = self.get_all_channels()
            for channel in self.get_all_channels():
                perms = message.author.permissions_in(channel)
                print(perms)
                print(type(perms))


with open("token.txt") as f:
    token = f.readline()


gaiden = Gaiden()
gaiden.run(token)
