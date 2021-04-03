from typing import Literal
import aiohttp
import discord
from discord.ext import commands

BASE_URL = "https://mikuapi.predeactor.net"


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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

def setup(bot):
    bot.add_cog(Anime(bot))
