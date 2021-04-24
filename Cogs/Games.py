from discord.ext import commands
import discord
import aiohttp
import asyncio
import re
import random
import sys
import traceback

class Board:
    def __init__(self, player1, player2):
        # Our board just needs to be a 3x3 grid. To keep formatting nice, each one is going to be a space to start
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

        # Randomize who goes first when the board is created
        if random.SystemRandom().randint(0, 1):
            self.challengers = {"x": player1, "o": player2}
        else:
            self.challengers = {"x": player2, "o": player1}

        # X's always go first
        self.X_turn = True

    def full(self):
        # For this check we just need to see if there is a space anywhere, if there is then we're not full
        for row in self.board:
            if " " in row:
                return False
        return True

    def can_play(self, player):
        # Simple check to see if the player is the one that's up
        if self.X_turn:
            return player == self.challengers["x"]
        else:
            return player == self.challengers["o"]

    def update(self, x, y):
        # If it's x's turn, we place an x, otherwise place an o
        letter = "x" if self.X_turn else "o"
        # Make sure the place we're trying to update is blank, we can't override something
        if self.board[x][y] == " ":
            self.board[x][y] = letter
        else:
            return False
        # If we were succesful in placing the piece, we need to switch whose turn it is
        self.X_turn = not self.X_turn
        return True

    def check(self):
        # Checking all possiblities will be fun...
        # First base off the top-left corner, see if any possiblities with that match
        # We need to also make sure that the place is not blank, so that 3 in a row that are blank doesn't cause a 'win'
        # Top-left, top-middle, top right
        if (
            self.board[0][0] == self.board[0][1]
            and self.board[0][0] == self.board[0][2]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]
        # Top-left, middle-left, bottom-left
        if (
            self.board[0][0] == self.board[1][0]
            and self.board[0][0] == self.board[2][0]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]
        # Top-left, middle, bottom-right
        if (
            self.board[0][0] == self.board[1][1]
            and self.board[0][0] == self.board[2][2]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]

        # Next check the top-right corner, not re-checking the last possiblity that included it
        # Top-right, middle-right, bottom-right
        if (
            self.board[0][2] == self.board[1][2]
            and self.board[0][2] == self.board[2][2]
            and self.board[0][2] != " "
        ):
            return self.challengers[self.board[0][2]]
        # Top-right, middle, bottom-left
        if (
            self.board[0][2] == self.board[1][1]
            and self.board[0][2] == self.board[2][0]
            and self.board[0][2] != " "
        ):
            return self.challengers[self.board[0][2]]

        # Next up, bottom-right corner, only one possiblity to check here, other two have been checked
        # Bottom-right, bottom-middle, bottom-left
        if (
            self.board[2][2] == self.board[2][1]
            and self.board[2][2] == self.board[2][0]
            and self.board[2][2] != " "
        ):
            return self.challengers[self.board[2][2]]

        # No need to check the bottom-left, all posiblities have been checked now
        # Base things off the middle now, as we only need the two 'middle' possiblites that aren't diagonal
        # Top-middle, middle, bottom-middle
        if (
            self.board[1][1] == self.board[0][1]
            and self.board[1][1] == self.board[2][1]
            and self.board[1][1] != " "
        ):
            return self.challengers[self.board[1][1]]
        # Left-middle, middle, right-middle
        if (
            self.board[1][1] == self.board[1][0]
            and self.board[1][1] == self.board[1][2]
            and self.board[1][1] != " "
        ):
            return self.challengers[self.board[1][1]]

        # Otherwise nothing has been found, return None
        return None

    def __str__(self):
        # Simple formatting here when you look at it, enough spaces to even out where everything is
        # Place whatever is at the grid in place, whether it's x, o, or blank
        _board = " {}  |  {}  |  {}\n".format(
            self.board[0][0], self.board[0][1], self.board[0][2]
        )
        _board += "———————————————\n"
        _board += " {}  |  {}  |  {}\n".format(
            self.board[1][0], self.board[1][1], self.board[1][2]
        )
        _board += "———————————————\n"
        _board += " {}  |  {}  |  {}\n".format(
            self.board[2][0], self.board[2][1], self.board[2][2]
        )
        return "```\n{}```".format(_board)

