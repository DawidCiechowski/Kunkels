# YET TO BE IMPLEMENTED. GOTTA SCRAP THROUGH CLOUDFLARE SOMEHOW! ALL THE CURRENT LIBRARIES DO NOT WORK
# SADGE
import io
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

import discord
from discord.ext import commands


class M(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="plot")
    async def _plot(self, ctx):
        x = np.linspace(0, 10, 100)
        plt.plot(x, x, label="linear")
        plt.legend()
        fig = plt.gcf()

        def fig_to_image(fig):
            data_stream = io.BytesIO()
            fig.savefig(data_stream)
            data_stream.seek(0)
            image = Image.open(data_stream)
            return image

        pil_image = fig_to_image(fig)
        pil_image.save("test.png")
        embed = discord.Embed(
            title="TEST", description="TEST", color=discord.Color.blue()
        )
        embed.set_image(url="attachment://image.png")
        await ctx.send(embed=embed, file=discord.File("test.png", filename="image.png"))


def setup(bot):
    bot.add_cog(M(bot))
