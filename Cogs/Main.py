from discord.ext import commands
from subprocess import Popen, PIPE
import discord

class Main(commands.Cog,name="General", description="Basic commands"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(hidden=True, description="Delete messages on mass")
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        print("Clearing messages")


    @commands.command(hidden=True, description="Latency to discord")
    async def ping(self, ctx):
        """"Latency to discord"""
        color = discord.Color(value=0x00FF00)
        em = discord.Embed(color=color, title="Bot ping to discord is:")
        em.description = f"{self.bot.latency * 1000//1} ms"
        em.set_footer(text="Psst...A heartbeat is 27 ms!")
        await ctx.send(embed=em)


    @commands.command(description="Get info of the bot")
    async def info(self, ctx):
        """Get info of the bot"""
        command = ['git',"describe","--always"]
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf8")
        fmt = (
            f"**{self.bot.user.name} commit:** `{stdout}`\n\n"
            f"Vote bot at [top.gg](https://top.gg/bot/799134976515375154/vote)/[discordbotlist.com](https://discordbotlist.com/bots/doorbanger/upvote).\n"
            f"Support: Koalaa#6001 or skot#6579\n"
        )
        embed = discord.Embed(description=fmt)
        await ctx.send(embed=embed)
        process.stdout.close()
    @commands.command(description="Invite link of bot")
    async def invite(self, ctx):
        """Get an invite link for the bot to invite it to other servers!"""
        embed = discord.Embed(
            description=f"[Invite me here](https://discordapp.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=3172417&scope=bot)",
            colour=discord.Colour(0xFF001D),
        )
        await ctx.send(embed=embed)


    @commands.command(hidden=True)
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split("d"))
        except Exception:
            await ctx.send("Format has to be in NdN!")
        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)


    @commands.command(hidden=True,description="For when you wanna settle the score some other way")
    async def choose(self, ctx, *, choices: str):
        """Chooses between multiple choices."""
        if "koala" in choices or "Koalaa" in choices or "koalaa" in choices:
            await ctx.send("I choose Koalaa cuz homo")
        elif "dan" in choices or "daniel" in choices or "Dan" in choices:
            embed = discord.Embed(
                title="scott x daniel is real ship", colour=discord.Colour.dark_red()
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/512906616929124371/721064750284275782/dan_rape.jpg"
            )
            await ctx.send(embed=embed)
        elif "staff" in choices and "dwraxk" in choices:
            await ctx.send("staff = rape koala")
            await asyncio.sleep(1)
            await ctx.send("dwraxk = rape howard")
        elif "scoot" in choices or "scott" in choices or "Scott" in choices:
            await ctx.send("I love scott cuz he gay :ok_hand: :eggplant: :sweat_drops:")
        elif "HS" in choices or "hs" in choices or "Hs" in choices:
            await ctx.send("ʳᵉᵉᵉᵉᵉ")
        elif "hs" in choices and "koala" in choices:
            await ctx.send("hs")
        else:
            await ctx.send(random.choice(choices))


    @commands.command(hidden=True)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒💲"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)
        d = random.choice(emojis)
        e = random.choice(emojis)
        f = random.choice(emojis)
        slotmachine = f"**[ {a} {b} {c} {d} {e} {f}]\n{ctx.author.name}**,"

        if a == b == c == d == e == f:
            await ctx.send(f"{slotmachine} All matching, Jackpot! 🎉")
        elif (a == b and b == d) or (a == c and c == d) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")


    @commands.command(hidden=True)
    async def reversecard(self, ctx, *, text: str):
        """!poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed

        """
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour.dark_red())
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/662589204974403585/665222655309250600/no_u.jpg"
        )
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev} ")
        await ctx.send(embed=embed)


    @commands.command(hidden=True)
    async def claps(self, ctx, *, message):
        """Adds clapping emojis to text"""
        await ctx.send(f":clap: {message} :clap:")


    @commands.command(hidden=True)
    async def allmembers(self, ctx):
        await ctx.message.delete()
        await ctx.send("Getting all members...", delete_after=19)
        members = {member for member in sorted(set(self.bot.get_all_members()))}
        print(members)
    @commands.command()
    async def privacy(self, ctx):
        """Our privacy policy"""
        embed= discord.Embed(title="Our privacy policy",description="We here at **Doorbanger** take your privacy very seriously!\nWe collect information such as **Member ID**, **Guild ID** and **Anonymous Usage of Commands** in order to further improve our service!")
        embed.set_footer(text="By using our bot, you agree that we collect data as listed.")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/799211893646295051/831897629708255253/27833342_1.jpg")
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Main(bot))
