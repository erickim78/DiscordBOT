import discord
from discord.ext import commands

import json
import osu

client = commands.Bot( command_prefix = '!')

@client.event
async def on_ready():
    print('BOT is running.')

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)} MS')


with open( 'config.json') as config_file:
    temp = json.load( config_file )

token = temp['token']
client.run(token)
