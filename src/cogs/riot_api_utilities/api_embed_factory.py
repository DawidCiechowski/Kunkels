from abc import ABC, abstractmethod
import io
from datetime import datetime

import discord
from discord.embeds import Embed
import matplotlib.pyplot as plt
from PIL import Image

from cogs.riot_api_utilities.riot_api import RiotApi
from cogs.riot_api_utilities.api_dataclasses.champion import champions_data


class UnknownTypeException(Exception):
    """Raised when factory is given an unknown type"""


class ApiEmbed(ABC):
    @abstractmethod
    def create_embed(self) -> discord.Embed:
        pass

    def _figure_to_image(self, figure) -> Image:
        """Protected function, converting matplotlib figure into pillow Image

        Args:
            figure (matplotlib.pyplot.figure): Matplotlib figure

        Returns:
            Image: A figure converted into pillow Image
        """

        data_stream = io.BytesIO()
        figure.savefig(data_stream)
        data_stream.seek(0)
        image = Image.open(data_stream)
        return image

    @staticmethod
    def _convert_unix_timestamp(timestamp: int) -> str:
        return datetime.utcfromtimestamp(timestamp / 1000).strftime("%H:%M %d-%m-%y")


class DamageEmbedApi(ApiEmbed):
    def __init__(self, api: RiotApi, summoner: str):
        self.api = api
        self.summoner = summoner

    def create_embed(self) -> discord.Embed:
        summoner = self.api.summoner_search(self.summoner)
        matches, _ = self.api.get_summoner_games(self.summoner)
        matches_dates = []
        damage_stats = []

        for match in matches:
            for participant in match.info.participants:

                if summoner.puuid == participant.puuid:
                    damage_stats.append(participant.total_damage_dealt_to_champions)

            matches_dates.append(
                self._convert_unix_timestamp(match.info.game_start_timestamp)
            )

        figure = plt.figure()

        plt.bar(matches_dates[::-1], damage_stats[::-1], color="maroon", width=0.5)
        # Rotate x labels by 30 degrees
        figure.autofmt_xdate(ha="right")

        pil_image = self._figure_to_image(figure)
        pil_image.save("test.png")
        embed = discord.Embed(
            title="Damage",
            description=f"Damage zadany przez: {summoner.name}",
            color=discord.Color.blue(),
        )
        embed.set_image(url="attachment://image.png")

        plt.clf()

        return embed


class DefenseEmbedApi(ApiEmbed):
    def __init__(self, api: RiotApi, summoner: str):
        self.api = api
        self.summoner = summoner

    def create_embed(self) -> discord.Embed:
        summoner = self.api.summoner_search(self.summoner)
        matches, _ = self.api.get_summoner_games(self.summoner)
        matches_dates = []
        defensive_stats = []

        for match in matches:
            for participant in match.info.participants:

                if summoner.puuid == participant.puuid:
                    defensive_stats.append(
                        participant.total_damage_taken
                        + participant.damage_self_mitigated
                    )

            matches_dates.append(
                self._convert_unix_timestamp(match.info.game_start_timestamp)
            )

        figure = plt.figure()

        plt.bar(matches_dates[::-1], defensive_stats[::-1], color="darkblue", width=0.5)
        # Rotate x labels by 30 degrees
        figure.autofmt_xdate(ha="right")
        plt.ylabel("Damage przyjety")
        plt.title(f"Damage przyjety przez: {summoner.name}")
        pil_image = self._figure_to_image(figure)
        pil_image.save("test.png")
        embed = discord.Embed(
            title="Def",
            description=f"Damage przyjety przez: {summoner.name}",
            color=discord.Color.blue(),
        )
        embed.set_image(url="attachment://image.png")

        plt.clf()

        return embed


class KdaEmbedApi(ApiEmbed):
    def __init__(self, api: RiotApi, summoner: str) -> None:
        self.api = api
        self.summoner = summoner

    def create_embed(self) -> discord.Embed:
        summoner = self.api.summoner_search(self.summoner)
        matches, _ = self.api.get_summoner_games(self.summoner)
        kills, deaths, assists = [], [], []
        matches_dates = []

        for match in matches:
            [
                (
                    kills.append(participant.kills),
                    deaths.append(participant.deaths),
                    assists.append(participant.assists),
                )
                for participant in match.info.participants
                if participant.puuid == summoner.puuid
            ]

            matches_dates.append(self._convert_unix_timestamp(match.info.game_creation))

        if kills and deaths and assists:
            plt.plot(matches_dates[::-1], kills[::-1], "b--", label="Kills")
            plt.plot(matches_dates[::-1], deaths[::-1], "r--", label="Deaths")
            plt.plot(matches_dates[::-1], assists[::-1], "g:", label="Assists")
            plt.legend()

        figure = plt.gcf()
        # Rotate x labels by 30 degrees
        figure.autofmt_xdate(ha="right")

        plt.title(
            f"KDA: Srednie = {round(sum(kills)/len(kills), 1)}/{round(sum(deaths)/len(deaths), 1)}/{round(sum(assists)/len(assists), 1)}"
        )
        pil_image = self._figure_to_image(figure)
        pil_image.save("test.png")
        embed = discord.Embed(
            title="KDA",
            description=f"KDA dla {summoner.name}",
            color=discord.Color.blue(),
        )
        embed.set_image(url="attachment://image.png")

        plt.clf()

        return embed


class SummonerEmbedApi(ApiEmbed):
    def __init__(self, api: RiotApi, summoner: str):
        self.api = api
        self.summoner = summoner

    def create_embed(self) -> discord.Embed:
        try:
            summoner_data = self.api.summoner_search(self.summoner)
        except Exception as err:
            return
        match, _ = self.api.summoners_last_game(self.summoner)
        match_timestamp = self._convert_unix_timestamp(match.info.game_creation)
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
        embed_message = f"""
```ini
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
                            **Polozone wardy**: {wards_placed}
                            """

        return discord.Embed(
            title=embed_title, description=embed_message, color=discord.Color.blue()
        )


class SpectateEmbedApi(ApiEmbed):
    def __init__(self, api: RiotApi, summoner: str):
        self.api = api
        self.summoner = summoner

    def create_embed(self) -> discord.Embed:
        """Generate a discord.Embed from spectate data.
        Ritos api is so freeaking baaaad, it literally doesnt give any useful information

        Args:
        -----
            summoner_name (str): A name of a summoner, to search data for

        Returns:
        -------
            discord.Embed: An embedded message generated from data, or a simple embed showcasing the player is not currently in-game
        """
        game_data = self.api.summoners_current_game(self.summoner)

        if not game_data:
            return False, None

        # ------------------------ Game Data -----------------------------------
        summoner_data = [
            participant
            for participant in game_data.participants
            if participant.summoner_name.lower() == self.summoner.lower()
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


class EmbedFactory:
    @staticmethod
    def factory_embed(type: str, api: RiotApi, summoner: str) -> ApiEmbed:
        if type.lower() == "damage":
            return DamageEmbedApi(api, summoner)
        elif type.lower() == "defense":
            return DefenseEmbedApi(api, summoner)
        elif type.lower() == "kda":
            return KdaEmbedApi(api, summoner)
        elif type.lower() == "summoner":
            return SummonerEmbedApi(api, summoner)
        elif type.lower() == "spectate":
            return SpectateEmbedApi(api, summoner)
        else:
            raise UnknownTypeException(f"{type} doesn't exists within factory")
