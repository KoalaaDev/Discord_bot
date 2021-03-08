import discord
from discord.ext import commands
import datetime
import pytz

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def timenow(self, ctx):
        dt_utcnow = datetime.datetime.now(tz=pytz.UTC)

        dt_hknow = dt_utcnow.astimezone(pytz.timezone('Hongkong'))
        print(dt_hknow)

        dt_thnow = dt_utcnow.astimezone(pytz.timezone('Asia/Bangkok'))

        time = await ctx.send(f"Right now the date is {timezone} ")
        await ctx.message.delete()


    @commands.command()
    async def timezonelist(self,ctx):
        
        for x in range(pages+1):
            upcoming = list(itertools.islice(controller.queue._queue, x*5,x*5+5))
            fmt = '\n'.join(f'```{k}. {str(song)}```' for k,song in enumerate(upcoming,start=x*5+1))
            page = discord.Embed(title=f'Queue', colour=discord.Colour.random())
            page.add_field(name=f"Now playing: `{player.current}`",value=fmt)
            page.set_footer(text=f"Page {next(pagenumber)}/{pages}")
            embeds.append(page)
        try:
            await ctx.send(embed=embeds[pageno-1])
        except IndexError:
            await ctx.send(embed=discord.Embed(description="Could not get page!"))

def setup(bot):
    bot.add_cog(Time(bot))








for tz in pytz.all_timezones:
     print(tz)
