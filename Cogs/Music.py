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
import spotify
from lyricsgenius import Genius
RURL = re.compile('https?:\/\/(?:www\.)?.+')


spotify_url = re.compile('https://open.spotify.com/(?P<type>track|playlist)/(?P<id>\w+)')
genius = Genius("4w6JWVchOkAqntnmro9NurDF11ljHGATRf-9m8yv8EQ8meU9HrrzEywcaooyRYdn")
config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apiconfig.yml')
with open(config_file_path) as f:
    config = yaml.safe_load(f)
    spotify_client = spotify.HTTPClient(config['music']['Spotify']['ClientID'],config['music']['Spotify']['ClientSecret'])
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
        self.last_songs = asyncio.Queue(maxsize=11)
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
        self.spotify_playlists = None
        self.bot.loop.create_task(self.controller_loop())
        self.check_autoplay_queue.start()
        self.check_listen.start()
        self.check_last_songs.start()
        self.update_playlist.start()
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
            self.YoutubeAPIKEY = itertools.cycle([x for x in config['music']["Youtube"].values()])
    async def YoutubeSuggestion(self):
        key = next(self.YoutubeAPIKEY)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.googleapis.com/youtube/v3/search?part=id&relatedToVideoId={self.now_playing_id}&type=video&key={key}&chart=mostpopular&maxResults=4&regionCode=SG&videoCategoryId=10") as video:
                Videos = await video.json()
                try:
                    return list(set(["https://www.youtube.com/watch?v="+x['id']['videoId'] for x in Videos['items']]))
                except KeyError:
                    print(f"Being Rate limited on \u001b[43m {key} \u001b[0m")
    @tasks.loop(hours=1)
    async def update_playlist(self):
        self.spotify_playlists = await spotify_client.featured_playlists(country="SG")
        print("Updating Spotify playlists")
    @tasks.loop(seconds=2.0)
    async def check_autoplay_queue(self):
        if self.auto_play_queue.empty() and self.now_playing_id and self.auto_play:
            videolist = await self.YoutubeSuggestion()
            if not videolist:
                return
            for video in videolist:
                tracks = await self.bot.wavelink.get_tracks(video)
                if not tracks:
                    tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{video}")
                try:
                    track = tracks[0]
                    if track.length<=480000:
                        self.now_playing_id = track.ytid
                        await self.auto_play_queue.put(Track(track.id, track.info, requester=self.requester))
                except TypeError:
                    print(self.guild_id, "Could not play", video)
            else:
                print(self.guild_id, "has generated ", [x.title for x in self.auto_play_queue._queue])
    @tasks.loop(seconds=5.0)
    async def check_last_songs(self):
        if self.last_songs.full():
            print("Song history full! Removing...")
            song = await self.last_songs.get()
            del song
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
            if self.current_track:
                self.current_track = None
            self.next.clear()
            song = await self.queue.get()
            self.now_playing_uri, self.now_playing_id, self.requester, self.current_track = song.uri, song.ytid, song.requester, song
            await player.play(song)
            MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{song}]({self.now_playing_uri}) [{song.requester}]")
            MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
            self.now_playing = await self.channel.send(embed=MusicEmbed)
            await self.next.wait()
            await self.last_songs.put(song)
            if self.loop:
                while self.loop:
                    if self.loop_queue:
                        if song not in self.queue._queue:
                            await self.queue.put(song)
                            print('readding song into queue')
                        list_of_songs = list(self.queue._queue)
                        for x in list_of_songs:
                            if self.now_playing:
                                await self.now_playing.delete()
                            self.next.clear()
                            await player.play(x)
                            MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{x}]({x.ytid}) [{x.requester}]")
                            MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
                            self.now_playing = await self.channel.send(embed=MusicEmbed)
                            list_of_songs = list(self.queue._queue)
                            await self.next.wait()
                    if self.now_playing:
                        await self.now_playing.delete()
                    self.next.clear()
                    await player.play(song)
                    MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{song}]({self.now_playing_uri}) [{song.requester}]")
                    MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
                    self.now_playing = await self.channel.send(embed=MusicEmbed)
                    self.current_track = song
                    await self.next.wait()
            if self.auto_play and not self.loop and self.queue.empty() and not self.auto_play_queue.empty():
                while self.auto_play and self.queue.empty() and not self.auto_play_queue.empty():
                    await self.now_playing.delete()
                    self.next.clear()
                    song = await self.auto_play_queue.get()
                    self.now_playing_uri = song.uri
                    self.now_playing_id = song.ytid
                    MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{song}]({song.uri}) [{song.requester}]")
                    MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
                    self.now_playing = await self.channel.send(embed=MusicEmbed)
                    self.current_track = song
                    await player.play(song)
                    await self.next.wait()
                    await self.last_songs.put(song)
