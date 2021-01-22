from discord.ext import commands
import requests
import discord

class API(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        pic = requests.get("https://aws.random.cat/meow").json()['file']
        embed = discord.Embed(title="Random Cat",Colour=discord.Colour.random())
        embed.set_image(url=pic)
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)
    @commands.command()
    async def dog(self, ctx, breed=None):
        if breed:
            picture_json = requests.get(f"https://dog.ceo/api/{breed}/image/random").json()
            if picture_json["status"] == "error":
                dogList = "\n".join(["affenpinscher","african","airedale","akita","appenzeller","shepherd australian","basenji","beagle","bluetick","borzoi","boxer","brabancon","briard","buhund-norwegian","bulldog-boston","bulldog-english","bulldog-french","bullterrier-staffordshire","cairn","cattledog-australian","chihuahua","chow"])
                Errorembed = discord.Embed(title="This breed is not available",color=discord.Color.random(),description=f"Select the following breeds:```{dogList}```")
                ctx.send(embed=Errorembed)
            else:
                pic = picture_json['message']
        else:
            pic = requests.get("https://random.dog/woof.json").json()['url']
        embed = discord.Embed(title="Random Dog",Colour=discord.Colour.random())
        embed.set_image(url=pic)
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)

    @commands.command()
    async def fox(self, ctx):
        pic = requests.get("https://randomfox.ca/floof/").json()['image']
        embed = discord.Embed(title="Random Fox",Colour=discord.Colour.random())
        embed.set_image(url=pic)
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)
    @commands.command()
    async def insult(self, ctx, lang="en"):
        params = {"lang":lang,"type":"json"}
        insult = requests.get("https://evilinsult.com/generate_insult.php",params=params).json()
        embed = discord.Embed(title=insult["insult"],Colour=discord.Colour.random())
        embed.set_footer(text=f"{lang} Insult Gen Service")
        await ctx.send(embed=embed)
    @commands.command(aliases=['bunny'])
    async def rabbit(self, ctx):
        pic = requests.get("https://api.bunnies.io/v2/loop/random/?media=gif,png").json()['media']['gif']
        embed = discord.Embed(title="Random Rabbit",Colour=discord.Colour.random())
        embed.set_image(url=pic)
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)
    @commands.command()
    async def duck(self, ctx):
        pic = requests.get("https://random-d.uk/api/v1/random?type=png").json()["url"]
        embed = discord.Embed(title="Random duck",Colour=discord.Colour.random())
        embed.set_image(url=pic)
        embed.set_footer(text="Animal Img Gen Service")
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(API(bot))
