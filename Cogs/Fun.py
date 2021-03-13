from discord.ext import commands
import random
import discord
import yaml
import os
from discord.ext.commands.cooldowns import BucketType

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balances = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bank.yml')

    @commands.command(hidden=true)
    async def jason(self,ctx):
        await ctx.message.delete()
        embed1 ="https://cdn.discordapp.com/attachments/263190635434082315/803952123237761024/Jason_hanging_out_on_a_swing.jpg"
        embed2 ="https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed3 ="https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed =discord.Embed(title="Surpirse!",colour=discord.Colour.blue())
        embed.set_image(url=random.choice([embed1,embed2,embed3]))
        await ctx.send(embed=embed,delete_after=5)

    @commands.command(aliases=["hotcalc"])
    async def hotcalc(self,ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command(aliases=["papeflip"])
    async def pepeflip(self, ctx):
        """Sends good luck with a crying or smiling pepe"""
        emoji1 = self.bot.get_emoji(799506321442996235)
        emoji2 = self.bot.get_emoji(742346196990951505)
        lmao = random.choice([emoji1,emoji2])
        bruh = await ctx.send("Good Luck!")
        await bruh.add_reaction(lmao)

    @commands.command(hidden=True)
    async def woohoo(self, ctx):
      gay = random.choice(["Koalaa","Skot","Alvin"])
      message = await ctx.send(f'Woohoo {gay} is confirmed gay!')
      emoji = get(client.emojis, name='pepelaugh')
      await message.add_reaction(emoji)

    async def get_currency(self, MemberID):
        with open(self.balances) as f:
            balances = yaml.safe_load(f)
            return balances.get(MemberID, None)
    async def create_account(self, MemberID):
        with open(self.balances,"r") as f:
            balances = yaml.safe_load(f)
        balances[MemberID] = 0
        with open(self.balances,"w") as f:
            balances = yaml.dump(balances, f)
    async def write(self, MemberID, amount):
        with open(self.balances) as f:
            balances = yaml.safe_load(f)
        balances[MemberID] = amount
        with open(self.balances,"w") as f:##W = write R = read
            balances = yaml.dump(balances, f)
    @commands.command(hidden=True)
    async def beg(self, ctx):
        balance = await self.get_currency(ctx.author.id)
        if not balance:
            await self.create_account(ctx.author.id)
            balance = await self.get_currency(ctx.author.id)
        await self.write(ctx.author.id, random.randint(1,100)+balance)
        await ctx.send("UR A LINCOLN")
    @commands.cooldown(1,86400,BucketType.user)
    @commands.command(hidden=True)
    async def daily(self, ctx):
        userbalance = await self.get_currency(ctx.author.id)
        print(userbalance)
        if not userbalance:
            await self.create_account(ctx.author.id)
            print("CREATING USER BALANCE")
def setup(bot):
    bot.add_cog(Fun(bot))
