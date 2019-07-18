#Importing Discord 
import discord
from discord.ext import commands
from discord.utils import get

#Importing OsuAPI Python Wrapper
import asyncio
from pyosu import OsuApi

#Importing MAL Py Wrapper
from jikanpy import Jikan

#Misc Imports
import json
import pprint
import random
import youtube_dl
import os
import shutil

#Config File Usage
with open( 'config.json') as config_file:
    config = json.load( config_file )

apikey = config['osuapikey']

#Instantiate API
osu_a = OsuApi(apikey)
mal = Jikan()

client = commands.Bot( command_prefix = '!')
serverid = config['serverid']

#Commands/Events
@client.event
async def on_ready():
    print('BOT is running.')

#Declare List of Eligible Command Channels
allowed = ["gamingstats", "statsbot"]

#Commands using prefix
@client.command( pass_context = True )
async def ping(ctx):
    await ctx.send(f' {round(client.latency*1000)} MS')

#@client.command( pass_context = True, aliases=['h'] )
#async def help(ctx):
#    await ctx.send("!join: Summon bot to current channel.\n!play 'url': Plays the audio from the given youtube url.\n!stop: Stops currently playing audio.\nleave: Disconnects bot from the current channel.\n")



@client.command( pass_context = True, aliases= ['summon', 'connect'])
async def join(ctx):
    global voice
    currentchannel = ctx.message.author.voice.channel
    voice = get( client.voice_clients, guild= ctx.guild )

    if voice and voice.is_connected():
        await voice.move_to( currentchannel )
    else:
        voice = await currentchannel.connect()
        print(f'The bot has connected to {currentchannel}')

    #await voice.disconnect()

@client.command( pass_context = True, aliases = ['exit', 'kick'])
async def leave(ctx):
    voice = get( client.voice_clients, guild=ctx.guild )

    if voice and voice.is_connected():
        await voice.disconnect()
        print("The bot has disconnected from voice chat")

