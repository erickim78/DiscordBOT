#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

import random
import json

with open( 'cogs/advice.json' ) as config_file:
    text = json.load( config_file )

def setup( client ):
    client.add_cog( games(client) )

class games( commands.Cog ):

    def __init__(self, client):
        self.client = client

    @commands.command( pass_context = True, aliases=['Rategirl','rateGirl'])
    async def rategirl( self, ctx ):
        if len(ctx.message.mentions) == 0:
            embed=discord.Embed(color=0x1dee17)
            embed.add_field(name="Incomplete Command", value="Example: !rategirl '@user'", inline=True)
            await ctx.send(embed=embed)
            return

        userid = ctx.message.mentions[0].id

        #hot = 0-8, crazy = 9-17
        i = sum_h = sum_c = 0
        while i < len( str(userid) ):
            if i < 9:
                sum_h += int( str(userid)[i] )
            else:
                sum_c += int( str(userid)[i] )
            i += 1
        
        random.seed( sum_h )
        hot = round(random.uniform(3.00, 10.00), 2)
        
        random.seed( sum_c )
        crazy = round(random.uniform( 3.00, 10.00), 2)
        
        if hot < 5 :
            advice =  text['1']
        elif hot > 5:
            if crazy > .60*hot +3.8:
                advice = text['3']
            elif hot < 8 and crazy > 4:
                advice = text['2']
            elif hot > 8 and crazy > 7 and crazy < .6*hot+4:
                advice = text['4']
            elif hot > 8 and crazy > 5 and crazy < 7:
                advice = text['5']
            elif hot > 8 and crazy < 4:
                advice = text['6']
            else:
                advice = text['7']
        
        imgURL = "https://i.imgur.com/hynRXh6.jpg"
        embed=discord.Embed(color=0x1dee17)
        embed.set_image(url = imgURL)
        embed.add_field(name=f'Rating for:', value=f'{ctx.message.mentions[0].mention}', inline=False)
        embed.add_field(name="Hot:", value=hot, inline=True)
        embed.add_field(name="Crazy:", value=crazy, inline=True)
        embed.add_field(name="Advice", value=advice, inline=False)
        await ctx.send(embed=embed)
