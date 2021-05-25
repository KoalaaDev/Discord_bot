import asyncio
import datetime
import discord
import humanize
import re
import sys
import traceback
import wavelink
from discord.ext import commands, tasks, menus
from typing import Union
import typing
import itertools
import collections
import random
import os
import aiohttp
import yaml
import spotify
import pycountry
import humanreadable as hr
import async_timeout
from lyricsgenius import Genius
from subprocess import Popen, PIPE
import copy
from Cogs.Utils import is_whitelisted
def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1
idgenerator = uniqueid()
RURL = re.compile("https?:\/\/(?:www\.)?.+")
spotify_countries = ['AD','AE','AG','AL','AM','AR','AT','AU','AZ','BA','BB','BD','BE','BF',
 'BG','BH','BI','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CH','CL','CM','CO',
 'CR','CV','CY','CZ','DE','DK','DM','DO','DZ','EC','EE','EG','ES','FI','FJ','FM',
 'FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT',
 'HU','ID','IE','IL','IN','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR',
 'KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','MA','MC','MD','ME',
 'MH','MK','ML','MN','MO','MR','MT','MV','MW','MX','MY','NA','NE','NG','NI','NL',
 'NO','NP','NR','NZ','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA',
 'RO','RS','RU','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST',
 'SV','SZ','TD','TG','TH','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US',
 'UY','UZ','VC','VN','VU','WS','XK','ZA','ZW']

spotify_url = re.compile(
    "https://open.spotify.com/(?P<type>track|playlist)/(?P<id>\w+)"
)
genius = Genius("4w6JWVchOkAqntnmro9NurDF11ljHGATRf-9m8yv8EQ8meU9HrrzEywcaooyRYdn")
config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "apiconfig.yml")

with open(config_file_path) as f:
    config = yaml.safe_load(f)
    spotify_client = spotify.HTTPClient(
        config["music"]["Spotify"]["ClientID"],
        config["music"]["Spotify"]["ClientSecret"],
    )


class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    __slots__ = "requester"

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get("requester")
class Paginator(menus.ListPageSource):

    def __init__(
            self, ctx, data, name, title, per_page, color=0x3498DB, footer="{total}",
            clear_reaction_after=False, delete_message_after=False
    ):
        """
        A function to paginate a list and returning embed.
        :param ctx: Context to do something. [commands.Context]
        :param data: Data to iterate and turn it to paginator [list]
        :param name: Name of the object on the data [str]
        :param title: Title of the embed [str]
        :param per_page: How many data to display every page on embed [int]
        :param color: Color of the embed [int / discord.Colour]
        :param footer: Footer of the embed [str] | default to '{total}' "{total} (1-x of x {name}) "
        :param clear_reaction_after: Clear the reaction after the paginator stopped [bool] | default to False
        :param delete_message_after: Delete the messages after the paginator stopped [bool] | default to False
        """
        self.title: str = title
        self.name: str = name
        self.ctx: Context = ctx
        self.data: list or tuple = data
        self.page: int = per_page
        self.color: Union[discord.Color, int] = color
        self.footer: str = footer
        self.clear_reaction: bool = clear_reaction_after
        self.delete_message: bool = delete_message_after

        super().__init__(data, per_page=self.page)

    # noinspection PyUnusedLocal
    async def write(self, menu, offset, fields=None):
        total_data = len(self.entries)
        total = f"{offset:,} - {min(total_data, offset + self.per_page -1):,} of {total_data:,} {self.name}"

        e = discord.Embed(color=self.color)
        e.set_footer(text=self.footer.format(total=total))

        for name, value in fields:
            e.add_field(name=name, value=value, inline=False)

        return e

    # noinspection PyUnresolvedReferences
    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1

        fields = []
        table = ("\n".join(f"**{num}**. {entry}" for num, entry, in enumerate(entries,start=1)))

        fields.append((self.title, table))
        return await self.write(menu, offset, fields)

    async def start(self):
        page = Paginator(self.ctx, self.data, self.name, self.title, int(self.per_page), self.color, self.footer)
        menu = MenuPages(
            source=page, clear_reactions_after=self.clear_reaction, delete_message_after=self.delete_message
        )
        await menu.start(self.ctx)

