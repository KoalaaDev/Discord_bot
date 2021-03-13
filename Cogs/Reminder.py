import discord
from discord.ext import commands
import random
import asyncio
import datetime
class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['RemindMe'])
    async def RemindMe(self, ctx, time: int = 5, *,message: str ):
        """Remind you of something"""
        await ctx.message.delete()
        remindertime = await ctx.send(f"I will remind you in {time} seconds: {message}")
        await asyncio.sleep(time)
        await ctx.send(f"Reminder for {ctx.author.mention} : {message}")
def setup(bot):
    bot.add_cog(Reminder(bot))

#Made by DebuggingMySelf
