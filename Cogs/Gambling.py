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
        self.result = "Cancelled"
        self.stop()
    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result
class CrashGUI(menus.Menu):
    def __init__(self, *, embed:discord.Embed):
        super().__init__()
        self.embed = embed
        self.result = False
    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=self.embed)

    @menus.button('🛑')
    async def do_deny(self, payload):
        self.result = True
        self.stop()
    async def prompt(self, ctx):
        await self.start(ctx)
        return self.result

class ColorPrompt(menus.Menu):
    def __init__(self, *, embed:discord.Embed):
        super().__init__(timeout=30.0, delete_message_after=True)
        self.embed = embed
        self.result = None

    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=self.embed)

    @menus.button('🟥')
    async def red(self, payload):
        self.result = 0
        self.stop()

    @menus.button('🟦')
    async def blue(self, payload):
        self.result = 1
        self.stop()
    @menus.button('🟨')
    async def green(self, payload):
        self.result = 2
        self.stop()
    @menus.button('🟩')
    async def yellow(self, payload):
        self.result = 3
        self.stop()
    # @menus.button("<:purple_squre:>")
    # async def purple(self, payload):
    #     self.result = 4
    #     self.stop()
    # @menus.button("<:orange_squre:>")
    # async def purple(self, payload):
    #     self.result = 5
    #     self.stop()
    # @menus.button("<:black_squre:>")
    # async def purple(self, payload):
    #     self.result = 6
    #     self.stop()
    # @menus.button("<:brown_squre:>")
    # async def purple(self, payload):
    #     self.result = 7
    #     self.stop()
    @menus.button('\N{CROSS MARK}')
    async def do_deny(self, payload):
        self.result = "Cancelled"
        self.stop()
    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result

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

        if money>=amount:
            return True
        else:
            embed= discord.Embed(title="Oops! It seems you don't have enough to attempt this! Maybe try ~beg?")
            await ctx.send(embed=embed)
            return False
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
            if Prompt.result=="Cancelled":
                return
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

    @commands.command()
    async def crash(self, ctx, amount: int):
        """Simulates a stock crash game.\n Press the button to withdraw out of the market before it's too late!"""
        if await self.has_money(ctx, amount):
            embed = discord.Embed(description="Press the stop button to cash out:")
            embed.set_author(name="Crash")
            CrashGame = CrashGUI(embed=embed)
            await CrashGame.prompt(ctx)
            CrashPoint = round(999999999 / random.randint(1, 1000000000),1)
            start = 1.0
            while not CrashGame.result:
                start = round(start+0.2,1)
                profit = round(amount*start-amount,2)
                embed.description = "Press the stop button to cash out:"+f"\n**Multiplier**:`{start}x`"+f"\n**Profit**:`{profit}` :money_with_wings:"
                await CrashGame.message.edit(embed=embed)
                to_continue = random.choices([1,0],weights=[1,4])[0]

                if start>CrashPoint:
                    if to_continue == 1:
                        CrashPoint += round(999999999 / random.randint(1, 1000000000),1)
                    else:
                        embed = discord.Embed(description=f"Sorry {ctx.author.mention}, but you didnt cash out in time!\n**Crash Multiplier**: `{CrashPoint if CrashPoint%2==0 else CrashPoint-0.1}x`")
                        embed.set_author(name="Crashed!")
                        embed.description += f"\nYou lost **{amount}** :money_with_wings:"
                        await CrashGame.message.edit(embed=embed)
                        await self.deduct(ctx, amount)
                        CrashGame.stop()
                        break
                await asyncio.sleep(1)
            else:
                embed = discord.Embed(description=f"Congrats {ctx.author.mention}, you cashed out in time!\n**Multiplier**:`{start}x`\n**Crashes at**:`{CrashPoint if CrashPoint%2==0 else CrashPoint-0.1}x`\n**Profit**:`{profit}` :money_with_wings:")
                embed.set_author(name="Cashed out!")
                await self.add(ctx, profit)
                await CrashGame.message.edit(embed=embed)

    @commands.command()
    async def dice(self, ctx, amount: int):
        """Roll 2 dice for 8x the amount you bet but losing may cost you!"""
        if await self.has_money(ctx, amount):
            embed = discord.Embed(title="Lets roll a dice!", description="Rolling...")
            embed.set_image(url="https://media.discordapp.net/attachments/748419224082317326/836856916235911239/0fbae2bd3a0bd45b0d6a25f6459d95a3.gif?width=200&height=200")
            image = await ctx.send(embed=embed)
            dicenum = [0, 1, 2, 3, 4, 5]
            dicepiclist = ["https://cdn.discordapp.com/attachments/830740652647776257/836895755335499776/1194685-200.png","https://cdn.discordapp.com/attachments/830740652647776257/836895884570263582/1194688-200.png","https://cdn.discordapp.com/attachments/830740652647776257/836895915478220810/1194684-200.png","https://cdn.discordapp.com/attachments/830740652647776257/836895958527770634/1194689-200.png","https://cdn.discordapp.com/attachments/830740652647776257/836896011901337620/1194690-200.png","https://cdn.discordapp.com/attachments/830740652647776257/836896043538710558/1194691-200.png"]
            dice1 = random.choice(dicenum)
            dice2 = random.choice(dicenum)
            dicepic1 = dicepiclist[dice1]
            dicepic2 = dicepiclist[dice2]
            await asyncio.sleep(3)
            if dice1 == dice2:
                await image.delete()
                embed = discord.Embed(title="YOU WIN :tada:", description=f"{ctx.author.mention} has gained {amount*8} :money_with_wings:!")
                embed.set_image(url=dicepic1)
                embed.set_thumbnail(url=dicepic2)
                await self.add(ctx, amount*8)
                await ctx.send(embed=embed)
            else:
                await image.delete()
                embed = discord.Embed(title="You lost! <:icri:742346196990951505>", description=f"{ctx.author.mention} has lost {amount} :money_with_wings:!")
                embed.set_image(url=dicepic1)
                embed.set_thumbnail(url=dicepic2)
                await self.deduct(ctx, amount)
                await ctx.send(embed=embed)

    @commands.command()
    async def spin(self, ctx, amount: int):
        # """Choose a color and hope for the best!"""
        if await self.has_money(ctx, amount):
            color = [0,1,2,3]
            ChosenColor = random.choice(color)
            print(ChosenColor)
            embed = discord.Embed(title="Pick a color!", description=f" 1). Red\n 2). Blue\n 3). Yellow\n 4). Green")
            CPrompt = ColorPrompt(embed=embed)
            await CPrompt.prompt(ctx)
            colorpic = ["https://cdn.discordapp.com/attachments/822865028335272017/837147968926777464/square_PNG75.png","https://cdn.discordapp.com/attachments/822865028335272017/837145168527228928/ContactBlueSquare200x200.png","https://cdn.discordapp.com/attachments/822865028335272017/837145225381019702/01.png","https://cdn.discordapp.com/attachments/822865028335272017/837145225381019702/01.png"]
            if CPrompt.result=="Cancelled":
                return
            await self.deduct(ctx, amount)
            if CPrompt.result == ChosenColor:
                await self.add(ctx, amount*4)
                embed = discord.Embed(title="YOU WIN :tada:", description=f"{ctx.author.mention} has gained {amount*4} :money_with_wings:!")
                win = await ctx.send(embed=embed)
                if CPrompt.result == "0":
                    embed.set_image(url=(colorpic[0]))
                    c0 = await ctx.send(embed = embed)
                elif CPrompt.result == "1":
                    embed.set_image(url=colorpic[1])
                    c1 = await ctx.send(embed = embed)
                elif CPrompt.result == "2":
                    embed.set_image(url=colorpic[2])
                    c2 = await ctx.send(embed = embed)
                elif CPrompt.result == "3":
                    embed.set_image(url=colorpic[3])
                    c3 = await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title="You lost! <:icri:742346196990951505>", description=f"{ctx.author.mention} has lost {amount} :money_with_wings:!\n The correct choice is...")
                embed.set_image(url=colorpic[ChosenColor])
                await self.deduct(ctx, amount)
                lose = await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Gambling(bot))
