import discord
from discord.ext import commands

client = commands.Bot( command_prefix = '!')

@client.event
async def on_ready():
    print('Yes Bossu.')

client.run('NTgzODAzMDYzNDc1ODk2MzIw.XPBxGQ.eiBhzQdDw1C_7wm82K1P5C_wApM')