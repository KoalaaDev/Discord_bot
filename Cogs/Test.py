import time
from datetime import datetime

import discord
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    def sm(self, game=None, item, currency="USD"):



def setup(bot):
    bot.add_cog(Test(bot))
