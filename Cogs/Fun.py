from discord.ext import commands
import random
import discord
import yaml
import asyncio
import os
from discord.ext.commands.cooldowns import BucketType
from asyncdagpi import Client
import math

class Fun(
    commands.Cog, description="Fun commands such as love calculator, 'Guess that pokemon!' and coin flips"
):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi = Client("ta1fnmIgn85mcfz32UG5nKgVeRWikmaZxZa392f0XwWC4yaDCOGUYPWscbZ5ULbk")
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

    @commands.command()
    async def pepeflip(self, ctx):
        """Sends good luck with a crying or smiling pepe"""
        emoji1 = self.bot.get_emoji(799506321442996235)
        emoji2 = self.bot.get_emoji(742346196990951505)
        lmao = random.choice([emoji1, emoji2])
        bruh = await ctx.send("Good Luck!")
        await bruh.add_reaction(lmao)

    @commands.command(hidden=True)
    async def woohoo(self, ctx):
        gay = random.choice(["Koalaa", "Skot", "Alvin"])
        message = await ctx.send(f"Woohoo {gay} is confirmed gay!")
        emoji = get(client.emojis, name="pepelaugh")
        await message.add_reaction(emoji)
    async def pokemonhints(self, ctx: commands.Context, embed: discord.Embed, obj, message):
        count = 1
        hints = [["Type", ",".join(obj.dict["Data"]["Type"])],["Abilities",",".join(obj.abilities)], ["weight",obj.weight]]
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
                    await ctx.send(f"Wrong Pokemon, {guesses_left} guess remaining!",delete_after=5)
                    continue
                if guesses_left<1:
                    pass
                else:
                    await ctx.send(f"Wrong Pokemon, {guesses_left} guesses remaining!",delete_after=5)
                count+=1
        else:
            embed = discord.Embed(title="You didnt guess it right! :(")
            embed.set_image(url=obj.answer)
            return await ctx.send(embed=embed)
    @commands.command(alias=['wtp'])
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
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
            await self.pokemonhints(ctx, embed, pokemon, message)
    @poke.error
    async def poll_handler(self, ctx, error):
    if isinstance(error, commands.MaxConcurrencyReached):
         await ctx.send(embed=discord.Embed(description="Woah slow down there! Finish your game first!"))
def setup(bot):
    bot.add_cog(Fun(bot))
