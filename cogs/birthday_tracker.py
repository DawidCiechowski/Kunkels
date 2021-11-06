from typing import Any, Dict
from datetime import datetime as dt

from discord.ext import tasks, commands
import discord


class BirthdayTracker(commands.Cog):

    __slots__ = ["bot", "birthdays"]

    def __init__(self, bot):
        self.bot = bot
        self.birthdays = self.set_birthdays()
        self._birthday_wisher.start()

    def set_birthdays(self) -> Dict[str, Any]:
        birthdays = {
            "Pyrcio": dt(year=1996, month=10, day=13),
            "Anhelion": dt(year=1996, month=11, day=6),
            "Kosa": dt(year=1996, month=5, day=15),
            "Ciacho": dt(year=1996, month=10, day=28),
        }

        return birthdays

    @staticmethod
    def __generate_birthday_embed(name, date) -> discord.Embed:
        today = dt.now()
        title = f"Wszystkieg najlepeszego {name}!"

        message = f"{name}!]\nWszystkiego najlepszego z okazji {today.year - date.year} urodzin! 🥳🥳🥳"

        return discord.Embed(
            title=title, description=message, color=discord.Color.orange()
        )

    @tasks.loop(hours=24)
    async def _birthday_wisher(self):
        channel = discord.utils.get(self.bot.get_all_channels(), name="birthday-wisher")
        now = dt.now()

        for key, value in self.birthdays.items():
            if now.month == value.month and now.day == value.day:
                await channel.send(embed=self.__generate_birthday_embed())

    @_birthday_wisher.before_loop
    async def awaitBot(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(BirthdayTracker(bot))
