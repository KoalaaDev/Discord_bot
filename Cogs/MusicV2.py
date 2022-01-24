import discord
import pomice
import datetime
import typing
import random
from pomice.objects import Track
from .ext.music import MusicQueue
from discord.ext import commands
import asyncio
import yaml
import os
from discord_components import DiscordComponents, Select, SelectOption

config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "apiconfig.yml")

class Player(pomice.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = MusicQueue()
        self.auto_play = self.loop = self.loopq = False
        self.context: commands.Context = None
        self.now_playing: discord.Message = None
        self.current_track: Track = None

    def build_stream_embed(self) -> typing.Optional[discord.Embed]:
        """Build the player Livestream embed"""
        track = self.current_track
        channel = self.channel
        embed = discord.Embed(title=f":red_circle: **LIVE** on {self.bot.user.name} | {channel.name}", colour=0xebb145)
        embed.description = f'Now Playing:\n[{track.title}]({track.uri})\n\n'
        embed.set_thumbnail(url=track.thumbnail)
        embed.add_field(name='Volume', value=f'**`{self.volume}%`**')
        embed.add_field(name='Requested By', value=track.requester)
        embed.set_footer(text="Youtube Live/Twitch")
        return embed

    def build_embed(self) -> typing.Optional[discord.Embed]:
        """Method which builds our players controller embed."""
        track = self.current_track
        channel = self.channel
        qsize = len(self.queue)
        track_type = "Spotify" if track.spotify else "Youtube"
        embed = discord.Embed(title=f':musical_note: {self.bot.user.name} Music | {channel.name}', colour=0xebb145)
        embed.description = f'Now Playing:\n[{track.title}]({track.uri})\n\n'
        embed.set_thumbnail(url=track.thumbnail)

        embed.add_field(name='Duration', value=str(datetime.timedelta(milliseconds=int(track.length))))
        embed.add_field(name='Queue Length', value=str(qsize))
        embed.add_field(name='Volume', value=f'**`{self.volume}%`**')
        embed.add_field(name='Requested By', value=track.requester)
        if self.auto_play:
            embed.add_field(name='Autoplay', value=f'**`{self.auto_play}`**')
        if self.loop:
            embed.add_field(name='Loop', value=f'**`{self.loop}`**')
        if self.loopq:
            embed.add_field(name='Loop', value='**`Queue`**')
        embed.set_footer(text=f"{track_type}")
        return embed

    async def is_position_fresh(self) -> bool:
        """Method which checks whether the player controller should be remade or updated."""
        try:
            async for message in self.context.channel.history(limit=5):
                if message.id == self.now_playing.id:
                    return True
        except (discord.HTTPException, AttributeError, discord.Forbidden):
            return False

        return False
                
    async def next(self) -> None:
        """Gets next song from queue and play it"""
        try:
            track: pomice.Track = await self.queue.get()
        except asyncio.queues.QueueEmpty:
            return
        self.current_track = track
        await self.play(track)
        if self.now_playing and await self.is_position_fresh():
            if self.current_track.is_stream:
                return await self.now_playing.edit(embed=self.build_stream_embed())
            return await self.now_playing.edit(embed=self.build_embed())
        if self.now_playing:
            await self.now_playing.delete()
        if self.current_track.is_stream:
            self.now_playing = await self.context.send(embed=self.build_stream_embed())
        else:
            self.now_playing = await self.context.send(embed=self.build_embed())
    async def loop_next(self) -> None:
        """Gets the current song being played and plays it again"""
        await self.play(self.current_track)
        return await self.now_playing.edit(embed=self.build_embed())

    async def loopq_next(self) -> None:
        """Get the next song and puts the last song played back into the queue"""
        await self.queue.put(self.current_track)
        await self.next()

    async def autoplay_next(self) -> None:
        """Uses the Youtube Mix to generate songs after the queue becomes empty"""
        if self.queue.is_empty:
            ytid = self.current_track.uri.split("https://www.youtube.com/watch?v=")[1]
            for attempt in range(5):
                mix = await self.get_tracks(f"https://www.youtube.com/watch?v={ytid}&list=RD{ytid}", ctx=self.context)
                if mix:
                    break
                print("\u001b[91m [AP] Retrying to load Mix \u001b[0m")
            for track in mix.tracks[1:]:
                await self.queue.put(track)
        await self.next()

    async def teardown(self):
        """Kills the player"""
        await self.destroy()
        if self.now_playing:
            await self.now_playing.delete()
    
    def set_context(self, ctx: commands.Context):
        """Gets the Context"""
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
            try:
                await self.pomice.create_node(bot=self.bot, spotify_client_id=self.spotify['ClientID'], spotify_client_secret=self.spotify['ClientSecret'],**n)
            except pomice.exceptions.NodeCreationError:
                pass

    @commands.Cog.listener()
    async def on_pomice_track_end(self, player: Player, track, _):
        if player.loop:
            await player.loop_next()
        elif player.loopq:
            await player.loopq_next()
        elif player.auto_play:
            await player.autoplay_next()
        else:
            await player.next()

    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, player: Player, track, _):
        print(f"\u001b[36m Track stuck after {_}ms reached! Skipping! \u001b[0m")
        await player.next()

    @commands.Cog.listener()
    async def on_pomice_track_exception(self, player: Player, track, _):
        print(f"\u001b[91m A track exception occured, Skipping! Exception:\n{_} \u001b[0m")
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

    @commands.command(aliases=['disconnect', 'dc', 'disc', 'lv', 'fuckoff', 'stop'])
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
            if player.current_track:
                MusicEmbed = discord.Embed(
                    title=f"Added {results.track_count} songs from {results.name}",
                    colour=discord.Colour.random()
                )
                MusicEmbed.set_footer(text=f"{self.bot.user.name} | {track_type}")
                await ctx.send(embed=MusicEmbed)
        else:
            track = results[0]
            track_type = "Spotify" if track.spotify else "Youtube"
            await player.queue.put(track)
            if player.current_track:
                MusicEmbed = discord.Embed(
                        title="Queued",
                        colour=discord.Colour.random(),
                        description=f"[{track.title}]({track.uri}) [{ctx.author.mention}]",
                    )
                MusicEmbed.set_footer(text=f"{self.bot.user.name} | {track_type}")
                await ctx.send(embed=MusicEmbed)
        if not player.is_playing:
            await player.next()

    @commands.command(aliases=['n', 's', 'next'])
    async def skip(self, ctx: commands.Context):
        """Skip the currently playing song."""
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        if player.loop:
            player.loop = False
            await player.stop()
            player.loop = True
            return await ctx.message.add_reaction("\N{OK Hand Sign}")
        await player.stop()
        try:
            await ctx.message.add_reaction("\N{OK Hand Sign}")
        except:
            await ctx.send("OK")
    
    @commands.command(aliases=["vol"])
    async def volume(self, ctx, *, vol: int):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return    
        await ctx.send(embed=discord.Embed(description=f"Setting the player volume to `{vol}`"),delete_after=2)
        await player.set_volume(vol)

    @commands.command(aliases=['mix', 'shuf'])
    async def shuffle(self, ctx: commands.Context):
        """Shuffle the players queue."""
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        if len(player.queue)<1:
            return await ctx.send('The queue is empty. Add some songs to shuffle the queue.', delete_after=15)
        random.shuffle(player.queue._queue)
        try:
            await ctx.message.add_reaction("\N{Twisted Rightwards Arrows}")
        except:
            await ctx.send("OK")

    @commands.command()
    async def clear(self, ctx: commands.Context):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        await player.queue.clear()
        player.loop = False
        player.loopq = False
        player.auto_play = False
        await player.stop()
        await ctx.message.add_reaction("\N{Octagonal Sign}")

    @commands.command(aliases=['l'])
    async def loop(self, ctx: commands.Context):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        player.loop = True if not player.loop else False
        try:
            await ctx.message.add_reaction("\N{OK Hand Sign}")
        except:
            await ctx.send(f"OK loop {player.loop}")
        # initialmsg = await ctx.send("Choose Loop Mode:",components = [Select(placeholder = "Select a mode!",options = [SelectOption(label = "Loop Track", value = "loop"),SelectOption(label = "Loop Queue", value = "q"), SelectOption(label = "Disabled", value = "disabled")])])
        # interaction = await self.bot.wait_for("select_option")
        # await interaction.send(f"{interaction.values[0]} selected!")
        # if interaction.values[0] == 'q':
        #     player.loopq = True
        # elif interaction.values[0] == 'loop':
        #     player.loop = True
        # elif interaction.values[0] == 'disabled':
        #     player.loop = False
        #     player.loop_queue = False
        # await initialmsg.delete()
        
    @commands.command(aliases=['lq'])
    async def loopq(self, ctx: commands.Context):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        player.loopq = True if not player.loopq else False
        try:
            await ctx.message.add_reaction("\N{OK Hand Sign}")
        except:
            await ctx.send(f"OK loop Queue {player.loopq}")
    
    @commands.command(aliases=['ap'])
    async def autoplay(self, ctx: commands.Context):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        player.auto_play = True if not player.auto_play else False
        try:
            await ctx.message.add_reaction("\N{OK Hand Sign}")
        except:
            await ctx.send(f"OK autoplay {player.auto_play}")

    @commands.command()
    async def history(self, ctx):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        songs = '\n'.join(player.history)
        await ctx.send(songs)
    
    @commands.command(aliases=['q'])
    async def queue(self, ctx, show: int = 10):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {show} tracks",
        )
        embed.add_field(name="Currently playing", value=getattr(player.current_track, "title", "No tracks currently playing."), inline=False)
        if upcoming := player.queue.upcoming :
            embed.add_field(
                name="Next up",
                value="\n".join(f'**{n}.** `{t.title}`' for n, t in enumerate(upcoming[:show], start=1)),
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def move(self, ctx, pos1: int, pos2: int):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        track = player.queue[pos1]
        del player.queue[pos1]
        player.queue.put_at_index(pos2, track)
        await ctx.message.add_reaction("\N{White Heavy Check Mark}")

    @commands.command(name='8d')
    async def _8d(self, ctx):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        if player._filter:
            await player.reset_filter()
            await ctx.send("Filter Reset")
        else:
            await player.set_filter(pomice.filters.Rotation(rotation_hertz=0.2))
            try:
                await ctx.message.add_reaction("\N{OK Hand Sign}")
            except:
                await ctx.send(f"8D effect enabled!")
    
    @commands.command()
    async def nightcore(self, ctx):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        if player._filter:
            await player.reset_filter()
            await ctx.send("Filter Reset")
        else:
            await player.set_filter(pomice.filters.Timescale(speed=1.19, pitch=1.2))
            try:
                await ctx.message.add_reaction("\N{OK Hand Sign}")
            except:
                await ctx.send(f"nightcore effect enabled!")
    
    @commands.command()
    async def karaoke(self, ctx):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        if player._filter:
            await player.reset_filter()
            await ctx.send("Filter Reset")
        else:
            await player.set_filter(pomice.filters.Karaoke())
            try:
                await ctx.message.add_reaction("\N{OK Hand Sign}")
            except:
                await ctx.send(f"karaoke effect enabled!")

    @commands.command()
    async def speed(self, ctx, speed):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)
        if not player.is_connected:
            return
        if player._filter:
            await player.reset_filter()
            await ctx.send("Filter Reset")
        else:
            await player.set_filter(pomice.filters.Timescale(speed=speed))
            try:
                await ctx.message.add_reaction("\N{OK Hand Sign}")
            except:
                await ctx.send(f"{speed}x speed effect enabled!")

def setup(bot: commands.Bot):
    bot.add_cog(MusicV2(bot))