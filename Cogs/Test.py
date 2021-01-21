import time
from datetime import datetime

import discord
from discord.ext import commands

WHITELIST = [line.strip() for line in open('Whitelist.txt','r+', buffering=1)]


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    def isep(self, type, *, what):
        if type == "kontol":
            

def setup(bot):
    bot.add_cog(Test(bot))
