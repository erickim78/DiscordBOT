#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

#Misc imports
import asyncio
import json
from pyosu import OsuApi

#API instanstiation
with open( 'config.json') as config_file:
    config = json.load( config_file )
osu_a = OsuApi( config['osuapikey'] )

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

            embed=discord.Embed(color=0xfda8f4)
            embed.add_field(name="Osu! Stats", value="IGN: " + username + "\nTop Play: " + songname + 
                " [" + difficultyname + "]   |  " + str(round(stars,2)) + "*" + "\nRank: #" + str(user.pp_rank) + 
                "\nPP: " + str(user.pp_raw), inline=True)
            await ctx.send(embed=embed)

        else:
            ctx.send("User not found")
