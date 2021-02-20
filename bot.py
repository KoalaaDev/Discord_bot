import asyncio
import os
import random
import urllib.parse
from datetime import datetime
import yaml
import discord
import urbandict
from discord.ext import commands
from discord.utils import get
from passlib.hash import sha512_crypt as sha512
from pyfiglet import Figlet

intents = discord.Intents.all()
with open("apiconfig.yml", "r") as f:
    config = yaml.safe_load(f)
    API_KEY = config['bot']['API_KEY']
    COGS_CONFIG = config['bot']['LOAD_COGS']

intents.members = True
intents.guilds = True
fonts = [
    "1943____",
    "starwars",
    "graffiti",
    "zone7___",
    "zig_zag_",
]
custom2_fig = Figlet(font=random.choice(fonts))
custom_fig = Figlet(font="starwars")
sponsor = [
    "No u",
    "Oh You're approaching me?",
    "#CommitHS",
    "Illusion 100",
    "FBI",
    "Notch",
]
print(custom2_fig.renderText("Message of the day:"))
print(custom_fig.renderText(random.choice(sponsor)))
async def get_prefix(bot, message):
    with open("prefixes.yaml") as f:
        server_prefixes = yaml.safe_load(f)
        return server_prefixes.get(message.guild.id,"~")
client = commands.Bot(
    command_prefix=get_prefix,
    description="A Totally normal bot!",
    case_insensitive=True,intents=intents
)

client.remove_command("help")
today = datetime.now()
d1 = today.strftime("%B %d, %Y %H:%M:%S")
print(f"\u001b[36m Starting HS Bot v2 at {d1} \u001b[0m")
if COGS_CONFIG == 'all':
    Cogs_to_load = [
        "Cogs." + cog.strip(".py") for cog in os.listdir("Cogs/")
        if "py" in cog and "pycache" not in cog
    ]
elif COGS_CONFIG == 'normal':
    Cogs_to_load = ["Cogs." + cog.strip(".py") for cog in os.listdir("Cogs/") if "py" in cog and "pycache" not in cog and "Grief" not in cog and "Test" not in cog]
elif COGS_CONFIG == 'disarmed':
    Cogs_to_load = ["Cogs." + cog.strip(".py") for cog in os.listdir("Cogs/")
    if "py" in cog and "pycache" not in cog and "Grief" not in cog and "Spying" not in cog and "Test" not in cog]
print(f"Detected {COGS_CONFIG.upper()} Cogs: ", ", ".join([*Cogs_to_load]))


# Events
@client.event
async def on_connect():
    print("\u001b[32m Successfully connected to discord! \u001b[0m")


@client.event
async def on_ready():
    for cogger in Cogs_to_load:
        try:
            client.load_extension(cogger)
            cogger = cogger.replace("Cogs.", "")
            print(f"Cog \u001b[43m {cogger} \u001b[0m loaded")
        except Exception as e:
            print(f"ERROR {cogger}: {e}")
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="help"))
    print("\u001b[33m Logged in as {0} ({0.id}) \u001b[0m".format(client.user))
    print("\u001b[36m Connected to " + str(len(client.guilds)) +
          " servers | Connected to " +
          str(len(set(client.get_all_members()))) + " users | " +
          "Connected to " + str(len(client.voice_clients)) +
          " voice clients \u001b[0m")
    print(
        "\u001b[37m ------------------------------------------------------------------------------------- \u001b[0m"
    )

@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = "Welcome {0.mention} to {1.name}!".format(member, guild)
        await guild.system_channel.send(to_send)

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        prefix = "".join(message.content.split()[1:])
        print("changing prefixes")
        with open('prefixes.yaml', 'r') as f:
            prefixes = yaml.safe_load(f)
        prefixes[message.guild.id] = prefix
        with open("prefixes.yaml","w") as f:
            yaml.dump(prefixes, f)
    await client.process_commands(message)
@client.event
async def on_guild_join(guild):
    print("\u001b[33m Joining server {0} \u001b[0m".format(guild.name))


@client.event
async def on_guild_leave(guild):
    print("\u001b[33m Left server {0} \u001b[0m".format(guild.name))
    print(f"deleting prefixes for {guild.name}")
    with open('prefixes.yaml', 'r') as f:
        prefixes = yaml.safe_load(f)
    prefixes.pop(guild.id,None)
    with open("prefixes.yaml","w") as f:
        yaml.dump(prefixes, f)

@client.event
async def on_disconnect():
    print("\u001b[33m Connection lost to discord! \u001b[0m")
    print("Retrying connection in 5 secs")
    await asyncio.sleep(5)


@client.event
async def on_resumed():
    print("\u001b[33m Connected back to discord! \u001b[0m")


# sorta good purpose
@client.command()
async def kick(ctx,
               member: discord.Member,
               days: int = 1,
               reason="ur smol hs"):
    await member.kick()
    await ctx.send(f"Kicked {member.name}")
    print(
        f"{member.name} has been kicked from \u001b[33m {ctx.guild.name} \u001b[0m"
    )


