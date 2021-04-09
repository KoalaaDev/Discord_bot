from discord.ext import commands
import vacefron
import aiohttp
import discord
import random
import io
import sys
import traceback
from asyncdagpi import Client, ImageFeatures


class Meme(commands.Cog, description="Generate memes and more!"):
    def __init__(self, bot):
        self.bot = bot
        self.api = vacefron.Client()
        self.dagpi = Client("ta1fnmIgn85mcfz32UG5nKgVeRWikmaZxZa392f0XwWC4yaDCOGUYPWscbZ5ULbk")
    async def session(self, url, param: dict = None):
        if param is None:
            param = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=param) as f:
                print(f.url)
                file = discord.File(io.BytesIO(await f.read()), filename="img.png")
                embed = discord.Embed()
                embed.set_image(url="attachment://img.png")
                return embed, file
    async def dagpiSession(self, effect, member, **kwargs):
        url = str(member.avatar_url_as(format=None, static_format="png", size=1024))
        img = await self.dagpi.image_process(effect, url, **kwargs)
        print(img.format)
        file = discord.File(fp=img.image,filename=f"image.{img.format}")
        embed = discord.Embed()
        embed.set_image(url=f"attachment://image.{img.format}")
        return file, embed
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            try:
                return await ctx.send(
                    embed=discord.Embed(description=f"Oops! Missing {error.param.name}, try run help on the command.")
                )
            except discord.HTTPException:
                pass
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )
    @commands.command()
    async def pixel(self, ctx, User:discord.Member):
        """Pixelates someone's profile picture"""
        pic, e = await self.dagpiSession(ImageFeatures.pixel(),User)
        await ctx.send(file=pic,embed=e)
    @commands.command()
    async def obama(self, ctx, User:discord.Member):
        """Gives someone an award awarded by himself"""
        pic, e = await self.dagpiSession(ImageFeatures.obama(),User)
        await ctx.send(file=pic,embed=e)
    @commands.command()
    async def satan(self, ctx, User:discord.Member):
        """Makes someone satan"""
        pic, e = await self.dagpiSession(ImageFeatures.satan(),User)
        await ctx.send(file=pic,embed=e)
    @commands.command()
    async def bad(self, ctx, User:discord.Member):
        """Bad bad bad"""
        pic, e = await self.dagpiSession(ImageFeatures.bad(),User)
        await ctx.send(file=pic,embed=e)
    @commands.command()
    async def sith(self, ctx, User:discord.Member):
        """Makes someone a sith lord"""
        pic, e = await self.dagpiSession(ImageFeatures.sith(),User)
        await ctx.send(file=pic,embed=e)
    @commands.command()
    async def fedora(self, ctx, User:discord.Member):
        """*Tips fedora"""
        pic, e = await self.dagpiSession(ImageFeatures.fedora(),User)
        await ctx.send(file=pic,embed=e)
    @commands.command()
    async def whyareyougay(self, ctx, User:discord.Member, User2:discord.Member):
        """wHy aRe U gAy"""
        pic, e = await self.dagpiSession(ImageFeatures.why_are_you_gay(),User, url2=str(User2.avatar_url_as(format=None, static_format="png", size=1024)))
        await ctx.send(file=pic,embed=e)
    @commands.command()
    async def five_guys_one_girl(self, ctx, User:discord.Member, User2:discord.Member):
        """Difficult to explain..."""
        pic, e = await self.dagpiSession(ImageFeatures.five_guys_one_girl(),User, url2=str(User2.avatar_url_as(format=None, static_format="png", size=1024)))
        await ctx.send(file=pic,embed=e)
    @commands.command()
    async def angel(self, ctx, User:discord.Member):
        """Turns someone to an angel"""
        pic, e = await self.dagpiSession(ImageFeatures.angel(),User)
        await ctx.send(file=pic,embed=e)
    @commands.command(aliases=['ussr'])
    async def communism(self, ctx, User:discord.Member):
        """For mother russia"""
        img, embed = await self.dagpiSession(ImageFeatures.communism(),User)
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def usa(self, ctx, User:discord.Member):
        """American patriotism"""
        img, embed = await self.dagpiSession(ImageFeatures.america(),User)
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def meme(self, ctx):
        """Gets a random meme"""
        embed, img = await self.session("https://api.cool-img-api.ml/meme")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def achievement(self, ctx, *, text:str):
        """Generates a minecraft achievement with the given text"""
        img = await self.session("https://api.cool-img-api.ml/achievement",{'text':text})
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def calling(self, ctx, *, text:str):
        img = await self.session("https://api.cool-img-api.ml/calling",{'text':text})
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def captcha(self, ctx, *, text:str):
        """Generates a Google Captcha with the given text"""
        img = await self.session("https://api.cool-img-api.ml/captcha",{'text':text})
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def challenge(self, ctx, *, text:str):
        img = await self.session("https://api.cool-img-api.ml/challenge",{'text':text})
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def clyde(self, ctx, *, text:str):
        img = await self.session("https://api.cool-img-api.ml/clyde",{'text':text})
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def facts(self, ctx, *, text:str):
        img = await self.session("https://api.cool-img-api.ml/facts",{'text':text})
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def scroll(self, ctx, *, text:str):
        img = await self.session("https://api.cool-img-api.ml/scroll",{'text':text})
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def alwayshasbeen(self, ctx, User: discord.Member):
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/alwayshasbeen?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def amiajoke(self, ctx, User: discord.Member):
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/amiajoke?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def bed(self, ctx, User: discord.Member, User2: discord.Member):
        pic_url = str(User.avatar_url).replace("webp",'png')
        pic2_url = str(User2.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/bed?image={pic_url}&image2={pic2_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def ship(self, ctx, User: discord.Member, User2: discord.Member):
        pic_url = str(User.avatar_url).replace("webp",'png')
        pic2_url = str(User2.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/ship?user={pic_url}&user2={pic2_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def blur(self, ctx, User: discord.Member):
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/blur?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def beautiful(self, ctx, User: discord.Member):
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/beautiful?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def gay(self, ctx, User: discord.Member):
        """Adds pride flag to someone's profile picture"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/gay?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def gun(self, ctx, User: discord.Member):
        """Makes someone point a gun at you"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/gun?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def hitler(self, ctx, User: discord.Member):
        """As bad as hitler meme"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/hitler?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def invert(self, ctx, User: discord.Member):
        """Inverts a user picture"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/invert?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def jail(self, ctx, User: discord.Member):
        """Jails a user"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/jail?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def jokeoverhead(self, ctx, User: discord.Member):
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/jokeoverhead?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def simp(self, ctx, User: discord.Member):
        """Adds the simp stamp over someone"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/simp?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def trash(self, ctx, User: discord.Member):
        """Makes someone look like trash"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/trash?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def triggered(self, ctx, User: discord.Member):
        """Add the triggered text over a user"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/triggered?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def wanted(self, ctx, User: discord.Member):
        """Makes someone a wanted criminal"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/wanted?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def wasted(self, ctx, User: discord.Member):
        """Adds GTA Wasted to a user"""
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/wasted?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def what(self, ctx, User: discord.Member):
        pic_url = str(User.avatar_url).replace("webp",'png')
        embed, img = await self.session(f"https://api.cool-img-api.ml/what?image={pic_url}")
        await ctx.send(file=img, embed=embed)
    @commands.command()
    async def batman_slap(
        self,
        ctx,
        text,
        text2,
        batman: discord.Member,
        robin: discord.Member,
    ):
        """Generates the meme"""
        if batman and robin:
            img = await self.api.batman_slap(
                text, text2, batman=batman.avatar_url, robin=robin.avatar_url
            )
            embed = discord.Embed()
            embed.set_image(url=img.url)
            await ctx.send(embed=embed)

    @commands.command()
    async def distracted(
        self,
        ctx,
        boyfriend: discord.Member,
        girlfriend: discord.Member,
        woman: discord.Member,
    ):
        """Generates the meme"""
        img = await self.api.distracted_bf(
            boyfriend.avatar_url, girlfriend.avatar_url, woman.avatar_url
        )
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def shame(self, ctx, user: discord.Member):
        """Generates the meme"""
        img = await self.api.dock_of_shame(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def table_flip(self, ctx, user: discord.Member):
        """Generates the meme"""
        img = await self.api.table_flip(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def first_time(self, ctx, user: discord.Member):
        """Generates the meme"""
        img = await self.api.first_time(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def heaven(self, ctx, user: discord.Member):
        """Generates the meme"""
        img = await self.api.heaven(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def npc(self, ctx, text1: str = None, text2: str = None):
        """Generates the meme"""
        img = await self.api.npc(text1, text2)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def stonks(self, ctx, user: discord.Member):
        """Generates the meme"""
        img = await self.api.stonks(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def wolverine(self, ctx, user: discord.Member):
        """Generates the meme"""
        img = await self.api.wolverine(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def widen(self, ctx, user: discord.Member):
        """Widens your profile User"""
        img = await self.api.wide(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def speedy(self, ctx, user: discord.Member):
        """Generates the meme"""
        img = await self.api.iam_speed(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def milk(
        self, ctx, user: discord.Member, user2: discord.Member
    ):
        """Generates the meme"""
        img = await self.api.i_can_milk_you(user.avatar_url, user2=user2.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def car_reverse(self, ctx, *, text: str = None):
        """Generates the meme"""
        img = await self.api.car_reverse(text)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def water(self, ctx, *, text: str = None):
        """Generates the meme"""
        img = await self.api.water(text)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def emergency(self, ctx, *, text: str = None):
        """Generates the meme"""
        img = await self.api.emergency_meeting(text)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def eject(self, ctx, member: discord.Member):
        """Generates the meme"""
        imposter = random.choice([True, False])
        img = await self.api.ejected(member.name, crewmate="random", impostor=imposter)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def rip(self, ctx, member: discord.Member):
        """Generates the meme"""
        img = await self.api.grave(member.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def changemymind(self, ctx, *, text: str = None):
        """Generates the meme"""
        embed, img = await self.session(
            "https://api.cool-img-api.ml/changemymind", {"text": text}
        )
        await ctx.send(file=img, embed=embed)


def setup(bot):
    bot.add_cog(Meme(bot))
