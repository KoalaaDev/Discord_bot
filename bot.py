import asyncio
import os
from datetime import datetime
import yaml
import discord
import sys
import traceback
from discord.ext import commands
from cogwatch import Watcher
from difflib import get_close_matches

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
with open("apiconfig.yml", "r") as f:
    config = yaml.safe_load(f)
    API_KEY = config["bot"]["API_KEY"]

intents.guilds = True

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
    activity=discord.Activity(type=discord.ActivityType.listening, name="help")
)


today = datetime.now()
d1 = today.strftime("%B %d, %Y %H:%M:%S")
print(f"\u001b[36m Starting AnimeSongBot at {d1} \u001b[0m")
Cogs_to_load = [
        "Cogs." + cog[:-3]
        for cog in os.listdir("Cogs/")
        if "py" in cog and "pycache" not in cog
    ]

print(f"Detected Cogs: ", ", ".join([*Cogs_to_load]))
# Events


@client.event
async def on_connect():
    print("\u001b[32m Successfully connected to discord! \u001b[0m")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        if len(ctx.guild.members) > 500:
            return
        cmd = ctx.invoked_with
        cmds = [cmd.name for cmd in client.commands if not cmd.hidden]
        matches = get_close_matches(cmd, cmds, 1)
        if len(matches) > 0:
            if invoke_suggestions:
                if matches[0] == 'play':
                    embed = discord.Embed(description=f'Command "{cmd}" not found, Assuming you meant "{matches[0]}"')
                    embed.set_footer(text="Note: this can be turned off in config")
                    await ctx.send(embed=embed)
                    return await ctx.invoke(client.get_command(matches[0]), search=ctx.message.content.split(cmd)[1])
                return await ctx.invoke(client.get_command(matches[0]))
            return await ctx.send(embed=discord.Embed(description=f'Command "{cmd}" not found, maybe you meant "{matches[0]}"?'))
    print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
    traceback.print_exception(
        type(error), error, error.__traceback__, file=sys.stderr
    )


@client.event
async def on_ready():
    COGS_FAILED = 0
    for cogger in Cogs_to_load:
        try:
            await client.load_extension(cogger)
            cogger = cogger.replace("Cogs.", "")
            print(f"Cog \u001b[102m {cogger} \u001b[0m loaded")
        except Exception as e:
            print(f"ERROR {cogger}: \u001b[101m {e} \u001b[0m")
            COGS_FAILED += 1
    else:
        print(
            f"\n\n \u001b[92m {len(client.cogs)} \u001b[0m LOADED | \u001b[91m {COGS_FAILED} \u001b[0m FAILED"
        )
    watcher = Watcher(client, path='Cogs', debug=False)
    await watcher.start()
    print("\u001b[33m COGWATCH STARTED... \u001b[0m")
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


client.run(API_KEY)
