
import discord
from typing import Optional
from datetime import datetime
from discord.ext import commands
import yaml

class TicketTool(commands.Cog):
  """A Ticket tool Module"""
  def __init__(self, bot):
      self.bot = bot
      with open("ticketing.yml") as f:
          self.config = yaml.safe_load(f)
  @commands.group()
  @commands.has_permissions(administrator=True)
  async def ticketconfig(self, ctx):
      """All ticketconfig settings."""
      guild = self.config.get(ctx.guild.id)
      if not guild:
          self.config[ctx.guild.id] =  {
                "channel": None,
                "closed_category": None,
                "open_category": None,
                "current_ticket": 0,
                "role": None,
                "message": "Your ticket has been created. You can add information by typing in this channel. \n\nA member of the ticket-handling-team will be with you as soon as they can.",
                "active": [],
                "closed": [],
            }
          with open("ticketing.yml", "w") as f:
              yaml.dump(self.config, f)


  @ticketconfig.command()
  async def channel(self, ctx, channel: discord.TextChannel):
      """Set the ticket-management channel."""
      guild = self.config.get(ctx.guild.id)
      guild['channel'] = channel
      await ctx.send(f"Channel has been set to {channel.mention}.")

  @ticketconfig.command()
  async def role(self, ctx, role: discord.Role):
      """Set the role for ticket managers."""
      guild = self.config.get(ctx.guild.id)
      guild['role'] = role.id
      await ctx.send(f"Ticket manager role has been set to {role.mention}.")
  @ticketconfig.command()
  async def save(self, ctx):
      """Saves the config"""
      with open("ticketing.yml", "w") as f:
          yaml.dump(self.config, f)

  @ticketconfig.group()
  async def category(self, ctx):
      """Set the categories for open and closed tickets."""

  @category.group()
  async def open(self, ctx, *, category: discord.CategoryChannel):
      """Set the category for open tickets."""
      guild = self.config.get(ctx.guild.id)
      guild['open_category'] = category.id
      await ctx.send(f"Category for open tickets has been set to {category.mention}")

  @category.group()
  async def closed(self, ctx, *, category: discord.CategoryChannel):
      """Set the category for closed tickets."""
      guild = self.config.get(ctx.guild.id)
      guild['closed_category'] = category.id
      await ctx.send(f"Category for closed tickets has been set to {category.mention}")

  @ticketconfig.command()
  async def message(self, ctx, *, message: str):
      """Set the message that is shown at the start of each ticket channel.\n\nUse ``{user.mention}`` to mention the person who created the ticket."""
      try:
          guild = self.config.get(ctx.guild.id)
          guild['message'] = message
          await ctx.send(f"The message has been set to `{message}`.")
      except KeyError:
          await ctx.send(
              "Setting the message failed. Please make sure to only use supported variables in  `\{\}`"
          )

  @ticketconfig.command()
  async def quicksetup(self, ctx):
      """Quickly sets configurations automatically."""
      settings = self.config.get(ctx.guild.id)
      if not settings["role"]:
          role = await ctx.guild.create_role(
              name="Support team",
              hoist=True,
              mentionable=False,
              reason="ticketconfig quicksetup",
          )
          settings['role'] = role.id
          await ctx.send("Ticket-manager role created.")
      if not settings["open_category"]:
          category = await ctx.guild.create_category(
              name="Open-tickets", reason="ticketconfig quicksetup"
          )
          settings['open_category'] = category.id
          await ctx.send("Category for open tickets created.")
      if not settings["closed_category"]:
          category = await ctx.guild.create_category(
              name="Closed-tickets", reason="ticketconfig quicksetup"
          )
          settings['closed_category'] = category.id
          await ctx.send("Category for closed tickets created.")
      settings = self.config.get(ctx.guild.id)
      if not settings["channel"]:
          overwrite = {
              ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
              ctx.guild.get_role(settings["role"]): discord.PermissionOverwrite(
                  read_messages=True,
                  send_messages=True,
                  embed_links=True,
                  attach_files=True,
                  manage_messages=True,
              ),
          }
          channel = await ctx.guild.create_text_channel(
              "ticket-management",
              overwrites=overwrite,
              category=ctx.guild.get_channel(settings["open_category"]),
              topic="Ticket management channel.",
              reason="ticketconfig quicksetup",
          )
          settings['channel'] = channel.id
          await ctx.send("Channel for ticket management created.")
      await ctx.send("Checking settings...")
      if await self._check_settings(ctx):
          await ctx.send("Quicksetup completed. Saving to config")

      else:
          await ctx.send("Something went wrong...")

  @ticketconfig.command()
  async def purge(self, ctx, are_you_sure: Optional[bool]):
      """Deletes all closed ticket channels."""
      if are_you_sure:
          with self.config.get(ctx.guild.id).get("closed") as closed:
              for channel in closed:
                  try:
                      channel_obj = ctx.guild.get_channel(channel)
                      if channel_obj:
                          await channel_obj.delete(reason="Ticket purge")
                      closed.remove(channel)
                  except discord.Forbidden:
                      await ctx.send(
                          f"I could not delete channel ID {channel} because I don't have the required permissions."
                      )
                  except discord.NotFound:
                      closed.remove(channel)
                  except discord.HTTPException:
                      await ctx.send(f"Something went wrong. Couldn't delete {channel.name}.")
                      return
      else:
          await ctx.send(
              f"This action will permanently delete all closed ticket channels.\nThis action is irreversible.\nConfirm with ``{ctx.clean_prefix}ticketconfig purge true``"
          )

  @commands.group()
  async def ticket(self, ctx):
      """Manage a ticket."""
      pass

  @ticket.command(aliases=["open"])
  async def create(
      self,
      ctx,
      *,
      reason: Optional[str] = "No reason provided.",
  ):
      """Create a ticket."""
      if await self._check_settings(ctx):
          settings = self.config.get(ctx.guild.id)
          name = f"ticket-{settings['current_ticket']}"
          self.config[ctx.guild.id]['current_ticket']=settings["current_ticket"] + 1
          found = False
          for channel in ctx.guild.channels:
              if channel.name == name.lower():
                  found = True
          if not found:
              overwrite = {
                  ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                  ctx.author: discord.PermissionOverwrite(
                      read_messages=True,
                      send_messages=True,
                      embed_links=True,
                      attach_files=True,
                  ),
                  ctx.guild.get_role(settings["role"]): discord.PermissionOverwrite(
                      read_messages=True,
                      send_messages=True,
                      embed_links=True,
                      attach_files=True,
                      manage_messages=True,
                  ),
              }
              ticketchannel = await ctx.guild.create_text_channel(
                  name,
                  overwrites=overwrite,
                  category=ctx.guild.get_channel(settings["open_category"]),
                  topic=reason,
              )
              await ticketchannel.send(settings["message"])
              embed = discord.Embed(
                  title=name,
                  description=reason,
                  timestamp=datetime.utcnow(),
              ).set_footer(text="Last updated at:")
              message = await ctx.guild.get_channel(settings["channel"]).send(embed=embed)
              self.config[ctx.guild.id]['active'].append([ticketchannel.id, message.id])
              with open("ticketing.yml", "w") as f:
                  yaml.dump(self.config, f)
          else:
              await ctx.send("You already have an open ticket. Please close your ticket first!")
      else:
          await ctx.send("Please finish the setup process before creating a ticket.")

  @ticket.command()
  async def close(self, ctx):
      """Close a ticket."""
      settings = self.config.get(ctx.guild.id)
      active = settings["active"]
      success = False
      for ticket in active:
          if ctx.channel.id in ticket:
              new_embed = (
                  await ctx.guild.get_channel(settings["channel"]).fetch_message(ticket[1])
              ).embeds[0]
              new_embed.add_field(
                  name=datetime.utcnow().strftime("%H:%m UTC"),
                  value=f"Ticket closed by {ctx.author}",
              )
              new_embed.timestamp = datetime.utcnow()
              await (
                  await ctx.guild.get_channel(settings["channel"]).fetch_message(ticket[1])
              ).edit(
                  embed=new_embed,
                  delete_after=10,
              )
              await ctx.send(embed=new_embed)
              await ctx.send(
                  "This ticket can no longer be edited using Ticket Tool.",
                  delete_after=30,
              )
              await ctx.channel.edit(
                  category=ctx.guild.get_channel(settings["closed_category"]),
                  name=f"{ctx.channel.name}-c-{datetime.utcnow().strftime('%B-%d-%Y-%H-%m')}",
                  overwrites={
                      ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                      ctx.guild.get_role(settings["role"]): discord.PermissionOverwrite(
                          read_messages=True,
                          send_messages=True,
                          embed_links=True,
                          attach_files=True,
                          manage_messages=True,
                      ),
                  },
              )
              await ctx.send("Ticket closed.")
              active.remove(ticket)
              self.config[ctx.guild.id]['closed'].append([ctx.channel.id, ctx.message.id])
              success = True
              with open("ticketing.yml", "w") as f:
                  yaml.dump(self.config, f)
      if not success:
          await ctx.send("This is not a ticket channel.")


  @ticket.command()
  @commands.has_permissions(ban_members=True, manage_messages=True, kick_members=True)
  async def update(self, ctx, ticket: Optional[discord.TextChannel] = None, *, update: str):
      """Update a ticket. This is visible to all participants of the ticket."""
      if ticket is None:
          channel = ctx.channel
      else:
          channel = ticket
      settings = self.config.get(ctx.guild.id)
      active = settings["active"]
      for ticket in active:
          if channel.id in ticket:
              await channel.edit(topic=f'{channel.topic}\n\n{ctx.author}:"{update}"')
              await ctx.send("Ticket updated.", delete_after=10)
          else:
              ctx.send(f"{channel.mention} is not a ticket channel.")

  @ticket.command()
  @commands.has_permissions(ban_members=True, manage_messages=True, kick_members=True)
  async def note(self, ctx, ticket: discord.TextChannel, *, note: str):
      """Add a staff-only note to a ticket."""
      channel = ticket
      ticket_found = False
      for ticket in self.config.get(ctx.guild.id).get("active"):
          if channel.id in ticket:
              message = await ctx.guild.get_channel(
                  await self.config.guild(ctx.guild).channel()
              ).fetch_message(ticket[1])
              new_embed = message.embeds[0]
              new_embed.add_field(name=f"{ctx.author}", value=note)
              new_embed.timestamp = datetime.utcnow()
              await message.edit(embed=new_embed)
              await ctx.send("Note added.", delete_after=10)
              ticket_found = True
      if not ticket_found:
          await ctx.send("This is not a ticket channel.")

  async def _check_settings(self, ctx: commands.Context) -> bool:
      settings = self.config.get(ctx.guild.id)
      count = 0
      if settings["channel"]:
          count += 1
      else:
          await ctx.send("Management channel not set up yet.")
      if settings["closed_category"]:
          count += 1
      else:
          await ctx.send("Category for closed tickets not set up yet.")
      if settings["open_category"]:
          count += 1
      else:
          await ctx.send("Category for open tickets not set up yet.")
      if settings["role"]:
          count += 1
      else:
          await ctx.send("Ticket manager role not set up yet.")
      if count == 4:
          return True
      else:
          return False
def setup(bot):
  bot.add_cog(TicketTool(bot))
