from discord.ext import tasks, commands


class Tasker(commands.Cog):

    __slots__ = ["bot", "index"]

    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=7.0)
    async def printer(self):
        self.index += 1


def setup(bot):
    bot.add_cog(Tasker(bot))