@client.command( pass_context = True, aliases = ['p'])
async def play(ctx, url: str):

    currentchannel = ctx.message.author.voice.channel
    voice = get( client.voice_clients, guild= ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to( currentchannel )
    else:
        voice = await currentchannel.connect()
    
    def check_songlist():
        Qexists = os.path.isdir("./Queue")
        if Qexists:
            location = os.path.abspath( os.path.realpath("Queue") )
            num_songs = len(os.listdir(location))
            try:
                file1 = os.listdir(location)[0]
            except:
                songlist.clear()
                return
            new_location = os.path.dirname( os.path.realpath(__file__))
            song_path = os.path.abspath( os.path.realpath("Queue") + "\\" + file1 )
            if num_songs != 0:
                exists = os.path.isfile("song.mp3")
                if exists:
                    os.remove("song.mp3")
                shutil.move(song_path, new_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')
                
                voice.play( discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_songlist() )
                voice.source = discord.PCMVolumeTransformer( voice.source )
                voice.source.volume = 0.04
            else:
                songlist.clear()
                return
        else:
            songlist.clear()
    
    localsong = os.path.isfile("song.mp3")
    try:
        if localsong:
            os.remove("song.mp3")
            songlist.clear()
        await ctx.send("Searching...")
    except PermissionError:
        print("Tried to delete currently playing song")
        await ctx.send("Only King Crimson has the power to erase the current song. Please use !queue")
        return

    Qexists = os.path.isdir("./Queue")
    try:
        folder = "./Queue"
        if Qexists:
            shutil.rmtree( folder )
    except:
        print("No Queue")

    voice = get(client.voice_clients, guild= ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL( ydl_opts ) as ydl:
        ydl.download( [url] )

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
           os.rename(file, "song.mp3")

    await ctx.send("Now Playing")
    voice.play( discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_songlist() )
    voice.source = discord.PCMVolumeTransformer( voice.source )
    voice.source.volume = 0.04


@client.command( pass_context = True)
async def pause(ctx):
    voice = get(client.voice_clients, guild= ctx.guild)
    if voice and voice.is_playing():
        voice.pause()

@client.command( pass_context = True)
async def resume(ctx):
    voice = get(client.voice_clients, guild= ctx.guild)
    if voice and voice.is_paused():
        voice.resume()

@client.command( pass_context = True )
async def skip(ctx):

    def check_songlist():
        Qexists = os.path.isdir("./Queue")
        if Qexists:
            location = os.path.abspath( os.path.realpath("Queue") )
            num_songs = len(os.listdir(location))
            try:
                file1 = os.listdir(location)[0]
            except:
                songlist.clear()
                return
            new_location = os.path.dirname( os.path.realpath(__file__))
            song_path = os.path.abspath( os.path.realpath("Queue") + "\\" + file1 )
            if num_songs != 0:
                exists = os.path.isfile("song.mp3")
                if exists:
                    os.remove("song.mp3")
                shutil.move(song_path, new_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')
                
                voice.play( discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_songlist() )
                voice.source = discord.PCMVolumeTransformer( voice.source )
                voice.source.volume = 0.04
            else:
                songlist.clear()
                print("Songlist Clear 1")
                return
        else:
            songlist.clear()
            print("Songlist Clear 2")
    def afterskip():
        voice.play( discord.FFmpegPCMAudio("song.mp3"), after= lambda e:check_songlist() )
        voice.source = discord.PCMVolumeTransformer( voice.source )
        voice.source.volume = 0.04

    voice = get( client.voice_clients, guild= ctx.guild)
    if voice and voice.is_playing():
        voice.stop()

        voice.play( discord.FFmpegPCMAudio("./Audio/join.wav"), after= lambda e:afterskip() )
        voice.source = discord.PCMVolumeTransformer( voice.source )
        voice.source.volume = 0.55

        #voice.stop()
          

@client.command( pass_contexxt = True )
async def stop(ctx):
    voice = get(client.voice_clients, guild= ctx.guild)

    songlist.clear()

    await ctx.send("Stopping")
    if voice and voice.is_playing():
        voice.stop()


songlist = {}
@client.command( pass_context = True, aliases = ['q'] )
async def queue(ctx, url: str):
    voice = get(client.voice_clients, guild= ctx.guild)
    if voice.is_playing() is False:
        await ctx.send("Only King Crimson can skip the !play command. Please use !play")
        return

    await ctx.send("Searching...")
    Qexists = os.path.isdir("./Queue")
    if Qexists is False:
        os.mkdir("Queue")

    location = os.path.abspath( os.path.realpath("Queue"))
    num_songs = len( os.listdir(location) )
    num_songs += 1

    add_queue = True
    while add_queue:
        if num_songs in songlist:
            num_songs += 1
        else:
            add_queue = False
            songlist[num_songs] = num_songs

    queue_path = os.path.abspath( os.path.realpath("Queue") + f"\song{num_songs}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with youtube_dl.YoutubeDL( ydl_opts ) as ydl:
        ydl.download( [url] )    
    await ctx.send("Added to Queue")


@client.command( pass_context = True )  
async def osu(ctx, username: str):
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

#Text Commands
@client.event
async def on_message( message ):
    #realmsg = str(message.content)

    channelcheck = False
    if str(message.channel) in allowed :
        channelcheck = True
     
    if channelcheck and message.content.find("!mal") != -1 :
        #inputname = realmsg[5:(len(realmsg))]
        #user = mal.user( username = inputname, request = 'animelist')
            
        await message.channel.send("Username: " )
    elif channelcheck and message.content.find("!qqq") != -1 :
        personalities = [  ["BOLD", 0], ["QUIRKY", 0], ["TIMID", 0], ["NAIVE", 0], ["HASTY", 0] ]
        questions = [0,1,2,3,4,5,6,7,8,9,10,11,12]

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
            
        count = 0
        while count < 6 :

            current = random.choice( questions )
            if current == 0 :
                await message.channel.send("Have you ever thought that if you dug in your backyard you could find buried treasure? \n\n1) Yes.\n2) No.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[3][1] += 2
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 1 :
                await message.channel.send("You're in class when you realize that you really have to go to the restroom. What do you do? \n\n1) Ask for permission to leave.\n2) Sneak out.\n3) Hold on until class ends.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[4][1] += 1
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 2
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 2 :
                await message.channel.send("You discover a beat-up-looking treasure chest in some ruins. What do you do? \n\n1) Open It!\n2) Get help opening it.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        personalities[4][1] += 2
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        personalities[4][1] -= 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 3 :
                await message.channel.send("If you saw someone doing something bad, could you scold them? \n\n1) Of Course.\n2) Not Really.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 4 :
                await message.channel.send("Are you truly sincere when you apologize? \n\n1) Of Course.\n2) That's not easy to admit.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        personalities[3][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 2
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 5 :
                await message.channel.send("You're hiking up a mountain when you reach diverging paths. Which kind do you take? \n\n1) Narrow.\n2) Wide.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[3][1] += 2
                        personalities[4][1] += 1
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        personalities[0][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")
            
            elif current == 6 :
                await message.channel.send("Everyone around you is laughing hard at something you think is pretty boring. What do you do? \n\n1) Nothing.\n2) Laugh Along.\n3) It depends on the situation.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 2
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[1][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 7 :
                await message.channel.send("Good news and bad news... Which one do you want to hear first? \n\n1) The good news.\n2) The bad news.\n3) I don't want either.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[4][1] += 2
                        personalities[3][1] += 1
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 8 :
                await message.channel.send("There's a rumor around about a ghost haunting the school bathrooms! What do you do?	 \n\n1) Avoid them.\n2) Go in there anyway.\n3) Bring your friends with you.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[1][1] += 1
                        personalities[0][1] -= 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[0][1] += 1
                        personalities[4][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")
            
            elif current == 9 :
                await message.channel.send("You see a cake that is past its expiration date, but only by one day. What do you do? \n\n1) Not a problem, eat it anyway.\n2) Think about it briefly, then decide.\n3) Get someone to try it first. \n4) Refuse to eat it.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[4][1] += 2
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("4") != -1 :
                        personalities[0][1] += 1
                        personalities[1][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 10 :
                await message.channel.send("You're eating at a very fancy restaurant known for its food. Which course do you select? \n\n1) Whatever is cheapest.\n2) Healthy fish.\n3) Prime Steak, enjoy the experience. \n4) Anything, it's all good.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[0][1] -= 1
                        personalities[1][1] += 2
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("4") != -1 :
                        personalities[2][1] += 1
                        personalities[3][1] += 2
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 11 :
                await message.channel.send("You find something at a great bargain price. What do you do? \n\n1) Buy it right away.\n2) Think about whether you need it.\n3) Demand an even bigger discount.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[1][1] += 1
                        personalities[4][1] += 2
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[4][1] -= 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 1
                        personalities[3][1] += 2
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 12 :
                await message.channel.send("You've been handed a large bag as a souvenir. What do you do? \n\n1) Shake it.\n2) Open it.\n3) Wait until I get home to open it.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[3][1] += 1
                        personalities[1][1] += 2
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[4][1] += 2
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            #Remove current question from list of questions    
            i = 0
            for x in questions:
                if current == x :
                    questions.pop(i)
                else :
                    i += 1

            count += 1
            
        #Determine Nature
        rand = random.randint(0,4)
        nature = personalities[rand]
        for x in personalities :
            if x[1] > nature[1] :
                nature = x

        #Send Nature to Discord Chat
        await message.channel.send(f"You are the {nature[0]} type.")

    await client.process_commands( message )

token = config['token']
client.run(token)
