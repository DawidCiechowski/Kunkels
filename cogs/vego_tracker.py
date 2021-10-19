from typing import Optional
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.riot_api_utilities.riot_api import RiotApi

RIOT_API_TOKEN = os.getenv("RIOT_API_TOKEN")


class Tracker(commands.Cog):

    __slots__ = "bot"

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.api = RiotApi(RIOT_API_TOKEN)

    @commands.command(
        name="summoner",
        aliases=["szukaj"],
        description="Finds information in regards to a summoner",
    )
    async def _summoner(self, ctx, *summoner: str):
        """Generate information about summoner

        Args:
            summoner (str): A summoner's name
        """
        summoner_name = " ".join(summoner)
        summoner_data = self.api.summoner_search(summoner_name)

        embed_title = f"**Summoner Search**"
        embed_message = (
            f"*Name*: {summoner_data.name}\n*Level:* {summoner_data.summoner_level}"
        )

        embed = discord.Embed(title=embed_title, description=embed_message)

        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Tracker(bot))
