from discord.ext import commands, menus
import random
import discord
import yaml
import asyncio
import os
from discord.ext.commands.cooldowns import BucketType
from asyncdagpi import Client
import math
from bs4 import BeautifulSoup
from typing import Union
import aiohttp
from Cogs.Music import Paginator
import random
class Fun(
    commands.Cog, description="Fun commands such as love calculator, 'Guess that pokemon!' and coin flips"
):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi = Client("ta1fnmIgn85mcfz32UG5nKgVeRWikmaZxZa392f0XwWC4yaDCOGUYPWscbZ5ULbk")
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(embed=discord.Embed(description="Woah slow down there! Finish your game first!"))
    @commands.command(hidden=True)
    async def jason(self, ctx):
        await ctx.message.delete()
        embed1 = "https://cdn.discordapp.com/attachments/263190635434082315/803952123237761024/Jason_hanging_out_on_a_swing.jpg"
        embed2 = "https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed3 = "https://cdn.discordapp.com/attachments/263190635434082315/803956006764937236/IMG_20190812_195149.jpg"
        embed = discord.Embed(title="Surpirse!", colour=discord.Colour.blue())
        embed.set_image(url=random.choice([embed1, embed2, embed3]))
        await ctx.send(embed=embed, delete_after=5)

    @commands.command()
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author
        if user.id == 801271445304246323:
            return await ctx.send(f"**{user.name}** is **100%** hot 💞")
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

    async def hints(self, ctx: commands.Context, embed: discord.Embed, obj, message, theme, hints):
        count = 1
        await ctx.send("Wrong answer, you have 3 guesses left!",delete_after=5)
        for i in hints:
            embed.add_field(name=i[0], value=f"{i[1]}")
            await message.edit(embed=embed)
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author
            try:
                guess = await self.bot.wait_for('message',check=check,timeout=15)
            except asyncio.TimeoutError:
                embed = discord.Embed(title="You didnt guess it on time :(")
                embed.set_image(url=obj.answer)
                return await ctx.send(embed=embed)
            if guess.content.title() == obj.name:
                return await guess.add_reaction("\N{White Heavy Check Mark}")
            else:
                guesses_left = len(hints)-count
                if guesses_left == 1:
                    await ctx.send(f"Wrong {theme}, {guesses_left} guess remaining!",delete_after=5)
                if guesses_left<1:
                    pass
                else:
                    await ctx.send(f"Wrong {theme}, {guesses_left} guesses remaining!",delete_after=5)
                count+=1
        else:
            embed = discord.Embed(title="You didnt guess it right! :(")
            embed.set_image(url=obj.answer)
            return await ctx.send(embed=embed)

    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    @commands.command(aliases=['wtp'])
    async def poke(self, ctx):
        """Starts a pokemon guessing game!"""
        pokemon = await self.dagpi.wtp()
        embed = discord.Embed(title=f"Hey {ctx.author.name}, Guess that Pokemon!")
        embed.set_image(url=pokemon.question)
        message = await ctx.send(embed=embed)
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            guess = await self.bot.wait_for('message',check=check,timeout=30)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="You didnt guess it on time :(")
            embed.set_image(url=pokemon.answer)
            return await ctx.send(embed=embed)
        if guess.content.title() == pokemon.name:
            return await guess.add_reaction("\N{White Heavy Check Mark}")
        else:
            await self.hints(ctx, embed, pokemon, message, "Pokemon", [["Type", ",".join(pokemon.dict["Data"]["Type"])],["Abilities",",".join(pokemon.abilities)], ["weight",pokemon.weight]])
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    @commands.command()
    async def logo(self, ctx):
        """Guess the logo"""
        logo = await self.dagpi.logo()
        embed = discord.Embed(title=f"Hey {ctx.author.name}, Guess that Logo!", description=f"```{logo.hint}```")
        embed.set_image(url=logo.question)
        message = await ctx.send(embed=embed)
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            guess = await self.bot.wait_for('message',check=check,timeout=30)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="You didnt guess it on time :(")
            embed.set_image(url=logo.answer)
            return await ctx.send(embed=embed)
        if guess.content.lower() == logo.brand.lower():
            return await guess.add_reaction("\N{White Heavy Check Mark}")
        else:
            embed = discord.Embed(title="You didnt guess it right! :(",description=f"```{logo.brand}```")
            embed.set_image(url=logo.answer)
            return await ctx.send(embed=embed)
    @commands.command()
    async def pickup(self, ctx):
        """Get a pickup line to pickup girls!"""
        pickup = await self.dagpi.pickup_line()
        embed = discord.Embed(title=pickup.line)
        embed.set_footer(text=f"Category: {pickup.category}")
        await ctx.send(embed=embed)
    @commands.command()
    async def fact(self, ctx):
        """Get a random fun fact"""
        fact = await self.dagpi.fact()
        embed = discord.Embed(title=fact)
        await ctx.send(embed=embed)
    @commands.command()
    async def joke(self, ctx):
        """Get a random joke for fun!"""
        joke = await self.dagpi.joke()
        embed = discord.Embed(title=joke)
        await ctx.send(embed=embed)
    @commands.command()
    async def roast(self, ctx):
        """Get a random joke for fun!"""
        roast = await self.dagpi.roast()
        embed = discord.Embed(title=roast)
        await ctx.send(embed=embed)
    @commands.command()
    async def yomama(self, ctx):
        """Get a Yo mama joke"""
        yomama = await self.dagpi.yomama()
        embed = discord.Embed(title=yomama)
        await ctx.send(embed=embed)
    @commands.command(aliases=["lovecalc"])
    async def lovecalculator(
        self, ctx: commands.Context, lover: Union[discord.Member,str], loved: Union[discord.Member,str]
    ):
        """Calculate the love percentage!"""
        if isinstance(lover, discord.Member):
            x = lover.display_name
        else:
            x = lover
        if isinstance(loved, discord.Member):
            y = loved.display_name
        else:
            y = loved
        url = "https://www.lovecalculator.com/love.php?name1={}&name2={}".format(
            x.replace(" ", "+"), y.replace(" ", "+")
        )
        async with aiohttp.ClientSession(headers={"Connection": "keep-alive"}) as session:
            async with session.get(url, ssl=False) as response:
                resp = await response.text()
        soup_object = BeautifulSoup(resp, "html.parser")

        description = soup_object.find("div", class_="result__score").get_text()

        if description is None:
            description = "Dr. Love is busy right now"
        else:
            description = description.strip()

        result_image = soup_object.find("img", class_="result__image").get("src")

        result_text = soup_object.find("div", class_="result-text").get_text()
        result_text = " ".join(result_text.split())

        try:
            z = description[:2]
            z = int(z)
            if z > 50:
                emoji = "❤"
            else:
                emoji = "💔"
            title = f"Dr. Love says that the love percentage for {x} and {y} is: {emoji} {description} {emoji}"
        except (TypeError, ValueError):
            title = "Dr. Love has left a note for you."

        em = discord.Embed(
            title=title, description=result_text, color=discord.Color.red(), url=url
        )
        em.set_image(url=f"https://www.lovecalculator.com/{result_image}")
        await ctx.send(embed=em)
    @commands.command()
    async def penis(self, ctx, *users: discord.Member):
       """Detects user's penis length
       This is 100% accurate.
       Enter multiple users for an accurate comparison!"""

       dongs = {}
       msg = ""
       state = random.getstate()

       for user in users:
           random.seed(user.id)
           dongs[user] = "8{}D".format("=" * random.randint(0, 30))

       random.setstate(state)
       dongs = sorted(dongs.items(), key=lambda x: x[1])

       for user, dong in dongs:
           msg += "**{}'s size:**\n{}\n".format(user.display_name, dong)

       Page = menus.MenuPages(Paginator(ctx, dongs, "Requested PP sizes", "PP size generator", 1), clear_reactions_after=True)
       await Page.start(ctx)
    @commands.command(hidden=True)
    async def kushal(self, ctx):
        await ctx.send("🗑️")
    @commands.command()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def xkcd(self, ctx, *, entry_number=None):
      """Post a random xkcd comic or post an xkcd with the number provided!"""

      # Creates random number between 0 and 2190 (number of xkcd comics at time of writing) and queries xkcd
      headers = {"content-type": "application/json"}
      url = "https://xkcd.com/info.0.json"
      async with aiohttp.ClientSession() as session:
          async with session.get(url, headers=headers) as response:
              xkcd_latest = await response.json()
              xkcd_max = xkcd_latest.get("num") + 1

      if entry_number is not None and int(entry_number) > 0 and int(entry_number) < xkcd_max:
          i = int(entry_number)
      else:
          i = random.randint(0, xkcd_max)
      headers = {"content-type": "application/json"}
      url = "https://xkcd.com/" + str(i) + "/info.0.json"
      async with aiohttp.ClientSession() as session:
          async with session.get(url, headers=headers) as response:
              xkcd = await response.json()

      # Build Embed
      embed = discord.Embed()
      embed.title = xkcd["title"] + " (" + xkcd["day"] + "/" + xkcd["month"] + "/" + xkcd["year"] + ")"
      embed.url = "https://xkcd.com/" + str(i)
      embed.description = xkcd["alt"]
      embed.set_image(url=xkcd["img"])
      await ctx.send(embed=embed)

    @commands.command()
    async def claptrap(self, ctx):
        """Can I shoot something now? Or climb some stairs? SOMETHING exciting?"""
        claptraps = [
            "Hey everybody! Check out my package!",
            "Let's get this party started!",
            "Glitching weirdness is a term of endearment, right?",
            "Recompiling my combat code!",
            "This time it'll be awesome, I promise!",
            "Look out everybody! Things are about to get awesome!",
            "Health! Eww, what flavor is red?",
            "Health over here!",
            "Sweet life juice!",
            "I found health!",
            "Healsies!",
            "Where'd all my bullets go?",
            "Bullets are dumb.",
            "Who needs ammo anyway, am I right?",
            "I need tiny death pellets!",
            "Need some ammo!",
            "Dangit, I'm out!",
            "Ammo reserves are spent!",
            "Crap, no more shots left!",
            "Hnngh! Empty!",
            "Coming up empty!",
            "Wheeeee!",
            "Yahooooo!",
            "Aaaaaaahhh!",
            "Watch as we observe the rare and beautiful Clappy Bird!",
            "I'm flying! I'm really flying!",
            "Look out below!",
            "Yipe!",
            "Yikes!",
            "Yeehaw!",
            "Hyah!",
            "Heyyah!",
            "Take that!",
            "Bop!",
            "Badass!",
            "Badass?! Aaahhh!",
            "Look out, a Badass!",
            "RUN FOR YOUR LIIIIIVES!!!",
            "Oh, he's big... REALLY big!",
            "Scary Badass dude, over there!",
            "Oh no, Badass!",
            "Save me from the Badass!",
            "Psst! Ad-ass-bay, over ere-bay!",
            "That guy looks an awful lot like a Badass!",
            "Step right up, to the Bulletnator 9000!",
            "I am a tornado of death and bullets!",
            "Stop me before I kill again, except don't!",
            "Hehehehe, mwaa ha ha ha, MWAA HA HA HA!",
            "I'm on a roll!",
            "Unts unts unts unts!",
            "Ha ha ha! Fall before your robot overlord!",
            "Can't touch this!",
            "Ha! Keep 'em coming!",
            "There is no way this ends badly!",
            "This is why I was built!",
            "You call yourself a badass?",
            "Wow, did I really do that?",
            "Is it dead? Can, can I open my eyes now?",
            "I didn't panic! Nope, not me!",
            "Not so tough after all!",
            "One down, any other takers?",
            "I have gaskets tougher than you!",
            "That was me! I did that!",
            "Like running over a bug!",
            "That was a close one!",
            "Don't tell me *that* wasn't awesome!",
            "Ha ha ha! Suck it!",
            "Wait, did I really do that?",
            "Holy moly!",
            "'Nade out!",
            "Grenade!",
            "Grenaaaade!",
            "Hot potato!",
            "Pull pin, throw!",
            "Take that!",
            "Throwing grenade!",
            "Bad guy go boom!",
            "Eat bomb, baddie!",
            "Present for you!",
            "Aww! Now I want a snow cone.",
            "Take a chill pill!",
            "Cryo me a river!",
            "Freeze! I don't know why I said that.",
            "Don't cryo!",
            "Frigid.",
            "Solid! Get it? As in... frozen?",
            "Icely done.",
            "You're a tiny glacier!",
            "Frozen and doh-zen.",
            "Freeze, in the reference of emotion!",
            "Freezy peezy!",
            "My assets... frozen!",
            "I can't feel my fingers! Gah! I don't have any fingers!",
            "Too cold... can't move!",
            "I am a robot popsicle!",
            "Brrh... So cold... brrh...",
            "Metal gears... frozen solid!",
            "*Why* do I even *feel* pain?!",
            "Why did they build me out of galvanized flesh?!",
            "Ow hohoho, that hurts! Yipes!",
            "My robotic flesh! AAHH!",
            "Yikes! Ohhoho!",
            "Woah! Oh! Jeez!",
            "If only my chassis... weren't made of recycled human body parts! Wahahaha!",
            "Pop pop!",
            "Crit-i-cal!",
            "*That* looks like it hurts!",
            "WOW! I hit 'em!",
            "Extra ouch!",
            "Shwing!",
            "Flesh fireworks!",
            "Oh, quit falling to pieces.",
            "Is that what people look like inside?",
            "Ooh, squishy bits!",
            "Meat confetti!",
            "Huh, robot's don't do that.",
            "Exploded!",
            "Eww! Cool.",
            "Heh heh heh, squishy bits!",
            "Disgusting. I love it!",
            "Personfetti.",
            "There is now gunk on my chassis.",
            "Oooh! Gigabits!",
            "Ooooh! Terrabits!",
            "Meatsplosion!",
            "This time it'll be awesome, I promise!",
            "Hey everybody, check out my package!",
            "Place your bets!",
            "Defragmenting!",
            "Recompiling my combat code!",
            "Running the sequencer!",
            "It's happening... it's *happening*!",
            "It's about to get magical!",
            "I'm pulling tricks outta my hat!",
            "You can't just program this level of excitement!",
            "What will he do next?",
            "Things are about to get awesome!",
            "Let's get this party started!",
            "Glitchy weirdness is term of endearment, right?",
            "Push this button, flip this dongle, voila! Help me!",
            "square the I, carry the 1... YES!",
            "Resequencing combat protocols!",
            "Look out everybody, things are about to get awesome!",
            "I have an IDEA!",
            "Round and around and around she goes!",
            "It's like a box of chocolates...",
            "Step right up to the sequence of Trapping!",
            "Hey everybody, check out my package!",
            "Loading combat packages!",
            "F to the R to the 4 to the G to the WHAAT!",
            "I'm a sexy dinosaur! Rawr!",
            "Oh god I can't stop!",
            "Don't ask me where this ammo's coming from!",
            "If I had veins, they'd be popping out right now!",
            "(unintelligible snarling)",
            "It's the only way to stop the voices!",
            "This was a *reeeally* bad idea!",
            "I AM ON FIRE!!! OH GOD, PUT ME OUT!!!",
            "I'm cloaking...",
            "Shoot him... he's the real one...",
            "I'm a robot ninja...",
            "I'm invisible!",
            "Mini-trap, pretend you're a Siren!",
            "Aww, I should've drawn tattoos on you!",
            "Burn them, my mini-phoenix!",
            "All burn before the mighty Siren-trap!",
            "Calm down!",
            "It's time to *phase* you suckers out!",
            "Tell me I'm the prettiest!",
            "Hack the planet!",
            "Activating good cop mode...",
            "To the skies, mini-trap!",
            "Fly mini-trap! Fly!",
            "I have *two* robot arms!",
            "Punch 'em in the face, mini-trap!",
            "Anarchy and mini-trap and awesomeness, oh my!",
            "Ratattattattatta! Powpowpowpow! Powpowpowpow! Pew-pew, pew-pew-pewpew!",
            "Score one for the turret-trap!",
            "Mini-trap on the field!",
            "100% more mini-trap turret!",
            "I'm going commando!",
            "Boiyoiyoiyoiyoing!",
            "Zing! Bullet reflection!",
            "I am rubber, and you are *so* dead!",
            "I'm a superball!",
            "Trouncy, flouncy... founcy... those aren't words.",
            "For you...I commit...seddoku...",
            "The robot is dead, long live the robot!",
            "Go on without me!",
            "Don't forget me!",
            "Love bullets!",
            "Never fear, sugar!",
            "Nurse Clap is here!",
            "Poof, all better, doll!",
            "Sugar, this won't hurt a bit!",
            "Take these, gorgeous, you'll feel better!",
            "Some days, you just can't get rid of an obscure pop-culture reference.",
            "Here, take this!",
            "Oh darn, oh boy, oh crap, oh boy, oh darn.",
            "Gotta blow up a bad guy, GOTTA BLOW UP A BAD GUY!",
            "Uh, how do I cast magic missile?",
            "Do *not* look behind my curtain!",
            "I'm made of magic!",
            "You can call me Gundalf!",
            "Avada kedavra!",
            "Kill, reload! *Kill, reload!* *KILL! RELOAD!*",
            "Like those guys who made only one song ever.",
            "All these bullets in just one shot.",
            "One shot, make it count!",
            "A whole lotta bullets in just one trigger pull!",
            "Boogie time!",
            "Laaasers! ",
            "Psychedelic, man! ",
            "One for you, one for you, one for you!",
            "It's time for my free grenade giveaway!",
            "How many ways can I say... THROWING GRENADE?!",
            "Grenade confetti!",
            "I brought you a present: EXPLOSIONS!",
            "Avast ye scurvy dogs!",
            "Is this really canon?",
            "Time to get swabby!",
            "I feel a joke about poop decks coming on!",
            "Hard to port whine!",
            "I'll stop talking when I'm dead!",
            "I'll die the way I lived: annoying!",
            "Come back here! I'll gnaw your legs off!",
            "This could've gone better!",
            "You look like something a skag barfed up!",
            "What's that smell? Oh wait, it's just *you*!",
            "Yo momma's *so* dumb, she couldn't think of a good ending for this 'yo momma' joke!",
            "You're one screw short of a screw!",
            "I bet your mom could do better!",
            "You look like something a skag barfed up!",
            "Oh yeah? Well, uh... yeah.",
            "What is that smell? Oh, never mind... it's just you!",
            "I'm leaking!",
            "Good thing I don't have a soul!",
            "Aww!",
            "Aww! Come on!",
            "You can't kill me!",
            "I'm too pretty to die!",
            "Crap!",
            "Robot down!",
            "No, nononono NO!",
            "I'll never go back to the bad place!",
            "I have many regrets!",
            "Can I just say... yeehaw.",
            "You are ace high!",
            "You're the wub to my dub!",
            "Hahaha... I ascend!",
            "Ha ha ha! I LIVE! Hahaha!",
            "Hahahahaha! I'm alive!",
            "Good, I didn't want any spare parts!",
            "Wow, that actually worked?",
            "You can't keep a good 'bot down!",
            "I'm back! Woo!",
            "Holy crap, that worked?",
            "Better lucky than good!",
            "Back for more!",
            "Here we go again!",
            "So... does this make me your favorite?",
            "What are YOU doing down here?",
            "We're like those buddies in that one show!",
            "This is no time to be lazy!",
            "You can thank me later!",
            "You love me, right?",
            "You, me... keeping on... together?",
            "I will save you!",
            "Up you go!",
            "We're like those buddies in that one show!",
            "You versus me! Me versus you! Either way!",
            "I will prove to you my robotic superiority!",
            "Dance battle! Or, you know... regular battle.",
            "Man versus machine! Very tiny streamlined machine!",
            "Care to have a friendly duel?",
            "I can take ya! ... I think.",
            "Ow, what was that for?",
            "Oh, it's on now!",
            "You wanna fight with me?! Put 'em up! ... Put 'em up?",
            "A million baddies, and you wanna hit me? Aww!",
            "Now? But I... I just... okay...",
            "Aw yeah!",
            "Woohoo! In your face!",
            "Who's a badass robot? This guy!",
            "I am so impressed with myself!",
            "Ha ha, this is in no way surprising! Ha ha!",
            "NOOO!",
            "Poop.",
            "I'll get you next time!",
            "No fair! I wasn't ready.",
            "You got me!",
            "Argh arghargh death gurgle gurglegurgle urgh... death.",
            "Oh well.",
            "Crap happens.",
            "So, it's a draw, eh?",
            "Until we meet again on the battlefield, friendo!",
            "What? No way, I totally had you!",
            "Wow, who say that coming?",
            "Yay! We both win!",
            "Is this any good? 'Cause it looks awesome!",
            "Mine!",
            "I'm rich!",
            "Oooh, shiny!",
            "Phat loots!",
            "That is some sweet lookin' stuff!",
            "Check me out!",
            "Now I will dominate!",
            "I'm so sexy!",
            "Roadkill!",
            "I am NOT sorry!",
            "Did someone feel something?",
            "Don't bother with plastic surgery - there's NO fixing that!",
            "Does this thing have whindshield wipers?",
            "Uh... wasn't me!",
            "Did you scratch the paint?",
            "My bad?",
            "Speedbump much?",
            "Honk honk!",
            "Didn't see you there.",
            "Well, this is awkward.",
            "Sorry! Sorry!",
            "Oh crap.",
            "Get outta the way!",
            "Didn't see you there!",
            "Move please!",
            "Woah Nelly!",
            "Woah!",
            "Switch with me... uh, please?",
            "Let's switch!",
            "Can we change seats?",
            "Let me try!",
            "Change places!",
            "Shiela! Noooo!",
            "She's ready to blow!",
            "I don't know how much longer I can hold on!",
            "Is it warm in here, or is it just me?",
            "You have served me well, car.",
            "Shield me, maiden!",
            "Nice shield, maiden!",
            "Go get them Athena!",
            "That is *so* hot!",
            "I am right behind you, Vault Hunting friend!",
            "Nice minions!",
            "So, uh... what OS does your drone use?",
            "Annihilate them for breakfast, Willy!",
            "I can do that to! ... Sorta... Except not.",
            "Go Wilhelm and company!",
            "They're in for a moon of pain!",
            "Did you fire six shots, or five?",
            "You jerks have NO idea what you're in for!",
            "I'm so glad I'm not one of those guys right now!",
            "Sling those guns, girl!",
            "YOU! ARE! SCARY!",
            "Kill 'em, Nisha! Kill 'em dead!",
            "This is going to suck for those guys!",
            "Bringing down the law, painfully!",
            "Nice one, Jack!",
            "You really can double your fun!",
            "No WAY those guys will know who's who!",
            "That is in no way disturbing.",
            "Confused, then abused!",
            "That is SO cool!",
            "Ice see what you did there!",
            "Oh my gosh, a challenge!",
            "I did a challenge? I did a challenge!",
            "Glad I didn't mess that up.",
            "I feel... complete! ... That's weird.",
            "I actually did something right for once!",
            "This, or that...?",
            "What's the difference?",
            "Perhaps I should test one out first.",
            "Hmmm...",
            "Maybe this one?",
            "So many choices!",
            "What to install next?",
            "I must be a rogue, 'cause there are so many skills!",
            "Hmmm, the possibilities are an infinite recursion.",
            "Do any of these come with a new paint job?",
            "What else can I do?",
            "Skill-icious! Why did I just say that?",
            "Which of these gives me my free will back?",
            "Parallel and series!",
            "GPS calibrated.",
            "What's that arrow? Oh, wait! That's me!",
            "Um, where am I?",
            "Everything's upside down!",
            "Where to go next?",
            "Shaken, not stirred",
            "The moon is not enough!",
            "I'm Trap, Claptrap. Double oh... Trap.",
            "I expect you to die!",
            "I'd do anything for a woman with a gun.",
            "In yo' FACE!",
            "Get ready for some Fragtrap face time!",
            "Chk-chk, BOOM!",
            "You're listening to 'Short-Range Damage Radio.'",
            "Up close and personal.",
            "I'm a tornado of death and bullets!",
            "Get off my lawn!",
            "Back in my day...",
            "At least I still have my teeth!",
            "Coffee? Black... like my soul.",
            "Crazy young whippersnappers...",
            "Take two bullets, then call me in the morning.",
            "Now you're sorted!",
            "Snoiped!",
            "Crack shot!",
            "You're brown bread!",
            "So amazes with every guns!",
            "For I spy... somethin'.",
            "This is why you do your homework!",
            "Pain school is now in session",
            "Guess who?",
            "Meet professor punch!",
            "Ready for the PUNCHline?!",
            "Make my day.",
            "Gimme your best shot.",
            "Hit me, baby!",
            "Ya feeling lucky, punk?",
            "Enterrrrr the CHAMPION!",
            "Why do I feel radioactive!?",
            "Armor soak increased!",
            "Ladies looove a tough guy!",
            "Insert Juggernaut quote or pun here.",
            "I am Fire, I am Death!",
            "Burn, baby, burn!",
            "Remember, use caution near an open flame!",
            "Sizzlin'!",
            "Give me your princesses!",
            "Da, da da da! It's electric!",
            "I'm rubbing my wheel on the carpet!",
            "I've finally got an electric personality!",
            "Shocking, isn't it?",
            "Lightening! Kukachow!",
            "Zippity doodah!",
            "Wait, this isn't vegetable juice!",
            "Something eating you?",
            "Gammier than a pumpkin!",
            "Time to melt some faces.",
            "I'm a mean, green, acid machine!",
            "Sip-a-green! Zzzz!",
            "Know what killed the baddies? The *Ice* age.",
            "The ice-bot cometh.",
            "Ice to meet you.",
            "Lets kicksome ice.",
            "Ooh! Pretty!",
            "Things are exploded and... stuff.",
            "Take that! And that... and that...",
            "Now with extra kapow!",
            "Looks like some of my *awesome* rubbed off!",
            "Cool! Now we're both super-crazy-amazing!",
            "Take this in return!",
            "Here you go, chum!",
            "These are the best kind of cooties!",
            "Get away from me!",
            "Eww, get lost!",
            "Do I smell funny?",
            "Ah! Get 'em away!",
            "Scram!",
            "Do I smell funny?",
            "Coolant, vented!",
            "Welcome to the Jam!",
            "Ah... Much better!",
            "Smells like Pina Coladas!",
            "Frost exhaust!",
            "Hyperiooooon Punch!",
            "YES!",
            "Show me what you got",
            "Gloves are comin' off!",
            "Stinging like a butterfly!",
            "One, two... PUNCH!",
            "Punching time!",
            "Gloves are coming off!",
            "One, two punch",
            "Sting like a butterfly!",
            "Secret handshake!",
            "Up top!",
            "Gimme five!",
            "High five!",
            "Up top!",
            "We're best friends!",
            "Still counts!",
            "I'll take what I can get!",
            "Close enough!",
            "Better than nothing!",
            "(Dejected whistling.)",
            "I feel like an idiot now.",
            "Yeah! Single-player bonus!",
            "I must look *really* stupid right now!",
            "Aww, way to leave me hanging, friend.",
            "Don't you like me?",
            "(Sobbing) I just want to be loved!",
            "I'm a Pandoracorn's butthole!",
            "I fart rainbows!",
            "Bask in my aura of death!",
            "Did you guys see that?!",
            "Can I shoot something now? Or climb some stairs? SOMETHING exciting?",
            "Times like these, I really start to question the meaning of my existence. Then I get distra-hey! What's this? This looks cool!",
            "It would really stink if I couldn't control what I was thinking. Like, who wants to know that I'm thinking about cheese and lint, right?",
            "How does math work? Does this skin make me look fat? If a giraffe and a car had a baby, would it be called a caraffe? Life's big questions, man. ",
            "Who needs memories when I can do all this cool stuff? Stuff that I currently am not doing! That's what I'd like to call a 'hint'.",
            "Does this mean I can start dancing? Pleeeeeeaaaaase?",
            "Ya know when there was that Vault monster scare? I had these friends, and boy times sure were scary! But, I didn't care because I had friends, and they were like... super-friends! And then they left me, but they saved the world and I was like 'I know those guys!' Even though they never came back after that I still knew they cared, because no one had ever been... nice to me before. ... What is this? My eye is like... leaking.",
            "It's really quiet... and lonely... (hums briefly) Also this 'stopped moving' thing makes me uncomfortable. It gives me time to stop and think... literally. I'VE STOPPED, AND I'M THINKING! IT HURTS ME!",
            "Oh. My. God. What if I'm like... a fish? And, if I'm not moving... I stop breathing? AND THEN I'LL *DIE*! HELP ME! HELP MEEEEE HEE HEE HEEE! *HHHHHHHELP*!",
            "So, this one time, I went to a party, and there was a beautiful subatomic particle accelerator there. Our circuits locked across the room and... I don't remember what happened next. I mean, I can't. We coulda gotten married and had gadgets together, but now, I'll never know.",
            "I never got to play with guns when I was but a lad, but then ol' Jackie came along, and he was awful mad. 'I need a robot!' he declared, 'that can do my mighty deeds'. Then he saw me standing there, and a thought he did conceive. He told a way to make me rad, he gave me slots for guns, then he sent me on my way and wished me 'have some fun!' Now I'm here, a hired hand, amidst such death and chaos, waiting to be moved around, for my... I have no idea what rhymes with 'chaos'! I REGRET ALL OF THIS!",
            "Ahem, ahem. What's going on? Did I break something?",
            "Ready to go on where you are, friend. Adiamo!"
        ]
        await ctx.send(random.choice(claptraps))

def setup(bot):
    bot.add_cog(Fun(bot))
