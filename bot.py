import discord
from discord.ext import commands

client = commands.Bot( command_prefix = '!')

@client.event
async def on_ready():
    print('Yes Bossu.')

@client.event
async def on_voice_state_update( member, before, after) :
    if 
    await member.send()

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)} MS')

client.run(token)
