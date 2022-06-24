import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
import os
import re
import urllib.request
import urllib.parse
import shutil
import pafy

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, description='This is music player bot!', intents=intents)

queues = {}

def get_url(keyword):
    params = {"search_query": keyword}
    queryString = urllib.parse.urlencode(params)
    html = urllib.request.urlopen("https://www.youtube.com/results?" + queryString)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]

def validate(str):
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    p = re.compile(regex)
    if (str == None):
        return False
    if(re.search(p, str)):
        return True
    else:
        return False

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(TEXT_CHANNEL_ID))
    await channel.send(f'Hello {member.name}')

@bot.event
async def on_voice_state_update(member, before, after):
    text_channel = bot.get_channel(int(TEXT_CHANNEL_ID))
    voice_channel = bot.get_channel(int(VOICE_CHANNEL_ID))

    if member.bot:
        return

    if not before.channel:
        #print(f'{member.name} joined {after.channel.name}')
        await text_channel.send(f'Hello {member.name}')

    if before.channel and not after.channel:
        await text_channel.send(f'Bye {member.name}')
        #print(f'{member.name} left channel')

    if before.channel and after.channel:
        if before.channel.id != after.channel.id:
            await text_channel.send(f'{member.name} left {before.channel.name} and joined {after.channel.name}')
        else:
            if member.voice.self_stream:
                await text_channel.send(f'{member.name} started streaming')
            elif member.voice.self_mute:
                await text_channel.send(f'{member.name} muted')
            elif member.voice.self_deaf:
                await text_channel.send(f'{member.name} deafened')
            else:
                await text_channel.send(f'{member.name} is back')

@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


bot.run(TOKEN)