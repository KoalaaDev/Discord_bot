from discord.ext import commands
import aiohttp
import discord
import sys
import traceback
import random
class API(commands.Cog, description="Random generator commands"):
    def __init__(self, bot):
        self.bot = bot
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            try:
                return await ctx.send(
                    embed=discord.Embed(description="This can only be used in NSFW channels!")
                )
            except discord.HTTPException:
                pass
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )
    async def getJSON(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as f:
                return await f.json()
    @commands.command()
    async def cat(self, ctx):
        """Gives a random cat picture"""  # Alvin be like meow meow *while sucking staff*
        if ctx.author.id == 451008924032827395 or ctx.author.id == 351664300009586688 or ctx.author.id == 267250931144458257 or ctx.author.id == 263190106821623810 or ctx.author.id == 546667581189128194:
            embed1 = "https://cdn.discordapp.com/attachments/541880222065098762/812999751339474954/alvin_lol.JPG"
            embed2 = "https://media.discordapp.net/attachments/664404159340085248/827191995160068116/Homepage_Panel_form_946x577_TC2.png?width=775&height=473"
            embed3 = "https://cdn.discordapp.com/attachments/664404159340085248/827599168922845204/image0.jpg"
            embed4 = "https://cdn.discordapp.com/attachments/664404159340085248/827599283929743380/20210301_153915.jpg"
            embed5 = "https://cdn.discordapp.com/attachments/664404159340085248/827599325827170334/IMG_20210325_153718.jpg"
            embed6 = "https://cdn.discordapp.com/attachments/664404159340085248/827599353978945576/IMG_20210302_153549.jpg"
            embed = discord.Embed(title="Random Cat", colour=discord.Colour.purple())
            embed.set_image(url=random.choice([embed1, embed2, embed3, embed4, embed5, embed6]))
        else:
            pic = await self.getJSON(f"https://aws.random.cat/meow")
            embed = discord.Embed(title="Random Cat", Colour=discord.Colour.purple())
            embed.set_image(url=pic["file"])
            embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)
    @commands.command()
    async def reddit(self, ctx, subreddit):
        """Get a random post from a subreddit"""
        data = await self.getJSON(f"https://api.iapetus11.me/reddit/gimme/{subreddit}")
        if data.get("success"):
            if data.get("nsfw") and not ctx.message.channel.is_nsfw():
                raise commands.NSFWChannelRequired(ctx.message.channel)
            elif data.get("nsfw") and ctx.message.channel.is_nsfw():
                embed = discord.Embed(title=data.get("title"))
                embed.set_image(url=data.get("image"))
                embed.set_footer(text=f"{data.get('upvotes')} ⬆️ | {data.get('downvotes')} ⬇️")
                await ctx.send(embed=embed)
            elif not data.get("nsfw"):
                embed = discord.Embed(title=data.get("title"))
                embed.set_image(url=data.get("image"))
                embed.set_footer(text=f"{data.get('upvotes')} ⬆️ | {data.get('downvotes')} ⬇️")
                await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(description="No posts found!"))
    @commands.command()
    async def dog(self, ctx):
        """Gives a random dog picture"""  # lincoln is dog woof woof
        pic = await self.getJSON("https://some-random-api.ml/img/dog")
        embed = discord.Embed(title="Random Dog", Colour=discord.Colour.random())
        embed.set_image(url=pic["link"])
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)
    @commands.is_nsfw()
    @commands.command()
    async def img(self, ctx, *, query):
        """Google searches your img (due to limitation only nsfw channels can use this)"""
        pic = await self.getJSON(f"https://normal-api.ml/image-search?query={query}&redirect=false")
        embed = discord.Embed(title=query, Colour=discord.Colour.random())
        embed.set_image(url=pic["image"])
        embed.set_footer(text="Img Gen Service")
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    async def insult(self, ctx, lang="en"):
        """Generates an insult in a specified language"""  # Why bully each other?
        params = {"lang": lang, "type": "json"}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://evilinsult.com/generate_insult.php", params=params
            ) as f:
                insult = await f.json()
        embed = discord.Embed(title=insult["insult"], Colour=discord.Colour.random())
        embed.set_footer(text=f"{lang} Insult Gen Service")
        await ctx.send(embed=embed)

    @commands.command()
    async def rabbit(self, ctx):
        """Gives a random rabbit picture"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.bunnies.io/v2/loop/random/?media=gif,png"
            ) as f:
                pic = await f.json()
        embed = discord.Embed(title="Random Rabbit", Colour=discord.Colour.random())
        embed.set_image(url=pic["media"]["gif"])
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)

    @commands.command()
    async def duck(self, ctx):
        """Gives a random duck picture"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://random-d.uk/api/v1/random?type=png") as f:
                pic = await f.json()
        embed = discord.Embed(title="Random duck", Colour=discord.Colour.random())
        embed.set_image(url=pic["url"])
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(API(bot))
