from __future__ import division
import string
from math import *
import discord
import cexprtk
from discord.ext import commands
from sympy import *

x, y, z, t = symbols("x y z t")
k, m, n = symbols("k m n", integer=True)
f, g, h = symbols("f g h", cls=Function)
init_printing(use_latex=True)


def parse(string: str):
    if "^" in string:
        return string.replace("^", "**")
    else:
        return string


class Math(commands.Cog, description="Math related commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: str):
        if not message.author.bot:
            if message.content.startswith(
                string.punctuation
            ) is False and message.content.lower().startswith("calculate"):
                try:
                    x = cexprtk.evaluate_expression(
                        message.content.strip("calculate"), {"pi": pi}
                    )
                    await message.add_reaction("\N{White Heavy Check Mark}")
                    await message.channel.send(x)
                except Exception:
                    await message.add_reaction("\N{Cross Mark}")
                    print(
                        f"[MATH COG] Encountered exception with {message.content}: {Exception}"
                    )
            else:
                pass

    @commands.command()
    async def solve(self, ctx, *, equation):
        """Solves linear equations"""
        eqn = solve(parse(equation))
        await ctx.send(eqn)

    @commands.command(
        aliases=[
            "differentiation",
            "diff",
        ]
    )
    async def differentiate(self, ctx, *, equation):
        eqn = diff(parse(equation))
        await ctx.send(eqn)

    @commands.command()
    async def integrate(self, ctx, *, equation):
        """Sloves integrate equations"""
        eqn = integrate(parse(equation))
        await ctx.send(eqn)

    @commands.command()
    async def factor(self, ctx, *, equation):
        """Solves factor equations"""
        eqn = factor(parse(equation))
        await ctx.send(eqn)

    @commands.command()
    async def expand(self, ctx, *, equation):
        """"Expands 2 factors"""
        eqn = expand(parse(equation))
        await ctx.send(eqn)

    @commands.command()
    async def poisson(self, ctx, lamd, times, iterate=False, greater_than=False):
        """Gets poisson probability distribution"""
        try:
            r = int(times)
            lam = float(cexprtk.evaluate_expression(lamd, {"pi": pi}))
        except ValueError:
            ctx.send("input a correct average or number")
        answer = (exp(-lam) * lam ** r) / factorial(r)
        embed = discord.Embed(
            title="Poisson distribution calculator",
            colour=discord.Color.random(),
            description=f"Answer is: ```{answer}```",
        )
        embed.add_field(name="Lambda", value=f"```{lam}```", inline=False)
        embed.add_field(name="r", value=f"```{r}```", inline=False)
        embed.add_field(name="Iterate", value=f"```{iterate}```", inline=False)
        embed.add_field(
            name="Greater than", value=f"```{greater_than}```", inline=False
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Math(bot))
