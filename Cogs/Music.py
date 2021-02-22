import asyncio
import datetime
import discord
import humanize
import re
import sys
import traceback
import wavelink
from discord.ext import commands, tasks
from typing import Union
import itertools
import collections
import random
import os
import aiohttp
import yaml
import spotipy
from lyricsgenius import Genius
RURL = re.compile('https?:\/\/(?:www\.)?.+')
genius = Genius("4w6JWVchOkAqntnmro9NurDF11ljHGATRf-9m8yv8EQ8meU9HrrzEywcaooyRYdn")
class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    __slots__ = ('requester')

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get('requester')

class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None
        self.last_songs = asyncio.LifoQueue(maxsize=11)
        self.now_playing_uri = None
        self.now_playing_id = None
        self.next = asyncio.Event()
        self.queue = asyncio.Queue()
        self.auto_play_queue = asyncio.Queue()
        self.auto_play = False
        self.volume = 50
        self.requester = None
        self.now_playing = None
        self.current_track =  None
        self.loop = False
        self.loop_queue = False
        self.bot.loop.create_task(self.controller_loop())
        self.check_autoplay_queue.start()
        self.check_listen.start()
        self.check_last_songs.start()
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apiconfig.yml')
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
            self.YoutubeAPIKEY = itertools.cycle([x for x in config['music'].values()])

    async def YoutubeSuggestion(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&relatedToVideoId={self.now_playing_id}&type=video&key={next(self.YoutubeAPIKEY)}") as video:
                Videos = await video.json()
                return list(set(["https://www.youtube.com/watch?v="+x['id']['videoId'] for x in Videos['items']]))

    @tasks.loop(seconds=1.0)
    async def check_autoplay_queue(self):
        if self.auto_play_queue.empty() and self.now_playing_id and self.auto_play:
            videolist = await self.YoutubeSuggestion()

            for video in videolist:
                tracks = await self.bot.wavelink.get_tracks(video)
                print(self.guild_id, self.auto_play_queue._queue)
                try:
                    track = tracks[0]
                    self.now_playing_id = track.ytid
                    await self.auto_play_queue.put(Track(track.id, track.info, requester=self.requester))
                except TypeError:
                    print(self.guild_id, video)
    @tasks.loop(seconds=5.0)
    async def check_last_songs(self):
        if self.last_songs.full():
            print("Song history full! Removing...")
            self.last_songs._queue.pop()
    @tasks.loop(seconds=1.0)
    async def check_listen(self):
        player = self.bot.wavelink.get_player(self.guild_id)
        channel = self.bot.get_channel(player.channel_id)
        global member_list
        try:
            member_list = [x.name for x in channel.members if x.bot == False]
        except AttributeError:
            member_list = None
        if not member_list and player.is_connected:
            embed = discord.Embed(title="Everyone left me alone..Disconecting!")
            embed.set_footer(text="I'll see you on the next doorbanging adventure!")
            if self.channel:
                await self.channel.send(embed=embed,delete_after=60)
            self.queue._queue.clear()
            await player.stop()
            await player.disconnect()
            if self.auto_play:
                self.auto_play = False
                self.auto_play_queue._queue.clear()
            if self.loop:
                self.loop = False

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)
        while True:
            if self.now_playing:
                await self.now_playing.delete()
            self.next.clear()
            song = await self.queue.get()
            self.now_playing_uri, self.now_playing_id, self.requester, self.current_track = song.uri, song.ytid, song.requester, song
            await player.play(song)
            MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{song}]({self.now_playing_uri}) [{song.requester}]")
            self.now_playing = await self.channel.send(embed=MusicEmbed)
            await self.next.wait()
            await self.last_songs.put(song)
            if self.loop:
                while self.loop:
                    if self.now_playing:
                        await self.now_playing.delete()
                    if self.loop_queue:
                        await self.now_playing.delete()
                        list_of_songs = list(self.queue._queue)
                        for x in list_of_songs:
                            await self.now_playing.delete()
                            self.next.clear()
                            await player.play(x)
                            MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{x}]({x.ytid}) [{x.requester}]")
                            self.now_playing = await self.channel.send(embed=MusicEmbed)
                            list_of_songs = list(self.queue._queue)
                            await self.next.wait()
                    self.next.clear()
                    await player.play(song)
                    MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{song}]({self.now_playing_uri}) [{song.requester}]")
                    self.now_playing = await self.channel.send(embed=MusicEmbed)
                    await self.next.wait()
            if self.auto_play and not self.loop and self.queue.empty() and not self.auto_play_queue.empty():
                while self.auto_play and self.queue.empty():
                    await self.now_playing.delete()
                    self.next.clear()
                    song = await self.auto_play_queue.get()
                    self.now_playing_uri = song.uri
                    self.now_playing_id = song.ytid
                    MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{song}]({song.uri}) [{song.requester}]")
                    self.now_playing = await self.channel.send(embed=MusicEmbed)
                    await player.play(song)
                    await self.next.wait()
                    await self.last_songs.put(song)
