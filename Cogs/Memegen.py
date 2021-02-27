from discord.ext import commands
import vacefron
import discord
import random
class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = vacefron.Client()
    @commands.command()
    async def batman_slap(self, ctx, text, text2, batman:discord.Member =None, robin:discord.Member =None):
        if batman and robin:
            img = await self.api.batman_slap(text, text2, batman=batman.avatar_url, robin=robin.avatar_url)
            embed = discord.Embed()
            embed.set_image(url=img.url)
            await ctx.send(embed=embed)
    @commands.command()
    async def distracted(self, ctx, boyfriend:discord.Member = None, girlfriend:discord.Member =None, woman:discord.Member =None):
        img = await self.api.distracted_bf(boyfriend, girlfriend, woman)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def shame(self, ctx, user:discord.Member = None):
        img = await self.api.dock_of_shame(user)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def shame(self, ctx, user:discord.Member = None):
        img = await self.api.dock_of_shame(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def car_reverse(self, ctx, text:discord.Member = None):
        img = await self.api.car_reverse(text.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def eject(self, ctx, member:discord.Member = None):
        imposter = random.choice([True,False])
        img = await self.api.ejected(member.name, crewmate = "random", impostor = imposter)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def rip(self, ctx, member:discord.Member = None):
        img = await self.api.grave(member.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Meme(bot))
