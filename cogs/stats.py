#Importing Discord 
import discord
from discord.ext import commands

#Misc imports
import asyncio
import json
from pyosu import OsuApi
from bot import config

def setup( client ):
    client.add_cog( stats(client) )

class stats( commands.Cog ):


    def __init__(self, client):
        self.client = client

    
    @commands.command( pass_context = True )
    async def osu(self, ctx, username: str):
        apikey = config['osuapikey']
        osu_a = OsuApi( apikey )

        user = await osu_a.get_user( username )
        topscore = await osu_a.get_user_best( username )

        if user != None :
            beatmap = await osu_a.get_beatmap( beatmap_id = topscore.beatmap_id )
            songname = beatmap.title
            difficultyname = beatmap.version
            stars = beatmap.difficultyrating

            await ctx.send("IGN: " + username + "\nRank: #" + str(user.pp_rank) + "\nTop Play: " + songname + 
                " [" + difficultyname + "]  " + str(round(stars,2)) + "*")
        else:
            ctx.send("User not found")
    