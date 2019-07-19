#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

#Misc Imports
import asyncio
import youtube_dl
import os
import shutil

songlist = {}

def setup( client ):
    client.add_cog( music(client) )

class music( commands.Cog ):


    def __init__(self, client):
        self.client = client


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

    @commands.command( pass_context = True, aliases = ['p'])
    async def play(self, ctx, url: str):
        client = self.client
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
                    voice.source.volume = 0.05
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
        voice.source.volume = 0.05

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
                    voice.source.volume = 0.05
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
            voice.source.volume = 0.05

        voice = get( client.voice_clients, guild= ctx.guild)
        if voice and voice.is_playing():
            voice.stop()

            voice.play( discord.FFmpegPCMAudio("./Audio/join.wav"), after= lambda e:afterskip() )
            voice.source = discord.PCMVolumeTransformer( voice.source )
            voice.source.volume = 0.65

            #voice.stop()      

    @commands.command( pass_contexxt = True )
    async def stop(self, ctx):
        client = self.client
        voice = get(client.voice_clients, guild= ctx.guild)

        songlist.clear()

        await ctx.send("Stopping")
        if voice and voice.is_playing():
            voice.stop()

    @commands.command( pass_context = True, aliases = ['q'] )
    async def queue(self, ctx, url: str):
        client = self.client
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

