import discord 
from discord.ext import commands 

import json

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.load_extension('cogs.vr')


bot.run('')