class Music(commands.Cog, wavelink.WavelinkMixin):

    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}
        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
            self.nodes = config['music']['nodes']
            self.spotify = config['music']['Spotify']

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)

        for n in self.nodes.values():
            await self.bot.wavelink.initiate_node(**n)

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node: wavelink.Node):
        print(f'Node {node.identifier} is ready!')
    @wavelink.WavelinkMixin.listener()
    async def on_track_end(self, node: wavelink.node.Node, event: wavelink.events.TrackEnd):
        controller = self.get_controller(event.player)
        controller.next.set()
    @wavelink.WavelinkMixin.listener()
    async def on_track_stuck(self, node: wavelink.node.Node, event: wavelink.events.TrackStuck):
        controller = self.get_controller(event.player)
        print(f"Track stuck! Skipping!")
        controller.next.set()
    @wavelink.WavelinkMixin.listener()
    async def on_track_exception(self, node: wavelink.node.Node, event: wavelink.events.TrackException):
        print(f"[{node.identifier}] An error has occured: {event.error}, Switching nodes!")
        await event.player.change_node()

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
        if ( before.channel and not after.channel)  and member.bot and member == self.bot.user:
            print("Player has been closed! Stopping!")
            if controller.auto_play:
                controller.auto_play = False
                controller.auto_play_queue._queue.clear()
            if controller.loop:
                controller.loop = False
            controller.queue._queue.clear()
            await player.stop()
            await player.disconnect()

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
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        song = query
        if not player.is_connected:
            await ctx.invoke(self.connect_)
        if spotify_url.match(query):
            if 'playlist' in query:
                id = query.strip('https://open.spotify.com/playlist/')
                if '?' in id:
                    id = id.split('?')[0]
                try:
                    list = await spotify_client.get_playlist(id)
                except spotify.NotFound:
                    ctx.send(embed=discord.Embed(description=f"Playlist could not be found"))
                except 
                song_names = [x['track']['name'] for x in list['tracks']['items']]
                artistsdata = [x['track']['artists'][0]['name'] for x in list['tracks']['items']]
                to_load = zip(song_names,artistsdata)
                for x in to_load:
                    tracks = await self.bot.wavelink.get_tracks(f'ytmsearch:{x[0]+" "+ x[1]}')
                    if tracks:
                        track = tracks[0]
                        await controller.queue.put(Track(track.id, track.info, requester=ctx.author.mention))
                else:
                    print(f"Adding {list['tracks']['total']} to queue")
                controller.auto_play_queue._queue.clear()
                MusicEmbed = discord.Embed(title=f"Added {list['tracks']['total']} songs from {list['name']}",colour=discord.Colour.random())
                MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
                return await ctx.send(embed=MusicEmbed)
            if "track" in query:
                id = query.strip('https://open.spotify.com/track/')
                if '?' in id:
                    id = id.split('?')[0]
                try:
                    track = await spotify_client.track(id)
                except spotify.NotFound:
                    return await ctx.send(embed=discord.Embed(description="Playlist not found. Try another!"),delete_after=10)
                song_name = track['name']
                song_artist = track['artists'][0]['name']
                tracks = await self.bot.wavelink.get_tracks(f'ytmsearch:{song_name } {song_artist}')
                if not tracks:
                    return await ctx.send(embed=discord.Embed(description='Could not find song'))
                track = tracks[0]
                await controller.queue.put(Track(track.id, track.info, requester=ctx.author.mention))
                controller.auto_play_queue._queue.clear()
                if not controller.queue.empty() and player.is_playing:
                    MusicEmbed = discord.Embed(title="Queued",colour=discord.Colour.random(),description=f"[{track.title}]({track.uri}) [{ctx.author.mention}]")
                    MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
                    return await ctx.send(embed=MusicEmbed)
                else:
                    return
        if not RURL.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            for x in range(3):
                if tracks:
                    break
                else:
                    print("Retrying...")
                    tracks = await self.bot.wavelink.get_tracks(f'{query}')
                    await asyncio.sleep(1)
        if not tracks:
            embed = discord.Embed(description='failed to find any songs on youtube or soundcloud')
            return await ctx.send(embed=embed,delete_after=5)


        if "list=" in query and RURL.match(query):
            playlist = tracks.tracks
            track = playlist[0]
            controller.auto_play_queue._queue.clear()
            for track in playlist:
                await controller.queue.put(Track(track.id, track.info, requester=ctx.author.mention))
            MusicEmbed = discord.Embed(title=f"Added {len(playlist)} songs from {tracks.data['playlistInfo']['name']}",colour=discord.Colour.random(),description=f"[{track.title}]({track.uri}) [{ctx.author.mention}]")
            MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
            await ctx.send(embed=MusicEmbed)

        else:
            track = tracks[0]
            controller.auto_play_queue._queue.clear()
            await controller.queue.put(Track(track.id, track.info, requester=ctx.author.mention))
            if not controller.queue.empty() and player.is_playing:
                MusicEmbed = discord.Embed(title="Queued",colour=discord.Colour.random(),description=f"[{track.title}]({track.uri}) [{ctx.author.mention}]")
                MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
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
    async def skip(self, ctx, times: int = 1):
        """Skip the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if not player.is_playing and controller.auto_play_queue.empty() and controller.queue.empty():
            return await ctx.send('I am not currently playing anything!', delete_after=15)
        if times<1:
            times = 1
        await ctx.message.add_reaction('\N{OK Hand Sign}')

        if controller.loop and controller.auto_play:
            controller.loop = False
            controller.auto_play = False
            for x in range(times):
                await player.stop()
                await asyncio.sleep(1)
            controller.loop = True
            controller.auto_play = True
        elif controller.loop:
            if controller.loop_queue:
                for x in range(times):
                    await player.stop()
                    await asyncio.sleep(1)
            else:
                controller.loop = False
                for x in range(times):
                    await player.stop()
                    await asyncio.sleep(1)
                controller.loop = True
        else:
            for x in range(times):
                await player.stop()
                await asyncio.sleep(1)
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
            if controller.queue.qsize()%5 == 0:
                pages = int(controller.queue.qsize()/5)
            else:
                pages = (controller.queue.qsize()//5)+1
            pagenumber = itertools.count(1)
            embeds = []
            for x in range(pages+1):
                upcoming = list(itertools.islice(controller.queue._queue, x*5,x*5+5))
                fmt = '\n'.join(f'```{k}. {str(song)}```' for k,song in enumerate(upcoming,start=x*5+1))
                page = discord.Embed(title=f'Queue', colour=discord.Colour.random())
                page.add_field(name=f"Now playing: `{player.current}`",value=fmt)
                page.set_footer(text=f"Page {next(pagenumber)}/{pages}")
                embeds.append(page)
            try:
                await ctx.send(embed=embeds[pageno-1])
            except IndexError:
                await ctx.send(embed=discord.Embed(description="Could not get page!"))
    @commands.command(aliases=['aq'])
    async def autoqueue(self, ctx, pageno=1):
        """Retrieve information on the next 5 songs from the queue."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not controller.auto_play:
            return await ctx.send('Autoplay is not enabled', delete_after=20)
        elif not player.is_connected:
            return
        elif controller.auto_play_queue.empty():
            return await ctx.send(embed=discord.Embed(description="Autoplay queue empty!"))
        else:
            if controller.auto_play_queue.qsize()%5 == 0:
                pages = int(controller.queue.qsize()/5)
            else:
                pages = (controller.auto_play_queue.qsize()//5)+1
            pagenumber = itertools.count(1)
            embeds = []
            for x in range(pages+1):
                upcoming = list(itertools.islice(controller.auto_play_queue._queue, x*5,x*5+5))
                print(upcoming)
                fmt = '\n'.join(f'```{k}. {str(song)}```' for k,song in enumerate(upcoming,start=x*5+1))
                page = discord.Embed(title=f'Autoplay Queue', colour=discord.Colour.random())
                page.add_field(name=f"Now playing: `{player.current}`",value=fmt)
                page.set_footer(text=f"Page {next(pagenumber)}/{pages}")
                embeds.append(page)
            try:
                await ctx.send(embed=embeds[pageno-1])
            except IndexError:
                await ctx.send(embed=discord.Embed(description="Could not get page!"))
    @commands.command(aliases=['lq'])
    async def lastqueue(self, ctx, pageno=1):
        """Retrieve information on the next 5 songs from the queue."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if controller.last_songs.empty():
            return await ctx.send(embed=discord.Embed(description='Song history empty'))
        else:
            if not controller.last_songs._queue:
                return
            if controller.last_songs.qsize()%5 == 0:
                pages = int(controller.last_songs.qsize()/5)
            else:
                pages = (controller.last_songs.qsize()//5)+1
            pagenumber = itertools.count(1)
            embeds = []
            for x in range(pages+1):
                upcoming = reversed(list(itertools.islice(controller.last_songs._queue, x*5,x*5+5)))
                fmt = '\n'.join(f'{k}. [{str(song)}]({song.uri})' for k,song in enumerate(upcoming,start=x*5+1))
                page = discord.Embed(title=f'Song history', description=fmt, colour=discord.Colour.random())
                page.set_footer(text=f"Page {next(pagenumber)}/{pages}")
                embeds.append(page)
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
            return await ctx.send(embed=discord.Embed(description="something broke oopsies"))
        if lyric:
            if len(lyric.lyrics)>2000:
                embed = discord.Embed(title=lyric.title,description=lyric.lyrics[:2000])
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
            await ctx.send(embed=discord.Embed(description="Could not remove"))
    @commands.command()
    async def playlist(self, ctx, mode: str =None, *, query:str =None):
        controller = self.get_controller(ctx)
        await asyncio.sleep(1)
        spotify_playlist_names = [x['name'] for x in controller.spotify_playlists['playlists']['items']]
        spotify_playlist_descriptions = [x['description'] for x in controller.spotify_playlists['playlists']['items']]
        spotify_playlist_urls = [x['external_urls']['spotify'] for x in controller.spotify_playlists['playlists']['items']]
        Spotify_List = zip(spotify_playlist_names,spotify_playlist_descriptions,spotify_playlist_urls)
        if mode == None:
            await ctx.send(embed=discord.Embed(description='Please select mode:\n```list```\n```play```\n```create```'))
        elif query == None and mode.lower() != 'list':
            await ctx.send(embed=discord.Embed(description='Query not selected'))
        if mode.lower() == "list":
            Embed = discord.Embed(title="Playlists")
            [Embed.add_field(name=x[0],value=x[1]) for x in Spotify_List]
            await ctx.send(embed=Embed)
        elif mode.lower() == 'play':
            play = self.bot.get_command("play")
            search = [x for x in Spotify_List if query in x[0]]
            if not search:
                search_results = await spotify_client.search(query,"playlist")
                url = search_results['playlists']['items'][0]['external_urls']['spotify']
                return await play(ctx,query=url)
                # return await ctx.send(embed=discord.Embed(description='Query not found'))

            return await play(ctx,query=search[0][2])
        else:
            await ctx.send(embed=discord.Embed(description='Hasnt been implemented :()'))
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
                        await asyncio.sleep(1)
                    else:
                        controller.loop = False
                        await player.stop()
                        await asyncio.sleep(1)
                        controller.loop = True
                else:
                    await player.stop()
                    await asyncio.sleep(1)
    @commands.command()
    async def information(self, ctx):
        """Retrieve various Node/Server/Player information."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        node = player.node

        used = humanize.naturalsize(node.stats.memory_used)
        total = humanize.naturalsize(node.stats.memory_allocated)
        free = humanize.naturalsize(node.stats.memory_free)
        cpu = node.stats.cpu_cores

        fmt = f'**Doorbanger:** `v2.6.1`\n\n' \
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
