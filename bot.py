import asyncio
import os
import random
import urllib.parse
from datetime import datetime
import yaml
import discord
import urbandict
import sys
import traceback
from discord.ext import commands
from discord.utils import get
from pretty_help import PrettyHelp
from pyfiglet import Figlet
from cogwatch import Watcher
from subprocess import Popen, PIPE
from difflib import get_close_matches
from subprocess import Popen
intents = discord.Intents.all()
intents.typing = False
intents.presences = False
with open("apiconfig.yml", "r") as f:
    config = yaml.safe_load(f)
    API_KEY = config["bot"]["API_KEY"]
    COGS_CONFIG = config["bot"]["LOAD_COGS"]

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
        if not message.guild:
            return "~"
        return server_prefixes.get(message.guild.id, "~")


client = commands.Bot(
    command_prefix=get_prefix,
    description="A bot with no restrictions!",
    case_insensitive=True,
    intents=intents,
    help_command=PrettyHelp(no_category="Main"),
    activity=discord.Activity(type=discord.ActivityType.listening, name="help")
)


today = datetime.now()
d1 = today.strftime("%B %d, %Y %H:%M:%S")
print(f"\u001b[36m Starting HS Bot v3 at {d1} \u001b[0m")
if COGS_CONFIG == "all":
    Cogs_to_load = [
        "Cogs." + cog.strip(".py")
        for cog in os.listdir("Cogs/")
        if "py" in cog and "pycache" not in cog
    ]
elif COGS_CONFIG == "normal":
    normal_blacklist = ["Grief", "Test", "Time", "Chess"]
    excluded = len(normal_blacklist)
    Cogs_to_load = [
        "Cogs." + cog.strip(".py")
        for cog in os.listdir("Cogs/")
        if "py" in cog
        and "pycache" not in cog
        and cog.strip(".py") not in normal_blacklist
    ]
elif COGS_CONFIG == "disarmed":
    disarmed_blacklist = ["Grief", "Test", "Spying", "Time"]
    excluded = len(disarmed_blacklist)
    Cogs_to_load = [
        "Cogs." + cog.strip(".py")
        for cog in os.listdir("Cogs/")
        if "py" in cog
        and "pycache" not in cog
        and cog.strip(".py") not in disarmed_blacklist
    ]
print(f"Detected {COGS_CONFIG.upper()} Cogs: ", ", ".join([*Cogs_to_load]))


# Events
@client.event
async def on_connect():
    print("\u001b[32m Successfully connected to discord! \u001b[0m")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        cmd = ctx.invoked_with
        cmds = [cmd.name for cmd in client.commands]
        # cmds = [cmd.name for cmd in bot.commands if not cmd.hidden] # use this to stop showing hidden commands as suggestions
        matches = get_close_matches(cmd, cmds)
        if len(matches) > 0:
            await ctx.send(embed=discord.Embed(description=f'Command "{cmd}" not found, maybe you meant "{matches[0]}"?'))
    print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
    traceback.print_exception(
        type(error), error, error.__traceback__, file=sys.stderr
    )
@client.event
async def on_ready():
    COGS_FAILED = 0
    for cogger in Cogs_to_load:
        try:
            client.load_extension(cogger)
            cogger = cogger.replace("Cogs.", "")
            print(f"Cog \u001b[102m {cogger} \u001b[0m loaded")
        except Exception as e:
            print(f"ERROR {cogger}: \u001b[101m {e} \u001b[0m")
            COGS_FAILED += 1
    else:
        print(
            f"\n\n \u001b[92m {len(client.cogs)} \u001b[0m LOADED | \u001b[91m {COGS_FAILED} \u001b[0m FAILED | \u001b[90m {excluded} \u001b[0m EXCLUDED"
        )
    watcher = Watcher(client, path='Cogs', debug=False)
    await watcher.start()
    print("\u001b[33m Logged in as {0} ({0.id}) \u001b[0m".format(client.user))
    print(
        "\u001b[36m Connected to "
        + str(len(client.guilds))
        + " servers | Connected to "
        + str(len(set(client.get_all_members())))
        + " users | "
        + "Connected to "
        + str(len(client.voice_clients))
        + " voice clients \u001b[0m"
    )
    print(
        "\u001b[7m ------------------------------------------------------------------------------------- \u001b[0m"
    )


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        if message.content.startswith(f"<@!{client.user.id}> "):
            prefix = " ".join(message.content.split()[1:])
            print("changing prefixes")
            with open("prefixes.yaml", "r") as f:
                prefixes = yaml.safe_load(f)
            prefixes[message.guild.id] = prefix
            with open("prefixes.yaml", "w") as f:
                yaml.dump(prefixes, f)
    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    print("\u001b[33m Joining server {0} \u001b[0m".format(guild.name))


