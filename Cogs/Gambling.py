from discord.ext import commands, menus, tasks
import discord
import asyncio
import asyncpg
import random
from discord.utils import get

class CoinPrompt(menus.Menu):
    def __init__(self, *, embed:discord.Embed):
        super().__init__(timeout=30.0, delete_message_after=True)
        self.embed = embed
        self.result = None

    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=self.embed)

    @menus.button("<:coinhead:831475175329366049>")
    async def heads(self, payload):
        self.result = 1
        self.stop()

    @menus.button("<:tails:831475250716868628>")
    async def tails(self, payload):
        self.result = 0
        self.stop()
    @menus.button('\N{CROSS MARK}')
    async def do_deny(self, payload):
        self.result = False
        self.stop()
    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result
class CrashGUI(menus.Menu):
    def __init__(self, *, embed:discord.Embed):
        super().__init__(timeout=30.0, delete_message_after=True)
        self.embed = embed
        self.multiplier = 1.0
        self.max_multiplier = random.uniform()
        self.result = None
        self.message = None
    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=self.embed)
    @tasks.loop(seconds=2.0)
    async def game_loop(self, ctx):
        pass
    @menus.button(':octagonal_sign:')
    async def do_deny(self, payload):
        self.stop()
class Gambling(commands.Cog, description="Coin flip and more!"):
    def __init__(self, bot):
        self.bot = bot
        self.heads_emoji = get(self.bot.emojis, name="coinhead")
        self.tails_emoji = get(self.bot.emojis, name="tails")
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
    async def has_money(self, ctx, amount):
        balance = await self.bot.db.fetchrow("SELECT * FROM userbalance WHERE user_id=$1",ctx.author.id)
        balance = balance.values()
        money = [x for x in balance][1]
        return True if money>=amount else False
    async def deduct(self, ctx, amount):
        await self.bot.db.execute("UPDATE userbalance SET balance=balance-$1 WHERE user_id=$2",amount,ctx.author.id)
    async def add(self, ctx, amount):
        await self.bot.db.execute("UPDATE userbalance SET balance=balance+$1 WHERE user_id=$2",amount,ctx.author.id)

    @commands.command(aliases=["flip"])
    async def coinflip(self, ctx, amount: int):
        """Does a coinflip for 2x the amount you bet"""
        if await self.has_money(ctx, amount):
            embed = discord.Embed(title="Bet which side the coin will land on!", description=f"<:coinhead:831475175329366049> **left:for heads**\n<:tails:831475250716868628> **right:for tails**")
            Prompt = CoinPrompt(embed=embed)
            await Prompt.prompt(ctx)
            embed = discord.Embed(title="Flipping...")
            embed.set_image(url="https://cdn.discordapp.com/attachments/273360137022996482/831460897691533312/coinflip.gif")
            message = await ctx.send(embed=embed)
            await self.deduct(ctx, amount)
            await asyncio.sleep(3)
            determine_flip = [1, 0]
            if random.choice(determine_flip) == 1:
                if Prompt.result == 1:
                    await self.add(ctx, amount*2)
                    embed = discord.Embed(title="YOU WIN :tada:", description=f"{ctx.author.mention} has gained {amount*2} :money_with_wings:!")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/273360137022996482/831460008524644352/unknown.png")
                    await message.edit(embed=embed)
                else:
                    embed = discord.Embed(title="You lost! <:icri:742346196990951505>", description=f"{ctx.author.mention} has lost {amount} :money_with_wings:!")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/273360137022996482/831460008524644352/unknown.png")
                    await message.edit(embed=embed)

            else:
                if Prompt.result == 0:
                    await self.add(ctx, amount*2)
                    embed = discord.Embed(title=":tada: YOU WIN :tada:", description=f"{ctx.author.mention} has gained {amount*2} :money_with_wings:!")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/273360137022996482/831462137473007627/tails.png")
                    await message.edit(embed=embed)
                else:
                    embed = discord.Embed(title="You lost! <:icri:742346196990951505>", description=f"{ctx.author.mention} has lost {amount} :money_with_wings:!")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/273360137022996482/831462137473007627/tails.png")
                    await message.edit(embed=embed)
        else:
            embed= discord.embed(title="Oops! It seems you don't have enough to attempt this! Maybe try ~beg?")
            await ctx.send(embed=embed)

    @commands.command()
    async def crash(self, ctx, amount: int):
        pass

def setup(bot):
    bot.add_cog(Gambling(bot))
