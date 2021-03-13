import discord
from discord.ext import commands
import datetime
import pytz
import itertools
import asyncio
class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(hidden=True)
    async def TzArea(self, ctx):
        await ctx.message.delete()
        tzlistchoice = [['AfricanTimezone','For African Timezone'],['AmericaTimezone','For America Continent Timezone'],['AntarticaTimezone','For Antartica Timezone'],['ArcticTimezone','For Arctic Timezone'],['AsiaTimezone','For Asian Timezone'],['AtlanicTimezone','For Altanic Timezone'],['AustraliaTimezone','For Australian Timezone'],['BrazilTimezone','For Brazil Timezone'],['COTUSTimezone','For COTUS Timezone'],['EuropeTimezone','For European Timezone'],['IndianTimezone','For Indian Timezone'],['OceaniaTimezone','For Oceania Timezone'],['PacificTimezone','For Pacific Timezone'],['timezonelist','For all Timezone']]
        embeds = []
        pages = 2
        cur_page = 0
        embed = discord.Embed(title=f"TzList")
        [embed.add_field(name=x[0],value=x[1]) for x in list(itertools.islice(tzlistchoice,0,4))]
        embed.set_footer(text=f"Page 1/{pages}")
        message = await ctx.send(embed=embed)
        embeds.append(embed)
        # getting the message object for editing and reacting
        embed2 = discord.Embed(title=f"TzList")
        [embed2.add_field(name=x[0],value=x[1]) for x in list(itertools.islice(tzlistchoice,5,13))]
        embed2.set_footer(text=f"Page 2/{pages}")
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        embeds.append(embed2)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=120, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=embeds[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=embeds[cur_page])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds

    @commands.command(hidden=True)
    async def AreaChoice(self, ctx, choice: str):
        await ctx.send(f"Your timezone list of choices is {choice}")
        with open(f"Cogs\\Timezone\\{choice}.txt") as timezone:
            showlist = timezone.read()
            print(timezone)
        await ctx.send(showlist)
        choice = ""

    @commands.command(hidden=True)
    async def timezone(self, ctx, tzchoice: str):
        dt_now = datetime.datetime.now(tz=pytz.{tzchoice})
    #
    # @commands.command()
    # async def timezonelist(self, ctx, area = "timezonelist.txt"):
    #     f = open(area, "r")
    #     await ctx.send(f.read())
    #     f.close()
        # for x in range(pages+1):
        #     upcoming = list(itertools.islice(controller.queue._queue, x*5,x*5+5))
        #     fmt = '\n'.join(f'```{k}. {str(song)}```' for k,song in enumerate(upcoming,start=x*5+1))
        #     page = discord.Embed(title=f'Queue', colour=discord.Colour.random())
        #     page.add_field(name=f"Now playing: `{player.current}`",value=fmt)
        #     page.set_footer(text=f"Page {next(pagenumber)}/{pages}")
        #     embeds.append(page)
        # try:
        #     await ctx.send(embed=embeds[pageno-1])
        # except IndexError:
        #     await ctx.send(embed=discord.Embed(description="Could not get page!"))

def setup(bot):
    bot.add_cog(Time(bot))


# for tz in pytz.all_timezones:
#      print(tz)
