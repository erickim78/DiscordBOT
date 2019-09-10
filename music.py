#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

#Misc Imports
import asyncio
import youtube_dl
import os
import shutil
import subprocess

#Global Variables
songlist = {}
players = {}
database = None
cursor = None

current_volume = 0.05
effect_volume = 0.25

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

#Helper Functions
def check_queue( id, ctx ):
    if songlist[id] != []:
        player = songlist[id].pop(0)
        players[id] = player
        ctx.voice_client.play(player, after=lambda e: check_queue(ctx.guild.id, ctx))

class YTDLSource( discord.PCMVolumeTransformer ):
    def __init__(self, source, *, data, volume = current_volume):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


#Music COG
def setup( client ):
    client.add_cog( music(client) )

class music( commands.Cog ):

    def __init__(self, client):
        self.client = client
        from bot import db
        global cursor
        global database
        database = db
        cursor = database.cursor()

    #Voice Channel Movement
    @commands.command(aliases= ['summon', 'connect'])
    async def join(self, ctx):
        currentchannel = ctx.message.author.voice.channel
        voice = get( self.client.voice_clients, guild= ctx.guild )

        if voice and voice.is_connected():
            await voice.move_to( currentchannel )
        else:
            voice = await currentchannel.connect()
            print(f'The bot has connected to {currentchannel}')

    @commands.command( pass_context = True, aliases = ['kick'])
    async def leave(self, ctx):
        voice = get( self.client.voice_clients, guild=ctx.guild )

        if voice and voice.is_connected():
            await voice.disconnect()

    #Music
    @commands.command( pass_context = True, aliases = ['p'])
    async def play(self, ctx, *, url):
        voice = get( self.client.voice_clients, guild= ctx.guild )
        if voice and voice.is_connected():
            await voice.move_to( ctx.message.author.voice.channel )
        else:
            voice = await ctx.message.author.voice.channel.connect()

        async with ctx.typing():
            player = await YTDLSource.from_url( url, loop= self.client.loop)
            player.volume = current_volume

            if voice and voice.is_playing():
                if ctx.guild.id in songlist:
                    songlist[ctx.guild.id].append(player)
                else:
                    songlist[ctx.guild.id] = [player]

                embed=discord.Embed(title="Added to Queue", description=format(player.title), color=0xff1515)
                await ctx.send(embed=embed)
            else:
                players[ctx.guild.id] = player
                ctx.voice_client.play(player, after=lambda e: check_queue(ctx.guild.id, ctx))

                embed=discord.Embed(title="Now Playing", description=format(player.title), color=0xff1515)
                await ctx.send(embed=embed)

        #MYSQL DB Update
        global cursor
        global database
        tablename = str(ctx.message.author).replace('#','')
        try:
            cursor.execute(f'CREATE TABLE {tablename} (Song varchar(255), Plays int)')
        except:
            print(f'Table for user {tablename} already exists')

        cursor.execute(f'SELECT * FROM {tablename} WHERE Song = \'{format(player.title)}\'')
        exists = cursor.fetchall()
        if exists == []:
            formula = f'INSERT INTO {tablename} (Song, Plays) VALUES (%s, %s)'
            temp = (format(player.title), 0)
            cursor.execute(formula, temp)
        cursor.execute(f'UPDATE {tablename} SET Plays = Plays + 1 WHERE Song = \'{format(player.title)}\'')
        database.commit()


    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild= ctx.guild)
        if voice and voice.is_playing():
            voice.pause()

    @commands.command( pass_context = True)
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild= ctx.guild)
        if voice and voice.is_paused():
            voice.resume()

    @commands.command( pass_context = True )
    async def skip(self, ctx):
        voice = get( self.client.voice_clients, guild= ctx.guild)

        if voice and voice.is_playing():
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./Audio/join.wav"))
            source.volume = effect_volume
            if ctx.guild.id in songlist:
                songlist[ctx.guild.id].insert(0, source)
            else:
                songlist[ctx.guild.id] = [source]
            voice.stop()

    @commands.command( pass_context = True )
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild= ctx.guild)
        await ctx.send("Stopping")
        if voice and voice.is_playing():
            voice.stop()

        songlist.clear()
        for target in os.listdir('./'):
            if target.endswith(".webm"):
                os.remove(os.path.join('./', target))

    @commands.command( pass_context = True )
    async def volume(self, ctx, value: int):
        global current_volume

        if ctx.voice_client is None:
            current_volume = value / 250
            embed=discord.Embed(title="Volume", description=f'{value}%'.format(value), color=0xff1515)
            await ctx.send(embed=embed)
            return

        if value > 100:
            await ctx.send("Please enter a number between 0-100")
            return
    
        ctx.voice_client.source.volume = value / 250
        current_volume = value / 250
        embed=discord.Embed(title="Volume", description=f'{value}%'.format(value), color=0xff1515)
        await ctx.send(embed=embed)