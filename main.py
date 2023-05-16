import discord 
from discord.ext import commands 

import json

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.load_extension('cogs.vr')


bot.run('MTEwNzkyMDUxMjE1NzQ5OTM5Mw.GQ1l3f.rX2UWMQB_v5aLvzI-OLESs_sau3JI1T-3vTc_c')