@client.command()
async def ban(ctx, member: discord.Member, days: int = 1, reason="ur big hs"):
    await member.ban(delete_message_days=days)
    await ctx.send("Banned {}".format(ctx.member))
    print(
        f"{member.name} has been banned from \u001b[33m {ctx.guild.name} \u001b[0m"
    )


@client.command()
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.dark_blue())
    embed.set_author(name="help")
    embed.add_field(name="-ping",
                    value="Gives ping to client (expressed in ms)",
                    inline=False)
    embed.add_field(name="-kick", value="Kicks specified user", inline=False)
    embed.add_field(name="-ban", value="Bans specified user", inline=False)
    embed.add_field(name="-info",
                    value="Gives information of a user",
                    inline=False)
    embed.add_field(name="-invite",
                    value="Returns invite link of the client",
                    inline=False)
    embed.add_field(name="-purge",
                    value="Clears an X amount of messages",
                    inline=False)
    embed.add_field(name="-echo", value="Repeats your message", inline=False)
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/591237894715342874/658309549027098634/hsisindian.png"
    )
    embed.set_footer(text="for voice commands type -voicehelp")
    await ctx.send(embed=embed)

@client.command()
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    print("Clearing messages")


@client.command()
async def ping(ctx):
    color = discord.Color(value=0x00FF00)
    em = discord.Embed(color=color, title="Pong! Your latency is:")
    em.description = f"{client.latency * 1000:.4f} ms"
    em.set_footer(text="Psst...A heartbeat is 27 ms!")
    await ctx.send(embed=em)


@client.command()
async def info(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("Please input a user.")
    else:
        await ctx.send(
            "The user's name is: {}".format(user.name) +
            "\nThe user's ID is: {}".format(user.id) +
            "\nThe user's current status is: {}".format(user.status) +
            "\nThe user's highest role is: {}".format(user.top_role) +
            "\nThe user joined at: {}".format(user.joined_at))


@client.command()
async def invite(ctx):
    embed = discord.Embed(
        description=
        "[Invite me here](https://discordapp.com/api/oauth2/authorize?client_id=654581273028853770&permissions=8&scope=bot)",
        colour=discord.Colour(0xFF001D),
    )
    await ctx.send(embed=embed)


@client.command()
async def echo(ctx, *, args):
    await ctx.message.delete()
    output = ""
    for word in args:
        output += word
        output += ""
        await ctx.send(output)


@client.command()
async def add(ctx, left: str, right: str):
    await ctx.send(left + right)


@client.command()
async def multiply(ctx, left: str, right: str):
    if left == "hs" and right == "hs":
        await ctx.send("hs2")
    else:
        await ctx.send(int(left) * int(right))


@client.command()
async def divide(ctx, left: int, right: int):
    await ctx.send(left / right)


@client.command()
async def minus(ctx, left: int, right: int):
    await ctx.send(left - right)


@client.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split("d"))
    except Exception:
        await ctx.send("Format has to be in NdN!")
    result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@client.command(
    description="For when you wanna settle the score some other way")
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    if "koala" in choices or "Koalaa" in choices or "koalaa" in choices:
        await ctx.send("I choose Koalaa cuz homo")
    elif "dan" in choices or "daniel" in choices or "Dan" in choices:
        embed = discord.Embed(title="scott x daniel is real ship",
                              colour=discord.Colour.dark_red())
        embed.set_image(
            url=
            "https://cdn.discordapp.com/attachments/512906616929124371/721064750284275782/dan_rape.jpg"
        )
        await ctx.send(embed=embed)
    elif "staff" in choices and "dwraxk" in choices:
        await ctx.send("staff = rape koala")
        await asyncio.sleep(1)
        await ctx.send("dwraxk = rape howard")
    elif "scoot" in choices or "scott" in choices or "Scott" in choices:
        await ctx.send(
            "I love scott cuz he gay :ok_hand: :eggplant: :sweat_drops:")
    elif "HS" in choices or "hs" in choices or "Hs" in choices:
        await ctx.send("ʳᵉᵉᵉᵉᵉ")
    elif "hs" in choices and "koala" in choices:
        await ctx.send("hs")
    else:
        await ctx.send(random.choice(choices))





@client.command()
async def slot(ctx):
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
    elif (a == b and b==d) or (a == c and c==d) or (b == c):
        await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
    else:
        await ctx.send(f"{slotmachine} No match, you lost 😢")


@client.command()
async def reversecard(ctx, *, text: str):
    """!poow ,ffuts esreveR
    Everything you type after reverse will of course, be reversed

    """
    await ctx.message.delete()
    embed = discord.Embed(colour=discord.Colour.dark_red())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/662589204974403585/665222655309250600/no_u.jpg"
    )
    t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    await ctx.send(f"🔁 {t_rev} ")
    await ctx.send(embed=embed)