class InteractiveEmbed(menus.Menu):
    """The Players interactive controller menu class."""

    def __init__(self, *, embed: discord.Embed, player: wavelink.Player):
        super().__init__(timeout=None)

        self.embed = embed
        self.player = player
        self.loop_settings = itertools.cycle(["q",""])
    def update_context(self, payload: discord.RawReactionActionEvent):
        """Update our context with the user who reacted."""
        ctx = copy.copy(self.ctx)
        ctx.author = payload.member

        return ctx
    async def update(self, payload):
        if self._can_remove_reactions:
            if payload.event_type == 'REACTION_ADD':
                message = self.bot.get_channel(payload.channel_id).get_partial_message(payload.message_id)
                await message.remove_reaction(payload.emoji, payload.member)
            elif payload.event_type == 'REACTION_REMOVE':
                return
        await super().update(payload)
    def reaction_check(self, payload: discord.RawReactionActionEvent):
        if payload.event_type == 'REACTION_REMOVE':
            return False

        if not payload.member:
            return False
        if payload.member.bot:
            return False
        if payload.message_id != self.message.id:
            return False
        if payload.member not in self.bot.get_channel(int(self.player.channel_id)).members:
            return False

        return payload.emoji in self.buttons

    async def send_initial_message(self, ctx: commands.Context, channel: discord.TextChannel) -> discord.Message:
        return await channel.send(embed=self.embed)

    @menus.button(emoji='\u25B6')
    async def resume_command(self, payload: discord.RawReactionActionEvent):
        """Resume button."""
        ctx = self.update_context(payload)

        command = self.bot.get_command('resume')
        ctx.command = command

        await self.bot.invoke(ctx)

    @menus.button(emoji='\u23F8')
    async def pause_command(self, payload: discord.RawReactionActionEvent):
        """Pause button"""
        ctx = self.update_context(payload)

        command = self.bot.get_command('pause')
        ctx.command = command

        await self.bot.invoke(ctx)
    @menus.button(emoji='\u23F8')
    async def pause_command(self, payload: discord.RawReactionActionEvent):
        """Pause button"""
        ctx = self.update_context(payload)

        command = self.bot.get_command('pause')
        ctx.command = command

        await self.bot.invoke(ctx)
    @menus.button(emoji='🛑')
    async def stop_command(self, payload: discord.RawReactionActionEvent):
        """Stop button."""
        ctx = self.update_context(payload)

        command = self.bot.get_command('stop')
        ctx.command = command

        await self.bot.invoke(ctx)
        await self.message.delete()
    @menus.button(emoji='\u23ED')
    async def skip_command(self, payload: discord.RawReactionActionEvent):
        """Skip button."""
        ctx = self.update_context(payload)

        command = self.bot.get_command('skip')
        ctx.command = command

        await self.bot.invoke(ctx)
    @menus.button(emoji='\U0001F500')
    async def shuffle_command(self, payload: discord.RawReactionActionEvent):
        """Shuffle button."""
        ctx = self.update_context(payload)

        command = self.bot.get_command('shuffle')
        ctx.command = command

        await self.bot.invoke(ctx)

    @menus.button(emoji='\u2795')
    async def volup_command(self, payload: discord.RawReactionActionEvent):
        """Volume up button"""
        ctx = self.update_context(payload)

        command = self.bot.get_command('vol_up')
        ctx.command = command

        await self.bot.invoke(ctx)

    @menus.button(emoji='\u2796')
    async def voldown_command(self, payload: discord.RawReactionActionEvent):
        """Volume down button."""
        ctx = self.update_context(payload)

        command = self.bot.get_command('vol_down')
        ctx.command = command

        await self.bot.invoke(ctx)

    @menus.button(emoji='\U0001F1F6')
    async def queue_command(self, payload: discord.RawReactionActionEvent):
        """Player queue button."""
        ctx = self.update_context(payload)

        command = self.bot.get_command('queue')
        ctx.command = command

        await self.bot.invoke(ctx)
    @menus.button(emoji='🅰️')
    async def autoplay_command(self, payload: discord.RawReactionActionEvent):
        """Player queue button."""
        ctx = self.update_context(payload)

        command = self.bot.get_command('autoplay')
        ctx.command = command

        await self.bot.invoke(ctx)