class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}
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
                                                     identifier='Koalaa-server-4',
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

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        player = self.bot.wavelink.get_player(member.guild.id)
        controller = self.get_controller(player)
        if ( before.channel and after.channel) and not (before.channel.id == after.channel.id) and member.bot and member == self.bot.user:
            print("reconnecting..")
            if controller.auto_play:
                controller.auto_play = False
                controller.auto_play_queue._queue.clear()
            if controller.loop:
                controller.loop = False
            controller.queue._queue.clear()
            await player.stop()
            await player.disconnect()
            await player.connect(after.channel.id)

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
        embed1 = discord.Embed(description=f'Connecting to **`{channel.name}...`**')
        msg = await ctx.send(embed=embed1, delete_after=15)
        await player.connect(channel.id)
        await msg.delete()
        embed2 = discord.Embed(description=f"Connected to **`{channel.name}`**")
        await ctx.send(embed=embed2, delete_after=15)
        controller = self.get_controller(ctx)
        controller.channel = ctx.channel


    @commands.command(aliases=["p"])
    async def play(self, ctx, *, query: str):
        """Search for and add a song to the Queue."""
        song = query
        if not RURL.match(query):
            query = f'ytmsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(f'{query}')
        if not tracks:
            print("falling back to youtube")
            query = f'ytsearch:{query}'
        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            print("falling back to soundcloud")
            query = f'scsearch:{query}'
        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            embed = discord.Embed(description='failed to find any songs on youtube or soundcloud')
            return await ctx.send(embed=embed,delete_after=5)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)
        if "list=" in query and RURL.match(query):
            playlist = tracks.tracks
            track = playlist[0]
            controller = self.get_controller(ctx)
            controller.auto_play_queue._queue.clear()
            for track in playlist:
                await controller.queue.put(Track(track.id, track.info, requester=ctx.author.mention))
            MusicEmbed = discord.Embed(title=f"Added {len(playlist)} songs from {tracks.data['playlistInfo']['name']}",colour=discord.Colour.random(),description=f"[{track.title}]({track.uri}) [{ctx.author.mention}]")
            await ctx.send(embed=MusicEmbed)

        else:
            track = tracks[0]
            controller = self.get_controller(ctx)
            controller.auto_play_queue._queue.clear()
            await controller.queue.put(Track(track.id, track.info, requester=ctx.author.mention))
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

    @commands.command(aliases=["s"])
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
            if controller.loop_queue:
                await player.stop()
            else:
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
        pbar = ""


        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        controller = self.get_controller(ctx)
        track = controller.current_track
        tlpbar = round(track.length // 15)
        pppbar = round(player.position // tlpbar)

        for i in range(15):
            if i == pppbar:
               pbar += ":radio_button:"
            else:
               pbar += "▬"
        embed = discord.Embed(title=f'Now playing: `{player.current}`', description=f"{pbar}[{datetime.timedelta(milliseconds=player.position)}/{datetime.timedelta(milliseconds=track.length)}]")
        controller.now_playing = await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, pageno=1):
        """Retrieve information on the next 5 songs from the queue."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not player.current and not controller.queue._queue:
            return await ctx.send('There are no songs currently in the queue.', delete_after=20)
        elif player.current and not controller.queue._queue:
            return await ctx.send(f"Currently only playing: `{player.current}`")
        elif not player.is_connected:
            return
        else:
            pages = (len(controller.queue._queue)//5)+1
            pagenumber = itertools.count(1)
            embeds = []
            for x in range(pages+1):
                upcoming = list(itertools.islice(controller.queue._queue, x*5,x*5+5))
                print(upcoming)
                fmt = '\n'.join(f'```{k}. {str(song)}```' for k,song in enumerate(upcoming,start=x*5+1))
                print(fmt)
                page = discord.Embed(title=f'Queue', colour=discord.Colour.random())
                page.add_field(name=f"Now playing: `{player.current}`",value=fmt)
                page.set_footer(text=f"Page {next(pagenumber)}/{pages}")
                embeds.append(page)
            print(embeds)
            try:
                await ctx.send(embed=embeds[pageno-1])
            except IndexError:
                await ctx.send(embed=discord.Embed(description="Could not get page!"))
    @commands.command(aliases=['disconnect', 'dc'])
    async def stop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.auto_play:
            controller.auto_play = False
        if controller.loop:
            controller.loop = False
        await player.stop()
        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.disconnect()
            return await ctx.send('There was no controller to stop.')
        await player.disconnect()

        await ctx.message.add_reaction("\N{Octagonal Sign}")

    @commands.command(aliases=['eq'])
    async def equalizer(self, ctx, equalizer: str,amount=1.0):
        """Equalizer for the player"""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            return

        eqs = {'flat': wavelink.Equalizer.flat(),
               'boost': wavelink.Equalizer.boost(),
               'metal': wavelink.Equalizer.metal(),
               'piano': wavelink.Equalizer.piano()}

        eq = eqs.get(equalizer.lower(), None)

        if not eq:
            joined = "\n".join(eqs.keys())
            return await ctx.send(f'Invalid EQ provided. Valid EQs:\n\n{joined}')

        await ctx.send(f'Successfully changed equalizer to {equalizer}', delete_after=15)
        await player.set_eq(eq)

    @commands.command()
    async def loop(self, ctx, mode="track"):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.loop == True:
            controller.loop = False
            await ctx.send("Loop disabled!")
        else:
            if "q" in mode.lower():
                if controller.loop_queue == False:
                    controller.loop = True
                    controller.loop_queue = True
                    await ctx.message.add_reaction("\N{Clockwise Rightwards and Leftwards Open Circle Arrows}")
                else:
                    controller.loop = False
                    controller.loop_queue = False
                    await ctx.send("loop track disabled!")
            else:
                controller.loop = True
                await ctx.message.add_reaction("\N{Clockwise Rightwards and Leftwards Open Circle Arrows}")
    @commands.command(aliases=['ap'])
    async def autoplay(self, ctx):
        controller = self.get_controller(ctx)
        if controller.auto_play == True:
            controller.auto_play = False
            controller.auto_play_queue._queue.clear()
            await ctx.send(embed=discord.Embed(description="Autoplay disabled"))
        else:
            controller.auto_play = True
            await ctx.send(embed=discord.Embed(description="Autoplay enabled"))

    @commands.command(aliases=["mix"])
    async def shuffle(self, ctx):
        controller = self.get_controller(ctx)
        if controller.queue._queue:
            random.shuffle(controller.queue._queue)
            await ctx.send(embed=discord.Embed(description="Shuffled"))
        else:
            await ctx.send(embed=discord.Embed(description="Nothing to shuffle!"))

    @commands.command(aliases=['clr','clear'])
    async def _clr(self, ctx):
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller.queue._queue.clear()
        if not controller.auto_play_queue.empty():
            controller.auto_play = False
            controller.auto_play_queue._queue.clear()
            await player.stop()


        await ctx.send(embed=discord.Embed(description="Cleared the queue"))
    @commands.command()
    async def lyrics(self,ctx):
        controller = self.get_controller(ctx)
        try:
            lyric = genius.search_song(controller.current_track.title,controller.current_track.author)
        except:
            await ctx.send(description="something broke oopsies")
        if lyric:
            if len(lyric.lyrics)>2000:
                embed = discord.Embed(title=controller.current_track.title,description=lyric.lyrics[:2000])
                embed2 = discord.Embed(description=lyric.lyrics[2000:])
                await ctx.send(embed=embed)
                await ctx.send(embed=embed2)
            else:
                embed = discord.Embed(title=controller.current_track.title,description=lyric.lyrics)
                await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(description="No lyrics found!"))
    @commands.command()
    async def remove(self, ctx,num: int = 1):
        controller = self.get_controller(ctx)
        try:
            del controller.queue._queue[num-1]
        except IndexError:
            await ctx.send(discord.Embed(description="Could not remove"))
    @commands.command(aliases=['back'])
    async def last(self, ctx, num = 0):
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if controller.last_songs.qsize()<1:
            return
        if controller.last_songs.qsize() >= num:
            controller.queue._queue.appendleft(controller.current_track)
            for x in range(num+1):
                last_song = await controller.last_songs.get()
                print(last_song)
                controller.queue._queue.appendleft(last_song)
                if controller.loop and controller.auto_play:
                    controller.loop = False
                    controller.auto_play = False
                    await player.stop()
                    await asyncio.sleep(1)
                    controller.loop = True
                    controller.auto_play = True
                elif controller.loop:
                    if controller.loop_queue:
                        await player.stop()
                    else:
                        controller.loop = False
                        await player.stop()
                        await asyncio.sleep(1)
                        controller.loop = True
                else:
                    await player.stop()
    @commands.command()
    async def information(self, ctx):
        """Retrieve various Node/Server/Player information."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        node = player.node

        used = humanize.naturalsize(node.stats.memory_used)
        total = humanize.naturalsize(node.stats.memory_allocated)
        free = humanize.naturalsize(node.stats.memory_free)
        cpu = node.stats.cpu_cores

        fmt = f'**Doorbanger:** `v2.3.1`\n\n' \
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
