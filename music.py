#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

#Misc Imports
import asyncio
import youtube_dl
import os
import shutil

#Global Var
songlist = {}
music_volume = 0.05
effect_volume = 0.50


def setup( client ):
    client.add_cog( music(client) )

class music( commands.Cog ):

    def __init__(self, client):
        self.client = client

    #Voice Channel Movement
    @commands.command(aliases= ['summon', 'connect'])
    async def join(self, ctx):
        client = self.client
        global voice
        currentchannel = ctx.message.author.voice.channel
        voice = get( client.voice_clients, guild= ctx.guild )

        if voice and voice.is_connected():
            await voice.move_to( currentchannel )
        else:
            voice = await currentchannel.connect()
            print(f'The bot has connected to {currentchannel}')

    @commands.command( pass_context = True, aliases = ['exit', 'kick'])
    async def leave(self, ctx):
        client = self.client
        voice = get( client.voice_clients, guild=ctx.guild )

        if voice and voice.is_connected():
            await voice.disconnect()
            print("The bot has disconnected from voice chat")

    #Music
    @commands.command( pass_context = True, aliases = ['p'])
    async def play(self, ctx):
        message = ctx.message.content
        url = message[6: len(message)]
        client = self.client
        currentchannel = ctx.message.author.voice.channel
        voice = get( client.voice_clients, guild= ctx.guild)

        if voice and voice.is_connected():
            if voice.is_playing() is False:
                await voice.move_to( currentchannel )
        else:
            voice = await currentchannel.connect()
        
        def check_songlist():
            Qexists = os.path.isdir("./Queue")

            if os.path.isfile("song.mp3"):
                os.remove("song.mp3")

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
                    shutil.move(song_path, new_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')
                    voice.play( discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_songlist() )
                    voice.source = discord.PCMVolumeTransformer( voice.source )
                    voice.source.volume = music_volume
                else:
                    songlist.clear()
                    return
            else:
                songlist.clear()
        
        if voice.is_playing():
            client = self.client
            voice = get(client.voice_clients, guild= ctx.guild)

            await ctx.send("Attempting to queue...")
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
                'default_search': 'auto',
                'outtmpl': queue_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            
            with youtube_dl.YoutubeDL( ydl_opts ) as ydl:
                ydl.download( [url] )    
                info = ydl.extract_info( url, download= False )

            video_title = info.get('title')
            if video_title == "None":
                video_title = url

            await ctx.send(f'Successfully added \"{video_title}\" to queue')

        else:
            await ctx.send("Searching...")
            
            if os.path.isfile("song.mp3"):
                os.remove("song.mp3")

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
                'default_search': 'auto',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL( ydl_opts ) as ydl:
                ydl.download( [url] )
                info = ydl.extract_info( url, download= False )

            video_title = info.get('title')
            print(video_title)
            if video_title == None:
                video_title = url

            print(video_title)
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")

            await ctx.send(f'Now playing \"{video_title}\"')
            voice.play( discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_songlist() )
            voice.source = discord.PCMVolumeTransformer( voice.source )
            voice.source.volume = music_volume

    @commands.command( pass_context = True)
    async def pause(self, ctx):
        client = self.client
        voice = get(client.voice_clients, guild= ctx.guild)
        if voice and voice.is_playing():
            voice.pause()

    @commands.command( pass_context = True)
    async def resume(self, ctx):
        client = self.client
        voice = get(client.voice_clients, guild= ctx.guild)
        if voice and voice.is_paused():
            voice.resume()

    @commands.command( pass_context = True )
    async def skip(self, ctx):
        client = self.client

        def check_songlist():
            Qexists = os.path.isdir("./Queue")

            if os.path.isfile("song.mp3"):
                os.remove("song.mp3")

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
                    shutil.move(song_path, new_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')
                    voice.play( discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_songlist() )
                    voice.source = discord.PCMVolumeTransformer( voice.source )
                    voice.source.volume = 0.05
                else:
                    songlist.clear()
                    print("Songlist Clear 1")
                    return
            else:
                songlist.clear()
                print("Songlist Clear 2")

        def afterskip():
            if os.path.isfile("song.mp3"):
                voice.play( discord.FFmpegPCMAudio("song.mp3"), after= lambda e: check_songlist() )
                voice.source = discord.PCMVolumeTransformer( voice.source )
                voice.source.volume = music_volume

        voice = get( client.voice_clients, guild= ctx.guild)
        if voice and voice.is_playing():
            voice.stop()

            voice.play( discord.FFmpegPCMAudio("./Audio/join.wav"), after= lambda e: afterskip() )
            voice.source = discord.PCMVolumeTransformer( voice.source )
            voice.source.volume = effect_volume

    @commands.command( pass_contexxt = True )
    async def stop(self, ctx):
        client = self.client
        voice = get(client.voice_clients, guild= ctx.guild)

        songlist.clear()

        await ctx.send("Stopping")
        if voice and voice.is_playing():
            voice.stop()
            if os.path.isfile("song.mp3"):
                os.remove("song.mp3")