@client.event
async def on_guild_leave(guild):
    print("\u001b[33m Left server {0} \u001b[0m".format(guild.name))
    print(f"deleting prefixes for {guild.name}")
    with open("prefixes.yaml", "r") as f:
        prefixes = yaml.safe_load(f)
    prefixes.pop(guild.id, None)
    with open("prefixes.yaml", "w") as f:
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
@client.command(hidden=True)
async def kick(ctx, member: discord.Member, days: int = 1, reason="ur smol hs"):
    await member.kick()
    await ctx.send(f"Kicked {member.name}")
    print(f"{member.name} has been kicked from \u001b[33m {ctx.guild.name} \u001b[0m")


@client.command(hidden=True)
async def ban(ctx, member: discord.Member, days: int = 1, reason="ur big hs"):
    await member.ban(delete_message_days=days)
    await ctx.send("Banned {}".format(ctx.member))
    print(f"{member.name} has been banned from \u001b[33m {ctx.guild.name} \u001b[0m")


# @client.command()
# async def help(ctx):
#     contents = [['~purge','Deletes X amount of messages in a channel'],['~ping','Gives ping to client (expressed in ms)']
#     ,['~invite','Returns invite link of the client'],['~echo','Repeats your message'],['~connect','Connect to a valid voice channel']
#     ####################################################################
#     ,['~play or ~p (song name or link)','Search for and add a song to the Queue'],['~autoplay or ~ap','Autoplay'],['~pause','Pause the player'],['~resume','Resume the player from a paused state'],['~skip','Skip the currently playing song']
#     ,['~volume (number)','Set the player volume'],['~now_playing','Retrieve the currently playing song'],['~queue','Retrieve information on the next 5 songs from the queue'],['~clear or ~clr','Clear queue'],['~shuffle','Shuffle queue']
#     ,['~stop','Stop and disconnect the player and controller'],['~equalizer','Equalizer for the player'],['~loop','Loop current playing song'],['~lyrics','Gives lyrics to the current playing song'],['~remove (number)','Remove the chosen song number in the queue']
#     ,['~last','Plays previous song'],['~playlist (list, play,refresh, region, save, delete)','***list***\n```gets spotify featured playlists at the set region\nNOTE: has an extra parameter saved (ex: playlist list saved) which gets saved playlists```\n***play***\n```plays your desired playlist (ex: playlist play [Name of playlist])```\n***region***\n```Changes your spotify featured playlist region (Needs a region where spotify is available)```\n***refresh***\n```Forces refresh of featured playlists```\n***save***\n```saves a playlist by the name (ex: playlist save (NAME OF PLAYLIST))']
#     ####################################################################
#     ,['~cat','Gives a random cat picture'],['~dog','Gives a random dog picture'],['~fox','Gives a random fox picture']
#     ,['~rabbit','Gives a random rabbit picture'],['~duck','Gives a random duck picture'],['~img','Google searches your img'],['~insult (@member)','Generates an insult for the tagged member']
#     ####################################################################
#     ,['~hotcalc (@member)','Generates a random percentage that determinds how hot you are'],['~pepeflip','Sends good luck with a crying or smiling pepe']
#     ####################################################################
#     ,['~batman_slap','Generates the meme'],['~distracted','Generates the meme']
#     ,['~shame','Generates the meme'],['~table_flip','Generates the meme'],['~first_time','Generates the meme'],['~heaven','Generates the meme'],['~npc','Generates the meme'],['~stonks','Generates the meme']
#     ,['~wolverine','Generates the meme'],['~widen','widens your profile picture'],['~speedy','Generates the meme'],['~milk','Generates the meme'],['~car_reverse','Generates the meme'],['~water','Generates the meme'],['~emergency','Generates the meme'],['~eject','Generates the meme']
#     ,['~rip','Generates the meme']]#ALVIN IS BIG FURRY
#     embeds = []
#     pages = 5
#     cur_page = 0
#     embed = discord.Embed(title=f"Help")
#     [embed.add_field(name=x[0],value=x[1]) for x in list(itertools.islice(contents,0,4))]
#     embed.set_footer(text=f"Page 1/{pages}")
#     message = await ctx.send(embed=embed)
#     embeds.append(embed)
#     # getting the message object for editing and reacting
#     embed2 = discord.Embed(title=f"Help")
#     [embed2.add_field(name=x[0],value=x[1]) for x in list(itertools.islice(contents,5,22))]
#     embed2.set_footer(text=f"Page 2/{pages}")
#     await message.add_reaction("◀️")
#     await message.add_reaction("▶️")
#     embeds.append(embed2)
#
#     embed3 = discord.Embed(title=f"Help")
#     [embed3.add_field(name=x[0],value=x[1]) for x in list(itertools.islice(contents,23,29))]
#     embed3.set_footer(text=f"Page 3/{pages}")
#     await message.add_reaction("◀️")
#     await message.add_reaction("▶️")
#     embeds.append(embed3)
#
#     embed4 = discord.Embed(title=f"Help")
#     [embed4.add_field(name=x[0],value=x[1]) for x in list(itertools.islice(contents,30,31))]
#     embed4.set_footer(text=f"Page 4/{pages}")
#     await message.add_reaction("◀️")
#     await message.add_reaction("▶️")
#     embeds.append(embed4)
#
#     embed5 = discord.Embed(title=f"Help")
#     [embed5.add_field(name=x[0],value=x[1]) for x in list(itertools.islice(contents,32,48))]
#     embed5.set_footer(text=f"Page 5/{pages}")
#     await message.add_reaction("◀️")
#     await message.add_reaction("▶️")
#     embeds.append(embed5)
#
#     def check(reaction, user):
#         return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
#         # This makes sure nobody except the command sender can interact with the "menu"
#
#     while True:
#         try:
#             reaction, user = await client.wait_for("reaction_add", timeout=120, check=check)
#             # waiting for a reaction to be added - times out after x seconds, 60 in this
#             # example
#
#             if str(reaction.emoji) == "▶️" and cur_page != pages:
#                 cur_page += 1
#                 await message.edit(embed=embeds[cur_page])
#                 await message.remove_reaction(reaction, user)
#
#             elif str(reaction.emoji) == "◀️" and cur_page > 1:
#                 cur_page -= 1
#                 await message.edit(embed=embeds[cur_page])
#                 await message.remove_reaction(reaction, user)
#
#             else:
#                 await message.remove_reaction(reaction, user)
#                 # removes reactions if the user tries to go forward on the last page or
#                 # backwards on the first page
#         except asyncio.TimeoutError:
#             await message.delete()
#             break
#             # ending the loop if user doesn't react after x seconds


