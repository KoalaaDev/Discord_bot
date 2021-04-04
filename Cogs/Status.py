from discord.ext import commands, tasks
from Cogs.Utils import is_whitelisted
import discord
import asyncio
class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.members = len(set(self.bot.get_all_members()))
        self.messages = [[discord.ActivityType.listening,"help"],[discord.ActivityType.listening,f"{len(self.bot.guilds)} Guilds | {self.members} Members"]]
        self.activity_types = {"playing":discord.ActivityType.playing,
                                "streaming":discord.ActivityType.streaming,
                                "listening":discord.ActivityType.listening,
                                "watching":discord.ActivityType.watching,
                                "custom":discord.ActivityType.custom}
        self.Animated_Status.start()
    @tasks.loop()
    async def Animated_Status(self):
        self.members = len(set(self.bot.get_all_members()))
        for i in self.messages:
            await self.bot.change_presence(activity=discord.Activity(type=i[0],name=i[1]))
            await asyncio.sleep(60)
    @is_whitelisted()
    @commands.command()
    async def addstatus(self, ctx, type, *, message):
        if type not in self.activity_types.keys():
            options = "\n".join(self.activity_types.keys())
            return await ctx.send("Choose from")
        self.messages.append([type:= self.activity_types.get(type),message])
        print(self.messages)
        await ctx.send("OK")


def setup(bot):
    bot.add_cog(Status(bot))
