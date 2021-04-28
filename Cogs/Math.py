from __future__ import division
import string
from math import *
import discord
import cexprtk
from discord.ext import commands
from sympy import *
import re
import discord
multiply_detect = re.compile("\d[a-z]")
x, y, z, t = symbols("x y z t")
k, m, n = symbols("k m n", integer=True)
f, g, h = symbols("f g h", cls=Function)
init_printing(use_latex=True)


def parse(string: str):
    if "^" in string:
        string = string.replace("^", "**")
    if "(" in string:
        string = re.sub(r"([a-z0-9])(\()",r"\1*\2", string)
    if multiply_detect.search(string):
        string = re.sub(r"([0-9])([a-z])",r"\1*\2", string)
    return string


class Math(commands.Cog, description="Math related commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def math(self,ctx, message: str):
        """Does some math for you!"""
        try:
            x = cexprtk.evaluate_expression(message, {"pi": pi})
            await ctx.message.add_reaction("\N{White Heavy Check Mark}")
            await ctx.send(x)
        except Exception:
            await ctx.message.add_reaction("\N{Cross Mark}")
            print(
                f"[MATH COG] Encountered exception with {message.content}: {Exception}"
            )


    @commands.command()
    async def solve(self, ctx, *, equation):
        """Solves linear equations"""
        parsed_eqn = parse(equation)
        try:
            eqn = solve(parsed_eqn)
        except SyntaxError:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://api.wolframalpha.com/v2/query", params={param}) as f:
                    print(f.url)
                    file = discord.File(io.BytesIO(await f.read()), filename="img.png")
                    embed = discord.Embed()
                    embed.set_image(url="attachment://img.png")

        await ctx.send(eqn)

    @commands.command(aliases=["differentiation","diff",])
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
    async def poisson(self, ctx, lamda, times, Continuous:bool =False, greater_than:bool =False):
        """Gets poisson probability distribution"""
        try:
            r = int(times)
            lam = float(cexprtk.evaluate_expression(lamda, {"pi": pi}))
        except ValueError:
            ctx.send("input a correct average or number")
        if Continuous:
            Sum = []
            for x in range(r+1):
                Sum.append((exp(-lam) * lam ** x) / factorial(x))
            answer = sum(Sum)
        else:
            answer = (exp(-lam) * lam ** r) / factorial(r)
        if greater_than:
            answer = 1-answer

        embed = discord.Embed(
            title="Poisson distribution calculator",
            colour=discord.Color.random(),
            description=f"Answer is: ```{answer}```",
        )
        embed.add_field(name="Lambda", value=f"```{lam}```", inline=False)
        embed.add_field(name="r", value=f"```{r}```", inline=False)
        embed.add_field(name="Continuous?", value=f"```{Continuous}```", inline=False)
        embed.add_field(
            name="Greater than?", value=f"```{greater_than}```", inline=False
        )
        await ctx.send(embed=embed)
    @commands.command()
    async def inverse(self, ctx, eqn):
        eqn = parse(eqn)
        eqn =solve(f"{eqn} - y",x)
        print(eqn)
        await ctx.send(eqn)
def setup(bot):
    bot.add_cog(Math(bot))
