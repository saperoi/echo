import hikari
import lightbulb
import comm
import math
import random
import datetime
import sqlite3
import time
import re

plugin = lightbulb.Plugin('admn')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("reason", "Reason for the ban", modifier=lightbulb.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("user", "The user to ban.")
@lightbulb.set_help("Ban a user. May use user ID or ping")
@lightbulb.command("ban", "Ban a user from the server.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ban(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    if ctx.options.reason == None:
        r = "Banned by <@" + str(ctx.author.id) + ">."
    else:
        r = str(ctx.options.reason) + "\t - \tBanned by <@" + str(ctx.author.id) + ">."
    await ctx.app.rest.ban_user(ctx.guild_id, u, reason=r)
    await comm.send_msg(ctx,"Banned <@" + str(u) + ">")

@ban.set_error_handler
async def ban_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID) to ban.")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option("reason", "Reason for the kick", modifier=lightbulb.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("user", "The user to kick.")
@lightbulb.set_help("Kick a user. May use user ID or ping")
@lightbulb.command("kick", "Kick a user from the server.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def kick(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    if ctx.options.reason == None:
        r = "Kicked by <@" + str(ctx.author.id) + ">."
    else:
        r = str(ctx.options.reason) + "\t - \tKicked by <@" + str(ctx.author.id) + ">."
    await ctx.app.rest.kick_user(ctx.guild_id, u, reason=r)
    await comm.send_msg(ctx,"Kicked <@" + str(u) + ">")

@kick.set_error_handler
async def kick_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID) to ban.")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("user", "The user to unban.")
@lightbulb.set_help("Unban a user. May use user ID or ping")
@lightbulb.command("unban", "Unban a user from the server.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def unban(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    await ctx.app.rest.unban_user(ctx.guild_id, u)
    await comm.send_msg(ctx,"Unbanned <@" + str(u) + ">")

@unban.set_error_handler
async def unban_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID) to unban.")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("amount", "The amount of messages to remove.", required=True, type=int)
@lightbulb.set_help("Purges an amount of messages. Must be between 0 abnd 100. Messages cannot be older than 14 days.")
@lightbulb.command("purge", "Purges a set amount of messages.", aliases=["clear"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def purge(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if 0 < int(ctx.options.amount) <= 100:
        messages = ( await ctx.app.rest.fetch_messages(ctx.channel_id).take_until(lambda m: datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14) > m.created_at).limit(int(ctx.options.amount) + 1))
        await ctx.app.rest.delete_messages(ctx.channel_id, messages)
    else:
        raise ValueError
    await comm.send_msg(ctx,"Purged " + str(len(messages)) + " messages.", delete_after=3)

@purge.set_error_handler
async def purge_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond("You did not provide an amount of messages to delete.")
    elif isinstance(exception, ValueError):
        await event.context.respond("Too many messages to delete. Max is 100.")

conmod = sqlite3.connect("./db/warn.db")
curmod = conmod.cursor()

def table_check(s):
    curmod.execute("CREATE TABLE IF NOT EXISTS mod_" + str(s) + "(uid, time, warn)")
    conmod.commit()

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.command("warn", "Warning command group")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def warn(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id)

@warn.child
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("reason", "Reason for the kick", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.option("user", "The user to warn.")
@lightbulb.set_help("Warn a user. May use user ID or ping")
@lightbulb.command("add", "Warning command group")
@lightbulb.implements(lightbulb.PrefixSubGroup)
async def add(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id)
    u = comm.user_id_check(ctx.options.user)
    curmod.execute("INSERT INTO mod_" + str(ctx.guild_id) + " VALUES (?, ?, ?)", (u, math.floor(time.time()), re.sub(r'[^a-zA-Z0-9]', '',ctx.options.reason)))
    await comm.send_msg(ctx,"Warned <@" + str(u) + "> for: " + ctx.options.reason)
    conmod.commit()

@add.set_error_handler
async def add_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID) to warn.")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@warn.child
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("timestamp", "Time stamp of the warn (used in place of an ID).", type=int)
@lightbulb.option("user", "The user to unwarn.")
@lightbulb.set_help("Unwarn a user. May use user ID or ping")
@lightbulb.command("rmv", "Warning command group")
@lightbulb.implements(lightbulb.PrefixSubGroup)
async def rmv(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id)
    u = comm.user_id_check(ctx.options.user)
    curmod.execute("DELETE FROM mod_" + str(ctx.guild_id) + " WHERE uid=" + str(u) + " AND time=" + str(ctx.options.timestamp))
    await comm.send_msg(ctx,"Unwarned <@" + str(u) + ">")
    conmod.commit()

@rmv.set_error_handler
async def rmv_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID) to unwarn.")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@warn.child
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("user", "The user to list warns from.")
@lightbulb.set_help("Lists a user's warns. May use user ID or ping")
@lightbulb.command("lst", "List warnings")
@lightbulb.implements(lightbulb.PrefixSubGroup)
async def lst(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id)
    u = comm.user_id_check(ctx.options.user)

    curmod.execute("SELECT time FROM mod_" + str(ctx.guild_id) + " WHERE uid=" + str(u))
    times = str(curmod.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(",)", "").split(",")

    curmod.execute("SELECT warn FROM mod_" + str(ctx.guild_id) + " WHERE uid=" + str(u))
    warnings = str(curmod.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("',", "'").split(",")

    m = ""
    for k in range(len(times)):
        m += str(times[k]) + ": " + str(warnings[k]) + "\n"
    if m == ": \n":
        await comm.send_msg(ctx,"This user has no warnings")
    else:
        await comm.send_msg(ctx,m)

    conmod.commit()

@lst.set_error_handler
async def lst_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID) to list warns from.")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")
