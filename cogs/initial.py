#Discord Imports
import discord
from discord.ext import commands

#MISC Imports
import asyncio


def setup( client ):
    client.add_cog( initial(client) )


class initial( commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('BOT is running.')

    @commands.command()
    async def load(self, ctx, extension):
        client = self.client
        client.load_extension( f'cogs.{extension}')
        print(f'Loading {extension}')

    @commands.command()
    async def unload(self, ctx, extension):
        client = self.client
        client.unload_extension( f'cogs.{extension}')
        print(f'Unloading {extension}')

