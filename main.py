import os 

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="Kunkels ", case_insensitive=False)

bot.load_extension("cogs.basic")
# bot.load_extension("cogs.music")
bot.load_extension("cogs.youtube")
bot.run(TOKEN)

