from typing import Dict, Any
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from cogs.riot_api_utilities.api_embed_factory import EmbedFactory, EmbedType
from cogs.riot_api_utilities.riot_api import RiotApi
from cogs.riot_api_utilities.constants import RIOT_API_TOKEN, TEAM


class Tracker(commands.Cog, name='Tracker'):

    __slots__ = "bot"

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.api = RiotApi(RIOT_API_TOKEN)
        self.currently_playing: Dict[str, Any] = {member: "" for member in TEAM}
        self._team.start()
        self.channels = []

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

        embed_api = EmbedFactory.factory_embed(
            EmbedType.SUMMONER, self.api, summoner_name
        )
        embed = embed_api.create_embed()
        await ctx.send(embed=embed)

    async def send_embed_to_all_channels(self, embed: discord.Embed):

        for channel in self.channels:
            await channel.send(embed=embed)

    @tasks.loop(minutes=1)
    async def _team(self):
        """If any of team members are in game ->"""
        for member in TEAM:
            spectator_data = self.api.summoners_current_game(member)
            if spectator_data and spectator_data.game_id != self.currently_playing[member]:
                embed = EmbedFactory.factory_embed(EmbedType.SPECTATE, self.api, member).create_embed()
                if embed != None:
                    await self.send_embed_to_all_channels(embed)
                    self.currently_playing[member] = spectator_data.game_id
                    continue

            if not spectator_data and self.currently_playing[member]:
                embed = EmbedFactory.factory_embed(EmbedType.SUMMONER, self.api, member)
                await self.send_embed_to_all_channels(embed.create_embed())
                self.currently_playing[member] = ""
                continue


    @_team.before_loop
    async def await_vego(self):
        await self.bot.wait_until_ready()

        self.channels = [
            channel
            for channel in self.bot.get_all_channels()
            if channel.name == "tracker"
        ]

    @commands.command(
        name="kda",
        description="Command showcasing a graph with last 10 games of a summoner",
    )
    async def _kda(self, ctx, *summoner):
        """Send an embeded message with kda stats from last 10 games

        Args:
        -----
            ctx : Context of a channel
            summoner: A name of a summoner to search stats for
        """
        summoner = " ".join(summoner)
        if summoner == "vego":
            summoner = "végø"
        embed_api = EmbedFactory.factory_embed(EmbedType.KDA, self.api, summoner)
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
        """Send an embeded message with damage stats from last 10 games

        Args:
        -----
            ctx ([type]): A context of a channel
            summoner (str):  A name of a summoner to search stats for
        """
        summoner = " ".join(summoner)
        if summoner == "vego":
            summoner = "végø"

        embed_api = EmbedFactory.factory_embed(EmbedType.DAMAGE, self.api, summoner)
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
        """Send an embeded message with defensive stats from last 10 games

        Args:
        -----
            ctx ([type]): A context of a channel
            summoner (str):  A name of a summoner to search stats for
        """
        summoner = " ".join(summoner)
        if summoner == "vego":
            summoner = "végø"

        embed_api = EmbedFactory.factory_embed(EmbedType.DEFENSE, self.api, summoner)
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
        """Send an embeded message with kill participation stats from last 10 games

        Args:
        -----
            ctx ([type]): A context of a channel
            summoner (str):  A name of a summoner to search stats for
        """
        summoner = " ".join(summoner)
        if summoner == "vego":
            summoner = "végø"

        embed_api = EmbedFactory.factory_embed(
            EmbedType.KILL_PARTICIPATION, self.api, summoner
        )
        await ctx.send(
            embed=embed_api.create_embed(),
            file=discord.File("test.png", filename="image.png"),
        )


async def setup(bot: Bot):
    await bot.add_cog(Tracker(bot))
