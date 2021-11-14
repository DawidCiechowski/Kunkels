import os

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# bot = commands.Bot(command_prefix="Czerwony ", case_insensitive=False)
bot = commands.Bot(command_prefix="Bialy ", case_insensitive=False)

bot.load_extension("cogs.utils.weather")
bot.load_extension("cogs.steam.steam")
bot.load_extension("cogs.utils.bot_utilities")
bot.load_extension("cogs.music.youtube")
bot.load_extension("cogs.riot_api_utilities.vego_tracker")
bot.load_extension("cogs.birthday.birthday_tracker")
bot.run(TOKEN)
