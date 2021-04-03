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
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )#NSFW stuff commands.is_nsfw()

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
                    await ctx.send(
                        "API unavailable. Status code: {code}\nIt may be due of a "
                        "maintenance.".format(code=status)
                    )
                    return
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
        """Generates random image of a Neko"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://neko.weeb.services/") as response:
                if response.status == 503:
                    await ctx.send("The API is actually in maintenance, please retry later.")
                    return
                try:
                    status = response.status
                    file = discord.File(io.BytesIO(await response.read()), filename="img.png")
                except aiohttp.ContentTypeError:
                    await ctx.send(
                        "API unavailable. Status code: {code}\nIt may be due of a "
                        "maintenance.".format(code=status)
                    )
                    return
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

def setup(bot):
    bot.add_cog(Anime(bot))
