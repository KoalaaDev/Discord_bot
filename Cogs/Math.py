from __future__ import division

from math import *

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
    elif "**" in string:
        return string.replace("**", "^")
    else:
        return string


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: str):
        if not message.author.bot:
            if message.content.startswith(
                    "-") is False and message.content[0].isdigit() is True:
                try:
                    x = cexprtk.evaluate_expression(message.content,
                                                    {"pi": pi})
                    print(message.content)
                    await message.channel.send(x)
                    await message.add_reaction('\N{White Heavy Check Mark}')
                except Exception:
                    await message.add_reaction('\N{Cross Mark}')

    @commands.command()
    async def HorFOV(self, ctx, VFOV, aspectRatio):
        aspectRatio = aspectRatio.split("/")
        horizontalFOV = (2 * atan(degrees(tan(float(VFOV) / 2))) *
                         (int(aspectRatio[0]) / int(aspectRatio[1])))

        await ctx.send(horizontalFOV)

    @commands.command()
    async def solve(self, ctx, *, equation):
        eqn = solve(parse(equation))
        await ctx.send(parse(eqn))

    @commands.command(aliases=[
        "differentiation",
        "diff",
    ])
    async def differentiate(self, ctx, *, equation):
        eqn = diff(parse(equation))
        await ctx.send(parse(eqn))

    @commands.command()
    async def integrate(self, ctx, *, equation):
        eqn = integrate(parse(equation))
        await ctx.send(parse(eqn))

    @commands.command()
    async def factor(self, ctx, *, equation):
        eqn = factor(parse(equation))
        await ctx.send(parse(eqn))

    @commands.command()
    async def latex(self, ctx, *, equation):
        expre = sympify(parse(equation), evaluate=False)
        preview(expre, viewer="file", filename="output.png")
        await ctx.send(file=discord.File(
            f"./output.png", filename="LaTeX_output.png", viewer='gimp'))


def setup(bot):
    bot.add_cog(Math(bot))
