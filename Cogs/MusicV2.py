import discord
from discord.ext.commands.core import command
import pomice
import datetime
import typing
from .ext.music import MusicQueue, HistoryQueue
from discord.ext import commands
import asyncio
import yaml
import os

config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "apiconfig.yml")

class Player(pomice.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = MusicQueue()
        self.history = HistoryQueue()
        self.autoplay = self.loop = False
        self.context: commands.Context = None
        self.now_playing: discord.Message = None

    def build_embed(self) -> typing.Optional[discord.Embed]:
        """Method which builds our players controller embed."""
        track = self.current
        channel = self.bot.get_channel(int(self.channel.id))
        qsize = len(self.queue)
        track_type = "Spotify" if track.spotify else "Youtube"
        if track.is_stream:
            embed = discord.Embed(title=f":red_circle: **LIVE** on {self.bot.user.name} | {channel.name}", colour=0xebb145)
        else:
            embed = discord.Embed(title=f'Interactive {self.bot.user.name} | {channel.name}', colour=0xebb145)
        embed.description = f'Now Playing:\n[{track.title}]({track.uri})\n\n'
        embed.set_thumbnail(url=track.thumb)

        embed.add_field(name='Duration', value=str(datetime.timedelta(milliseconds=int(track.length))))
        embed.add_field(name='Queue Length', value=str(qsize))
        embed.add_field(name='Volume', value=f'**`{self.volume}%`**')
        embed.add_field(name='Requested By', value=track.requester)
        if self.auto_play:
            embed.add_field(name='Autoplay', value=f'**`{self.auto_play}`**')
        embed.set_footer(text=f"{track_type}")
        return embed

    def YoutubeDJ(self) -> typing.List:
        pass
    async def next(self) -> None:
        if self.now_playing and len(self.queue)>1:
            await self.now_playing.edit(embed=self.build_embed())
        try:
            track: pomice.Track = self.queue.get_nowait()
        except asyncio.queues.QueueEmpty:  
            return await self.teardown()
        await self.play(track)
        self.now_playing = await self.context.send(embed=self.build_embed())

    async def teardown(self):
        await self.destroy()
        if self.now_playing:
            await self.now_playing.delete()
    
    def set_context(self, ctx: commands.Context):
        self.context = ctx

        
class MusicV2(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
            self.nodes = config["music"]["nodes"]
            self.spotify = config["music"]["Spotify"]
        self.pomice = pomice.NodePool()
        bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        for n in self.nodes.values():
            await self.pomice.create_node(bot=self.bot, spotify_client_id=self.spotify['ClientID'], spotify_client_secret=self.spotify['ClientSecret'],**n)
    @commands.Cog.listener()
    async def on_pomice_track_end(self, player: Player, track, _):
        await player.next()

    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, player: Player, track, _):
        await player.next()

    @commands.Cog.listener()
    async def on_pomice_track_exception(self, player: Player, track, _):
        await player.next()
        
    @commands.command(aliases=['summon'])
    async def connect(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None) -> None:
        if not channel:
            channel = getattr(ctx.author.voice, "channel", None)
            if not channel:
                return await ctx.send("You must be in a voice channel in order to use this command!")

        # With the release of discord.py 1.7, you can now add a compatible
        # VoiceProtocol class as an argument in VoiceChannel.connect().
        # This library takes advantage of that and is how you initialize a player.
        await ctx.author.voice.channel.connect(cls=Player)
        player: Player = ctx.voice_client
    
        # Set the player context so we can use it so send messages
        player.set_context(ctx=ctx)
        await ctx.send(f"Joined the voice channel `{channel.name}`")

    @commands.command(aliases=['disconnect', 'dc', 'disc', 'lv', 'fuckoff'])
    async def leave(self, ctx: commands.Context):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)

        await player.destroy()
        await ctx.send("Player has left the channel.")

    @commands.command(aliases=['pla', 'p'])
    async def play(self, ctx: commands.Context, *, search: str) -> None:
        # Checks if the player is in the channel before we play anything
        if not (player := ctx.voice_client):
            await ctx.invoke(self.connect) 

        # If you search a keyword, Pomice will automagically search the result using YouTube
        # You can pass in "search_type=" as an argument to change the search type
        # i.e: player.get_tracks("query", search_type=SearchType.ytmsearch)
        # will search up any keyword results on YouTube Music
        player: Player = ctx.voice_client
        # We will also set the context here to get special features, like a track.requester object
        results = await player.get_tracks(search, ctx=ctx)     
        if not results:
            return await ctx.send("No results were found for that search term", delete_after=7)
        
        if isinstance(results, pomice.Playlist):
            track_type = "Spotify" if results.spotify else "Youtube"
            for track in results.tracks:
                await player.queue.put(track)
            MusicEmbed = discord.Embed(
                title=f"Added {results.track_count} songs from {results.name}",
                colour=discord.Colour.random(),
                url=results.uri,
            )
            MusicEmbed.set_footer(text=f"{self.bot.user.name} | {track_type}")
            await ctx.send(embed=MusicEmbed)
        else:
            track = results[0]
            track_type = "Spotify" if track.spotify else "Youtube"
            await player.queue.put(track)
            MusicEmbed = discord.Embed(
                    title="Queued",
                    colour=discord.Colour.random(),
                    description=f"[{track.title}]({track.uri}) [{ctx.author.mention}]",
                )
            MusicEmbed.set_footer(text=f"{self.bot.user.name} | {track_type}")
            await ctx.send(embed=MusicEmbed)
        if not player.is_playing:
            await player.next()

def setup(bot: commands.Bot):
    bot.add_cog(MusicV2(bot))