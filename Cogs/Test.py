import time
from datetime import datetime

import discord
from discord.ext import commands

import random


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jason(self, ctx):
        await ctx.message.delete()
        embed1 = "https://cdn.discordapp.com/attachments/263190635434082315/803952123237761024/Jason_hanging_out_on_a_swing.jpg"
        embed2 = "https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed3 = "https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed = discord.Embed(title="Surpirse!", colour=discord.Colour.blue())
        embed.set_image(url=random.choice([embed1, embed2, embed3]))
        await ctx.send(embed=embed, delete_after=5)


def setup(bot):
    bot.add_cog(Test(bot))
