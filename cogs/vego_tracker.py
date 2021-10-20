from typing import Optional
import os
from datetime import datetime

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

    @staticmethod
    def _convert_unix_timestamp(timestamp: int) -> str:
        return datetime.utcfromtimestamp(timestamp).strftime("%H:%M %d-%m-%Y")

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
        match, timeline = self.api.summoners_last_game(summoner_name)
        match_timestamp = self._convert_unix_timestamp(match.info.game_creation / 1000)
        game_mode = match.info.game_mode
        damage_chart = []
        for participant in match.info.participants:
            damage_chart.append(participant.total_damage_dealt_to_champions)
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

        damage_chart.sort()
        damage_index = damage_chart.index(total_damage_to_champions) + 1

        embed_title = f"__SUMMONER SEARCH__"
        embed_message = f"""**Nick**: {summoner_data.name}
                            **Poziom:** {summoner_data.summoner_level}
                            **Ostatni Mecz:** {match_timestamp}\n**Mode:** {game_mode}
                            **KDA:** {kills}/{deaths}/{assists}\n**Wygrana:** {win}
                            **Champ:** {champion}
                            **Rola:** {role}
                            **Dmg zadany innym:** {total_damage_to_champions}
                            **Miejsce pod wzgledem dmg:** {damage_index}
                            **Polozone wardy**: {wards_placed}
                            **Calkowity dmg przyjety:** {total_damage_taken}
                            **Dmg wyleczony:** {self_healed_damage}
                            **Teammaci wyleczeni:** {teammate_healed_damage}"""

        embed = discord.Embed(title=embed_title, description=embed_message)

        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Tracker(bot))
