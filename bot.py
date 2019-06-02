import discord
from discord.ext import commands

import asyncio
from pyosu import OsuApi

import json

with open( 'config.json') as config_file:
    temp = json.load( config_file )

apikey = temp['osuapikey']

osu = OsuApi(apikey)


client = commands.Bot( command_prefix = '!')

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
            


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)} MS')

with open( 'config.json') as config_file:
    temp = json.load( config_file )

token = temp['token']
client.run(token)
