import asyncio
import datetime
import discord
import humanize
import itertools
import re
import sys
import traceback
import wavelink
from discord.ext import commands, tasks
from typing import Union
import itertools
import random
import os
import requests
import yaml
RURL = re.compile('https?:\/\/(?:www\.)?.+')
class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None
        self.now_playing_uri = None
        self.now_playing_id = None
        self.next = asyncio.Event()
        self.queue = asyncio.Queue()
        self.auto_play_queue = asyncio.Queue()
        self.auto_play = False
        self.user = None
        self.volume = 50
        self.now_playing = None
        self.loop = False
        self.bot.loop.create_task(self.controller_loop())
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apiconfig.yml')
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
            self.YoutubeAPIKEY = config['music']['YoutubeAPIKEY']
    def YoutubeSuggestion(self):
        Videos = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&relatedToVideoId={self.now_playing_id}&type=video&key={self.YoutubeAPIKEY}").json()
        return list(set(["https://www.youtube.com/watch?v="+x['id']['videoId'] for x in Videos['items']]))


    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)
        while True:
            if self.now_playing:
                await self.now_playing.delete()
            self.next.clear()
            song = await self.queue.get()
            await player.play(song)
            MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{song}]({self.now_playing_uri}) [{self.user}]")
            self.now_playing = await self.channel.send(embed=MusicEmbed)
            await self.next.wait()
            if self.loop:
                while self.loop:
                    self.next.clear()
                    await player.play(song)
                    await self.next.wait()
            if self.auto_play and not self.loop and self.queue.empty() and not self.auto_play_queue.empty():
                while self.auto_play and self.queue.empty():
                    await self.now_playing.delete()
                    self.next.clear()
                    song = await self.auto_play_queue.get()
                    MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{song}]({song.uri}) [{self.user}]")
                    self.now_playing = await self.channel.send(embed=MusicEmbed)
                    await player.play(song)
                    await self.next.wait()
