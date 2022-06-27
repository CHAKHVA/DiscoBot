import discord
from discord.ext import commands

from disco import Disco

import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')


intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX, description='This is music player bot!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged on as {bot.user.name}')


bot.add_cog(Disco(bot))
bot.run(TOKEN)