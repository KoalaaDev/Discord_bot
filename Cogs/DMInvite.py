import discord
from discord.ext import commands
import re

from Cogs.Utils import is_whitelisted

INVITE_URL_RE = re.compile(r"(discord\.(?:gg|io|me|li)|discord(?:app)?\.com\/invite)\/(\S+)", re.I)
class DmInvite(commands.Cog):
    """Respond to invites send in DMs."""

    def __init__(self, bot):
        self.bot = bot
        self.link = "https://discord.com/oauth2/authorize?client_id=799134976515375154&permissions=3172417&scope=bot"
        self.message = f"I've detected a discord server invite. If you'd like to invite me please click the [link]({self.link})."
        self.link = "https://discord.com/oauth2/authorize?client_id=799134976515375154&permissions=3172417&scope=bot"
        self.embedToggle = True
        self.InviteToggle = True
    @is_whitelisted()
    @commands.group(hidden=True)
    async def dminvite(self, ctx):
        """Group Commands for DM Invites."""
    @is_whitelisted()
    @dminvite.command()
    async def settings(self, ctx):
        """DM Invite Settings."""
        embed = discord.Embed(title="DM Invite Settings", color=discord.Color.red())
        embed.add_field(
            name="Tracking Invites", value="Yes" if await self.InviteToggle else "No"
        )
        embed.add_field(name="Embeds", value="Yes" if await self.embedToggle else "No")
        embed.add_field(name="Message", value=self.message)
        embed.add_field(name="Permissions Value", value=await self.bot._config.invite_perm())
        await ctx.send(embed=embed)

    @is_whitelisted()
    @dminvite.command()
    async def toggle(self, ctx, toggle: bool = None):
        """Turn DM responding on/off."""
        if toggle:
            self.embedToggle = False
            await ctx.send(
                "{} will no longer auto-respond to invites sent in DMs.".format(self.bot.name)
            )
        else:
            self.embedToggle = True
            await ctx.send("{} will auto-respond to invites sent in DMs.".format(self.bot.name))

    @is_whitelisted()
    @dminvite.command()
    async def embeds(self, ctx, toggle: bool = None):
        """Toggle whether the message is an embed or not."""
        if toggle:
            self.embedToggle = False
            await ctx.send("Responses will no longer be sent as an embed.")
        else:
            self.embedToggle = True
            await ctx.send(
                "Responses will now be sent as an embed. You can now use other markdown such as link masking etc."
            )
    @is_whitelisted()
    @dminvite.command()
    async def message(self, ctx, *, message: str):
        """Set the message that the bot will respond with.

        **Available Parameters**:
        {link} - return the bots oauth url with the permissions you've set with the core inviteset.
        """
        self.message = message
        await ctx.message.add_reaction("\N{White Heavy Check Mark}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild:
            return
        if message.author.bot:
            return
        if self.InviteToggle:
            link_res = INVITE_URL_RE.findall(message.content)
            if link_res:
                msg = self.message
                if self.embedToggle:
                    embed = discord.Embed(color=discord.Color.red(), description=msg)
                    return await message.author.send(embed=embed)

                await message.author.send(msg)

def setup(bot):
    bot.add_cog(DmInvite(bot))