@client.command(hidden=True, description="Delete messages on mass")
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    print("Clearing messages")


@client.command(hidden=True, description="Latency to discord")
async def ping(ctx):
    color = discord.Color(value=0x00FF00)
    em = discord.Embed(color=color, title="Pong! Your latency is:")
    em.description = f"{client.latency * 1000:.4f} ms"
    em.set_footer(text="Psst...A heartbeat is 27 ms!")
    await ctx.send(embed=em)


@client.command(description="Get info of the bot")
async def info(ctx):
    """Get info of the bot"""
    command = ['git',"describe","--always"]
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode("utf8")
    fmt = (
        f"**{client.user.name} commit:** `{stdout}`\n\n"
        f"Vote bot at [top.gg](https://top.gg/bot/799134976515375154/vote)/[discordbotlist.com](https://discordbotlist.com/bots/doorbanger/upvote).\n"
        f"Support: Koalaa#6001 or skot#6579\n"
    )
    embed = discord.Embed(description=fmt)
    await ctx.send(embed=embed)
    process.stdout.close()
@client.command(hidden=True, description="Invite link of bot")
async def invite(ctx):
    embed = discord.Embed(
        description=f"[Invite me here](https://discordapp.com/api/oauth2/authorize?client_id={client.user.id}&permissions=0&scope=bot)",
        colour=discord.Colour(0xFF001D),
    )
    await ctx.send(embed=embed)


@client.command(hidden=True, description="Echo your text")
async def echo(ctx, *, args):
    await ctx.message.delete()
    output = ""
    for word in args:
        output += word
        output += ""
        await ctx.send(output)


@client.command(hidden=True)
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split("d"))
    except Exception:
        await ctx.send("Format has to be in NdN!")
    result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@client.command(hidden=True,description="For when you wanna settle the score some other way")
async def choose(ctx, *choices: str):
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


@client.command(hidden=True)
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
    elif (a == b and b == d) or (a == c and c == d) or (b == c):
        await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
    else:
        await ctx.send(f"{slotmachine} No match, you lost 😢")


@client.command(hidden=True)
async def reversecard(ctx, *, text: str):
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


@client.command(hidden=True)
async def claps(ctx, *, message):
    """Adds clapping emojis to text"""
    await ctx.send(f":clap: {message} :clap:")


@client.command(hidden=True)
async def dict(ctx, *, word: str):
    """Gets a term from urbandictionary"""
    urb = urbandict.define(word)
    if "There aren't any definitions" in urb[0]["def"]:
        await ctx.send("No definitions found")
    msg = "**{0}**\n".format(word)
    msg += "`Definition:` {0}\n".format(urb[0]["def"].replace("\n", ""))
    msg += "`Example:` {0}".format(urb[0]["example"].replace("\n", ""))
    await ctx.send(msg)


@client.command(hidden=True)
async def allmembers(ctx):
    await ctx.message.delete()
    await ctx.send("Getting all members...", delete_after=19)
    members = {member for member in sorted(set(client.get_all_members()))}
    print(members)


client.run(API_KEY)
# if not input("Use jojo account?"):
#     client.run("NjU0NTgxMjczMDI4ODUzNzcw.XfHoUQ.AYl_OYnkThODtoXePBOXqwDCo4k")  # Popekanga account
# else:
#     client.run("Nzk5MTM0OTc2NTE1Mzc1MTU0.X__KcQ.Xwz2VzbVPu2fnQxjsTs7dVHH-Ww")
