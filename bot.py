#Importing Discord 
import discord
from discord.ext import commands
from discord.utils import get

#Importing OsuAPI Python Wrapper
import asyncio
from pyosu import OsuApi

#Importing MAL Py Wrapper
from jikanpy import Jikan

#Misc Imports
import json
import pprint
import random
import youtube_dl
import os
import shutil

#Config File Usage
with open( 'config.json') as config_file:
    config = json.load( config_file )

#Instantiate API
mal = Jikan()

client = commands.Bot( command_prefix = '!')
serverid = config['serverid']

#Cogs Commands
@client.command()
async def load(ctx, extension):
    client.load_extension( f'cogs.{extension}')
@client.command()
async def unload(ctx, extension):
    client.unload_extension( f'cogs.{extension}')

#Load Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#Commands/Events
@client.event
async def on_ready():
    print('BOT is running.')

#Commands using prefix
@client.command( pass_context = True )
async def ping(ctx):
    await ctx.send(f' {round(client.latency*1000)} MS')

token = config['token']
client.run(token)
