import datetime
import functools
import sys
import time
import typing
import subprocess

import discord
from discord.ext import commands

if len(sys.argv) < 3:
    print(
        "Error: Missing arguments -- You should use the main.py file to run the bot for a more user-friendly interface."
    )
    sys.exit(1)
token = sys.argv[1]
prefix = sys.argv[2]
print(f"Token recieved: {token!r}")
time.sleep(1)
print(f"\033[1A\033[2K\rPrefix recieved: {prefix!r}")
time.sleep(1)
print("\033[1A\033[2K\rLoading bot...")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"\033[1A\033[2K\033[1A\033[2K\033[1A\033[2K\rLogged in as {bot.user}")
    await bot.tree.sync()


def command(
    required_permissions: list[str] | None = None,
) -> typing.Callable[[typing.Callable], typing.Callable]:
    def decorator(func: typing.Callable) -> typing.Callable:
        @bot.hybrid_command()
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs) -> None:
            if not isinstance(ctx.author, discord.Member):
                await ctx.reply(
                    "You must be a member of this server to use this command."
                )
            elif required_permissions and not all(
                getattr(ctx.author.guild_permissions, perm)
                for perm in required_permissions
            ):
                await ctx.reply(
                    f"You need the following permissions to use this command: `{', '.join(required_permissions)}`"
                )
            else:
                try:
                    await func(ctx, *args, **kwargs)
                except Exception as e:  # noqa: BLE001
                    await ctx.reply(f"An error occured: `{type(e).__name__}: {e}`")

        return wrapper

    return decorator


@command(["moderate_members"])
async def mute(
    ctx: commands.Context,
    user: discord.Member,
    duration: int,
    unit: str = "seconds",
    reason: str = "No reason provided",
):
    match unit:
        case "seconds" | "second" | "secs" | "sec" | "s":
            pass
        case "minutes" | "minute" | "mins" | "min" | "m":
            duration *= 60
        case "hours" | "hour" | "hrs" | "hr" | "h":
            duration *= 3600
        case "days" | "day" | "d":
            duration *= 86400
        case "weeks" | "week" | "w":
            duration *= 604800
        case _:
            raise ValueError(f"Invalid unit: {unit!r}")
    await user.timeout(
        datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=duration), reason=reason
    )
    await ctx.reply(
        f":checkmark: Successfully muted {user.mention} for {duration} {unit}!"
    )


@command(["kick_members"])
async def kick(
    ctx: commands.Context, user: discord.Member, reason: str = "No reason provided"
) -> None:
    await user.kick(reason=reason)
    await ctx.reply(f":checkmark: Successfully kicked {user.mention}!")


@command(["ban_members"])
async def ban(
    ctx: commands.Context, user: discord.Member, reason: str = "No reason provided"
) -> None:
    await user.ban(reason=reason, delete_message_days=14)
    await ctx.reply(f":checkmark: Successfully banned {user.mention}!")


@command(["send_messages", "view_channel"])
async def say(ctx: commands.Context, message: str, times: int = 1) -> None:
    if not 1 <= times <= 100:
        raise ValueError("Times must be between 1 and 100.")
    else:
        for _ in range(times):
            await ctx.send(message)


@command(["manage_messages"])
async def purge(ctx: commands.Context, amount: int = 100) -> None:
    if not 1 <= amount <= 100:
        raise ValueError("Amount must be between 1 and 100.")
    elif not isinstance(ctx.channel, discord.TextChannel):
        raise ValueError("This command can only be used in a text channel.")
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.reply(
            f":checkmark: Successfully purged {amount} messages!", delete_after=1
        )


@command(["moderate_members"])
async def unmute(ctx: commands.Context, user: discord.Member) -> None:
    await user.timeout(None)
    await ctx.reply(f":checkmark: Successfully unmuted {user.mention}!")


@command(["ban_members"])
async def unban(ctx: commands.Context, user: discord.User) -> None:
    if ctx.guild is None:
        raise ValueError("This command can only be used in a server.")
    await ctx.guild.unban(user)


@command(["manage_guild"])
async def kickbot(ctx: commands.Context) -> None:
    if ctx.guild is None:
        raise ValueError("This command can only be used in a server.")
    await ctx.reply("Goodbye!")
    await ctx.guild.leave()


@command(["manage_roles"])
async def makerole(
    ctx: commands.Context,
    name: str,
    colour: str = "000000",
    hoist: bool = False,
    mentionable: bool = False,
) -> None:
    if ctx.guild is None:
        raise ValueError("This command can only be used in a server.")
    await ctx.guild.create_role(
        name=name, colour=int(colour, 16), hoist=hoist, mentionable=mentionable
    )
    await ctx.reply(f":checkmark: Successfully created role {name}!")


