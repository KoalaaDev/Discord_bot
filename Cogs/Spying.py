import time
from datetime import datetime
import string
import discord
from discord.ext import commands
from rich.traceback import install
import os
install()
import yaml

class Spying(commands.Cog, name="Spying logic"):
    def __init__(self, bot):
        self.bot = bot
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apiconfig.yml')
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
            self.text_message_channel = self.bot.get_channel(config['spying']['text_spying_channel'])
            self.bot_channel = self.bot.get_channel(config['spying']['bot_text_spying_channel'])
            self.member_update_channel = self.bot.get_channel(config['spying']['member_update_spying_channel'])
            self.guild_update_channel = self.bot.get_channel(config['spying']['guild_update_spying_channel'])
            self.connected_voice_channels = self.bot.get_channel(config['spying']['connected_voice_channels'])
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if not after.channel:
            return await self.connected_voice_channels.send(embed=discord.Embed(description=f"{member.name} disconnected from {before.channel.name}"))
        if not before.channel and after.channel:
            return await self.connected_voice_channels.send(embed=discord.Embed(description=f"{member.name} joined {after.channel.name}"))
        if before.channel and after.channel:
            return await self.connected_voice_channels.send(embed=discord.Embed(description=f"{member.name} moved from {before.channel.name} to {after.channel.name}"))
    @commands.Cog.listener()
    async def on_message(self, message: str):
        if message.author.bot:
            if message.author != self.bot.user and message.author.id != 799134976515375154 and message.author.id != 654581273028853770:
                if message.embeds:
                    await self.bot_channel.send(embed=message.embeds[0])
                else:
                    botEmbed = discord.Embed(
                        title=f"BOT {message.author}",
                        description=f"```{message.content}```",
                    )
                    try:
                        await self.bot_channel.send(embed=botEmbed)
                    except AttributeError:
                        pass
                    print(
                        f"[SPY COG] BOT {message.author} detected, Sent to appropriate channel"
                    )
            else:
                pass
        elif message.channel == self.text_message_channel or message.content.startswith(string.punctuation):
            print(f"[SPY COG] Did not log {message.content} from {message.author}")
        else:
            ts = time.time()
            st = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            with open("logs.txt", "a") as text_file:
                if message.attachments:
                    img = message.attachments[0].url
                    print(message.attachments[0].filename)
                    log = " {}".format(img)
                    if message.attachments[0].filename.endswith(('3g2','3gp','amv','asf','avi','drc','f4a','f4b','f4p','f4v','flv','m2ts','m2v','m4p','m4v','mkv','mng','mov','mp2','mp4','mpe','mpeg','mpg','mpv','mts','mxf','nsv','ogg','ogv','qt','rm','rmvb','roq','svi','ts','vob','webm','wmv','yuv')):
                        try:
                            await self.text_message_channel.send(f"{message.author}:{message.attachments[0].url}")
                        except AttributeError:
                            pass
                    else:
                        PictureEmbed = discord.Embed(
                            title=
                            f"Text Channel: {message.channel}\n Guild: {message.guild}",
                            description=f"{message.author}:",
                            colour=discord.Color.red(),
                        )
                    PictureEmbed.set_footer(text=f"<{st}>")
                    PictureEmbed.set_image(url=log)
                    try:
                        await self.text_message_channel.send(embed=PictureEmbed)
                    except AttributeError:
                        pass
                    print(
                        f"<{st}> in text channel {message.channel} at {message.guild} | {message.author}:{log}",
                        file=text_file,
                    )
                else:
                    Embedded = discord.Embed(
                        description=
                        f"```{discord.utils.escape_mentions(message.content)}```",
                        colour=discord.Colour.red(),
                    )
                    Embedded.set_footer(text=f"<{st[:-3]}> {message.channel} | {message.guild}")
                    Embedded.set_author(name=message.author,icon_url=message.author.avatar_url)
                    try:
                        await self.text_message_channel.send(embed=Embedded)
                    except AttributeError:
                        pass
                    print(
                        f"<{st}> in text channel {message.channel} at {message.guild} | {message.author}: {message.content}",
                        file=text_file,
                    )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        if before.bot or after.bot:
            print(
                f"[SPY COG] Did not record bot account status: {after}\nStatus:{after.status}\n"
            )
        else:
            if before.roles != after.roles:
                shorter, longer = sorted([after.roles, before.roles], key=len)
                Embedded = discord.Embed(
                    title="{after.guild.name}",
                    description=f"{before.name}'s role has been changed from {before.role.name} to {after.role.name}",
                )
                Embedded.set_image(url=after.avatar_url)
                Embedded.set_footer(text=f"Role Update Detector Service <{st}>")
                try:
                    await self.member_update_channel.send(embed=Embedded)
                except AttributeError:
                    pass
            elif before.status != after.status:
                if after.status == discord.Status.dnd:
                    dndEmbedded = discord.Embed(
                        title="Status indicator: :red_circle: ",
                        description=
                        f"{before.name} from {before.guild} has been set to Do Not Disturb ",
                        colour=discord.Colour(0xFCEC00),
                    )
                    dndEmbedded.set_footer(text=f"Status Update Detector Service <{st}>")
                    dndEmbedded.set_image(url=after.avatar_url)
                    try:
                        await self.member_update_channel.send(embed=dndEmbedded)
                    except AttributeError:
                        pass
                if after.status == discord.Status.online:
                    Embedded = discord.Embed(
                        title="Status indicator: :green_circle:  ",
                        description=f"{before.name} from {before.guild} is now Online ",
                        colour=discord.Colour(0xFCEC00),
                    )
                    Embedded.set_footer(
                        text=f"Status Update Detector Service <{st}>")
                    Embedded.set_image(url=after.avatar_url)
                    try:
                        await self.member_update_channel.send(embed=Embedded)
                    except AttributeError:
                        pass
                if after.status == discord.Status.idle:
                    Embedded = discord.Embed(
                        title="Status indicator: :orange_circle:  ",
                        description=f"{before.name} from {before.guild} went Away/AFK ",
                        colour=discord.Colour(0xFCEC00),
                    )
                    Embedded.set_footer(
                        text=f"Status Update Detector Service <{st}>")
                    Embedded.set_image(url=after.avatar_url)
                    try:
                        await self.member_update_channel.send(embed=Embedded)
                    except AttributeError:
                        pass
                if after.status == discord.Status.offline:
                    Embedded = discord.Embed(
                        title="Status indicator: :black_circle:",
                        description=f"{before.name} from {before.guild} has gone Offline ",
                        colour=discord.Colour(0xFCEC00),
                    )
                    Embedded.set_footer(
                        text=f"Status Update Detector Service <{st}>")
                    Embedded.set_image(url=after.avatar_url)
                    try:
                        await self.member_update_channel.send(embed=Embedded)
                    except AttributeError:
                        pass
            elif before.activity != after.activity:
                if before.activity==None or after.activity==None:
                    pass
                else:
                    if after.activity.type == discord.ActivityType.playing:
                        playEmbedded = discord.Embed(
                            title=":video_game: Game Detector Service :video_game: ",
                            description=f"{before.name} from {before.guild}  is now playing {after.activity.name}",
                            colour=discord.Colour.orange(),
                        )
                        playEmbedded.add_field(name="Match:",
                                               value=after.activity.details)
                        playEmbedded.set_image(url=after.activity.large_image_url)
                        playEmbedded.set_footer(
                            text=f"Activity Update Detector Service <{st}>")
                        try:
                            await self.member_update_channel.send(embed=playEmbedded)
                        except:
                            pass

                    elif after.activity.type == discord.ActivityType.streaming:
                        streamingEmbedded = discord.Embed(
                            title="Streamer Detector Service",
                            description=f"{before.name} from {before.guild} is now streaming {after.activity.name}",
                            colour=discord.Colour.orange(),
                        )
                        streamingEmbedded.add_field(name="Details:",
                                                    value=after.activity.details)
                        streamingEmbedded.add_field(name="Url",
                                                    value=after.activity.url,
                                                    inline=False)
                        streamingEmbedded.set_footer(
                            text=f"Activity Update Detector Service <{st}>")
                        try:
                            await self.member_update_channel.send(embed=streamingEmbedded)
                        except AttributeError:
                            pass
                    elif after.activity.type == discord.ActivityType.listening:
                        listeningEmbedded = discord.Embed(
                            title="Music Detector Service :musical_note:",
                            description=f"{before.name} from {before.guild} is now listening to {after.activity.title}",
                            colour=discord.Colour.green(),
                        )
                        listeningEmbedded.add_field(name="Started:",
                                                    value=after.activity.start)
                        listeningEmbedded.add_field(name="Duration",
                                                    value=after.activity.duration)
                        listeningEmbedded.add_field(
                            name="Artist:", value=after.activity.artist.title())
                        listeningEmbedded.add_field(name="Album",
                                                    value=after.activity.album)
                        listeningEmbedded.set_footer(
                            text=f"Activity Update Detector Service <{st}>")
                        listeningEmbedded.set_image(
                            url=after.activity.album_cover_url)
                        try:
                            await self.member_update_channel.send(embed=listeningEmbedded)
                        except AttributeError:
                            pass
                    elif after.activity.type == discord.ActivityType.watching:
                        watchingEmbedded = discord.Embed(
                            title="Activity Update Detector Service",
                            description=f"{before.name} from {before.guild} is now watching {after.activity.name}",
                            colour=discord.Colour.orange(),
                        )
                        watchingEmbedded.add_field(name="Details:",
                                                   value=after.activity.details)
                        watchingEmbedded.set_footer(
                            text=f"Activity Update Detector Service <{st}>")
                        try:
                            await self.member_update_channel.send(embed=watchingEmbedded)
                        except AttributeError:
                            pass
                    elif after.activity.type == discord.ActivityType.custom:
                        customEmbedded = discord.Embed(
                            title="Custom Status Update Detector Service",
                            description=f"{before.name} from {before.guild} changed/added custom status to ```{after.activity.name}```",
                            colour=discord.Colour.blue(),
                        )
                        customEmbedded.set_footer(text=f"{st}")
                        try:
                            await self.member_update_channel.send(embed=customEmbedded)
                        except AttributeError:
                            pass
                    elif after.activity.type is None:
                        pass
            elif before.display_name != after.display_name:
                Embedded = discord.Embed(
                    title="Name Update Detector Service",
                    description=f"{before.name} was renamed from {before.display_name} to {after.display_name} at {before.guild} ",
                    colour=discord.Colour.green(),
                )
                Embedded.set_footer(text=st)
                try:
                    await self.member_update_channel.send(embed=Embedded)
                except AttributeError:
                    pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.name != after.name:
            embed = discord.Embed(
                title=f"At {before.name}",
                description=f"Guild name changed from {before.name} to {after.name}",
                colour=discord.Colour(0x5032A8),
            )
            embed.set_footer(text="Guild update service")
            try:
                await self.guild_update_channel.send(embed=embed)
            except AttributeError:
                pass
        elif before.emojis != after.emojis:
            embed = discord.Embed(
                title=f"At {before.name}",
                description=f"Added/removed {discord.Emoji.name} in {before.name} to {after.name}",
            )
            embed.set_footer(text="Guild update service")
            try:
                await self.guild_update_channel.send(embed=embed)
            except AttributeError:
                pass
        elif before.bans != after.bans:
            embed = discord.Embed(
                title=f"At {before.name}",
                description=f"Banned/Unbanned {before.user} in {before.name} to {after.name}",
            )
            embed.set_footer(text="Guild update service")
            try:
                await self.guild_update_channel.send(embed=embed)
            except AttributeError:
                pass
        elif before.region != after.region:
            embed = discord.Embed(
                title=f"At {before.name}",
                description=f"Changed region from {before.region} to {after.region} in {after.name}",
            )
            embed.set_footer(text="Guild update service")
            try:
                await self.guild_update_channel.send(embed=embed)
            except AttributeError:
                pass

def setup(bot):
    bot.add_cog(Spying(bot))
