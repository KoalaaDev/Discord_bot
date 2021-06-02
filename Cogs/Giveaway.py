import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Giveaways are now ready!")

    def convert(self, time):
        pos = ["s","m","h","d"]

        time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return val * time_dict[unit]

    @commands.command(name="giftstart", aliases=["gstart","gcreate"])
    @commands.has_permissions(administrator = True)
    async def giveaway_start(self, ctx):
        question1 = discord.Embed(title=  "Giveaway Question #1", color = ctx.author.color)
        question1.add_field(name = "Question:", value = f"Which channel would you like to host the giveaway in? Mention it!")
        question1.add_field(name = "Channel Mention Example:", value =f"Mention a channel like {ctx.channel.mention}")
        question1.set_footer(text = "Channel Check")

        question2 = discord.Embed(title=  "Giveaway Question #2", color = ctx.author.color)
        question2.add_field(name = "Question:", value = f"How long would you like this giveaway to last? ")
        question2.add_field(name = "Time Example:", value =f"Mention your number first and then type a unit.\nUnits: (s|m|h|d)")
        question2.set_footer(text = "Don't fail the questions!")

        question3 = discord.Embed(title=  "Giveaway Question #3", color = ctx.author.color)
        question3.add_field(name = "Last Question:", value = f"What is the prize of this giveaway?")
        question3.set_footer(text = "Don't fail the questions!")

        errorEmbed1 = discord.Embed(title = 'Giveaway Failed', color = ctx.author.color)
        errorEmbed1.add_field(name = "Reason:", value = "You did not mention a channel properly")
        errorEmbed1.add_field(name = "Channel:", value = f"{ctx.channel.mention}")

        errorEmbed2 = discord.Embed(title = 'Giveaway Failed', color = ctx.author.color)
        errorEmbed2.add_field(name = "Reason:", value = "You did not mention the time properly!")
        errorEmbed2.add_field(name = "Channel:", value = f"Write a number and then units (s|m|h|d)")

        timeDelay = discord.Embed(title = 'Giveaway Failed', color = ctx.author.color)
        timeDelay.add_field(name = "Reason:", value = "You did not answer in time!")
        timeDelay.add_field(name = "Next Steps:", value = "Make sure you answer in 45 seconds")

        questions = [question1, question2, question3]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(embed = i)

            try:
                msg = await self.bot.wait_for('message', timeout=45.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(embed = timeDelay)
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(embed = errorEmbed1)
            return

        channel = self.bot.get_channel(c_id)
        time = self.convert(answers[1])

        if time == -1:
            await ctx.send(embed = errorEmbed2)
            return
        elif time == -2:
            await ctx.send(f"The time must be an integer. Please enter an integer next time")
            return

        prize = answers[2]

        await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")
        embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)
        embed.add_field(name = "Hosted by:", value = ctx.author.mention)
        embed.set_footer(text = f"Ends {answers[1]} from now!")
        my_msg = await channel.send(embed = embed)
        await my_msg.add_reaction("🎉")
        await asyncio.sleep(time)
        new_msg = await channel.fetch_message(my_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        if len(users) == 0:
            em = discord.Embed(title = 'Giveaway Failed', color = ctx.author.color)
            em.add_field(name = "Reason:", value = "No one joined D:")
            await channel.send(embed = em)
            return
        winner = random.choice(users)
        newembed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)
        newembed.add_field(name = "Hosted by:", value = ctx.author.mention)
        newembed.add_field(name = "Winner", value = f"{winner.mention}")
        newembed.set_footer(text = f"Ends {answers[1]} from now!")
        await my_msg.edit(embed = newembed)
        await channel.send(f"Congratulations! {winner.mention} won {prize}")

    @commands.command(name="giftrrl", aliases=["reroll"])
    @has_permissions(manage_guild=True)
    # @has_role("admin")
    async def giveaway_reroll(self, ctx, channel : discord.TextChannel, id_: int):
        try:
            msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The channel or ID mentioned was incorrect")
        users = await msg.reactions[0].users().flatten()
        if len(users) <= 0:
            emptyEmbed = Embed(title="Giveaway Time !!",
                                   description=f"Win a Prize today")
            emptyEmbed.add_field(name="Hosted By:", value=ctx.author.mention)
            emptyEmbed.set_footer(text="No one won the Giveaway")
            await msg.edit(embed=emptyEmbed)
            return
        if len(users) > 0:
            winner = choice(users)
            winnerEmbed = Embed(title="Giveaway Time !!",
                                description=f"Win a Prize today",
                                colour=0x00FFFF)
            winnerEmbed.add_field(name=f"Congratulations On Winning Giveaway", value=winner.mention)
            await msg.edit(embed=winnerEmbed)
            return

def setup(bot):
    bot.add_cog(Giveaways(bot))
