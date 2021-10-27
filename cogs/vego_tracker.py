from typing import Optional, Union, Tuple
import os
from datetime import datetime
import time

import discord
from discord.ext import commands
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

    @staticmethod
    def _convert_unix_timestamp(timestamp: int) -> str:
        return datetime.utcfromtimestamp(timestamp).strftime("%H:%M %d-%m-%Y")

    def __generate_summoner_embed(self, summoner: str) -> discord.Embed:
        summoner_data = self.api.summoner_search(summoner)
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

        damage_chart.sort()
        damage_index = damage_chart.index(total_damage_to_champions) + 1

        damage_taken_chart.sort()
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

    @commands.command(
        name="vego",
        aliases=["grubas", "swinia"],
        description="Check if Vego is online and playing lol, and if so, show statistics",
    )
    async def _vego(self, ctx):
        while True:
            embed, game_data = self.__generate_spectate_embed("vegø")
            if not embed or not game_data:
                print("Not playing")
                time.sleep(5)
                continue
            else:
                last_message = await ctx.channel.history(limit=1)
                if last_message.content() == f"Game ID: {game_id}":
                    print("Playing the same game")
                    time.sleep(5)
                    continue
                else:
                    await ctx.send(embed=embed)
                    game_id = game_data.game_id
                    await ctx.send(f"Game ID: {game_id}")
                    time.sleep(5)


def setup(bot: Bot):
    bot.add_cog(Tracker(bot))