class Hangman():
    def __init__(self, userID, list):
        self.userID = userID
        self.token = None
        self.hangman = None
        self.stages = iter(list)
        self.stage = next(self.stages)
        self.has_ended = False
        self.has_won = False
    async def start_hangman(self):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://hangman-api.herokuapp.com/hangman") as response:
                HangmanGame = await response.json()
                self.hangman = HangmanGame.get("hangman")
                self.token = HangmanGame.get("token")
                #start hangman game
    async def guess_hangman(self, letter: str):
        async with aiohttp.ClientSession() as session:
            async with session.put("https://hangman-api.herokuapp.com/hangman",params={"token": self.token, "letter": letter }) as response:
                if response.status == 304:
                    return "Already tried that letter"
                try:
                    status = response.status
                    HangmanGame = await response.json()
                    self.hangman = HangmanGame.get("hangman")
                    self.token = HangmanGame.get("token")
                    if response.get('correct'):
                        if self.has_won():
                            self.has_won = True
                            self.has_ended = True
                            return True
                        else:
                            return True
                    else:
                        try:
                            self.stage = next(self.stages)
                            return False
                        except StopIteration:
                            self.has_ended = True
                            return False
                except AttributeError:
                    return
                    #guess the letter in the hangman game
    async def hint_hangman(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://hangman-api.herokuapp.com/hangman/hint",params={"token": self.token }) as response:
                HangmanGame = await response.json()
                HangmanHint = HangmanGame.get("hint")
                self.token = HangmanGame.get("token")
                return HangmanHint
                #give hints

    async def solution_hangman(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://hangman-api.herokuapp.com/hangman",params={"token": self.token }) as response:
                HangmanGame = await response.json()
                HangmanSolution = HangmanGame.get("solution")
                self.token = HangmanGame.get("token")
                return HangmanSolution
    async def has_won(self):
        if self.has_won and self.hangman_game == await solution_hangman():
            return True
        else:
            return False
class Games(commands.Cog):
    """Pretty self-explanatory"""

    boards = {}
    def __init__(self, bot):
        self.bot = bot
        self.hangman_games = {}
    def create(self, server_id, player1, player2):
        self.boards[server_id] = Board(player1, player2)

        # Return whoever is x's so that we know who is going first
        return self.boards[server_id].challengers["x"]
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            try:
                return await ctx.send(
                    embed=discord.Embed(description=f"Oops! Missing {error.param.name}, try run help on the command.")
                )
            except discord.HTTPException:
                pass
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )
    @commands.group(aliases=["tic", "tac", "toe"], invoke_without_command=True)
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    async def tictactoe(self, ctx, *, option: str):
        """Updates the current server's tic-tac-toe board
        You obviously need to be one of the players to use this
        It also needs to be your turn
        Provide top, left, bottom, right, middle as you want to mark where to play on the board

        EXAMPLE: ~tictactoe middle top
        RESULT: Your piece is placed in the very top space, in the middle"""
        player = ctx.message.author
        board = self.boards.get(ctx.message.guild.id)
        # Need to make sure the board exists before allowing someone to play
        if not board:
            await ctx.send(embed=discord.Embed(title="There are currently no Tic-Tac-Toe games setup!"))
            return
        # Now just make sure the person can play, this will fail if o's are up and x tries to play
        # Or if someone else entirely tries to play
        if not board.can_play(player):
            await ctx.send(embed=discord.Embed(title="You cannot play right now!"))
            return

        # Search for the positions in the option given, the actual match doesn't matter, just need to check if it exists
        top = re.search("top", option)
        middle = re.search("middle", option)
        bottom = re.search("bottom", option)
        left = re.search("left", option)
        right = re.search("right", option)

        # Just a bit of logic to ensure nothing that doesn't make sense is given
        if top and bottom:
            await ctx.send(embed=discord.Embed(title="That is not a valid location! Use some logic, come on!"))
            return
        if left and right:
            await ctx.send(embed=discord.Embed(title="That is not a valid location! Use some logic, come on!"))
            return
        # Make sure at least something was given
        if not top and not bottom and not left and not right and not middle:
            await ctx.send(embed=discord.Embed(title="Please provide a valid location to play!"))
            return

        x = 0
        y = 0
        # Simple assignments
        if top:
            x = 0
        if bottom:
            x = 2
        if left:
            y = 0
        if right:
            y = 2
        # If middle was given and nothing else, we need the exact middle
        if middle and not (top or bottom or left or right):
            x = 1
            y = 1
        # If just top or bottom was given, we assume this means top-middle or bottom-middle
        # We don't need to do anything fancy with top/bottom as it's already assigned, just assign middle
        if (top or bottom) and not (left or right):
            y = 1
        # If just left or right was given, we assume this means left-middle or right-middle
        # We don't need to do anything fancy with left/right as it's already assigned, just assign middle
        elif (left or right) and not (top or bottom):
            x = 1

        # If all checks have been made, x and y should now be defined
        # Correctly based on the matches, and we can go ahead and update the board
        # We've already checked if the author can play, so there's no need to make any additional checks here
        # board.update will handle which letter is placed
        # If it returns false however, then someone has already played in that spot and nothing was updated
        if not board.update(x, y):
            await ctx.send(embed=discord.Embed(title="Someone has already played there!"))
            return
        # Next check if there's a winner
        winner = board.check()
        if winner:
            # Get the loser based on whether or not the winner is x's
            # If the winner is x's, the loser is o's...obviously, and vice-versa
            loser = (
                board.challengers["x"]
                if board.challengers["x"] != winner
                else board.challengers["o"]
            )
            await ctx.send(embed=discord.Embed(description="{} has won this game of TicTacToe, better luck next time {}".format(winner.mention, loser.mention)))
            # This game has ended, delete it so another one can be made
            try:
                del self.boards[ctx.message.guild.id]
            except KeyError:
                pass
        else:
            # If no one has won, make sure the game is not full. If it has, delete the board and say it was a tie
            if board.full():
                await ctx.send(embed=discord.Embed(title="This game has ended in a tie!"))
                try:
                    del self.boards[ctx.message.guild.id]
                except KeyError:
                    pass
            # If no one has won, and the game has not ended in a tie, print the new updated board
            else:
                player_turn = (
                    board.challengers.get("x")
                    if board.X_turn
                    else board.challengers.get("o")
                )
                fmt = str(board) + "\n***{} It is now your turn to play!***".format(
                    player_turn.mention
                )
                await ctx.send(embed=discord.Embed(description=fmt))

    @tictactoe.command(name="start", aliases=["challenge", "create"])
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    async def start_tictactoe(self, ctx, player2: discord.Member):
        """Starts a game of tictactoe with another player\nEXAMPLE: ~tictactoe start @OtherPerson\nRESULT: A new game of tictactoe"""
        player1 = ctx.message.author
        # For simplicities sake, only allow one game on a server at a time.
        # Things can easily get confusing (on the server's end) if we allow more than one
        if self.boards.get(ctx.message.guild.id) is not None:
            await ctx.send(embed=discord.Embed(title="Sorry but only one Tic-Tac-Toe game can be running per server!"))
            return
        # Make sure we're not being challenged, I always win anyway
        if player2 == ctx.message.guild.m:
            await ctx.send(embed=discord.Embed(title="You want to play? Alright lets play.\n\nI win, so quick you didn't even notice it."))
            return
        if player2 == player1:
            await ctx.send(embed=discord.Embed(title="You can't play yourself, I won't allow it. Go find some friends"))
            return

        # Create the board and return who has been decided to go first
        x_player = self.create(ctx.message.guild.id, player1, player2)
        fmt = "A tictactoe game has just started between {} and {}\n".format(
            player1.mention, player2.mention
        )
        # Print the board too just because
        fmt += str(self.boards[ctx.message.guild.id])

        # We don't need to do anything weird with assigning x_player to something
        # it is already a member object, just use it
        fmt += (
            "I have decided at random, and {} is going to be `x` this game. It is your turn first! "
            "Use the {}tictactoe command, and a position, to choose where you want to play".format(
                x_player.mention, ctx.prefix
            )
        )
        await ctx.send(embed=discord.Embed(description=fmt))

    @tictactoe.command(name="delete", aliases=["stop", "remove", "end"])
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    async def stop_tictactoe(self, ctx):
        """Force stops a game of tictactoe
        This should realistically only be used in a situation like one player leaves
        Hopefully a moderator will not abuse it, but there's not much we can do to avoid that

        EXAMPLE: ~tictactoe stop
        RESULT: No more tictactoe!"""
        if self.boards.get(ctx.message.guild.id) is None:
            await ctx.send(embed=discord.Embed(title="There are no tictactoe games running on this server!"))
            return

        del self.boards[ctx.message.guild.id]
        await ctx.send(embed=discord.Embed(title="I have just stopped the game of TicTacToe, a new should be able to be started now!"))

    @commands.group()
    @commands.bot_has_permissions(send_messages=True)
    async def hangman(self, ctx):
        Stages = [
"""```
-------------
|
|
|
|
--------------------------```""",
"""```
-------------
|           |
|
|
|
|
--------------------------```""",
"""```
-------------
|           |
|           O
|
|
|
--------------------------```""",
"""```
-------------
|           |
|           O
|           |
|
|
--------------------------```""",
"""```
-------------
|           |
|           O
|          /|
|
|
--------------------------```""",
"""```
-------------
|           |
|           O
|          /|\\
|
|
--------------------------```""",
"""```
-------------
|           |
|           O
|          /|\\
|          /
|
--------------------------```""",
"""```
-------------
|           |
|           O
|          /|\\
|          / \\
|
--------------------------```"""]
        if not self.hangman_games.get(ctx.author.id):
            self.hangman_games[ctx.author.id] = Hangman(ctx.author.id,Stages)

    @hangman.command()
    @commands.bot_has_permissions(send_messages=True)
    async def start(self, ctx):
        hangman_game = self.hangman_games.get(ctx.author.id)
        await hangman_game.start_hangman()
        e = discord.Embed(title=hangman_game.hangman,description=hangman_game.stage)
        await ctx.send(embed=e)

    @hangman.command()
    @commands.bot_has_permissions(send_messages=True)
    async def guess(self, ctx, *, letter):
        hangman_game = self.hangman_games.get(ctx.author.id)
        x = len(letter)
        if x != 1:
            return await ctx.send("Please enter only 1 letter")
        guess = await hangman_game.guess_hangman(letter)
        if guess == "Already tried that letter":
            return await ctx.send("Already tried that!")
        if not guess:
            if hangman_game.has_ended:
                del self.hangman_games[ctx.author.id]
                embed = discord.Embed(description=hangman_game.stage)
                embed.set_author(name=hangman_game.hangman)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=hangman_game.stage)
                embed.set_author(name=hangman_game.hangman)
                embed.set_footer(text="Wrong guess!")
                await ctx.send(embed=embed)
        else:
            if hangman_game.has_ended:
                del self.hangman_games[ctx.author.id]
                if hangman_game.has_won:
                    await ctx.send("You Win!")
                    embed = discord.Embed(description=hangman_game.stage)
                    embed.set_author(name=hangman_game.hangman)
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=hangman_game.stage)
                embed.set_author(name=hangman_game.hangman)
                embed.set_footer(text="Correct guess!")
                await ctx.send(embed=embed)

    @hangman.command()
    async def hint(self, ctx):
        hangman_game = self.hangman_games.get(ctx.author.id)
        hint = await hangman_game.hint_hangman()
        await ctx.send(hint)

    @hangman.command()
    async def solution(self, ctx):
        hangman_game = self.hangman_games.get(ctx.author.id)
        solution = await hangman_game.solution_hangman()
        await ctx.send(solution)
        del self.hangman_games[ctx.author.id]
def setup(bot):
    bot.add_cog(Games(bot))