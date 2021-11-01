from typing import Optional, Union, Tuple
import os
from datetime import datetime
import time

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from cogs.riot_api_utilities.api_dataclasses.spectator import SpectatorData

from cogs.riot_api_utilities.riot_api import RiotApi
from cogs.riot_api_utilities.api_dataclasses.champion import champions_data

RIOT_API_TOKEN = os.getenv("RIOT_API_TOKEN")


class Tracker(commands.Cog):

    __slots__ = "bot"

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.api = RiotApi(RIOT_API_TOKEN)
        self._vego.start()

    @staticmethod
    def _convert_unix_timestamp(timestamp: int) -> str:
        return datetime.utcfromtimestamp(timestamp).strftime("%H:%M %d-%m-%Y")

    def __generate_summoner_embed(self, summoner: str) -> discord.Embed:
        try:
            summoner_data = self.api.summoner_search(summoner)
        except Exception as err:
            return
        match, _ = self.api.summoners_last_game(summoner)
        match_timestamp = self._convert_unix_timestamp(match.info.game_creation / 1000)
        game_mode = match.info.game_mode
        damage_chart = []
        damage_taken_chart = []
        for participant in match.info.participants:
            damage_chart.append(participant.total_damage_dealt_to_champions)
            damage_taken_chart.append(
                participant.total_damage_taken + participant.damage_self_mitigated
            )
            if summoner_data.puuid == participant.puuid:
                role = participant.role
                deaths = participant.deaths
                assists = participant.assists
                kills = participant.kills
                win = "Tak" if participant.win else "Nie"
                champion = participant.champion_name
                total_damage_to_champions = participant.total_damage_dealt_to_champions
                wards_placed = participant.wards_placed
                total_damage_taken = (
                    participant.total_damage_taken + participant.damage_self_mitigated
                )
                self_healed_damage = (
                    participant.total_heal - participant.total_heals_on_teammates
                )
                teammate_healed_damage = participant.total_heals_on_teammates
                true_damage_dealt = participant.true_damage_dealt_to_champions
                magic_damage_dealt = participant.magic_damage_dealt_to_champions
                physical_damage_dealt = participant.physical_damage_dealt_to_champions

        damage_chart.sort(reverse=True)
        damage_index = damage_chart.index(total_damage_to_champions) + 1

        damage_taken_chart.sort(reverse=True)
        damage_taken_index = damage_taken_chart.index(total_damage_taken) + 1

        embed_title = "__SUMMONER SEARCH__"
        embed_message = f"""```ini
[Generalne informacje]```
                            
                            **Nick**: {summoner_data.name}
                            **Poziom:** {summoner_data.summoner_level}
                            **Ostatni Mecz:** {match_timestamp}\n**Mode:** {game_mode}
                            **KDA:** {kills}/{deaths}/{assists}\n**Wygrana:** {win}
                            **Champ:** {champion}
                            **Rola:** {role}
                            
                            ```fix
Informacje ofensywne```
                            
                            **Dmg calkowity zadany innym:** {total_damage_to_champions}
                            **Miejsce pod wzgledem dmg:** {damage_index}
                            **Zadany dmg magiczny:** {magic_damage_dealt}
                            **Zadany dmg fizyczny:** {physical_damage_dealt}
                            **Zadany true dmg:** {true_damage_dealt}
                            
                            ```fix
=Informacje defensywne```
                            
                            **Calkowity dmg przyjety:** {total_damage_taken}
                            **Miejsce pod wzgledem przyjetego dmg:** {damage_taken_index}
                            **Dmg wyleczony:** {self_healed_damage}
                            **Teammaci wyleczeni:** {teammate_healed_damage}
                            **Polozone wardy**: {wards_placed}"""

        return discord.Embed(
            title=embed_title, description=embed_message, color=discord.Color.blue()
        )

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
            summoner_name = "vegø"

        embed = self.__generate_summoner_embed(summoner_name)
        await ctx.send(embed=embed)

    def __generate_spectate_embed(
        self, summoner_name: str
    ) -> Tuple[Union[discord.Embed, bool], Optional[SpectatorData]]:
        """Generate a discord.Embed from spectate data.
        Ritos api is so freeaking baaaad, it literally doesnt give any useful information

        Args:
        -----
            summoner_name (str): A name of a summoner, to search data for

        Returns:
        -------
            discord.Embed: An embedded message generated from data, or a simple embed showcasing the player is not currently in-game
        """
        game_data = self.api.summoners_current_game(summoner_name)

        if not game_data:
            return False, None

        # ------------------------ Game Data -----------------------------------
        summoner_data = [
            participant
            for participant in game_data.participants
            if participant.summoner_name.lower() == summoner_name.lower()
        ][0]
        champ_data = [
            data
            for data in champions_data.data
            if int(data.key) == summoner_data.champion_id
        ][0]
        game_mode = game_data.game_mode
        summoner_name = summoner_data.summoner_name
        champion_name = champ_data.name
        game_minutes = int(game_data.game_length / 60)
        game_seconds = game_data.game_length % 60

        title = "__Tracker__"
        description = f"""
        ```ini
[Generalne informacje]
        ```
        **Nick:** {summoner_name}
        **Mode:** {game_mode}
        **Gra:** {champion_name}
        **Czas gry:** {game_minutes}:{game_seconds}
        """

        return (
            discord.Embed(
                title=title, description=description, color=discord.Color.dark_blue()
            ),
            game_data,
        )

    @tasks.loop(minutes=5)
    async def _vego(self):
        embed, game_data = self.__generate_spectate_embed("vegø")
        channel = discord.utils.get(self.bot.get_all_channels(), name="malaria")
        last_message = None

        last_message_id = channel.last_message_id
        try:
            last_message = (
                await channel.fetch_message(channel.last_message_id)
                if last_message_id
                else None
            )
        except discord.errors.NotFound as err:
            pass

        embed_title = (
            last_message.embeds[0].title
            if last_message and last_message.embeds
            else discord.Embed()
        )

        if not embed or not game_data:
            if embed_title == "__Tracker__" or not last_message:
                summonr_embed = self.__generate_summoner_embed("vegø")
                await channel.send(embed=summonr_embed)
            return

        await channel.send(embed=embed)

    @_vego.before_loop
    async def await_vego(self):
        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(Tracker(bot))
