#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

import random
import json
from datetime import datetime


with open( 'cogs/advice.json' ) as config_file:
    text = json.load( config_file )

def setup( client ):
    client.add_cog( games(client) )

class games( commands.Cog ):

    def __init__(self, client):
        self.client = client

    #Credit to NadekoBOT for game idea
    @commands.command( pass_context = True, aliases=['Rategirl','rateGirl'] )
    async def rategirl( self, ctx ):
        client= self.client
        if len(ctx.message.mentions) == 0:
            embed=discord.Embed(color=0x1dee17)
            embed.add_field(name="Incomplete Command", value="Example: !rategirl '@user'", inline=True)
            await ctx.send(embed=embed)
            return

        userid = ctx.message.mentions[0].id

        i = sum_h = sum_c = 0
        while i < len( str(userid) ):
            if i < 9:
                sum_h += int( str(userid)[i] )
            else:
                sum_c += int( str(userid)[i] )
            i += 1
        
        if len(client.guilds) == 0:
            guildid = random.randint(1,999)
        else:
            guildid= client.guilds[0].id

        c_date = datetime.today().strftime('%Y%m%d')

        random.seed( sum_h*guildid*int(c_date) )
        hot = round(random.uniform(4.00, 10.00) +0.5, 2) 
        
        random.seed( sum_c*guildid*int(c_date) )
        crazy = round(random.uniform( 3.00, 10.00) , 2)

        if hot < 8 and crazy < 9:
            crazy = round( crazy + 1.00, 2)

        if hot > 9.99:
            hot = 9.99
        
        if crazy > 9.99:
            crazy = 9.99

        if hot < 5 :
            advice =  text['1']
        elif hot > 5:
            if crazy > .60*hot +3.8:
                advice = text['3']
            elif hot < 8 and crazy > 3:
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
        embed.add_field(name=f'Rating For:', value=f'{ctx.message.mentions[0].mention}', inline=False)
        embed.add_field(name="Hot:", value=hot, inline=True)
        embed.add_field(name="Crazy:", value=crazy, inline=True)
        embed.add_field(name="Advice", value=advice, inline=False)
        await ctx.send(embed=embed)

    @commands.command( pass_context = True, aliases=['magicconch'])
    async def conch( self, ctx ):
        rand = random.randint(0,17)
    
        responses = ["IT IS CERTAIN.", "IT IS DECIDEDLY SO.", "WITHOUT A DOUBT", "YES - DEFINITELY", "YOU MAY RELY ON IT.", "AS I SEE IT, YES.", "MOST LIKELY.", "SIGNS POINT TO YES.", "TRY ASKING AGAIN",
        "ASK AGAIN LATER.", "BETTER NOT TELL YOU NOW.", "CANNOT PREDICT NOW", "CONCENTRATE AND ASK AGAIN.", " DON'T COUNT ON IT.", "MY REPLY IS NO.", "MY SOURCES SAY NO.", "OUTLOOK NOT SO GOOD.", "VERY DOUBTFUL"]

        imgURL = "https://i.imgur.com/RLsojmN.jpg"
        embed=discord.Embed(color=0xf1d3ed)
        embed.set_image( url = imgURL )
        embed.add_field(name="Magic Conch", value=responses[rand], inline=False)
        await ctx.send(embed=embed)

        temp = await ctx.send( responses[rand], tts= True )
        await temp.delete()
