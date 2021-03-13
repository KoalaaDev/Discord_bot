import discord
from discord.ext import commands
import random
import asyncio
class PasswordGen(commands.Cog, description="Secure yourself today!"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def passwordgen(self, ctx, num: int = 20):
        """A password generator"""#Lmao who would use this?
        choices = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*"
        print(choices := random.choices(choices, k = num))
        passwordshow = await ctx.send(f"{''.join(choices)}")
        await ctx.message.delete()
        await asyncio.sleep(3)
        await passwordshow.delete()
def setup(bot):
    bot.add_cog(PasswordGen(bot))
