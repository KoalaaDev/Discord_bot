import time
from datetime import datetime

import discord
from discord.ext import commands

WHITELIST = [line.strip() for line in open('Whitelist.txt','r+', buffering=1)]


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    def whitelist(self, ctx, user=None):
        with open('Whitelist.txt','a+') as r:
            r.write(user)

    @commands.command()
    async def embed(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour.purple())
        embed.add_field(name=f"**Rule 1**",
                        value="""Be respectful. Please remember that everyone else here is human (though we do have a few bots.)
Follow Discords Terms of Service AND Community guidelines:
https://discordapp.com/terms, https://discordapp.com/guidelines""",
                        inline=False)
        embed.add_field(name="**Rule 2**",
                        value="Any form of discrimination, academic dishonesty and offensive jokes involving race, religion and/or ethnicity, gender, and sexuality are prohibited.",
                        inline=False)
        embed.add_field(name="**Rule 3**",
                        value="Use proper grammar and spelling.",
                        inline=False)
        embed.add_field(name="**Rule 4**",
                        value="Speaking in languages other than English are only allowed in language subject channels.",
                        inline=False)
        embed.add_field(name="**Rule 5**",
                        value="Read the channel topics and descriptions before sending anything: Post content in the correct channels and don’t go offtopic.",
                        inline=False)
        embed.add_field(name="**Rule 6**",
                        value="NSFW content/discussion and excessive usage of inappropriate language are prohibited. Any moderator decisions will be made purely out of context, on a case by case basis, and as such there is no blacklist of words. If there is you have any problem with the moderator's discretion, notify admins",
                        inline=False)
        embed.add_field(name="**Rule 7**",
                        value="Mentioning the moderators or a specific person without proper reason is prohibited.",
                        inline=False)
        embed.add_field(name="**Rule 8**",
                        value="Joining the server with the intent to cause harm (EX: Causing drama, being toxic to others, raiding, advertising, etc..) Will result in serious actions. We do NOT allow people to harm or harass our members here, and we do not allow people join to cause drama.",
                        inline=False)
        embed.add_field(name="**Rule 9**",
                        value="No provocation: such as instigating others to violate the rules, deliberately making members/staff angry, or being toxic.",
                        inline=False)
        embed.add_field(name="**Rule 10**",
                        value="Publicly criticising, starting debates over, or commenting on a moderator’s actions: If you have issues with any of the mods/staff members in the server please DM one of the mods directly. Criticising it in the server causes drama; breaking this rule will result in mutes/bans.",
                        inline=False)
        embed.add_field(name="**Rule 11**",
                        value="Don't post someone's personal information without their permission.",
                        inline=False)
        embed.add_field(name="**Rule 12**",
                        value="No flooding, spamming or raiding: Flooding can refer to all of these things: typing irrelevant or repeated messages, using caps, emoticons, etc. Remember that raiding is against Discord TOS. Discussion of raiding another server is punishable.",
                        inline=False)
        embed.add_field(name="**Rule 13**",
                        value="No bypassing either punishments or rules: for example, leaving and rejoining to escape a mute or saying that you were not being toxic, but rather just having some 'fun' will result in heavier punishments than originally.",
                        inline=False)
        embed.add_field(name="**Rule 14**",
                        value="Profile pictures used must be appropriate. Nicknames that are inappropriate or use unusual or unreadable Unicode are prohibited.",
                        inline=False)
        embed.add_field(name="**Rule 15**",
                        value="Sending any harmful material such as viruses, IP grabbers or malware results in an immediate and permanent ban.",
                        inline=False)
        embed.set_footer(text=ctx.author)
        await ctx.send(embed=embed)

    @commands.command()
    async def testing(self,ctx):
        await ctx.message.delete()
        for x in ctx.guild.members:
            if x in WHITELIST:
                print('found member')
            else:
                print("no")
def setup(bot):
    bot.add_cog(Test(bot))
