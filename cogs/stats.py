#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

#Misc imports
import asyncio
import json
import math
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

    @commands.command( pass_context = True )
    async def symbol(self, ctx):
        
        message = ctx.message
        def check(author):
            def check2( answer ):
                if answer.author != message.author:
                    return False
                try:
                    int(answer.content)
                    return True
                except ValueError :
                    return False
            return check2

        client = self.client
        exp = [12,15,20,27,36,47,60,75,92,111,132,155,180,207,236,267,300,335,372]
        embed=discord.Embed(color=0xf89221)
        embed.add_field(name="Select Symbol", value="1) Vanishing Journey\n2) Chu Chu Island\n3) Lachelein\n4) Arcana\n5) Morass\n6) Esfera\n\n7) Quit", inline=True)
        await ctx.send(embed=embed)

        done = False

        symboltype = await client.wait_for('message', check=check(message.author))

        while done is False:
            if symboltype.content == "7":
                done = True
                return
            elif symboltype.content == "1":
                done = True
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What level is your symbol?", value="I.E. Growth Level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                level = int(temp.content) - 1
                
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What is your current symbol exp?", value="x, where x/? to next level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                num = int(temp.content)

                total = 0
                while level < len(exp):
                    total += exp[level]
                    level += 1

                answer = math.ceil( (total-num) / 14 )

                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="Result", value=f'It will take {answer} days to max your symbol', inline=False)
                await ctx.send(embed=embed)
                

            elif symboltype.content == "2":
                done = True
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What level is your symbol?", value="I.E. Growth Level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                level = int(temp.content) - 1
                
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What is your current symbol exp?", value="x, where x/? to next level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                num = int(temp.content)

                total = 0
                while level < len(exp):
                    total += exp[level]
                    level += 1

                answer = math.ceil( (total-num) / 15 )

                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="Result", value=f'It will take {answer} days to max your symbol', inline=False)
                await ctx.send(embed=embed)

            elif symboltype.content == "3":
                done = True
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What level is your symbol?", value="I.E. Growth Level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                level = int(temp.content) - 1
                
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What is your current symbol exp?", value="x, where x/? to next level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                num = int(temp.content)

                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What floor of Dream Defender can you clear?", value="Enter a number between 1-170", inline=True)
                await ctx.send(embed=embed)

                valid = False
                while valid is False:
                    temp = await client.wait_for('message', check=check(message.author))
                    if int(temp.content) < 1 or int(temp.content) > 170:
                        embed=discord.Embed(color=0xf89221)
                        embed.add_field(name="Invalid Floor", value="Enter a number between 1-170", inline=True)
                        await ctx.send(embed=embed)
                    else:
                        floor = int(temp.content)
                        valid = True


                total = 0
                while level < len(exp):
                    total += exp[level]
                    level += 1

                answer = math.ceil( (total-num) / (math.floor( floor/30 ) + 0.967) )

                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="Result", value=f'It will take {answer} days to max your symbol', inline=False)
                await ctx.send(embed=embed)

            elif symboltype.content == "4":
                done = True
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What level is your symbol?", value="I.E. Growth Level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                level = int(temp.content) - 1
                
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What is your current symbol exp?", value="x, where x/? to next level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                num = int(temp.content)

                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What is your average score in Spirit Savior?", value="Enter a number between greater than 0", inline=True)
                await ctx.send(embed=embed)

                valid = False
                while valid is False:
                    temp = await client.wait_for('message', check=check(message.author))
                    if int(temp.content) < 0 or int(temp.content) > 10000:
                        embed=discord.Embed(color=0xf89221)
                        embed.add_field(name="Invalid Score", value="Enter a number greater than 0", inline=True)
                        await ctx.send(embed=embed)
                    else:
                        score = int(temp.content)*3
                        valid = True

                total = 0
                while level < len(exp):
                    total += exp[level]
                    level += 1

                answer = math.ceil( (total-num) / math.floor( score/1000 ) )

                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="Result", value=f'It will take {answer} days to max your symbol', inline=False)
                await ctx.send(embed=embed)

            elif symboltype.content == "5":
                done = True
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What level is your symbol?", value="I.E. Growth Level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                level = int(temp.content) - 1
                
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What is your current symbol exp?", value="x, where x/? to next level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                num = int(temp.content)

                total = 0
                while level < len(exp):
                    total += exp[level]
                    level += 1

                answer = math.ceil( (total-num) / 8 )

                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="Result", value=f'It will take {answer} days to max your symbol', inline=False)
                await ctx.send(embed=embed)

            elif symboltype.content == "6":
                done = True
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What level is your symbol?", value="I.E. Growth Level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                level = int(temp.content) - 1
                
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="What is your current symbol exp?", value="x, where x/? to next level.", inline=True)
                await ctx.send(embed=embed)

                temp = await client.wait_for('message', check=check(message.author))
                num = int(temp.content)

                total = 0
                while level < len(exp):
                    total += exp[level]
                    level += 1

                answer = math.ceil( (total-num) / 8 )

                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="Result", value=f'It will take {answer} days to max your symbol', inline=False)
                await ctx.send(embed=embed)

            else:
                embed=discord.Embed(color=0xf89221)
                embed.add_field(name="Invalid Response", value=f'Please select the number corresponding to desired symbol', inline=False)
                await ctx.send(embed=embed)