class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}
        self.Toggle = itertools.cycle([True,False])
        self.autoplay = itertools.cycle([True,False])
        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())
    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)

        node = await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                                     port=8080,
                                                     rest_uri='http://127.0.0.1:8080',
                                                     password='youshallnotpass',
                                                     identifier='TEST',
                                                     region='singapore')
        # Set our node hook callback
        node.set_hook(self.on_event_hook)
    async def on_event_hook(self, event):
        """Node hook callback."""
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)
            controller.next.set()

    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, commands.Context):
            gid = value.guild.id
        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller
    @tasks.loop(seconds=2.0)
    async def check_autoplay_queue(self, ctx):
        controller = self.get_controller(ctx)
        if controller.auto_play_queue.empty() and controller.now_playing_id:
            videolist = controller.YoutubeSuggestion()

            for video in videolist:
                tracks = await self.bot.wavelink.get_tracks(video)
                print(controller.auto_play_queue._queue)
                try:
                    track = tracks[0]
                    controller.now_playing_id = track.ytid
                    await controller.auto_play_queue.put(track)
                except TypeError:
                    print(video)
    @tasks.loop(seconds=60.0)
    async def check_listen(self, ctx):
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        channel = self.bot.get_channel(player.channel_id)
        member_list = [x.name for x in channel.members if x.bot == False]
        if not member_list:
            await player.stop()
            try:
                del self.controllers[ctx.guild.id]
            except KeyError:
                await player.disconnect()
            await player.disconnect()
            self.check_autoplay_queue.cancel()
            controller.auto_play = False
            controller.loop = False
    async def cog_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def cog_command_error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to a valid voice channel."""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        msg = await ctx.send(f'Connecting to **`{channel.name}...`**', delete_after=15)
        await player.connect(channel.id)
        await msg.edit(content=f"Connected to **`{channel.name}`**", delete_after=15)
        controller = self.get_controller(ctx)
        controller.channel = ctx.channel
        self.check_listen.start(ctx)
    @commands.command(aliases=["p"])
    async def play(self, ctx, *, query: str):
        """Search for and add a song to the Queue."""
        song = query
        if not RURL.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            return await ctx.send('Could not find any songs on Youtube with that query.')
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        track = tracks[0]
        controller = self.get_controller(ctx)
        controller.now_playing_id = track.ytid
        controller.now_playing_uri = track.uri
        controller.user = ctx.author.mention
        controller.auto_play_queue._queue.clear()

        await controller.queue.put(track)
        if not controller.queue.empty() and player.is_playing:
            MusicEmbed = discord.Embed(title="Queued",colour=discord.Colour.random(),description=f"[{track.title}]({track.uri}) [{ctx.author.mention}]")
            await ctx.send(embed=MusicEmbed)

    @commands.command()
    async def pause(self, ctx):
        """Pause the player."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('I am not currently playing anything!', delete_after=15)

        await ctx.message.add_reaction("\N{Double Vertical Bar}")
        await player.set_pause(True)

    @commands.command()
    async def resume(self, ctx):
        """Resume the player from a paused state."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.paused:
            return await ctx.send('I am not currently paused!', delete_after=15)

        await ctx.message.add_reaction("\N{Black Right-Pointing Triangle}")
        await player.set_pause(False)

    @commands.command()
    async def skip(self, ctx):
        """Skip the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if not player.is_playing and not controller.auto_play_queue.empty():
            return await ctx.send('I am not currently playing anything!', delete_after=15)

        await ctx.message.add_reaction('\N{OK Hand Sign}')

        if controller.loop and controller.auto_play:
            controller.loop = False
            controller.auto_play = False
            await player.stop()
            await asyncio.sleep(1)
            controller.loop = True
            controller.auto_play = True
        elif controller.loop:
            controller.loop = False
            await player.stop()
            await asyncio.sleep(1)
            controller.loop = True
        else:
            await player.stop()

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, *, vol: int):
        """Set the player volume."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        vol = max(min(vol, 1000), 0)
        controller.volume = vol

        await ctx.send(f'Setting the player volume to `{vol}`')
        await player.set_volume(vol)

    @commands.command(aliases=['np', 'current', 'nowplaying'])
    async def now_playing(self, ctx):
        """Retrieve the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        controller = self.get_controller(ctx)
        await controller.now_playing.delete()

        controller.now_playing = await ctx.send(f'Now playing: `{player.current}`')

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        """Retrieve information on the next 5 songs from the queue."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not player.current and not controller.queue._queue:
            return await ctx.send('There are no songs currently in the queue.', delete_after=20)
        if player.current and not controller.queue._queue:
            return await ctx.send(f"Currently only playing: `{player.current}`")
        else:
            upcoming = list(itertools.islice(controller.queue._queue, 0, 5))

            fmt = '\n'.join(f'```{k}. {str(song)}```' for k,song in enumerate(upcoming,start=1))
            embed = discord.Embed(title=f'Queue', colour=discord.Colour.random())
            embed.add_field(name=f"Now playing: `{player.current}`",value=fmt)
            await ctx.send(embed=embed)

    @commands.command(aliases=['disconnect', 'dc'])
    async def stop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        controller.auto_play = False
        controller.loop = False
        await player.stop()
        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.disconnect()
            return await ctx.send('There was no controller to stop.')
        await player.disconnect()
        self.check_autoplay_queue.cancel()
        self.check_listen.cancel()
        await ctx.message.add_reaction("\N{Octagonal Sign}")

    @commands.command(aliases=['eq'])
    async def equalizer(self, ctx, equalizer: str,amount=1.0):
        """Equalizer for the player"""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        EqualizerPlayer = wavelink.eqs.Equalizer(levels=[("band",0),("gain",1.0)])
        if equalizer == "bassboost":
            await player.set_eq(EqualizerPlayer.boost())
            await ctx.send(f'Bass Boosted')
        if equalizer == "reset":
            await player.set_eq(EqualizerPlayer.flat())
            await ctx.send("Reset the equalizer")
        if equalizer == "piano":
            await player.set_eq(EqualizerPlayer.piano())
            await ctx.send("Piano equalizer")
        if equalizer == "metal":
            await player.set_eq(EqualizerPlayer.metal())
            await ctx.send("Metal equalizer")

    @commands.command()
    async def loop(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        controller.loop = next(self.Toggle)
        if controller.loop == True:
            await ctx.message.add_reaction("\N{Clockwise Rightwards and Leftwards Open Circle Arrows}")
        else:
            await ctx.send("Loop disabled!")

    @commands.command(aliases=['ap'])
    async def autoplay(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        controller.auto_play = next(self.autoplay)

        if controller.auto_play == True:
            self.check_autoplay_queue.start(ctx)
            await ctx.send("Autoplay enabled!")
        else:
            self.check_autoplay_queue.stop()
            controller.auto_play_queue._queue.clear()
            await ctx.send("Autoplay disabled!")

    @commands.command(aliases=["mix"])
    async def shuffle(self, ctx):
        controller = self.get_controller(ctx)
        if controller.queue._queue:
            random.shuffle(controller.queue._queue)
            await ctx.send("Shuffled")
        else:
            await ctx.send("Nothing in queue")

    @commands.command(aliases=['clr','clear'])
    async def _clr(self, ctx):
        controller = self.get_controller(ctx)
        controller.queue._queue.clear()
        controller.now_playing_id = None
        if not controller.auto_play_queue.empty():
            await ctx.invoke(self.skip)
            controller.auto_play_queue._queue.clear()
        await ctx.send("Cleared the queue")

    @commands.command()
    async def information(self, ctx):
        """Retrieve various Node/Server/Player information."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        node = player.node

        used = humanize.naturalsize(node.stats.memory_used)
        total = humanize.naturalsize(node.stats.memory_allocated)
        free = humanize.naturalsize(node.stats.memory_free)
        cpu = node.stats.cpu_cores

        fmt = f'**WaveLink:** `{wavelink.__version__}`\n\n' \
              f'Connected to `{len(self.bot.wavelink.nodes)}` nodes.\n' \
              f'Best available Node `{self.bot.wavelink.get_best_node().__repr__()}`\n' \
              f'`{len(self.bot.wavelink.players)}` players are distributed on nodes.\n' \
              f'`{node.stats.players}` players are distributed on server.\n' \
              f'`{node.stats.playing_players}` players are playing on server.\n\n' \
              f'Server Memory: `{used}/{total}` | `({free} free)`\n' \
              f'Server CPU: `{cpu}`\n\n' \
              f'Server Uptime: `{datetime.timedelta(milliseconds=node.stats.uptime)}`'
        await ctx.send(fmt)

def setup(bot):
    bot.add_cog(Music(bot))