class MusicController:
    def __init__(self, bot, guild_id,context: commands.Context):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None
        self.context  = context
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
        self.current_track = None
        self.loop = False
        self.loop_queue = False
        self.spotify_playlists = None
        self.spotify_region = "SG"
        self.remote_control = False
        self.bot.loop.create_task(self.controller_loop())
        self.check_autoplay_queue.start()
        self.check_last_songs.start()
        self.update_playlist.start()
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
            self.YoutubeAPIKEY = itertools.cycle([x for x in config["music"]["Youtube"].values()])
    def build_embed(self) -> typing.Optional[discord.Embed]:
        """Method which builds our players controller embed."""
        player = self.bot.wavelink.get_player(self.guild_id)
        track = player.current
        if not track:
            track = self.current_track
        channel = player.bot.get_channel(int(player.channel_id))
        qsize = self.queue.qsize()
        aqsize = self.auto_play_queue.qsize()
        embed = discord.Embed(title=f'Interactive {player.bot.user.name} | {channel.name}', colour=0xebb145)
        embed.description = f'Now Playing:\n[{track.title}]({track.uri})\n\n'
        embed.set_thumbnail(url=track.thumb)

        embed.add_field(name='Duration', value=str(datetime.timedelta(milliseconds=int(track.length))))
        if self.queue.empty() and self.auto_play:
            embed.add_field(name='Auto Queue Length', value=str(aqsize))
        else:
            embed.add_field(name='Queue Length', value=str(qsize))
        embed.add_field(name='Volume', value=f'**`{player.volume}%`**')
        embed.add_field(name='Requested By', value=track.requester)
        if self.auto_play:
            embed.add_field(name='Autoplay', value=f'**`{self.auto_play}`**')
        embed.set_footer(text=f"{player.node.region}")
        return embed
    async def YoutubeSuggestion(self):
        key = next(self.YoutubeAPIKEY)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://www.googleapis.com/youtube/v3/search?part=id&relatedToVideoId={self.now_playing_id}&type=video&key={key}&chart=mostpopular&maxResults=10&regionCode=SG&videoCategoryId=10&topicId=/m/04rlf&videoCaption=closedCaption&relevanceLanguage=en&videoLicense=youtube&videoDefinition=high"
            ) as video:
                Videos = await video.json()
                try:
                    return list(set(["https://www.youtube.com/watch?v=" + x["id"]["videoId"] for x in Videos["items"]]))
                except KeyError:
                    print(f"Being Rate limited on \u001b[43m {key} \u001b[0m")

    @tasks.loop(hours=1)
    async def update_playlist(self):
        spotify_playlists = await spotify_client.featured_playlists(country=self.spotify_region)
        spotify_playlist_names = [x["name"] for x in spotify_playlists["playlists"]["items"]]
        spotify_playlist_descriptions = [x["description"] for x in spotify_playlists["playlists"]["items"]]
        spotify_playlist_urls = [x["external_urls"]["spotify"] for x in spotify_playlists["playlists"]["items"]]
        self.spotify_playlists = zip(spotify_playlist_names, spotify_playlist_descriptions, spotify_playlist_urls)
        print(f"[{self.guild_id}] Updating Spotify playlists for {self.spotify_region}")

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
                    if self.current_track:
                        if (
                            track.length <= 480000
                            and not track.title.startswith(self.current_track.title)
                            and track.title not in [x.title for x in self.last_songs._queue]
                        ):
                            self.now_playing_id = track.ytid
                            await self.auto_play_queue.put(
                                Track(track.id, track.info, requester=self.requester)
                            )
                except TypeError:
                    print(self.guild_id, "Could not play", video)
            else:
                print(
                    self.guild_id,
                    "has generated ",
                    [x.title for x in self.auto_play_queue._queue],
                )

    @tasks.loop(seconds=5.0)
    async def check_last_songs(self):
        if self.last_songs.full():
            print("Song history full! Removing...")
            song = await self.last_songs.get()
            del song

    async def is_position_fresh(self) -> bool:
            """Method which checks whether the player controller should be remade or updated."""
            try:
                async for message in self.context.channel.history(limit=5):
                    if message.id == self.now_playing.id:
                        return True
            except (discord.HTTPException, AttributeError):
                return False

            return False


    async def controller_loop(self):
        await self.bot.wait_until_ready()
        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)
        while True:
            if self.now_playing and not await self.is_position_fresh():
                try:
                    await self.now_playing.delete()
                    self.now_playing = None
                except AttributeError:
                    pass
            if self.current_track:
                self.current_track = None
            self.next.clear()
            song = await self.queue.get()

            (
                self.now_playing_uri,
                self.now_playing_id,
                self.requester,
                self.current_track,
            ) = (song.uri, song.ytid, song.requester, song)
            await player.play(song)
            MusicEmbed = discord.Embed(
                title="Now playing",
                colour=discord.Colour.random(),
                description=f"[{song}]({self.now_playing_uri}) [{song.requester}]",
            )
            MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
            if not self.now_playing:
                EmbeddedMessage = InteractiveEmbed(embed=self.build_embed(), player=player)
                await EmbeddedMessage.start(self.context)
                self.now_playing = EmbeddedMessage.message
            else:
                await self.now_playing.edit(embed=self.build_embed())
            await self.next.wait()
            await self.last_songs.put(song)
            if self.loop:
                while self.loop:
                    if self.loop_queue:
                        if song not in self.queue._queue:
                            await self.queue.put(song)
                        list_of_songs = list(self.queue._queue)
                        for x in list_of_songs:
                            if self.now_playing and not await self.is_position_fresh():
                                print("Clearing interactive")
                                await self.now_playing.delete()
                                self.now_playing = None
                            self.next.clear()
                            await player.play(x)
                            MusicEmbed = discord.Embed(title="Now playing",colour=discord.Colour.random(),description=f"[{x}]({x.ytid}) [{x.requester}]",)
                            MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
                            if not self.now_playing:
                                EmbeddedMessage = InteractiveEmbed(embed=self.build_embed(), player=player)
                                await EmbeddedMessage.start(self.context)
                                self.now_playing = EmbeddedMessage.message
                            else:
                                await self.now_playing.edit(embed=self.build_embed())
                            list_of_songs = list(self.queue._queue)
                            await self.next.wait()
                    else:
                        if self.now_playing and not await self.is_position_fresh():
                            await self.now_playing.delete()
                            self.now_playing = None
                        self.next.clear()
                        await player.play(song)
                        MusicEmbed = discord.Embed(
                            title="Now playing",
                            colour=discord.Colour.random(),
                            description=f"[{song}]({self.now_playing_uri}) [{song.requester}]",
                        )
                        MusicEmbed.set_footer(
                            text=f"{self.bot.user.name} | {player.node.region}"
                        )
                        if not self.now_playing:
                            EmbeddedMessage = InteractiveEmbed(embed=self.build_embed(), player=player)
                            await EmbeddedMessage.start(self.context)
                            self.now_playing = EmbeddedMessage.message
                        else:
                            await self.now_playing.edit(embed=self.build_embed())
                        self.current_track = song
                        await self.next.wait()
            if (self.auto_play and not self.loop and self.queue.empty() and not self.auto_play_queue.empty()):
                while (self.auto_play and self.queue.empty() and not self.auto_play_queue.empty()):
                    if self.now_playing and not await self.is_position_fresh():
                        print("Clearing interactive")
                        await self.now_playing.delete()
                        self.now_playing = None
                    self.next.clear()
                    song = await self.auto_play_queue.get()
                    (
                        self.now_playing_uri,
                        self.now_playing_id,
                        self.requester,
                        self.current_track,
                    ) = (song.uri, song.ytid, song.requester, song)
                    MusicEmbed = discord.Embed(
                        title="Now playing",
                        colour=discord.Colour.random(),
                        description=f"[{song}]({song.uri}) [{song.requester}]",
                    )
                    MusicEmbed.set_footer(
                        text=f"{self.bot.user.name} | {player.node.region}"
                    )
                    if not self.now_playing:
                        EmbeddedMessage = InteractiveEmbed(embed=self.build_embed(), player=player)
                        await EmbeddedMessage.start(self.context)
                        self.now_playing = EmbeddedMessage.message
                    else:
                        await self.now_playing.edit(embed=self.build_embed())
                    self.current_track = song
                    await player.play(song)
                    await self.next.wait()
                    await self.last_songs.put(song)


