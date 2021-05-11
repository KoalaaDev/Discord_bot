from typing import Literal
import aiohttp
import random
import discord
from discord.ext import commands
import sys
import traceback
import io
import asyncio
import hmtai
from asyncdagpi import Client
BASE_URL = "https://mikuapi.predeactor.net"


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi = Client("ta1fnmIgn85mcfz32UG5nKgVeRWikmaZxZa392f0XwWC4yaDCOGUYPWscbZ5ULbk")
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            try:
                return await ctx.send(
                    embed=discord.Embed(description="This can only be used in NSFW channels!")
                )
            except discord.HTTPException:
                pass
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
        )#NSFW stuff @commands.is_nsfw()

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def megumin(self, ctx: commands.Context):
        """Generates random picture of Megumin"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://waifu.pics/api/sfw/megumin") as response:
                if response.status == 503:
                    await ctx.send("The API is actually in maintenance, please retry later.")
                    return
                try:
                    status = response.status
                    url = await response.json()
                except aiohttp.ContentTypeError:
                        return await ctx.send(
                            "API unavailable. Status code: {code}\nIt may be due of a "
                            "maintenance.".format(code=status)
                        )
        embed = discord.Embed(
            color=discord.Color.red()
        )
        try:
            embed.set_image(url=url["url"])
        except KeyError:
            await ctx.send(
                "I received an incorrect format from the API\nStatus code: {code}".format(
                    code=status
                )
            )
        await ctx.send(embed=embed)
####picture
    @commands.command(hidden=True)
    async def anime(self, ctx, *, command=None):
        """You can either use anime (command) or use the command directly!"""
        cmd = self.bot.get_command(command)
        if not cmd:
            search = self.bot.get_command("anisearch")
            return await search(ctx,query=command)
        await cmd(ctx)
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def miku(self, ctx: commands.Context):
        """Generates random image of Hatsune Miku"""
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + "/random") as response:
                if response.status == 503:
                    await ctx.send("The API is actually in maintenance, please retry later.")
                    return
                try:
                    status = response.status
                    url = await response.json()
                except aiohttp.ContentTypeError:
                        return await ctx.send(
                            "API unavailable. Status code: {code}\nIt may be due of a "
                            "maintenance.".format(code=status)
                        )
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        try:
            embed.set_image(url=url["url"])
        except KeyError:
            await ctx.send(
                "I received an incorrect format from the API\nStatus code: {code}".format(
                    code=status
                )
            )
        await ctx.send(embed=embed)

    @commands.command(aliases=["catgirl"])
    @commands.bot_has_permissions(embed_links=True)
    async def neko(self, ctx: commands.Context):
        """Generates random image of a Neko (may take awhile to load)"""
        async with aiohttp.ClientSession() as session:
            if ctx.message.channel.is_nsfw():
                async with session.get("https://nekos.life/api/lewd/neko") as response:
                    if response.status == 503:
                        await ctx.send("The API is actually in maintenance, please retry later.")
                        return
                    try:
                        status = response.status
                        url = await response.json()
                    except aiohttp.ContentTypeError:
                        return await ctx.send(
                                "API unavailable. Status code: {code}\nIt may be due of a "
                                "maintenance.".format(code=status)
                            )
                    embed = discord.Embed(
                        color=discord.Color.blue()
                    )
                    try:
                        embed.set_image(url=url["neko"])
                    except KeyError:
                        await ctx.send(
                            "I received an incorrect format from the API\nStatus code: {code}".format(
                                code=status
                            )
                        )
                    await ctx.send(embed=embed)
            else:
                async with session.get("https://nekos.life/api/neko") as response:
                    if response.status == 503:
                        await ctx.send("The API is actually in maintenance, please retry later.")
                        return
                    try:
                        status = response.status
                        url = await response.json()
                    except aiohttp.ContentTypeError:
                        return await ctx.send(
                                "API unavailable. Status code: {code}\nIt may be due of a "
                                "maintenance.".format(code=status)
                            )
                    embed = discord.Embed(
                        color=discord.Color.blue()
                    )
                    try:
                        embed.set_image(url=url["neko"])
                    except KeyError:
                        await ctx.send(
                            "I received an incorrect format from the API\nStatus code: {code}".format(
                                code=status
                            )
                        )
                    await ctx.send(embed=embed)
####Text
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def wallpaper(self, ctx: commands.Context):
        """Generates random anime wallpaper"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        try:
            embed.set_image(url=hmtai.useHM("v2","wallpaper"))
        except KeyError:
            await ctx.send(
                "I received an incorrect format from the API\nStatus code: {code}".format(
                    code=status
                )
            )
        await ctx.send(embed=embed)

    @commands.command(aliases=["mw"])
    @commands.bot_has_permissions(embed_links=True)
    async def mobileWallpaper(self, ctx: commands.Context):
        """Generates random anime mobileWallpaper"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        try:
            embed.set_image(url=hmtai.useHM("v2","mobileWallpaper"))
        except KeyError:
            await ctx.send(
                "I received an incorrect format from the API\nStatus code: {code}".format(
                    code=status
                )
            )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def jahy(self, ctx: commands.Context):
        """Generates a random picture of jahy"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        try:
            embed.set_image(url=hmtai.useHM("v2","jahy"))
        except KeyError:
            await ctx.send(
                "I received an incorrect format from the API\nStatus code: {code}".format(
                    code=status
                )
            )
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def trap(self, ctx: commands.Context):
        """Shows trap hentai"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://waifu.pics/api/nsfw/trap") as response:
                if response.status == 503:
                    return await ctx.send("The API is actually in maintenance, please retry later.")
                try:
                    status = response.status
                    url = await response.json()
                except aiohttp.ContentTypeError:
                        return await ctx.send(
                            "API unavailable. Status code: {code}\nIt may be due of a "
                            "maintenance.".format(code=status)
                        )
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        try:
            embed.set_image(url=url["url"])
        except KeyError:
            await ctx.send(
                "I received an incorrect format from the API\nStatus code: {code}".format(
                    code=status
                )
            )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def waifu(self, ctx):
        """Generates a random waifu"""
        waifu = await self.dagpi.waifu()
        embed = discord.Embed(title=waifu["name"],description=waifu["description"])
        if waifu['age']:
            embed.add_field(name="age",value=waifu['age'])
        if waifu.get("birthday_year"):
            embed.add_field(name="Date of birth",value=" ".join([waifu["birthday_day"],waifu["birthday_month"],waifu["birthday_year"]]))
        embed.set_image(url=waifu['display_picture'])
        embed.set_footer(text=f"{waifu.get('likes')} ⬆️ | {waifu.get('like_rank')} rank")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def manga(self, ctx, *, query):
        """Searches a manga"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://crunchy-bot.live/api/manga/details?terms={query}") as response:
                if response.status == 503:
                    return await ctx.send("The API is actually in maintenance, please retry later.")
                try:
                    status = response.status
                    url = await response.json()
                except aiohttp.ContentTypeError:
                        return await ctx.send(
                            "API unavailable. Status code: {code}\nIt may be due of a "
                            "maintenance.".format(code=status)
                        )
        for search in url:
            embed = discord.Embed(
                title=search['english'],description=search['description'], color=discord.Color.blue()
            )
            embed.add_field(name="Type", value=search['type'])
            if search['volumes'] != "Unknown":
                embed.add_field(name="Volumes", value=search['volumes'])
            if search['chapters'] != "Unknown":
                embed.add_field(name="Chapters", value=search['chapters'])
            embed.add_field(name="Status", value=search['status'])
            embed.add_field(name="Published", value=search['published'])
            embed.add_field(name="Genres", value=search['genres'])
            embed.add_field(name="Authors", value=search['authors'])
            embed.add_field(name="Popularity", value=search['popularity'])
            embed.add_field(name="Characters and actor", value=", ".join([x['character'] for x in search['characters_and_actor']]))
            embed.set_footer(text=f"{search['favorites']}❤️| {search['ranked']}| {search['score']} Score")
            await ctx.send(embed=embed)
            await asyncio.sleep(1)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def hentai(self, ctx: commands.Context, type="img"):
        """Gives hentai"""
        if type == "gif":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/Random_hentai_gif") as response:
                    if response.status == 503:
                        await ctx.send("The API is actually in maintenance, please retry later.")
                        return
                    try:
                        status = response.status
                        url = await response.json()
                    except aiohttp.ContentTypeError:
                            return await ctx.send(
                                "API unavailable. Status code: {code}\nIt may be due of a "
                                "maintenance.".format(code=status)
                            )
            embed = discord.Embed(
                color=discord.Color.blue()
            )
            try:
                embed.set_image(url=url["url"])
            except KeyError:
                await ctx.send(
                    "I received an incorrect format from the API\nStatus code: {code}".format(
                        code=status
                    )
                )
            await ctx.send(embed=embed)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/hentai") as response:
                    if response.status == 503:
                        await ctx.send("The API is actually in maintenance, please retry later.")
                        return
                    try:
                        status = response.status
                        url = await response.json()
                    except aiohttp.ContentTypeError:
                            return await ctx.send(
                                "API unavailable. Status code: {code}\nIt may be due of a "
                                "maintenance.".format(code=status)
                            )
            embed = discord.Embed(
                color=discord.Color.blue()
            )
            try:
                embed.set_image(url=url["url"])
            except KeyError:
                await ctx.send(
                    "I received an incorrect format from the API\nStatus code: {code}".format(
                        code=status
                    )
                )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def fox(self, ctx: commands.Context, type="img"):
        """Gives a random fox picture \n If do ~fox girl will give a anime fox girl"""
        if type == "girl":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/fox_girl") as response:
                    if response.status == 503:
                        await ctx.send("The API is actually in maintenance, please retry later.")
                        return
                    try:
                        status = response.status
                        url = await response.json()
                    except aiohttp.ContentTypeError:
                            return await ctx.send(
                                "API unavailable. Status code: {code}\nIt may be due of a "
                                "maintenance.".format(code=status)
                            )
            embed = discord.Embed(
                color=discord.Color.blue()
            )
            try:
                embed.set_image(url=url["url"])
            except KeyError:
                await ctx.send(
                    "I received an incorrect format from the API\nStatus code: {code}".format(
                        code=status
                    )
                )
            await ctx.send(embed=embed)
        else:
            """Gives a random fox picture"""
            async with aiohttp.ClientSession() as session:
                async with session.get("https://randomfox.ca/floof/") as f:
                    pic = await f.json()
            embed = discord.Embed(title="Random Fox", Colour=discord.Colour.random())
            embed.set_image(url=pic["image"])
            embed.set_footer(text="Animal Img Gen Service")
            await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def ass(self, ctx: commands.Context):
        """Anime ass very nice"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"ass"))
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def bdsm(self, ctx: commands.Context):
        """If you don't know what it is, search it up"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"bdsm"))
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def cum(self, ctx: commands.Context):
        """Sticky white stuff"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"cum"))
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def femdom(self, ctx: commands.Context):
        """Femdom"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"femdom"))
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def orgy(self, ctx: commands.Context):
        """Group Lewd Acts"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"orgy"))
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def blowjob(self, ctx: commands.Context):
        """You know what this is"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"blowjob"))
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def foot(self, ctx: commands.Context):
        """Feet"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"foot"))
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def ahegao(self, ctx: commands.Context):
        """Happy faces"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"ahegao"))
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def uniform(self, ctx: commands.Context):
        """School Uniforms"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"uniform"))
        await ctx.send(embed=embed)

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def gangbang(self, ctx: commands.Context):
        """The people in the picture is more social than you"""
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        choice = random.choice(["v1","v2"])
        embed.set_image(url=hmtai.useHM(choice,"gangbang"))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Anime(bot))
