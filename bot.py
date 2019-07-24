#Importing Discord 
import discord
from discord.ext import commands

#Importing MAL Py Wrapper
#from jikanpy import Jikan

#Misc Imports
import json
import os

#Config File Usage
with open( 'config.json') as config_file:
    config = json.load( config_file )

#Configure Bot
client = commands.Bot( command_prefix = '!')
serverid = config['serverid']

#Loading All Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.load_extension('music')

#Run Bot
token = config['token']
client.run(token)
