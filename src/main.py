import os
import asyncio
from discord.ext import commands
import discord

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DEBUG = os.getenv("DEBUG", "False") == "True"

intents = discord.Intents.default()
intents.message_content = True
if not DEBUG:
    bot = commands.Bot(command_prefix="Czerwony ", case_insensitive=False, intents=intents)
else:
    bot = commands.Bot(command_prefix="Bialy ", case_insensitive=False, intents=intents)

async def load():
    await bot.load_extension('cogs.riot_api_utilities.vego_tracker')
    await bot.load_extension('cogs.music.youtube')

async def main():
    await load()
    await bot.start(TOKEN)
    
asyncio.run(main())


