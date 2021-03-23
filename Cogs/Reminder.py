from discord.ext import commands
import asyncio
import humanreadable as hr
import discord

class Reminder(commands.Cog, description="Never forget anything again!"):
    def __init__(self, bot):
        self.bot = bot
    async def cog_command_error(self, ctx, error):
        if isinstance(error, UnitNotFoundError):
            try:
                return await ctx.send(
                    embed=discord.Embed(description="Improper Time")
                )
            except discord.HTTPException:
                pass
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def RemindMe(self, ctx, *, time):
        """Remind you of something, input a human readable time or seconds"""
        try:
            time = int(time)
        except ValueError:
            try:
                time = hr.Time(time).seconds
            except hr.error.UnitNotFoundError:
                return await ctx.message.add_reaction("\N{Cross Mark}")
        prompt = await ctx.send(embed=discord.Embed(description=f"Enter your message"))

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        msg = await self.bot.wait_for('message',check=check)
        await prompt.delete()
        await msg.add_reaction("\N{White Heavy Check Mark}")
        await asyncio.sleep(time)
        await ctx.send(embed=discord.Embed(title=f"Reminder!",description=f"{member.mention} {msg.content}"))
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def Remind(self, ctx,member: discord.Member, *, time):
        """Remind you of something, input a human readable time"""
        try:
            time = int(time)
        except ValueError:
            try:
                time = hr.Time(time).seconds
            except hr.error.UnitNotFoundError:
                return await ctx.message.add_reaction("\N{Cross Mark}")
        prompt = await ctx.send(embed=discord.Embed(description=f"Enter your message"))

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        msg = await self.bot.wait_for('message',check=check)
        await prompt.delete()
        try:
            await msg.delete()
        except:
            pass
        await msg.add_reaction("\N{White Heavy Check Mark}")
        await asyncio.sleep(time)
        await ctx.send(embed=discord.Embed(title=f"Reminder by {ctx.author.name}",description=f"{member.mention} {msg.content}"))

def setup(bot):
    bot.add_cog(Reminder(bot))


# Made by DebuggingMySelf
