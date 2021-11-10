import os
from dataclasses import dataclass, field
from os import name
from typing import Any, List, Dict

import requests
from dataclasses_json import dataclass_json, config
import discord
from discord.ext.commands import Bot
from discord.ext import commands


WEATHERS = {
    "Clouds": "☁️",
    "Sun": "☀️",
    "Sunny": "☀️",
    "Rain": "🌧️",
    "Tornado": "🌪️",
    "Fog": "🌫️",
    "Foggy": "🌫️",
    "Snow": "🌨️",
}
WEATHER_API_HOST = os.getenv("WEATHER_API_HOST")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


@dataclass_json
@dataclass
class WeatherInfo:
    coord: Dict[str, float]
    weather: List[Dict[str, Any]]
    base: str
    main: Dict[str, Any]
    visibility: int
    wind: Dict[str, Any]
    clouds: Dict[str, Any]
    dt: int
    sys: Dict[str, Any]
    timezone: int
    call_id: str = field(metadata=config(field_name="id"))
    name: str
    cod: int


class Weather(commands.Cog):

    __slots__ = ["city"]

    def __init__(self, bot: Bot):
        self.bot = bot

    def __weather_api_call(self, city: str) -> Any:
        URL = "https://community-open-weather-map.p.rapidapi.com/weather"
        querystring = {"q": city, "units": "metric"}
        headers = {
            "x-rapidapi-host": WEATHER_API_HOST,
            "x-rapidapi-key": WEATHER_API_KEY,
        }

        return requests.get(URL, headers=headers, params=querystring)

    @commands.command(
        name="weather",
        aliases=["pogoda", "dla Anheliona"],
        description="Returns weather report for given city",
    )
    async def _weather(self, ctx, *city: str) -> discord.Embed:

        if not city:
            title = "BLAD! XXXXXXXXX"
            message = "PODAJ KURWA MIASTO!\n\nFUNKCJI UZYWA SIE TAK\n\n```Czerwony weather London```"
            error_embed = discord.Embed(
                title=title, description=message, color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            return

        city = "".join(city)
        weather_info = WeatherInfo.from_dict(self.__weather_api_call(city).json())

        if not weather_info:
            title = "BLAD! XXXXXXXXXXXXXXXXXXXXX"
            message = "WYGLADA NA TO, ZE SIE WYJEBALEM ROBIAC TEGO CALLA LUB PODALES CHUJOWE MIASTO\nNARA"
            error_embed = discord.Embed(
                title=title, description=message, color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            return

        title = f"Pogoda dla {city}"
        message = f"""
        **Pogoda**: {WEATHERS[weather_info.weather[0]['main']]}
        **Temperatura**: {weather_info.main["temp"]}°C
        **Odczuwalna**: {weather_info.main["feels_like"]}°C
        **Cisnienie**: {weather_info.main["pressure"]}hPa
        **Widocznosc**: {weather_info.visibility}
        **Predkosc wiatru**: {weather_info.wind["speed"]}km/h
        **Kierunek wiatru**: {weather_info.wind["deg"]}°
        """

        embed_message = discord.Embed(
            title=title, description=message, color=discord.Color.blue()
        )
        await ctx.send(embed=embed_message)


def setup(bot: Bot):
    bot.add_cog(Weather(bot))
