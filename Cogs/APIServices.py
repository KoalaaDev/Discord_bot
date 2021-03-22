from discord.ext import commands
import aiohttp
import discord


class API(commands.Cog, description="Random generator commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        """Gives a random cat picture"""  # Alvin be like meow meow *while sucking staff*
        if ctx.author.id == 451008924032827395:
            pic = "https://cdn.discordapp.com/attachments/541880222065098762/812999751339474954/alvin_lol.JPG"
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://aws.random.cat/meow") as f:
                    pic = await f.json()
        embed = discord.Embed(title="Random Cat", Colour=discord.Colour.purple())
        embed.set_image(url=pic["file"])
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx, breed=None):
        """Gives a random dog picture"""  # lincoln is dog woof woof
        if breed:
            picture_json = requests.get(
                f"https://dog.ceo/api/{breed}/image/random"
            ).json()
            if picture_json["status"] == "error":
                dogList = "\n".join(
                    [
                        "affenpinscher",
                        "african",
                        "airedale",
                        "akita",
                        "appenzeller",
                        "shepherd australian",
                        "basenji",
                        "beagle",
                        "bluetick",
                        "borzoi",
                        "boxer",
                        "brabancon",
                        "briard",
                        "buhund-norwegian",
                        "bulldog-boston",
                        "bulldog-english",
                        "bulldog-french",
                        "bullterrier-staffordshire",
                        "cairn",
                        "cattledog-australian",
                        "chihuahua",
                        "chow",
                    ]
                )
                Errorembed = discord.Embed(
                    title="This breed is not available",
                    color=discord.Color.random(),
                    description=f"Select the following breeds:```{dogList}```",
                )
                ctx.send(embed=Errorembed)
            else:
                pic = picture_json["message"]
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://random.dog/woof.json") as f:
                    pic = await f.json()
        embed = discord.Embed(title="Random Dog", Colour=discord.Colour.random())
        embed.set_image(url=pic["url"])
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    async def img(self, ctx, *, query):
        """Google searches your img"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://normal-api.ml/image-search?query={query}&redirect=false"
            ) as f:
                pic = await f.json()
        embed = discord.Embed(title=query, Colour=discord.Colour.random())
        embed.set_image(url=pic["image"])
        embed.set_footer(text="Img Gen Service")
        await ctx.send(embed=embed)

    @commands.command()
    async def fox(self, ctx):
        """Gives a random fox picture"""  # Alvins sex toy xD
        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomfox.ca/floof/") as f:
                pic = await f.json()
        embed = discord.Embed(title="Random Fox", Colour=discord.Colour.random())
        embed.set_image(url=pic["image"])
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)

    @commands.command()
    async def insult(self, ctx, lang="en"):
        """Generates an insult for the tagged member"""  # Why bully each other?
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
