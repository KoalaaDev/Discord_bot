from discord.ext import commands
import random
import asyncio
import discord


class AniSearch(commands.Cog, description="Find yourself an anime to watch"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def anisearch(self, ctx, *,query):
        """Anime information Searcher"""

        entries = await self.client.search('anime', query, limit=5)
        if not entries:
            print(f'No entries found for "{query}"')
            return

        for i, anime in enumerate(entries, 1):
            embed = discord.Embed(title=anime.title, description=anime.synopsis)
            embed.add_field(name="Sub-Type", value=anime.type)
            embed.add_field(name="Status", value=anime.status)
            embed.add_field(name='Episodes:', value=anime.episode_count)
            embed.add_field(name='Age Rating:', value=anime.age_rating_guide)
            embed.add_field(name='Popularity:', value=anime.popularity_rank)
            embed.add_field(name='Rating:', value=anime.rating_rank)
            await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(AniSearch(bot))
