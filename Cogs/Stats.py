from discord.ext import commands
import asyncio
import discord
from Cogs.Utils import is_whitelisted
import matplotlib.pyplot as plt
import numpy as np
import io

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @is_whitelisted()
    @commands.command(hidden=True)
    async def UserStats(self, ctx, member:discord.Member):
        fetchuser = await self.bot.db.fetchrow("SELECT * FROM command WHERE user_id = $1", member.id)
        mostuser = [x for x in fetchuser.items() if x[1]][2:]
        commands = [x[0] for x in mostuser]
        usage = [x[1] for x in mostuser]
        print(usage)
        y_pos = np.arange(len(commands))
        data_stream = io.BytesIO()
        plt.bar(y_pos, usage, align='center', alpha=0.5)
        plt.xticks(y_pos, commands)
        plt.ylabel('Times used')
        plt.title(f"{member.name}'s Bot command usage")
        plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
        plt.close()
        data_stream.seek(0)
        chart = discord.File(data_stream,filename="usage.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://usage.png")
        await ctx.send(embed=embed, file=chart)
def setup(bot):
    bot.add_cog(Stats(bot))
