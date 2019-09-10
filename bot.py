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

#MYSQL
import mysql.connector
pwd = config['mysqlpasswd']
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd=pwd,
    database="discordbot",
    auth_plugin='mysql_native_password'
)


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
