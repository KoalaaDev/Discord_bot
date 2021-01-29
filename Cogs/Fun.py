from discord.ext import commands
import random
import discord
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jason(self,ctx):
        await ctx.message.delete()
        embed1 ="https://cdn.discordapp.com/attachments/263190635434082315/803952123237761024/Jason_hanging_out_on_a_swing.jpg"
        embed2 ="https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed3 ="https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed =discord.Embed(title="Surpirse!",colour=discord.Colour.blue())
        embed.set_image(url=random.choice([embed1,embed2,embed3]))
        await ctx.send(embed=embed,delete_after=5)

    @commands.command()
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

    @commands.command()
    async def pepeflip(self, ctx):
        emoji1 = get(client.emojis, name='pepelaugh')
        emoji2 = get(client.emojis, name='icri')
        lmao = random.choice([emoji1,emoji2])
        bruh = await ctx.send("Good Luck!")
        await bruh.add_reaction(lmao)

    @commands.command()
    async def woohoo(self, ctx):
      gay = random.choice(["Koalaa","Skot","Alvin"])
      message = await ctx.send(f'Woohoo {gay} is confirmed gay!')
      emoji = get(client.emojis, name='pepelaugh')
      await message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(Fun(bot))
