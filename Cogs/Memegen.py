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
        img = await self.api.distracted_bf(boyfriend.avatar_url, girlfriend.avatar_url, woman.avatar_url)
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
    async def table_flip(self, ctx, user:discord.Member = None):
        img = await self.api.table_flip(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def first_time(self, ctx, user:discord.Member = None):
        img = await self.api.first_time(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def heaven(self, ctx, user:discord.Member = None):
        img = await self.api.heaven(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def npc(self, ctx, user:discord.Member = None):
        img = await self.api.npc(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def stonks(self, ctx, user:discord.Member = None):
        img = await self.api.stonks(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def wolverine(self, ctx, user:discord.Member = None):
        img = await self.api.wolverine(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def widen(self, ctx, user:discord.Member = None):
        img = await self.api.wide(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def speedy(self, ctx, user:discord.Member = None):
        img = await self.api.iam_speed(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def milk(self, ctx, user:discord.Member = None, user2:discord.Member = None):
        img = await self.api.i_can_milk_you(user.avatar_url, user2 = user2.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def car_reverse(self, ctx, *, text:str = None):
        img = await self.api.car_reverse(text)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def water(self, ctx, *, text:str = None):
        img = await self.api.water(text)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def emergency(self, ctx, *, text:str = None):
        img = await self.api.emergency_meeting(text)
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
