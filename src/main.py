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
    bot = commands.Bot(command_prefix="Bialy ", case_insensitive=False)

async def load():
    await bot.load_extension('cogs.riot_api_utilities.vego_tracker')

async def main():
    await load()
    await bot.start(TOKEN)
# # bot.add_cog(Tracker(bot))
# cog = bot.get_cog('Tracker')
# bot.run(TOKEN)
    
asyncio.run(main())

    # # bot.load_extension("cogs.utils.weather")
    # # bot.load_extension("cogs.steam.steam")
    # # bot.load_extension("cogs.utils.bot_utilities")
    # # bot.load_extension("cogs.music.youtube")
    # await bot.add_cog(Tracker(bot))
    # # bot.load_extension("cogs.birthday.birthday_tracker")
    # cog = bot.get_cog('Tracker')
    # await bot.run(TOKEN)

