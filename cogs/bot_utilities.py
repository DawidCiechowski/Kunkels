from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Bot


class BotUtils(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._last_member = None

    @commands.command(pass_context=True)
    async def greet(self, ctx, *, user: discord.Member = None):
        """Says hello

        Args:
            ctx : Channel context
            user (discord.Member): [User]
        """

        member = user or ctx.author

        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f"Hello {member.name}")
        else:
            await ctx.send(f"Hello {member.name}... Feels kind of similiar")

        self._last_member = member

    @commands.command(name="szczekaj", pass_context=True)
    async def _szczekaj(self, ctx):
        await ctx.send(f"{ctx.message.author} Miau?")

    @commands.command(name="mute", aliases=["wycisz", "zamknij ryj", "morda", "stfu"])
    # @commands.has_role("Eddy")
    async def _mute(
        self, ctx, *, member: Optional[discord.Member] = None, time: Optional[int] = 5
    ):
        """Mute a member of a channel

        Args:
            member (Optional[discord.Member], optional): A member to be muted. Defaults to None.
            time (Optional[int]), optional): For how long a user is to be muted
        """
        if member is None:
            message = f"Czerwony **mute** *<Jakas menda>*"
            embed = discord.Embed(
                title="__Uzycie__", description=message, color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

        await ctx.send("Not implemented")

    @commands.command(name="clear", aliases=["wyczysc"])
    async def _clear(self, ctx, *, amount: int = 5):
        """Clear messages from the text channel

        Args:
            amount (int, optional): The amount of messages to remove. Defaults to 5.
        """
        await ctx.channel.purge(limit=int(amount))

    @commands.command(name="ban", aliases=["zbanuj"])
    @commands.has_permissions(ban_members=True)
    async def _ban(
        self,
        ctx,
        *,
        member: Optional[discord.Member] = None,
        reason: Optional[str] = "",
    ):
        """Ban a user from a channel

        Args:
            ctx ([type]): [description]
            member (Optional[discord.Member], optional): A member of discord channel. Defaults to None.
            reason (Optional[str], optional): A reason for banning the user. Defaults to "".
        """
        if member is None:
            message = f"Czerwony **ban** *<Jakas menda>*\nDodatkowe parametry: *<Powod wyjebania>*\nOpcjonalne nazwy komendy: [**zbanuj**]"
            embed = discord.Embed(
                title="__Uzycie__", description=message, color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        await member.ban(reason=reason)

    @commands.command(name="kick", aliases=["wyjeb", "wypierdol", "wykop"])
    @commands.has_permissions(kick_members=True)
    async def _kick(
        self,
        ctx,
        *,
        member: Optional[discord.Member] = None,
        reason: Optional[str] = "",
    ):
        """Kick a user from discord channel

        Args:
            ctx ([type]): [description]
            member (Optional[discord.Member], optional): A member of a Discord. Defaults to None.
            reason (Optional[str], optional): A reason for kicking the user. Defaults to "".
        """
        if member is None:
            message = f"Czerwony **kick** *<Jakas menda>*\nDodatkowe parametry: *<Powod wyjebania>*\nOpcjonalne nazwy komendy: [**wypierdol**, **wyjeb**, **wykop**]"
            embed = discord.Embed(
                title="__Uzycie__", description=message, color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="Wypierdolenie",
            description=f"{ctx.message.author.name} wyjebal {member.name}. Powod:\n{reason}",
            color=discord.Color.dark_magenta,
        )
        await ctx.send(embed=embed)
        await member.kick(reason=reason)

    @commands.command(name="unban", aliases=["odbanuj"])
    @commands.has_permissions(unban_members=True)
    async def _unban(self, ctx, *, member: Optional[discord.Member] = None):
        if member is None:
            message = f"Czerwony **unban** *<Jakas menda>*\nOpcjonalne nazwy komendy: [**odbanuj**]"
            embed = discord.Embed(
                title="__Uzycie__", description=message, color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="Odpierdolenie",
            description=f"{ctx.message.author.name} przywrocil {member.name}.",
            color=discord.Color.dark_magenta,
        )
        await ctx.send(embed=embed)
        await member.unban()


def setup(bot):
    bot.add_cog(BotUtils(bot))
