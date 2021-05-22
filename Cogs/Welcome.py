import discord
from discord.ext import commands

class Welcome(commands.Cog):
    """Basic Automated Welcome"""
    def __init__(self, bot):
        self.bot = bot
        self.guilds = []
    @commands.Cog.listener()
    async def on_ready():
        print("Welcome")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id in self.guilds:
            embed = discord.Embed(title=f"Welcome to the server!", description="Please read the rules and Hope you enjoy your stay here!")
            await member.send(embed=embed)
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id in self.guilds:
            embed = discord.Embed(title=f"Sad to see you go :(")
            await member.send(embed=embed)

    @commands.group()
    async def welcome(self, ctx):
        pass
    @welcome.command()
    async def toggle(self, ctx):
        if ctx.guild.id not in self.guilds:
            self.guilds.append(ctx.guild.id)
        else:
            self.guilds.remove(ctx.guild.id)

def setup(bot):
    bot.add_cog(Welcome(bot))
