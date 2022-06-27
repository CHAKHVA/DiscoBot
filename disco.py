import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio

import pafy

from helper import Helper

class Disco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def volume(self, ctx, volume: int):
        '''Changes the player's volume'''

        if ctx.voice_client is None:
            return await ctx.send('Not connected to a voice channel.')

        ctx.voice_client.source.volume = volume / 100
        await ctx.send('Changed volume to {}%'.format(volume))
    
    @commands.command(pass_context=True, aliases=['j', 'joi'])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f'The bot has connected to {channel}\n')

        await ctx.send(f'Joined {channel}')
    
    @commands.command(pass_context=True, aliases=['l', 'lea'])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'The bot has left {channel}')
        else:
            print('Bot was told to leave voice channel, but was not in one')
            await ctx.send("Don't think I am in a voice channel")

    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play(self, ctx, *, url):
        if not Helper.validate(url):
            url = Helper.get_url(url)
            audio = pafy.new(url)
            best = audio.getbestaudio()
            url = best.url
        
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(url))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
    
    @commands.command(pass_context=True, aliases=['pa', 'pau'])
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('Music paused')
            voice.pause()
            await ctx.send('Music paused')
        else:
            print('Music not playing failed pause')
            await ctx.send('Music not playing failed pause')

    @commands.command(pass_context=True, aliases=['r', 'res'])
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print('Resumed music')
            voice.resume()
            await ctx.send('Resumed music')
        else:
            print('Music is not paused')
            await ctx.send('Music is not paused')
    
    @commands.command(pass_context=True, aliases=['s', 'sto'])
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('Music stopped')
            voice.stop()
            await ctx.send('Music stopped')
        else:
            print('No music playing failed to stop')
            await ctx.send('No music playing failed to stop')
