from discord.ext import commands
import discord
import asyncpg
from Cogs.Utils import is_whitelisted
class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @is_whitelisted()
    @commands.command(hidden=True)
    async def addUser(self, ctx, member: discord.Member):
        user = await self.bot.db.fetchrow("SELECT user_id FROM admin WHERE user_id=$1", member.id)
        if not user:
            await self.bot.db.execute("INSERT INTO admin (user_id,username) VALUES ($1, $2)", member.id, member.name)
        else:
            await ctx.send("User already exists")
    @is_whitelisted()
    @commands.command(hidden=True)
    async def removeuser(self, ctx, member: discord.Member):
        await self.bot.db.execute("DELETE FROM admin WHERE user_id=$1", member.id)
def setup(bot):
    bot.add_cog(Database(bot))
