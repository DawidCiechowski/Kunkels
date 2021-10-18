import os

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="Czerwony ", case_insensitive=False)

bot.load_extension("cogs.bot_utilities")
# bot.load_extension("cogs.music")
bot.load_extension("cogs.youtube")
bot.run(TOKEN)