@command(["manage_roles"])
async def deleterole(ctx: commands.Context, role: discord.Role) -> None:
    if ctx.guild is None:
        raise ValueError("This command can only be used in a server.")
    await role.delete()
    await ctx.reply(f":checkmark: Successfully deleted {role.mention}!")


@command(["manage_roles"])
async def addrole(
    ctx: commands.Context, user: discord.Member, role: discord.Role
) -> None:
    await user.add_roles(role)
    await ctx.reply(f":checkmark: Successfully added {role.mention} to {user.mention}!")


@command(["manage_roles"])
async def removerole(
    ctx: commands.Context, user: discord.Member, role: discord.Role
) -> None:
    await user.remove_roles(role)
    await ctx.reply(
        f":checkmark: Successfully removed {role.mention} from {user.mention}!"
    )


@command(["manage_roles"])
async def moverole(ctx: commands.Context, role: discord.Role, position: int) -> None:
    await role.edit(position=position)
    await ctx.reply(
        f":checkmark: Successfully moved {role.mention} to position {position}!"
    )


@command(["manage_roles"])
async def colour(ctx: commands.Context, role: discord.Role, colour: str) -> None:
    await role.edit(colour=int(colour, 16))
    await ctx.reply(
        f":checkmark: Successfully changed the colour of {role.mention} to {colour}!"
    )


@command(["manage_roles"])
async def hoist(ctx: commands.Context, role: discord.Role) -> None:
    await role.edit(hoist=True)
    await ctx.reply(f":checkmark: Successfully hoisted {role.mention}!")


@command(["manage_roles"])
async def unhoist(ctx: commands.Context, role: discord.Role) -> None:
    await role.edit(hoist=False)
    await ctx.reply(f":checkmark: Successfully unhoisted {role.mention}!")


@command(["manage_roles"])
async def mentionable(ctx: commands.Context, role: discord.Role) -> None:
    await role.edit(mentionable=True)
    await ctx.reply(f":checkmark: Successfully made {role.mention} mentionable!")


@command(["manage_roles"])
async def unmentionable(ctx: commands.Context, role: discord.Role) -> None:
    await role.edit(mentionable=False)
    await ctx.reply(f":checkmark: Successfully made {role.mention} unmentionable!")


@command(["manage_channels"])
async def makechannel(
    ctx: commands.Context,
    name: str,
    category: discord.CategoryChannel | None = None,
    type: str = "text",
):
    if ctx.guild is None:
        raise ValueError("This command can only be used in a server.")
    match type:
        case "text":
            await ctx.guild.create_text_channel(name=name, category=category)
        case "voice":
            await ctx.guild.create_voice_channel(name=name, category=category)
        case "threads" | "forum":
            await ctx.guild.create_forum(name=name, category=category)
        case _:
            raise ValueError(f"Invalid channel type: {type!r}")
    await ctx.reply(f":checkmark: Successfully created channel {name}!")


@command(["manage_channels"])
async def deletechannel(ctx: commands.Context, channel: discord.TextChannel) -> None:
    await channel.delete()
    await ctx.reply(f":checkmark: Successfully deleted {channel.mention}!")


@command([])
async def update(ctx: commands.Context) -> None:
    subprocess.run(["bash", "update_bot.sh"])
    ctx.reply("Done!")


helptext = f"""```
Help for MeowBot <UwU>:
EXAMPLE: {prefix}command <required> [optional] - description
{prefix}help - Shows this message
{prefix}mute <user> <duration> [unit] [reason] - Mutes a user for a specified duration
{prefix}kick <user> [reason] - Kicks a user
{prefix}ban <user> [reason] - Bans a user
{prefix}say <message> [times] - Says a message
{prefix}purge [amount] - Purges a specified amount of messages
{prefix}unmute <user> - Unmutes a user
{prefix}unban <user> - Unbans a user
{prefix}kickbot - Kicks the bot from the server
{prefix}makerole <name> [colour] [hoist] [mentionable] - Creates a role
{prefix}deleterole <role> - Deletes a role
{prefix}addrole <user> <role> - Adds a role to a user
{prefix}removerole <user> <role> - Removes a role from a user
{prefix}moverole <role> <position> - Moves a role to a specified position
{prefix}colour <role> <colour> - Changes the colour of a role
{prefix}hoist <role> - Hoists a role
{prefix}unhoist <role> - Unhoists a role
{prefix}mentionable <role> - Makes a role mentionable
{prefix}unmentionable <role> - Makes a role unmentionable
{prefix}makechannel <name> [category] [type] - Creates a channel
{prefix}deletechannel <channel> - Deletes a channel
{prefix}update - Update the bot.
```"""


@command()
async def help(ctx: commands.Context) -> None:
    await ctx.reply(helptext)


bot.run(token)
