from discord.ext import commands
import requests
import discord

class API(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        pic = requests.get("https://aws.random.cat/meow").json()['file']
        embed = discord.Embed(title="Random Cat",Colour=discord.Colour.random())
        embed.set_image(url=pic)
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)
    @commands.command()
    async def dog(self, ctx):
        pic = requests.get("https://random.dog/woof.json").json()['url']
        embed = discord.Embed(title="Random Dog",Colour=discord.Colour.random())
        embed.set_image(url=pic)
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)

    @commands.command()
    async def fox(self, ctx):
        pic = requests.get("https://randomfox.ca/floof/").json()['image']
        embed = discord.Embed(title="Random Fox",Colour=discord.Colour.random())
        embed.set_image(url=pic)
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)
    @commands.command()
    async def insult(self, ctx, lang="en"):
        params = {"lang":lang,"type":"json"}
        insult = requests.get("https://evilinsult.com/generate_insult.php",params=params).json()
        embed = discord.Embed(title=insult["insult"],Colour=discord.Colour.random())
        embed.set_footer(text=f"{lang} Insult Gen Service")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(API(bot))
