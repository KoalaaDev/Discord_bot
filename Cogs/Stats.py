from discord.ext import commands
import asyncio
import discord
from Cogs.Utils import is_whitelisted
class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @is_whitelisted()    
    @commands.command()
    async def UserCommand(self, ctx, member:discord.Member):
        fetchuser = await self.bot.db.fetchrow("SELECT user_id FROM command WHERE user_id = $1", member.id)
        print(fetchuser.values())


def setup(bot):
    bot.add_cog(Stats(bot))
