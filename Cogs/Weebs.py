from typing import Literal
import aiohttp
import discord
from discord.ext import commands
import sys
import traceback
import io
BASE_URL = "https://mikuapi.predeactor.net"


class Anime(commands.Cog):
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
            title="Here's a picture of Megumin!", color=discord.Color.blue()
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
    @commands.command()
    async def anime(self, ctx, command):
        """You can either use anime (command) or use the command directly!"""
        cmd = self.bot.get_command(command)
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
            title="Here's a pic of Hatsune Miku!", color=discord.Color.blue()
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
    async def neko(self, ctx: commands.Context):
        """Generates random image of a Neko (may take awhile to load)"""
        async with aiohttp.ClientSession() as session:
            if ctx.message.channel.is_nsfw():
                async with session.get("https://waifu.pics/api/nsfw/neko") as response:
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
                        title="Here's a gif of anime girls cuddling!", color=discord.Color.blue()
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
                async with session.get("https://neko.weeb.services/") as response:
                    if response.status == 503:
                        await ctx.send("The API is actually in maintenance, please retry later.")
                        return
                    try:
                        status = response.status
                        file = discord.File(io.BytesIO(await response.read()), filename="img.png")
                    except aiohttp.ContentTypeError:
                        return await ctx.send(
                            "API unavailable. Status code: {code}\nIt may be due of a "
                            "maintenance.".format(code=status)
                        )
                    embed = discord.Embed(
                        title="Here's a pic of a Neko!", color=discord.Color.blue()
                    )
                    try:
                        embed.set_image(url="attachment://img.png")
                    except KeyError:
                        await ctx.send(
                            "I received an incorrect format from the API\nStatus code: {code}".format(
                                code=status
                            )
                        )
                    await ctx.send(file=file,embed=embed)
####Text
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def cuddle(self, ctx: commands.Context):
        """Generates random gif of anime girls cuddling"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.willz.repl.co/anime/cuddle?key=R7SDV-EfV2V-7FWZC-UIUvQ") as response:
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
            title="Here's a gif of anime girls cuddling!", color=discord.Color.blue()
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
    async def kiss(self, ctx: commands.Context):
        """Generates random gif of a random anime kissing scene"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.willz.repl.co/anime/kiss?key=R7SDV-EfV2V-7FWZC-UIUvQ") as response:
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
            title="Here's a gif of a random anime kissing scene!", color=discord.Color.blue()
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
    async def tsundere(self, ctx: commands.Context):
        """Generates random gif of a tsundere"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.willz.repl.co/anime/tsundere?key=R7SDV-EfV2V-7FWZC-UIUvQ") as response:
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
            title="Here's a gif of a random tsundere!", color=discord.Color.blue()
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
    async def drunk(self, ctx: commands.Context):
        """Generates random gif of a drunk anime character"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.willz.repl.co/anime/drunk?key=R7SDV-EfV2V-7FWZC-UIUvQ") as response:
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
            title="Here's a gif of a drunk anime character!", color=discord.Color.blue()
        )
        try:
            embed.set_image(url=url["message"])
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
    async def fuck(self, ctx: commands.Context):
        """Shows an anime girl being fucked"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.willz.repl.co/anime/fuck?key=R7SDV-EfV2V-7FWZC-UIUvQ") as response:
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
            title="Anime fuck", color=discord.Color.blue()
        )
        try:
            embed.set_image(url=url["gif"])
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
    async def cum(self, ctx: commands.Context):
        """Shows an anime girl being creampied"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.willz.repl.co/anime/cum?key=R7SDV-EfV2V-7FWZC-UIUvQ") as response:
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
            title="Anime cum", color=discord.Color.blue()
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

    @commands.is_nsfw()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def anal(self, ctx: commands.Context):
        """Shows an anime girl doing anal"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.willz.repl.co/anime/anal?key=R7SDV-EfV2V-7FWZC-UIUvQ") as response:
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
            title="Anime anal", color=discord.Color.blue()
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
            title="trap hentai", color=discord.Color.blue()
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

def setup(bot):
    bot.add_cog(Anime(bot))
