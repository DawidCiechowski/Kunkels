import os

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from cogs.riot_api_utilities.api_embed_factory import EmbedFactory
from cogs.riot_api_utilities.riot_api import RiotApi

RIOT_API_TOKEN = os.getenv("RIOT_API_TOKEN")


class Tracker(commands.Cog):

    __slots__ = "bot"

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.api = RiotApi(RIOT_API_TOKEN)
        self._vego.start()

    @commands.command(
        name="summoner",
        aliases=["szukaj"],
        description="Finds information in regards to a summoner",
    )
    async def _summoner(self, ctx, *summoner: str):
        """Send information in regards to the summoner

        Args:
        -----
            summoner (str): A summoner's name
        """
        summoner_name = " ".join(summoner)

        if summoner_name == "vego":
            summoner_name = "végø"

        embed_api = EmbedFactory.factory_embed("summoner", self.api, summoner_name)
        await ctx.send(embed=embed_api.create_embed())

    @tasks.loop(minutes=5)
    async def _vego(self):
        """A task for sending information in regards to Vego games
        Option 1: No channel? NO message -> break out leave
        Option 2: If there is a game,
        """

        embed_api = EmbedFactory.factory_embed("spectate", self.api, "végø")
        embed, game_data = embed_api.create_embed()
        channels = [
            channel
            for channel in self.bot.get_all_channels()
            if channel.name == "vego-tracker"
        ]

        for channel in channels:
            last_message = None
            last_message_id = channel.last_message_id
            try:
                last_message = (
                    await channel.fetch_message(last_message_id)
                    if last_message_id
                    else None
                )
            except discord.errors.NotFound as err:
                pass

            last_message_embed_title = (
                last_message.embeds[0].title
                if last_message and last_message.embeds
                else discord.Embed()
            )

            if not embed or not game_data:
                if last_message_embed_title == "__Tracker__" or not last_message:
                    embed_api = EmbedFactory.factory_embed("summoner", self.api, "végø")
                    await channel.send(embed=embed_api.create_embed())
                else:
                    break

            # If the game is ongoing, but the signal already has been sent
            # to the channel, don't send it again
            if last_message_embed_title == "__Tracker__":
                break

            await channel.send(embed=embed)

    @_vego.before_loop
    async def await_vego(self):
        await self.bot.wait_until_ready()

    @commands.command(
        name="kda",
        description="Command showcasing a graph with last 10 games of a summoner",
    )
    async def _kda(self, ctx, *summoner):
        summoner = " ".join(summoner)
        if summoner == "vego":
            summoner = "végø"
        embed_api = EmbedFactory.factory_embed("kda", self.api, summoner)
        await ctx.send(
            embed=embed_api.create_embed(),
            file=discord.File("test.png", filename="image.png"),
        )

    @commands.command(
        name="damage",
        description="Show the damage done in last 10 games",
        aliases=["dmg"],
    )
    async def _damage(self, ctx, *summoner):
        summoner = " ".join(summoner)
        if summoner == "vego":
            summoner = "végø"

        embed_api = EmbedFactory.factory_embed("damage", self.api, summoner)
        await ctx.send(
            embed=embed_api.create_embed(),
            file=discord.File("test.png", filename="image.png"),
        )

    @commands.command(
        name="def",
        description="A bar chart with damage taken",
        aliases=["obrona", "defensywa", "defense"],
    )
    async def _def(self, ctx, *summoner):
        summoner = " ".join(summoner)
        if summoner == "vego":
            summoner = "végø"

        embed_api = EmbedFactory.factory_embed("defense", self.api, summoner)
        await ctx.send(
            embed=embed_api.create_embed(),
            file=discord.File("test.png", filename="image.png"),
        )

    @commands.command(
        name="kp",
        description="Graph for kill participation stats",
        aliases=["participation", "udzial"],
    )
    async def _kp(self, ctx, *summoner):
        summoner = " ".join(summoner)
        if summoner == "vego":
            summoner = "végø"

        embed_api = EmbedFactory.factory_embed("kp", self.api, summoner)
        await ctx.send(
            embed=embed_api.create_embed(),
            file=discord.File("test.png", filename="image.png"),
        )


def setup(bot: Bot):
    bot.add_cog(Tracker(bot))
