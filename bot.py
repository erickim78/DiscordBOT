#Importing Discord 
import discord
from discord.ext import commands

#Importing OsuAPI Python Wrapper
import asyncio
from pyosu import OsuApi

#Importing MAL Py Wrapper
from jikanpy import Jikan

import json
import pprint


#Config File Usage
with open( 'config.json') as config_file:
    temp = json.load( config_file )

apikey = temp['osuapikey']


#Instantiate API
osu = OsuApi(apikey)
mal = Jikan()


client = commands.Bot( command_prefix = '!')


#Commands/Events
@client.event
async def on_ready():
    print('BOT is running.')

@client.event
async def on_message( message ):
    realmsg = str(message.content)

    if message.content.find("!osu") != -1 :
        username = realmsg[5:(len(realmsg))]
        user = await osu.get_user( username )
        topscore = await osu.get_user_best( username )

        if( user != None ) :
            beatmap = await osu.get_beatmap( beatmap_id = topscore.beatmap_id )
            songname = beatmap.title
            difficultyname = beatmap.version
            stars = beatmap.difficultyrating

            await message.channel.send("Username: " + username + "\nRank: " + str(user.pp_rank) + "\nTop Play: " + songname + " [" + difficultyname + "]  " + str(round(stars,2)) + "*")
    elif message.content.find("!mal") != -1 :
        inputname = realmsg[5:(len(realmsg))]
        user = mal.user( username = inputname, request = 'animelist')
        
        await message.channel.send("Username: " )
    
     
@client.command
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)} MS')


#Run BOT
with open( 'config.json') as config_file:
    temp = json.load( config_file )

token = temp['token']
client.run(token)