@client.command()
async def hslanguage(ctx, *, name: str):
    await ctx.message.delete()
    hslanguage = sha512.hash(name, rounds=5000)
    user = ctx.author
    await user.send(
        f"""Converted {name} in sha512 to: ```css\n{hslanguage}```""")


@client.command()
async def claps(ctx, *, message):
    await ctx.send(f":clap: {message} :clap:")


@client.command()
async def ytsearch(ctx, *, search: str):
    encoded = urllib.parse.quote_plus(search)
    if search == "hs" or search == "HS":
        await ctx.send(
            f"HS RESULTS: https://www.youtube.com/results?search_query={encoded}"
        )
    else:
        await ctx.send(
            f"Link to results: https://www.youtube.com/results?search_query={encoded}"
        )


@client.command()
async def google(ctx, *, search: str):
    encoded = urllib.parse.quote_plus(search)
    if search == "hs" or search == "HS":
        await ctx.send(f"HS RESULTS:https://www.google.com/search?q={encoded}")
    else:
        await ctx.send(f"results: https://www.google.com/search?q={encoded}")


@client.command()
async def dict(ctx, *, word: str):
    urb = urbandict.define(word)
    if "There aren't any definitions" in urb[0]["def"]:
        await ctx.send("No definitions found")
    msg = "**{0}**\n".format(word)
    msg += "`Definition:` {0}\n".format(urb[0]["def"].replace("\n", ""))
    msg += "`Example:` {0}".format(urb[0]["example"].replace("\n", ""))
    await ctx.send(msg)


@client.command()
async def allmembers(ctx):
    await ctx.message.delete()
    await ctx.send("Getting all members...", delete_after=19)
    members = [member for member in sorted(set(client.get_all_members()))]
    print(members)


@client.command()
async def allguilds(ctx):
    await ctx.message.delete()
    await ctx.send("Getting all guilds...", delete_after=19)
    guilds = [guild for guild in client.guilds]
    print(guilds)
    await ctx.send(guilds, delete_after=20)


@client.command()
async def changeregion(ctx, *, region):
    await ctx.message.delete()
    # region=['amsterdam','brazil','dubai','eu_central','india','hongkong','singapore','russia','us_west','us_south','us_central','us_east','sydney','southafrica','london','japan']
    server = ctx.message.guild
    try:
        await server.edit(region=region)
        print(f"changed region to {region}")
    except Exception as e:
        print(f"Fail to change regions: {e}")


@client.command()
async def unbanall(ctx):
    for guild in client.guilds:
        bans = await guild.bans()
        for user in bans:
            try:
                await guild.unban(user[0].name)
                ctx.send("Unbanning everyone...")
                print(f"unbanned {user}")
            except discord.NotFound:
                print(f"did not find {user} in {guild}")


@client.command()
async def listbans(ctx):
    for guild in client.guilds:
        for member in guild.members:
            members = get(await guild.bans(), user=member)
            if members == "None":
                pass
            else:
                print(f"{guild}'s ban list:", members)


@client.command()
async def unbanid(ctx, *, id: int):
    if id is None:
        await ctx.send("Please input id")
    for guild in client.guilds:
        try:
            user = await client.fetch_user(id)
            await guild.unban(user)
            await ctx.send("unbanning user id from bot servers")
            print(f"unbanned {ctx.message.author} from {guild}")
        except discord.errors.NotFound:
            print(f"could not find {ctx.message.author} in {guild}'s ban list")


@client.command()
async def inviteall(ctx):
    for guild in client.guilds:
        for channel in guild.channels:
            try:
                invitelinknew = await channel.create_invite(
                    destination=channel,
                    xkcd=True,
                    max_age=0,
                    max_uses=0,
                    reason=f"Invite sent by {guild.owner}",
                )
                await ctx.send(invitelinknew)
                print(invitelinknew)
            except discord.errors.NotFound:
                print(f"Could not find invite for {guild}")


@client.command()
async def load_jsk(ctx):
    client.load_extension("jishaku")


@client.command()
async def offline(ctx):
    await client.change_presence(status=discord.Status.invisible)
    print("[bot going offline] Going under!")


@client.command()
async def idle(ctx):
    await client.change_presence(status=discord.Status.idle)
    print("[bot going away] Going AFK!")

@client.command()
async def invitelink(ctx, id):
    server = client.get_guild(id)
    link = server.channels.create_invite(destination=server,
                                             xkcd=True,
                                             max_age=0,
                                             max_uses=0)
    await ctx.send(link)


client.run(API_KEY)
# if not input("Use jojo account?"):
#     client.run("NjU0NTgxMjczMDI4ODUzNzcw.XfHoUQ.AYl_OYnkThODtoXePBOXqwDCo4k")  # Popekanga account
# else:
#     client.run("Nzk5MTM0OTc2NTE1Mzc1MTU0.X__KcQ.Xwz2VzbVPu2fnQxjsTs7dVHH-Ww")
