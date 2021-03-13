from discord.ext import commands
import discord
import chess

class ChessGame():
    def __init__(self, id):
        self.board = chess.Board()
        self.id = id
        self.player2 = None
    def make_move(self, move: str):
        return self.board.push_san(move)

    def check_checkmate(self):
        return self.board.is_checkmate()

class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
    def get_chess_game(self, context: commands.Context):
        userid = context.author.id
        try:
            Chess_game = self.games[userid]
        except KeyError:
            Chess_game = ChessGame(userid)
            self.games[userid] = Chess_game
        return Chess_game
    @commands.command(aliases=["chess"])
    async def chess(self, ctx, Player2: discord.Member):
        """Starts a chess game"""
        game = self.get_chess_game(ctx)
        game.player2 = Player2
        await ctx.send(embed=discord.Embed(title=f"{ctx.author} VS {Player2}", description=f"```{game.board}```",footer=f"{game.id}"))
    @commands.command(aliases=["move"])
    async def move(self, ctx, move: str):
        """Move chess pieces on the board"""
        game = self.get_chess_game(ctx)
        try:
            game.make_move(move)
        except ValueError:
            return await ctx.send(embed=discord.Embed(title="Illegal move!", description=f"```{game.board.legal_moves}```"))
        await ctx.send(embed=discord.Embed(title=f"{ctx.author} VS {game.player2}", description=f"```{game.board}```",footer=f"{game.id}"))
def setup(bot):
    bot.add_cog(Chess(bot))
