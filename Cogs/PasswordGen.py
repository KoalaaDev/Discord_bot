from discord.ext import commands
import random
import asyncio


class PasswordGen(commands.Cog, description="Secure yourself today!"):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            try:
                return await ctx.send(
                    embed=discord.Embed(
                        description="This command can only be used in DMS!"
                    )
                )
            except discord.HTTPException:
                pass
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

    @commands.dm_only()
    @commands.command()
    async def passwordgen(self, ctx, num: int = 20):
        """A password generator"""  # Lmao who would use this?
        choices = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*"
        print(choices := random.choices(choices, k=num))
        passwordshow = await ctx.send(
            embed=discord.Embed(description=f"{''.join(choices)}")
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(PasswordGen(bot))
