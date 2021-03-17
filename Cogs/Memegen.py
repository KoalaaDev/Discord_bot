from discord.ext import commands
import vacefron
import aiohttp
import discord
import random
import io


class Meme(commands.Cog, description="Generate memes and more!"):
    def __init__(self, bot):
        self.bot = bot
        self.api = vacefron.Client()

    async def session(self, url, param: dict = {}):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=param) as f:
                print(f.url)
                return discord.File(io.BytesIO(await f.read()), filename="img.png")

    # @commands.command()
    # async def communism(self, ctx, picture:discord.Member  = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/communist?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def meme(self, ctx):
    #     img = await self.session("https://api.cool-img-api.ml/meme")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def achievement(self, ctx, *, text:str = None):
    #     img = await self.session("https://api.cool-img-api.ml/achievement",{'text':text})
    #     await ctx.send(file=img)
    # @commands.command()
    # async def calling(self, ctx, *, text:str = None):
    #     img = await self.session("https://api.cool-img-api.ml/calling",{'text':text})
    #     await ctx.send(file=img)
    # @commands.command()
    # async def captcha(self, ctx, *, text:str = None):
    #     img = await self.session("https://api.cool-img-api.ml/captcha",{'text':text})
    #     await ctx.send(file=img)
    # @commands.command()
    # async def challenge(self, ctx, *, text:str = None):
    #     img = await self.session("https://api.cool-img-api.ml/challenge",{'text':text})
    #     await ctx.send(file=img)
    # @commands.command()
    # async def clyde(self, ctx, *, text:str = None):
    #     img = await self.session("https://api.cool-img-api.ml/clyde",{'text':text})
    #     await ctx.send(file=img)
    # @commands.command()
    # async def facts(self, ctx, *, text:str = None):
    #     img = await self.session("https://api.cool-img-api.ml/facts",{'text':text})
    #     await ctx.send(file=img)
    # @commands.command()
    # async def scroll(self, ctx, *, text:str = None):
    #     img = await self.session("https://api.cool-img-api.ml/scroll",{'text':text})
    #     await ctx.send(file=img)
    # @commands.command()
    # async def alwayshasbeen(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/alwayshasbeen?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def amiajoke(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/amiajoke?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def bad(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/bad?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def bed(self, ctx, picture: discord.Member = None, picture2: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     pic2_url = str(picture2.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/bed?image={pic_url}&image2={pic2_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def ship(self, ctx, picture: discord.Member = None, picture2: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     pic2_url = str(picture2.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/ship?image={pic_url}&image2={pic2_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def blur(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/blur?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def beautiful(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/beautiful?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def gay(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/gay?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def gun(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/gun?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def hitler(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/hitler?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def invert(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/invert?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def jail(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/jail?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def jokeoverhead(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/jokeoverhead?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def simp(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/simp?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def trash(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/trash?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def triggered(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/triggered?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def wanted(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/wanted?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def wasted(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/wasted?image={pic_url}")
    #     await ctx.send(file=img)
    # @commands.command()
    # async def what(self, ctx, picture: discord.Member = None):
    #     pic_url = str(picture.avatar_url).replace("webp",'png')
    #     img = await self.session(f"https://api.cool-img-api.ml/what?image={pic_url}")
    #     await ctx.send(file=img)
    @commands.command()
    async def batman_slap(
        self,
        ctx,
        text,
        text2,
        batman: discord.Member = None,
        robin: discord.Member = None,
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
        boyfriend: discord.Member = None,
        girlfriend: discord.Member = None,
        woman: discord.Member = None,
    ):
        """Generates the meme"""
        img = await self.api.distracted_bf(
            boyfriend.avatar_url, girlfriend.avatar_url, woman.avatar_url
        )
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def shame(self, ctx, user: discord.Member = None):
        """Generates the meme"""
        img = await self.api.dock_of_shame(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def table_flip(self, ctx, user: discord.Member = None):
        """Generates the meme"""
        img = await self.api.table_flip(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def first_time(self, ctx, user: discord.Member = None):
        """Generates the meme"""
        img = await self.api.first_time(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def heaven(self, ctx, user: discord.Member = None):
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
    async def stonks(self, ctx, user: discord.Member = None):
        """Generates the meme"""
        img = await self.api.stonks(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def wolverine(self, ctx, user: discord.Member = None):
        """Generates the meme"""
        img = await self.api.wolverine(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def widen(self, ctx, user: discord.Member = None):
        """Widens your profile picture"""
        img = await self.api.wide(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def speedy(self, ctx, user: discord.Member = None):
        """Generates the meme"""
        img = await self.api.iam_speed(user.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def milk(
        self, ctx, user: discord.Member = None, user2: discord.Member = None
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
    async def eject(self, ctx, member: discord.Member = None):
        """Generates the meme"""
        imposter = random.choice([True, False])
        img = await self.api.ejected(member.name, crewmate="random", impostor=imposter)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def rip(self, ctx, member: discord.Member = None):
        """Generates the meme"""
        img = await self.api.grave(member.avatar_url)
        embed = discord.Embed()
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def changemymind(self, ctx, *, text: str = None):
        """Generates the meme"""
        img = await self.session(
            "https://api.cool-img-api.ml/changemymind", {"text": text}
        )
        await ctx.send(file=img)


def setup(bot):
    bot.add_cog(Meme(bot))
