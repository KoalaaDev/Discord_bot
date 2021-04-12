from typing import Literal
import aiohttp
import discord
from discord.ext import commands
import sys
import traceback
import io
import asyncio
from asyncdagpi import Client
BASE_URL = "https://mikuapi.predeactor.net"


class anime(commands.Cog):
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
                        title="Here's a pic of a Neko!", color=discord.Color.blue()
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
                        title="Here's a pic of a Neko!", color=discord.Color.blue()
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
                title="Hentai", color=discord.Color.blue()
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
                title="Hentai", color=discord.Color.blue()
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
                title="Fox girl", color=discord.Color.blue()
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

def setup(bot):
    bot.add_cog(Anime(bot))
