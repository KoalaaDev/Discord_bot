from discord.ext import commands
import discord
import asyncpg
import random
import aiohttp
import sys
import traceback
from .Utils import is_whitelisted
TIME_DURATION_UNITS = (
    ('week', 60*60*24*7),
    ('day', 60*60*24),
    ('hour', 60*60),
    ('min', 60),
    ('sec', 1)
)


def human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def has_voted(self, userID):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.statcord.com/v3/799134976515375154/votes/{userID}",headers={"Authorization": "statcord.com-CJ7dPIXSPIrNecsFqdjB"}) as resp:
                resp = await resp.json()
        return resp.get("didVote")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed= discord.Embed(title=random.choice(["Slow down there!","Chill down"]), description=f"Please wait {human_time_duration(round(error.retry_after))}")
            await ctx.send(embed=embed)


    @commands.command()
    async def register(self, ctx):
        """Register's your user balance!\nDon't fuss if you didn't do this as one will be created for you if you haven't!\nNote: If you already registered this command does nothing"""
        is_registered = await self.bot.db.fetchrow("SELECT user_id FROM userbalance WHERE user_id=$1", ctx.author.id)
        if not is_registered:
            await self.bot.db.execute("INSERT INTO userbalance (user_id, balance) VALUES ($1, $2)", ctx.author.id, 0)
            embed = discord.Embed(title="It seems your new!",description=f"Registering account for {ctx.author.mention}")
            embed.set_footer(text="This message will only appear once!")
            await ctx.send(embed=embed, delete_after=10)

    @commands.cooldown(1,86400,commands.BucketType.user)
    @commands.command()
    async def beg(self, ctx):
        """Get up to 1000 :money_with_wings: for voting us on top.gg"""
        await ctx.invoke(self.register)
        if await self.has_voted(ctx.author.id):
            amount = random.choices([100,200,300,400,500,600,700,800,900,1000],weights=[2,2,2,3,3,3,2,2,1,0.5])
            await self.bot.db.execute("UPDATE userbalance SET balance=balance+$1 WHERE user_id=$2",amount[0],ctx.author.id)
            await ctx.send(embed=discord.Embed(title="Thanks for voting on top.gg!",description=f"{ctx.author.mention} received {amount[0]} :money_with_wings: for voting!"))
        else:
            await ctx.send(embed=discord.Embed(title="You did not vote for us today! :(",description=f"Please vote at [top.gg](https://top.gg/bot/799134976515375154/vote)"))
            ctx.command.reset_cooldown(ctx)
    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        await ctx.invoke(self.register)
        fetch = await self.bot.db.fetchrow("SELECT * FROM userbalance WHERE user_id=$1",ctx.author.id)
        row = fetch.values()
        balance = [x for x in row][1]
        embed = discord.Embed(title=f"{ctx.author.name}'s balance", description=f"Currently you have {balance} :money_with_wings:")
        await ctx.send(embed=embed)
    @is_whitelisted()
    @commands.command(hidden=True)
    async def addtobalance(self, ctx, amount):
        await ctx.invoke(self.register)
        await self.bot.db.execute("UPDATE userbalance SET balance=balance+$1 WHERE user_id=$2",amount,ctx.author.id)
        await ctx.send(embed=discord.Embed(description=f"Added {amount} :money_with_wings:"))

def setup(bot):
    bot.add_cog(Economy(bot))