class Music(
    commands.Cog,
    wavelink.WavelinkMixin,
    description="Play music on your server!\nYoutube, Spotify, Soundcloud supported!\n Comes with multiple features",
):
    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}
        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(bot=self.bot)
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
            self.nodes = config["music"]["nodes"]
            self.spotify = config["music"]["Spotify"]
        self.bot.loop.create_task(self.start_nodes())
        self.check_controllers.start()
    async def destroy_nodes(self):
        for n in self.nodes.values():
            await self.bot.wavelink.destroy_node(n['identifier'])

    async def is_whitelisted(self, userID):
        GetUser = await self.bot.db.fetchrow("SELECT user_id FROM admin WHERE user_id = $1", userID)
        return True if GetUser else False
    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)

        for n in self.nodes.values():
            try:
                await self.bot.wavelink.initiate_node(**n)
            except wavelink.errors.NodeOccupied:
                pass

    @tasks.loop(seconds=10)
    async def check_controllers(self):
        Deletion_list = []
        for id, controller in self.controllers.items():
            player = self.bot.wavelink.get_player(controller.guild_id)
            if player.channel_id:
                channel = self.bot.get_channel(player.channel_id)
                members = [x for x in channel.members if x.bot == False]
            else:
                members = None
            if not player.is_playing and not player.is_connected and controller.queue.empty():
                print(f"stopping controller for {controller.guild_id}")
                Deletion_list.append(controller)
            if player.is_connected and not members:
                print(f"There is noone in the channel! Stopping controller for {controller.guild_id}")
                Deletion_list.append(controller)
        for controller in Deletion_list:
            ctx = controller.context
            await ctx.invoke(self.stop)
    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node: wavelink.Node):
        print(f"\u001b[97m Node {node.identifier} \u001b[92m ONLINE \u001b[97m")

    @wavelink.WavelinkMixin.listener()
    async def on_track_end(
        self, node: wavelink.node.Node, event: wavelink.events.TrackEnd
    ):
        controller = self.get_controller(event.player.guild_id)
        if not controller:
            return
        try:
            controller.next.set()
        except AttributeError:
            pass
        if controller.now_playing and controller.queue.empty() and not controller.auto_play and not controller.loop:
            await controller.now_playing.delete()
            controller.now_playing = None
    @wavelink.WavelinkMixin.listener()
    async def on_track_stuck(
        self, node: wavelink.node.Node, event: wavelink.events.TrackStuck
    ):
        controller = self.get_controller(event.player.guild_id)
        print(f"Track stuck! Skipping!")
        controller.next.set()

    @wavelink.WavelinkMixin.listener()
    async def on_track_exception(
        self, node: wavelink.node.Node, event: wavelink.events.TrackException
    ):
        print(
            f"[{node.identifier}] An error has occured:  {event.error}, Switching!"
        )
        await event.player.change_node()

    def get_controller(self, value: Union[commands.Context, int]):
        if isinstance(value, commands.Context):
            gid = value.guild.id
        else:
            gid = value
        try:
            controller = self.controllers[gid]
            return controller
        except KeyError:
            if not isinstance(value, int):
                controller = MusicController(self.bot, gid, value)
                self.controllers[gid] = controller
                return controller

    # @commands.Cog.listener()
    # async def on_voice_state_update(
    #     self,
    #     member: discord.Member,
    #     before: discord.VoiceState,
    #     after: discord.VoiceState,
    # ):
    #     player = self.bot.wavelink.get_player(member.guild.id)
    #     controller = self.get_controller(player)
    #     if (
    #         (before.channel and not after.channel)
    #         and member.bot
    #         and member == self.bot.user
    #     ):
    #         if controller.remote_control:
    #             return await player.connect(before.channel.id)
    #         print("Player has been closed! Stopping!")
    #         if controller.auto_play:
    #             controller.auto_play = False
    #             controller.auto_play_queue._queue.clear()
    #         if controller.loop:
    #             controller.loop = False
    #         controller.queue._queue.clear()
    #         await player.stop()
    #         await player.disconnect()
    #         del self.controllers[member.guild.id]
    #     if controller.remote_control:
    #         if before.channel and after.channel:
    #             if (
    #                 member == self.bot.user
    #                 and any([x.id in whitelist for x in before.channel.members])
    #                 and not any([x.id in whitelist for x in after.channel.members])
    #             ):
    #                 return await player.connect(before.channel.id)
    async def cog_before_invoke(self, ctx: commands.Context):
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_playing and not controller.queue.empty() and not player.current and player.is_connected:
            message = await ctx.send(embed=discord.Embed(description="Music player got stuck! Attempting to resume!"))
            await ctx.invoke(self.stop)
            await ctx.invoke(self.connect_)
            await message.edit(embed=discord.Embed(description="Resuming song again, if it does not play contact devs!"), delete_after=10)
    async def cog_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True
    async def cog_command_error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(
                    embed=discord.Embed(description="This command can not be used in Private Messages.")
                )
            except discord.HTTPException:
                pass
        if isinstance(error, commands.MissingRequiredArgument):
            try:
                return await ctx.send(embed=discord.Embed(description=f"Oops! Missing {error.param.name}, try run help on the command."))
            except discord.HTTPException:
                pass
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

    @commands.command(name="connect", hidden=True)
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        """Connect to a valid voice channel."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if player.is_playing:
            if controller.remote_control:
                if not await self.is_whitelisted(ctx.author.id):
                    return await ctx.message.add_reaction("\N{Cross Mark}")
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                return await ctx.send(embed=discord.Embed(description="No channel to join. Please either specify a valid channel or join one."),delete_after=5)

        embed1 = discord.Embed(description=f"Connecting to **`{channel.name}...`**")
        msg = await ctx.send(embed=embed1, delete_after=15)
        await player.connect(channel.id)
        await msg.delete()
        embed2 = discord.Embed(description=f"Connected to **`{channel.name}`**")
        await ctx.send(embed=embed2, delete_after=15)

        controller.channel = ctx.channel

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, query: str = None):
        """Search for songs on Youtube, Spotify and soundcloud."""
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)

        song = query
        if not player.is_connected:
            await ctx.invoke(self.connect_)
        if controller.remote_control:
            channel = self.bot.get_channel(player.channel_id)
            members = [x.id for x in channel.members if x.bot is False]
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.send(
                    embed=discord.Embed(
                        description="Music controller is locked by owner!"
                    )
                )
        if player.paused and not query:
            return await ctx.invoke(self.resume)
        elif not player.paused and not query:
            return await ctx.send(embed=discord.Embed(description=f"Oops! Missing query, try run help on the command."))

        if spotify_url.match(query):
            if "playlist" in query:
                id = query.strip("https://open.spotify.com/playlist/")
                if "?" in id:
                    id = id.split("?")[0]
                try:
                    playlist = await spotify_client.get_playlist(id)
                except spotify.NotFound:
                    return await ctx.send(
                        embed=discord.Embed(description=f"Playlist could not be found")
                    )
                except spotify.Forbidden:
                    print("spotify rate limited!")
                song_names = [x["track"]["name"] for x in playlist["tracks"]["items"] if x["track"]]
                artistsdata = [x["track"]["artists"][0]["name"] for x in playlist["tracks"]["items"] if x["track"]]


                to_load = zip(song_names, artistsdata)
                for x in to_load:
                    tracks = await self.bot.wavelink.get_tracks(
                        f'ytmsearch:{x[0]+" "+ x[1]}'
                    )
                    if tracks:
                        track = tracks[0]
                        await controller.queue.put(
                            Track(track.id, track.info, requester=ctx.author.mention)
                        )
                else:
                    print(f"Adding {playlist['tracks']['total']} to queue")
                controller.auto_play_queue._queue.clear()
                MusicEmbed = discord.Embed(
                    title=f"Added {playlist['tracks']['total']} songs from {playlist['name']}",
                    url=query,
                    colour=discord.Colour.random(),
                )
                MusicEmbed.set_footer(
                    text=f"{self.bot.user.name} | {player.node.region}"
                )
                return await ctx.send(embed=MusicEmbed)
            if "track" in query:
                id = query.strip("https://open.spotify.com/track/")
                if "?" in id:
                    id = id.split("?")[0]
                try:
                    track = await spotify_client.track(id)
                except spotify.NotFound:
                    return await ctx.send(
                        embed=discord.Embed(
                            description="Playlist not found. Try another!"
                        ),
                        delete_after=10,
                    )
                song_name = track["name"]
                song_artist = track["artists"][0]["name"]
                tracks = await self.bot.wavelink.get_tracks(
                    f"ytmsearch:{song_name } {song_artist}"
                )
                if not tracks:
                    return await ctx.send(
                        embed=discord.Embed(description="Could not find song")
                    )
                track = tracks[0]
                await controller.queue.put(
                    Track(track.id, track.info, requester=ctx.author.mention)
                )
                controller.auto_play_queue._queue.clear()
                if not controller.queue.empty() and player.is_playing:
                    MusicEmbed = discord.Embed(
                        title="Queued",
                        colour=discord.Colour.random(),
                        description=f"[{track.title}]({track.uri}) [{ctx.author.mention}]",
                    )
                    MusicEmbed.set_footer(
                        text=f"{self.bot.user.name} | {player.node.region}"
                    )
                    return await ctx.send(embed=MusicEmbed)
                else:
                    return
        if not RURL.match(query):
            query = f"ytsearch:{query}"

        tracks = await self.bot.wavelink.get_tracks(f"{query}")

        if not tracks:
            for x in range(3):
                if tracks:
                    break
                else:
                    print("Retrying...")
                    tracks = await self.bot.wavelink.get_tracks(f"{query}")
                    await asyncio.sleep(1)
        if not tracks:
            embed = discord.Embed(
                description="failed to find any songs on youtube or soundcloud"
            )
            return await ctx.send(embed=embed, delete_after=5)

        if (
            "list=" in query
            and RURL.match(query)
            and isinstance(tracks, wavelink.TrackPlaylist)
        ):
            playlist = tracks.tracks
            track = playlist[0]
            controller.auto_play_queue._queue.clear()
            for track in playlist:
                await controller.queue.put(
                    Track(track.id, track.info, requester=ctx.author.mention)
                )
            MusicEmbed = discord.Embed(
                title=f"Added {len(playlist)} songs from {tracks.data['playlistInfo']['name']}",
                colour=discord.Colour.random(),
                url=query,
            )
            MusicEmbed.set_footer(text=f"{self.bot.user.name} | {player.node.region}")
            await ctx.send(embed=MusicEmbed)

        else:
            track = tracks[0]
            controller.auto_play_queue._queue.clear()
            await controller.queue.put(
                Track(track.id, track.info, requester=ctx.author.mention)
            )
            if not controller.queue.empty() and player.is_playing:
                MusicEmbed = discord.Embed(
                    title="Queued",
                    colour=discord.Colour.random(),
                    description=f"[{track.title}]({track.uri}) [{ctx.author.mention}]",
                )
                MusicEmbed.set_footer(
                    text=f"{self.bot.user.name} | {player.node.region}"
                )
                await ctx.send(embed=MusicEmbed)

    @commands.command()
    async def pause(self, ctx):
        """Pause the player."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        if not player.is_playing:
            return await ctx.send(
                "I am not currently playing anything!", delete_after=15
            )

        await ctx.message.add_reaction("\N{Double Vertical Bar}")
        await player.set_pause(True)

    @commands.command()
    async def resume(self, ctx):
        """Resume the player from a paused state."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        if not player.paused:
            return await ctx.send("I am not currently paused!", delete_after=15)

        await ctx.message.add_reaction("\N{Black Right-Pointing Triangle}")
        await player.set_pause(False)

    @commands.command(aliases=["s","next"])
    async def skip(self, ctx, times: int = 1):
        """Skip the currently playing song or if specified how many songs."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        if (
            not player.is_playing
            and controller.auto_play_queue.empty()
            and controller.queue.empty()
        ):
            return await ctx.send(
                "I am not currently playing anything!", delete_after=15
            )
        if times < 1:
            times = 1
        await ctx.message.add_reaction("\N{OK Hand Sign}")

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

    @commands.command(aliases=["vol"])
    async def volume(self, ctx, *, vol: int):
        """Set the music player volume."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        vol = max(min(vol, 1000), 0)
        controller.volume = vol

        await ctx.send(embed=discord.Embed(description=f"Setting the player volume to `{vol}`"),delete_after=2)
        await player.set_volume(vol)
    @commands.command(hidden=True)
    async def vol_up(self, ctx):
        """Set the player volume upwards by 10."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        vol = player.volume+10
        if vol<100 and vol>90:
            vol = 100
        elif vol>100:
            return await ctx.send(embed=discord.Embed(description="Max volume reached!"))
        controller.volume = vol
        await player.set_volume(vol)
        await controller.now_playing.edit(embed=controller.build_embed())
    @commands.command(hidden=True)
    async def vol_down(self, ctx):
        """Set the player volume downwards by 10."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        vol = player.volume-10
        if vol<100 and vol>90:
            vol = 100
        elif vol<0:
            return await ctx.send(embed=discord.Embed(description="Bot muted!"))
        controller.volume = vol

        controller.volume = vol
        await player.set_volume(vol)
        await controller.now_playing.edit(embed=controller.build_embed())
    @commands.command(aliases=["np", "current", "nowplaying"])
    async def now_playing(self, ctx):
        """Displays the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        pbar = ""

        if not player.current:
            return await ctx.send("I am not currently playing anything!")

        controller = self.get_controller(ctx)
        track = controller.current_track
        tlpbar = round(track.length // 15)
        pppbar = round(player.position // tlpbar)

        for i in range(15):
            if i == pppbar:
                pbar += ":radio_button:"
            else:
                pbar += "▬"
        embed = discord.Embed(
            title=f"Now playing: `{player.current}`",
            description=f"{pbar}[{datetime.timedelta(milliseconds=player.position)}/{datetime.timedelta(milliseconds=track.length)}]",
        )
        controller.now_playing = await ctx.send(embed=embed)

    @commands.command(aliases=["q"])
    async def queue(self, ctx, pageno=1):
        """Retrieve the queue in pages of 5 per page."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not player.current and not controller.queue._queue:
            return await ctx.send(
                "There are no songs currently in the queue.", delete_after=20
            )
        elif player.current and not controller.queue._queue:
            return await ctx.send(f"Currently only playing: `{player.current}`")
        elif not player.is_connected:
            return
        else:
            pages = menus.MenuPages(source=Paginator(ctx,[f"`{x.title}`[{x.requester}]" for x in list(controller.queue._queue)],"in Queue",f"Now playing {player.current}\nUp next!",5), clear_reactions_after=True)
            await pages.start(ctx)
    @commands.command(aliases=["aq"])
    async def autoqueue(self, ctx, pageno=1):
        """Retrieve the auto play queue in pages of 5 per page."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not controller.auto_play:
            return await ctx.send("Autoplay is not enabled", delete_after=20)
        elif not player.is_connected:
            return
        elif controller.auto_play_queue.empty():
            return await ctx.send(
                embed=discord.Embed(description="Autoplay queue empty!")
            )
        else:
            if controller.queue.empty():
                pages = menus.MenuPages(source=Paginator(ctx,[f"`{x.title}`" for x in list(controller.auto_play_queue._queue)],"in Autoplay Queue",f"Now playing {player.current}\nUp next!",5), clear_reactions_after=True)
            else:
                pages = menus.MenuPages(source=Paginator(ctx,[f"`{x.title}`" for x in list(controller.auto_play_queue._queue)],"in Autoplay Queue",f"Now playing {player.current}",5), clear_reactions_after=True)
            await pages.start(ctx)
    @commands.command(aliases=["lq"])
    async def lastqueue(self, ctx, pageno=1):
        """Retrieve the song history in pages of 5 per page."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if controller.last_songs.empty():
            return await ctx.send(embed=discord.Embed(description="Song history empty"))
        else:
            pages = menus.MenuPages(source=Paginator(ctx,[f"`{x.title}`" for x in list(controller.last_songs._queue)],"in History",f"Last played songs",5), clear_reactions_after=True)
            await pages.start(ctx)
    @commands.command(aliases=["disconnect", "dc"])
    async def stop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        if controller.auto_play:
            controller.auto_play = False
        if controller.loop:
            controller.loop = False
        await player.stop()
        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.disconnect()
            return await ctx.send("There was no controller to stop.")
        await player.disconnect()

        await ctx.message.add_reaction("\N{Octagonal Sign}")

    @commands.command(aliases=["eq"])
    async def equalizer(self, ctx, equalizer: str, amount=1.0):
        """Equalizer for the player"""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        if not player.is_connected:
            return

        eqs = {
            "flat": wavelink.Equalizer.flat(),
            "boost": wavelink.Equalizer.boost(),
            "metal": wavelink.Equalizer.metal(),
            "piano": wavelink.Equalizer.piano(),
        }

        eq = eqs.get(equalizer.lower(), None)

        if not eq:
            joined = "\n".join(eqs.keys())
            return await ctx.send(f"Invalid EQ provided. Valid EQs:\n\n{joined}")

        await ctx.send(
            f"Successfully changed equalizer to {equalizer}", delete_after=15
        )
        await player.set_eq(eq)

    @commands.command()
    async def loop(self, ctx, mode="track"):
        """Loop current playing song"""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        if controller.loop is True:
            controller.loop = False
            await ctx.send("Loop disabled!")
        else:
            if "q" in mode.lower():
                if controller.loop_queue is False:
                    controller.loop = True
                    controller.loop_queue = True
                    await ctx.message.add_reaction(
                        "\N{Clockwise Rightwards and Leftwards Open Circle Arrows}"
                    )
                else:
                    controller.loop = False
                    controller.loop_queue = False
                    await ctx.send("loop track disabled!")
            else:
                controller.loop = True
                await ctx.message.add_reaction(
                    "\N{Clockwise Rightwards and Leftwards Open Circle Arrows}"
                )

    @commands.command(aliases=["ap"])
    async def autoplay(self, ctx):
        """Enable auto play"""
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        if controller.auto_play is True:
            controller.auto_play = False
            controller.auto_play_queue._queue.clear()
            await controller.now_playing.edit(embed=controller.build_embed())
        else:
            controller.auto_play = True
            await controller.now_playing.edit(embed=controller.build_embed())

    @commands.command(aliases=["mix"])
    async def shuffle(self, ctx):
        """Shuffles the queue"""
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        if controller.queue._queue:
            random.shuffle(controller.queue._queue)
            await ctx.message.add_reaction("\N{Twisted Rightwards Arrows}")
        else:
            await ctx.send(embed=discord.Embed(description="Nothing to shuffle!"))

    @commands.command(aliases=["clr"])
    async def clear(self, ctx):
        """Clear queue"""
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        controller.queue._queue.clear()
        if not controller.auto_play_queue.empty():
            controller.auto_play = False
            controller.auto_play_queue._queue.clear()
            await player.stop()

        await ctx.send(embed=discord.Embed(description="Cleared the queue"))

    @commands.command()
    async def lyrics(self, ctx):
        """Gives lyrics of current playing song"""
        controller = self.get_controller(ctx)
        try:
            lyric = genius.search_song(
                controller.current_track.title, controller.current_track.author
            )
        except:
            return await ctx.send(
                embed=discord.Embed(description="something broke oopsies")
            )
        if lyric:
            if len(lyric.lyrics) > 2000:
                embed = discord.Embed(
                    title=lyric.title, description=lyric.lyrics[:2000]
                )
                embed2 = discord.Embed(description=lyric.lyrics[2000:])
                await ctx.send(embed=embed)
                await ctx.send(embed=embed2)
            else:
                embed = discord.Embed(
                    title=controller.current_track.title, description=lyric.lyrics
                )
                await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(description="No lyrics found!"))

    @commands.command()
    async def remove(self, ctx, num: int = 1):
        """Removes the chosen song in queue"""
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if controller.remote_control:
            if not await self.is_whitelisted(ctx.author.id):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        try:
            del controller.queue._queue[num - 1]
            await ctx.message.add_reaction("\N{White Heavy Check Mark}")
        except IndexError:
            await ctx.send(embed=discord.Embed(description="Could not remove"))

    @commands.group(aliases=["playlists", "pl"])
    async def playlist(self, ctx):
        """Add, play and delete playlists from Spotify!"""


        if ctx.invoked_subcommand is None:
            return await ctx.send(embed=discord.Embed(description="Please select:"+ "\n".join([f"```{x.name}```" for x in self.playlist.commands])))

    @playlist.command()
    async def list(self, ctx, *, query=None):
        """Gets all the playlists from Spotify recommended and saved playlists"""
        controller = self.get_controller(ctx)
        await asyncio.sleep(1)
        if not query:
            Embed = discord.Embed(title="Featured Playlists")
            [Embed.add_field(name=x[0], value=x[1]) for x in controller.spotify_playlists if x[1]]
            Embed.set_footer(text=f"{pycountry.countries.get(alpha_2=controller.spotify_region).name}")
            return await ctx.send(embed=Embed)
        elif query.lower() in ["saved", "save", "stored"]:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"saved_playlists.yml",),"r",) as f:
                saved_playlist = yaml.safe_load(f)
            playlists = saved_playlist.get(ctx.guild.id)
            if not playlists:
                return await ctx.send(embed=discord.Embed(description="No playlists saved yet"))
            Embed = discord.Embed(title="Saved Playlists")
            controller.spotify_playlists = zip([x for x in playlists], [x for x in playlists.values()])
            [Embed.add_field(name=x[0], value=x[1][0]) for x in controller.spotify_playlists if x[1]]
            Embed.set_footer(text=f"{pycountry.countries.get(alpha_2=controller.spotify_region).name}")
            return await ctx.send(embed=Embed)
    @playlist.command(aliases=['choose'])
    async def pick(self, ctx, *, query):
        """Plays a specified playlist if available"""
        controller = self.get_controller(ctx)
        await asyncio.sleep(1)
        play = self.bot.get_command("play")
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"saved_playlists.yml",),"r",) as f:
            saved_playlist = yaml.safe_load(f)
            playlists = saved_playlist.get(ctx.guild.id, None)
        if playlists:
            search = playlists.get(query, None)
            if search:
                search = search[1]
                return await play(ctx, query=search)
        else:
            search = None
        if not search:
            search_results = [x for x in controller.spotify_playlists if query in x[0]]
            if search_results:
                return await play(ctx, query=search_results[0][2])
            else:
                search = None
        if not search:
            search_results = await spotify_client.search(query, "playlist",controller.spotify_region)
            if search_results:
                try:
                    url = search_results["playlists"]["items"][0][
                        "external_urls"
                    ]["spotify"]
                    await ctx.message.add_reaction("\N{White Heavy Check Mark}")
                    return await play(ctx, query=url)

                except IndexError:
                    return await ctx.message.add_reaction("\N{Cross Mark}")
            else:
                return await ctx.send(
                    embed=discord.Embed(description="Query not found")
                )
    @playlist.command()
    async def refresh(self, ctx):
        """Force refresh the daily playlist"""
        controller = self.get_controller(ctx)
        print("FORCE REFRESH PLAYLIST")
        try:
            controller.update_playlist.restart()
            await ctx.message.add_reaction("\N{White Heavy Check Mark}")
        except Exception as e:
            await message.add_reaction("\N{Cross Mark}")
    @playlist.command()
    async def region(self, ctx, *, query):
        """Change spotify region for different regional featured playlists"""
        controller = self.get_controller(ctx)
        if len(query) > 2:
            query = pycountry.countries.get(name=query).alpha_2
        if query.upper() in spotify_countries:
            controller.spotify_region = query.upper()
            controller.update_playlist.restart()
            return await ctx.message.add_reaction("\N{White Heavy Check Mark}")
        else:
            return await ctx.message.add_reaction("\N{Cross Mark}")
    @playlist.command()
    async def save(self, ctx, *, query=None):
        """Save a playlist"""
        controller = self.get_controller(ctx)
        if query:
            with open(
                os.path.join(os.path.dirname(os.path.dirname(__file__)),"saved_playlists.yml",),"r",) as f:
                saved_playlist = yaml.safe_load(f)
            search = [x for x in controller.spotify_playlists if query in x[0]]
            if search:
                url = search[0][2]
                description = search[0][1]
                name = search[0][0]
            elif spotify_url.match(query):
                id = query.strip("https://open.spotify.com/playlist/")
                if "?" in id:
                    id = id.split("?")[0]
                try:
                    playlist = await spotify_client.get_playlist(id)
                except spotify.NotFound:
                    return await ctx.send(
                        embed=discord.Embed(description=f"Playlist could not be found")
                    )
                except spotify.Forbidden:
                    print("spotify rate limited!")
                url = playlist["external_urls"]["spotify"]
                description = playlist["description"]
                if description == "":
                    description = "No description provided!"
                name = playlist["name"]
            elif RURL.match(query) and "playlist" in query:
                data = await self.bot.wavelink.get_tracks(f"{query}")
                print(data.data)
            else:
                search_results = await spotify_client.search(query, "playlist")
                url = search_results["playlists"]["items"][0]["external_urls"]["spotify"]
                description = search_results["playlists"]["items"][0]["description"]
                name = search_results["playlists"]["items"][0]["name"]
            if not saved_playlist:
                saved_playlist = {}
            if saved_playlist.get(ctx.message.guild.id, None):
                saved_playlist[ctx.message.guild.id][name] = [description,f"{url}",]
                with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"saved_playlists.yml",),"w",) as f:
                    yaml.dump(saved_playlist, f)
                    await ctx.message.add_reaction("\N{White Heavy Check Mark}")
            else:
                saved_playlist[ctx.message.guild.id] = {
                    name: [description, f"{url}"]
                }
                with open(
                    os.path.join(
                        os.path.dirname(os.path.dirname(__file__)),
                        "saved_playlists.yml",
                    ),
                    "w",
                ) as f:
                    yaml.dump(saved_playlist, f)
                    await ctx.message.add_reaction("\N{White Heavy Check Mark}")
        else:
            with open(
                os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "saved_playlists.yml",
                ),
                "r",
            ) as f:
                saved_playlist = yaml.safe_load(f)
                guild_playlist = saved_playlist[ctx.message.guild.id]
                current_queue = list(controller.queue._queue)
    @playlist.command()
    async def delete(self, ctx, *, query):
        """Delete a playlist"""
        controller = self.get_controller(ctx)
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"saved_playlists.yml",),"r",) as f:
            saved_playlist = yaml.safe_load(f)
        try:
            saved_playlist[ctx.message.guild.id].pop(query)
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"saved_playlists.yml",),"w",) as f:
                yaml.dump(saved_playlist, f)
            return await ctx.message.add_reaction("\N{White Heavy Check Mark}")
        except:
            return await ctx.message.add_reaction("\N{Cross Mark}")
    @commands.command(aliases=["wl"], hidden=True)
    async def whitelist(self, ctx):
        if not await self.is_whitelisted(ctx.author.id):
            return await ctx.message.add_reaction("\N{Cross Mark}")
        controller = self.get_controller(ctx)
        if controller.remote_control:
            controller.remote_control = False
            await ctx.message.add_reaction("\N{OK Hand Sign}")
            await asyncio.sleep(1)
            return await ctx.message.delete()
        else:
            controller.remote_control = True
            await ctx.message.add_reaction("\N{White Heavy Check Mark}")
            await asyncio.sleep(1)
            return await ctx.message.delete()

    @commands.command(aliases=["back"])
    async def last(self, ctx, num=0):
        """Plays last played song"""
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if controller.remote_control:
            channel = self.bot.get_channel(player.channel_id)
            members = [x.id for x in channel.members if x.bot is False]
            if (
                any([x in whitelist for x in members])
                and ctx.message.author.id not in whitelist
            ):
                return await ctx.message.add_reaction("\N{Cross Mark}")
        if controller.last_songs.qsize() < 1:
            return
        if controller.last_songs.qsize() >= num:
            controller.queue._queue.appendleft(controller.current_track)
            for x in range(num + 1):
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
    @commands.command(aliases=['boost','bassboost'])
    async def bass(self, ctx, amount:int):
        """Bass boost the song by any amount of percentage!\n do eq command to reset"""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        amount = 1+amount/100
        levels = [(0, -0.075*amount), (1, .125*amount), (2, .125*amount), (3, .1*amount), (4, .1*amount),
                  (5, .05*amount), (6, 0.075*amount), (7, .0), (8, .0), (9, .0),
                  (10, .0), (11, .0), (12, .125), (13, .15), (14, .05)]

        await ctx.send(
            f"Successfully changed bass boost to {amount}x", delete_after=15
        )
        await player.set_eq(wavelink.Equalizer.build(levels=levels))
    @commands.command(hidden=True)
    async def information(self, ctx):
        """Retrieve various Node/Server/Player information."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        node = player.node

        used = humanize.naturalsize(node.stats.memory_used)
        total = humanize.naturalsize(node.stats.memory_allocated)
        free = humanize.naturalsize(node.stats.memory_free)
        cpu = node.stats.cpu_cores
        command = ['git',"describe","--always"]
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf8")
        fmt = (
            f"**{self.bot.user.name} commit:** `{stdout}`\n\n"
            f"Connected to `{len(self.bot.wavelink.nodes)}` nodes.\n"
            f"Best available Node `{self.bot.wavelink.get_best_node().__repr__()}`\n"
            f"`{len(self.bot.wavelink.players)}` players are distributed on nodes.\n"
            f"`{node.stats.players}` players are distributed on server.\n"
            f"`{node.stats.playing_players}` players are playing on server.\n"
            f"`{len(self.controllers)}` controllers.\n\n"
            f"Server Memory: `{used}/{total}` | `({free} free)`\n"
            f"Server CPU: `{cpu}`\n\n"
            f"Server Uptime: `{datetime.timedelta(milliseconds=node.stats.uptime)}`"
        )
        await ctx.send(fmt)
        process.stdout.close()


    @commands.command(hidden=True)
    async def addnode(self, ctx, rest_uri, region):
        if not await self.is_whitelisted(ctx.author.id):
            return await ctx.message.add_reaction("\N{Cross Mark}")
        try:
            host,port = rest_uri.split(":")
            identifier = f"{self.bot.user.name}-{region}-{next(idgenerator)}"
            await self.bot.wavelink.initiate_node(host=host,
                                                     port=port,
                                                     rest_uri=f"http://{rest_uri}",
                                                     password='youshallnotpass',
                                                     identifier=identifier,
                                                     region=region)
            return await ctx.message.add_reaction("\N{White Heavy Check Mark}")
        except Exception as e:
            print(e)
            return await ctx.message.add_reaction("\N{Cross Mark}")

    @commands.command(hidden=True)
    async def listnode(self, ctx):
        if not await self.is_whitelisted(ctx.author.id):
            return await ctx.message.add_reaction("\N{Cross Mark}")
        embed = discord.Embed(title="All servers")
        for y,x in enumerate(self.bot.wavelink.nodes.keys(),start=1):
            embed.add_field(name=y,value=x)
        await ctx.send(embed=embed)
    @commands.command(hidden=True)
    async def destroynode(self, ctx, identifier: str):
        if not await self.is_whitelisted(ctx.author.id):
            return await ctx.message.add_reaction("\N{Cross Mark}")
        try:
            await self.bot.wavelink.destroy_node(identifier=identifier)
            return await ctx.message.add_reaction("\N{White Heavy Check Mark}")
        except Exception:
            return await ctx.message.add_reaction("\N{Cross Mark}")
def setup(bot):
    bot.add_cog(Music(bot))
