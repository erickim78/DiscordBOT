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
import random


#Config File Usage
with open( 'config.json') as config_file:
    config = json.load( config_file )

apikey = config['osuapikey']


#Instantiate API
osu = OsuApi(apikey)
mal = Jikan()


client = commands.Bot( command_prefix = '!')

serverid = config['serverid']

#Commands/Events
@client.event
async def on_ready():
    print('BOT is running.')

#Declare List of Eligible Command Channels
allowed = ["gamingstats", "statsbot"]

#Text Commands
@client.event
async def on_message( message ):
    realmsg = str(message.content)

    if str(message.channel) in allowed : #and str( message.author) == "The Old Man" 

        if message.content.find("!osu") != -1 :
            username = realmsg[5:(len(realmsg))]
            user = await osu.get_user( username )
            topscore = await osu.get_user_best( username )

            if user != None :
                beatmap = await osu.get_beatmap( beatmap_id = topscore.beatmap_id )
                songname = beatmap.title
                difficultyname = beatmap.version
                stars = beatmap.difficultyrating

                await message.channel.send("Username: " + username + "\nRank: " + str(user.pp_rank) + "\nTop Play: " + songname + 
                    " [" + difficultyname + "]  " + str(round(stars,2)) + "*")
        
        elif message.content.find("!mal") != -1 :
            inputname = realmsg[5:(len(realmsg))]
            user = mal.user( username = inputname, request = 'animelist')
            
            await message.channel.send("Username: " )

        elif message.content.find("!pokemonquiz") != -1 :
            personalities = [  ["bold", 0], ["brave", 0], ["calm", 0], ["docile", 0], ["hardy", 0], ["hasty", 0], ["impish", 0], ["jolly", 0], ["lonely", 0],
             ["naive", 0],  ["quiet", 0], ["quirky", 0], ["rash", 0], ["relaxed", 0], ["sassy", 0], ["timid", 0] ]

            questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            
            count = 0

            while count < 9 :
                current = random.choice( questions )

                if random.choice( questions ) == 1 :
                    await message.channel.send("Have you ever blurted something out without thinking about the consequences first? (Send the number corresponding to your answer.)\n\n1) Yes.\n2) No.")          
                    done = False
                    while done == False :

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

                        temp = await client.wait_for('message', check=check(message.author) )

                        if temp.content.find("1") != -1 :
                            personalities[8][1] += 1
                            personalities[13][1] += 1
                            done == True
                        elif temp.content.find("2") != -1 :
                            personalities[4][1] += 1
                            done = True
                        else :
                            await temp.channel.send("Invalid Response, Try Again.")
                    questions.pop(0)
                    count += 1
                elif random.choice( questions ) == 2 :
                    count += 1

                

                

        
        #elif message.content.find("!")   

@client.command
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)} MS')


token = config['token']
client.run(token)
