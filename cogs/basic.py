import discord
from discord.ext import commands
from discord.ext.commands import Bot

class Greetings(commands.Cog):
    
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
        
        
def setup(bot):
    bot.add_cog(Greetings(bot))