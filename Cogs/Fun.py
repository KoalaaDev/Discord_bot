from discord.ext import commands
import random
import discord
import yaml
import asyncio
import os
from discord.ext.commands.cooldowns import BucketType
from asyncdagpi import Client
import math
from bs4 import BeautifulSoup
import aiohttp

class Fun(
    commands.Cog, description="Fun commands such as love calculator, 'Guess that pokemon!' and coin flips"
):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi = Client("ta1fnmIgn85mcfz32UG5nKgVeRWikmaZxZa392f0XwWC4yaDCOGUYPWscbZ5ULbk")
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(embed=discord.Embed(description="Woah slow down there! Finish your game first!"))
    @commands.command(hidden=True)
    async def jason(self, ctx):
        await ctx.message.delete()
        embed1 = "https://cdn.discordapp.com/attachments/263190635434082315/803952123237761024/Jason_hanging_out_on_a_swing.jpg"
        embed2 = "https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed3 = "https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed = discord.Embed(title="Surpirse!", colour=discord.Colour.blue())
        embed.set_image(url=random.choice([embed1, embed2, embed3]))
        await ctx.send(embed=embed, delete_after=5)

    @commands.command()
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    async def hints(self, ctx: commands.Context, embed: discord.Embed, obj, message, theme, hints):
        count = 1
        await ctx.send("Wrong answer, you have 3 guesses left!",delete_after=5)
        for i in hints:
            embed.add_field(name=i[0], value=f"{i[1]}")
            await message.edit(embed=embed)
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author
            try:
                guess = await self.bot.wait_for('message',check=check,timeout=15)
            except asyncio.TimeoutError:
                embed = discord.Embed(title="You didnt guess it on time :(")
                embed.set_image(url=obj.answer)
                return await ctx.send(embed=embed)
            if guess.content.title() == obj.name:
                return await guess.add_reaction("\N{White Heavy Check Mark}")
            else:
                guesses_left = len(hints)-count
                if guesses_left == 1:
                    await ctx.send(f"Wrong {theme}, {guesses_left} guess remaining!",delete_after=5)
                if guesses_left<1:
                    pass
                else:
                    await ctx.send(f"Wrong {theme}, {guesses_left} guesses remaining!",delete_after=5)
                count+=1
        else:
            embed = discord.Embed(title="You didnt guess it right! :(")
            embed.set_image(url=obj.answer)
            return await ctx.send(embed=embed)

    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    @commands.command(aliases=['wtp'])
    async def poke(self, ctx):
        """Starts a pokemon guessing game!"""
        pokemon = await self.dagpi.wtp()
        embed = discord.Embed(title=f"Hey {ctx.author.name}, Guess that Pokemon!")
        embed.set_image(url=pokemon.question)
        message = await ctx.send(embed=embed)
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            guess = await self.bot.wait_for('message',check=check,timeout=30)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="You didnt guess it on time :(")
            embed.set_image(url=pokemon.answer)
            return await ctx.send(embed=embed)
        if guess.content.title() == pokemon.name:
            return await guess.add_reaction("\N{White Heavy Check Mark}")
        else:
            await self.hints(ctx, embed, pokemon, message, "Pokemon", [["Type", ",".join(pokemon.dict["Data"]["Type"])],["Abilities",",".join(pokemon.abilities)], ["weight",pokemon.weight]])
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    @commands.command()
    async def logo(self, ctx):
        """Guess the logo"""
        logo = await self.dagpi.logo()
        embed = discord.Embed(title=f"Hey {ctx.author.name}, Guess that Logo!", description=f"```{logo.hint}```")
        embed.set_image(url=logo.question)
        message = await ctx.send(embed=embed)
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            guess = await self.bot.wait_for('message',check=check,timeout=30)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="You didnt guess it on time :(")
            embed.set_image(url=logo.answer)
            return await ctx.send(embed=embed)
        if guess.content.lower() == logo.brand.lower():
            return await guess.add_reaction("\N{White Heavy Check Mark}")
        else:
            embed = discord.Embed(title="You didnt guess it right! :(",description=f"```{logo.brand}```")
            embed.set_image(url=logo.answer)
            return await ctx.send(embed=embed)
    @commands.command()
    async def pickup(self, ctx):
        """Get a pickup line to pickup girls!"""
        pickup = await self.dagpi.pickup_line()
        embed = discord.Embed(title=pickup.line)
        embed.set_footer(text=f"Category: {pickup.category}")
        await ctx.send(embed=embed)
    @commands.command()
    async def fact(self, ctx):
        """Get a random fun fact"""
        fact = await self.dagpi.fact()
        embed = discord.Embed(title=fact)
        await ctx.send(embed=embed)
    @commands.command()
    async def joke(self, ctx):
        """Get a random joke for fun!"""
        joke = await self.dagpi.joke()
        embed = discord.Embed(title=joke)
        await ctx.send(embed=embed)
    @commands.command()
    async def roast(self, ctx):
        """Get a random joke for fun!"""
        roast = await self.dagpi.roast()
        embed = discord.Embed(title=roast)
        await ctx.send(embed=embed)
    @commands.command()
    async def yomama(self, ctx):
        """Get a Yo mama joke"""
        yomama = await self.dagpi.yomama()
        embed = discord.Embed(title=yomama)
        await ctx.send(embed=embed)
    @commands.command(aliases=["lovecalc"])
    async def lovecalculator(
        self, ctx: commands.Context, lover: discord.Member, loved: discord.Member
    ):
        """Calculate the love percentage!"""

        x = lover.display_name
        y = loved.display_name

        url = "https://www.lovecalculator.com/love.php?name1={}&name2={}".format(
            x.replace(" ", "+"), y.replace(" ", "+")
        )
        async with aiohttp.ClientSession(headers={"Connection": "keep-alive"}) as session:
            async with session.get(url, ssl=False) as response:
                resp = await response.text()
        print(resp)
        soup_object = BeautifulSoup(resp, "html.parser")

        description = soup_object.find("div", class_="result__score").get_text()

        if description is None:
            description = "Dr. Love is busy right now"
        else:
            description = description.strip()

        result_image = soup_object.find("img", class_="result__image").get("src")

        result_text = soup_object.find("div", class_="result-text").get_text()
        result_text = " ".join(result_text.split())

        try:
            z = description[:2]
            z = int(z)
            if z > 50:
                emoji = "❤"
            else:
                emoji = "💔"
            title = f"Dr. Love says that the love percentage for {x} and {y} is: {emoji} {description} {emoji}"
        except (TypeError, ValueError):
            title = "Dr. Love has left a note for you."

        em = discord.Embed(
            title=title, description=result_text, color=discord.Color.red(), url=url
        )
        em.set_image(url=f"https://www.lovecalculator.com/{result_image}")
        await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Fun(bot))
