from discord.ext import commands

import dbl


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc5OTEzNDk3NjUxNTM3NTE1NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE3MzQ0OTYyfQ.j5X0iCjjQtMd-PupQ186u2K8072RXNHdSiOU2eCIqyo'
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)  # Autopost will post your guild count every 30 minutes


def setup(bot):
    bot.add_cog(TopGG(bot))
