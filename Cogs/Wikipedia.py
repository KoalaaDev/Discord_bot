import discord
import wikipedia
from discord.ext import commands


class Wikipedia(commands.Cog, description="Wikipedia related commands"):
    def __init__(self, bot):
        self.bot = bot
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
    async def wiki(self, ctx, query):
        """Searches wikipedia for information"""
        search = wikipedia.summary(wikipedia.search(query)[0])
        print(search)
        if len(search) > 2000:
            embed = discord.Embed(
                title=f"{wikipedia.search(query)[0]}",
                description=f"{search[:2000]}",
                colour=discord.Colour(0xFCEC00),
            )
            embed2 = discord.Embed(
                description=f"{search[2000:]}", colour=discord.Colour(0xFCEC00)
            )
            await ctx.send(embed=embed)
            await ctx.send(embed=embed2)
        else:
            embed = discord.Embed(
                title=f"{wikipedia.search(query)[0]}",
                description=f"{search}",
                colour=discord.Colour(0xFCEC00),
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wikipedia(bot))
