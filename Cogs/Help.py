import discord
from discord.ext import commands
import itertools

class CustomHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        ctx = self.context
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        e.set_author(name=f"{ctx.bot.user.name} Help")
        e.set_footer(text=self.get_footer_note())
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)
    def get_opening_note(self):
            """Returns help command's opening note. This is mainly useful to override for i18n purposes.
            The default implementation returns ::
                Use `{prefix}{command_name} [command]` for more info on a command.
                You can also use `{prefix}{command_name} [category]` for more info on a category.
            Returns
            -------
            :class:`str`
                The help command opening note.
            """
            command_name = self.invoked_with
            return f"Remember you can get more information on a command using `{self.clean_prefix}{command_name} <name of command>`\nIf you're still lost you can join the [support server](https://discord.gg/YWb3AdW)."
    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        note = self.get_opening_note()
        if note:
            self.paginator.add_line(note, empty=True)

        no_category = '\u200b{0.no_category}'.format(self)
        def get_category(command, *, no_category=no_category):
            cog = command.cog
            return cog.qualified_name if cog is not None else no_category

        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
        to_iterate = itertools.groupby(filtered, key=get_category)

        for category, commands in to_iterate:
            commands = sorted(commands, key=lambda c: c.name) if self.sort_commands else list(commands)
            self.add_bot_commands_formatting(commands, category)

        note = self.get_ending_note()
        if note:
            self.paginator.add_line()
            self.paginator.add_line(note)

        await self.send_pages()
    def add_bot_commands_formatting(self, commands, heading):
            """Adds the minified bot heading with commands to the output.
            The formatting should be added to the :attr:`paginator`.
            The default implementation is a bold underline heading followed
            by commands separated by an EN SPACE (U+2002) in the next line.
            Parameters
            -----------
            commands: Sequence[:class:`Command`]
                A list of commands that belong to the heading.
            heading: :class:`str`
                The heading to add to the line.
            """
            if commands:
                # U+2002 Middle Dot
                joined = ' '.join(f"`{c.name}`"for c in commands)
                self.paginator.add_line('**%s**:' % heading)
                self.paginator.add_line(joined)
    async def send_command_help(self, command):
            ctx = self.context

            embed = discord.Embed(
                color=discord.Color.green(),description="")
            embed.set_author(name=f"Command help for {command.name}",icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Thanks for using {ctx.bot.user.name}!",icon_url=ctx.author.avatar_url)
            embed.description = command.help or "No description provided"
            embed.description += "\n**Don't include <> or [] on the command itself.**"
            if (command.hidden == True or command.enabled == False) and await ctx.bot.is_owner(ctx.author) == False:
                return await ctx.send(embed=discord.Embed(description=f'No command called "{command.qualified_name}" found.'))
            if command.signature:
                embed.add_field(name=":pencil:  Usage", value=f"`{self.clean_prefix}{command.qualified_name} {command.signature} `\n",inline=False)
            else:
                embed.add_field(name=":pencil:  Usage", value=f"`{self.clean_prefix}{command.qualified_name}`\n",inline=False)


            if len(command.aliases) > 0:
                formatted = [f"`{self.clean_prefix}{x}`" for x in command.aliases]
                embed.add_field(name=":fork_and_knife:  Aliases", value=", ".join(formatted),inline=False)
            embed.add_field(name=":newspaper:  Still lost and confused?", value="[Join our support server](https://discord.gg/YWb3AdW)")
            await ctx.send(embed=embed)

    async def send_group_help(self, group):
        ctx = self.context
        pre = self.clean_prefix

        embed = discord.Embed(color=discord.Color.blurple())
        embed.set_author(name=f"Command help for {group.name}",icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"Thanks for using {ctx.bot.user.name}!",icon_url=ctx.author.avatar_url)
        if group.signature:
            embed.add_field(name=":pencil:  Usage", value=f"`{self.clean_prefix}{group.qualified_name} {group.signature} <subcommand>`\n",inline=False)
        else:
            embed.add_field(name=":pencil:  Usage", value=f"`{self.clean_prefix}{group.qualified_name} <subcommand>`\n",inline=False)

        embed.description = group.help or "No description provided."
        embed.description += f"\n\n**Use `{pre}help {group.qualified_name} <sub_command>` to get help on a group command.**"

        if await ctx.bot.is_owner(ctx.author):
            group_commands = [command for command in group.commands]
            if len(group_commands) == 0:
                return await ctx.send(embed=discord.Embed(description="This command is still Work in progress! Check back later!"))
        else:
            group_commands = [
                command
                for command in group.commands
                if command.hidden == False and command.enabled == True
            ]

        if len(group_commands) == 0:
            return await ctx.send(f'No command called "{group.qualified_name}" found.')
        command_help = ""
        for command in group_commands:
            if command.signature:
                command_help += f":small_orange_diamond: `{pre}{command.qualified_name} {command.signature}` \n"
            else:
                command_help += f":small_orange_diamond: `{pre}{command.qualified_name}` \n"

        embed.add_field(name=":zap: Sub-commands", value=command_help,inline=False)
        embed.add_field(name=":newspaper:  Still lost and confused?", value="[Join our support server](https://discord.gg/YWb3AdW)")
        await ctx.send(embed=embed)
    def get_footer_note(self):
        ctx = self.context
        """:class:`str`: Returns help command's ending note. This is mainly useful to override for i18n purposes."""
        return f"Thanks for using {ctx.bot.user.name} ❤️ (Total Commands: {len([command for command in ctx.bot.commands if command.hidden == False or command.enabled == True])})"
    async def send_cog_help(self, cog):
        pass
class Help(commands.Cog):
    """Help command cog"""

    def __init__(self, client):
        self.client = client
        self.client._original_help_command = client.help_command
        client.help_command = CustomHelp()
        client.help_command.cog = self

    def cog_unload(self):
        self.client.help_command = self.client._original_help_command


def setup(client):
    client.add_cog(Help(client))
