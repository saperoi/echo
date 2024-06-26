import hikari
import lightbulb
import comm
import math
import random
import datetime
import sqlite3
import time
import base64
import requests
import json

plugin = lightbulb.Plugin('admn')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("data", "Data for banning. First user mention/id, then the reason (optional). Seperate users with at least one whiteline, if no reason is given, the one from the previous user will be used. If it's the first listed, the reason defaults to 'Banned by <your user>'", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.set_help("Bans users")
@lightbulb.command("ban", "Ban users from the server.", aliases=["BAN"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def ban(ctx: lightbulb.Context):
    comm.log_com(ctx)
    lines = [line.split(" ") for line in str(ctx.options.data).split("\n") if line != '']
    linetuples = [[line[0], None if len(line) == 1 or "".join(line[1:]) == "" else " ".join(line[1:])] for line in lines]
    for entrynum in range(len(linetuples)):
        u = linetuples[entrynum][0]
        u = comm.user_id_check(u)
        if entrynum == 0:
            if linetuples[entrynum][1] == None:
                linetuples[entrynum][1] = "Banned by <@" + str(ctx.author.id) + ">."
            else:
                linetuples[entrynum][1] = str(linetuples[entrynum][1]) + "\t - \tBanned by <@" + str(ctx.author.id) + ">."
        else:
            if linetuples[entrynum][1] == None:
                linetuples[entrynum][1] = linetuples[entrynum-1][1]
            else:
                linetuples[entrynum][1] = str(linetuples[entrynum][1]) + "\t - \tBanned by <@" + str(ctx.author.id) + ">."
        await ctx.app.rest.ban_user(ctx.guild_id, linetuples[entrynum][0], reason=linetuples[entrynum][1])
        await comm.send_msg(ctx,f"Banned <@{str(linetuples[entrynum][0])}>")

@ban.set_error_handler
async def ban_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("A ValueError occurred")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("One of the users listed do not exist")

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("ban_export", "Exports bans in server to a JSON.", aliases=["BAN_EXPORT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def ban_export(ctx: lightbulb.Context):
    comm.log_com(ctx)
    bans = await ctx.app.rest.fetch_bans(ctx.guild_id)
    j = "{"
    for ban in bans:
        j += '\n\t"' + str(ban.user.id) + '": {' + '\n\t\t"name": "' + str(ban.user.username) + "#" + str(ban.user.discriminator) + '", ' + '\n\t\t"banreason": "' + str(ban.reason).replace('"', '\\"').replace('\n', '\\n') + '"\n\t},'
    j = j[:-1] + "\n}"
    await ctx.respond(attachment = "data:application/json;base64,{}".format(base64.b64encode(str.encode(j)).decode() ))

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("ban_import", "Exports bans in server to a JSON.", aliases=["BAN_IMPORT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def ban_import(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.event.message.attachments == [] or "json" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
        return
    j = [a for a in ctx.event.message.attachments if "json" in a.media_type][0].url
    j = requests.get(j).text
    j = json.loads(j, strict=False)
    for x in j.keys():
        try:
            await ctx.app.rest.ban_user(ctx.guild_id, int(x), reason=f"{j[x]['banreason']}\t-\tBan import by <@{str(ctx.author.id)}>")
            await comm.send_msg(ctx,f"Banned <@{x}>")
        except:
            await comm.send_msg(ctx,f"Exception occured with {x}")

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS) | lightbulb.owner_only)
@lightbulb.command("bancount", "Count bans in a server", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def bancount(ctx: lightbulb.Context):
    comm.log_com(ctx)
    bans = await ctx.app.rest.fetch_bans(ctx.guild_id)
    await ctx.respond("This server has " + str(len(bans)) + " bans.")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option("reason", "Reason for the kick", modifier=lightbulb.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("user", "The user to kick.", type=hikari.Member)
@lightbulb.set_help("Kick a user. May use user ID or ping")
@lightbulb.command("kick", "Kick a user from the server.", aliases=["KICK"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def kick(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.options.user.id
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
@lightbulb.option("user", "The user to unban.", type=hikari.User)
@lightbulb.set_help("Unban a user. May use user ID or ping")
@lightbulb.command("unban", "Unban a user from the server.", aliases=["UNBAN"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def unban(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.options.user.id
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
@lightbulb.set_help("Purges an amount of messages. Must be between 0 and 100. Messages cannot be older than 14 days.")
@lightbulb.command("purge", "Purges a set amount of messages.", aliases=["clear", "PURGE", "CLEAR"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def purge(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if 0 < int(ctx.options.amount) <= 100:
        messages = ( await ctx.app.rest.fetch_messages(ctx.channel_id).take_until(lambda m: datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14) > m.created_at).limit(int(ctx.options.amount) + 1))
        await ctx.app.rest.delete_messages(ctx.channel_id, messages)
    else:
        raise ValueError
    await ctx.respond("Purged " + str(len(messages)) + " messages.", delete_after=3)

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
@lightbulb.command("warn", "Warning command group", aliases=["WARN"])
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def warn(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id)

@warn.child
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("reason", "Reason for the kick", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.option("user", "The user to warn.", type=hikari.Member)
@lightbulb.set_help("Warn a user. May use user ID or ping")
@lightbulb.command("add", "Warning command group", aliases=["ADD"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def add(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id)
    u = ctx.options.user.id
    curmod.execute("INSERT INTO mod_" + str(ctx.guild_id) + " VALUES (?, ?, ?)", (u, math.floor(time.time()), ctx.options.reason))
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
@lightbulb.option("user", "The user to unwarn.", type=hikari.Member)
@lightbulb.set_help("Unwarn a user. May use user ID or ping")
@lightbulb.command("rmv", "Warning command group", aliases=["RMV"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def rmv(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id)
    u = ctx.options.user.id
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
@lightbulb.option("user", "The user to list warns from.", type=hikari.Member)
@lightbulb.set_help("Lists a user's warns. May use user ID or ping")
@lightbulb.command("lst", "List warnings", aliases=["LST"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def lst(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id)
    u = ctx.options.user.id

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

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("data", "Data for banning. First user mention/id, then the reason (optional). Seperate users with at least one whiteline, if no reason is given, the one from the previous user will be used. If it's the first listed, the reason defaults to 'Banned by <your user>'", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.set_help("Bans users")
@lightbulb.command("speedban", "Ban users from the server.", aliases=["SPEEDBAN"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def speedban(ctx: lightbulb.Context):
    comm.log_com(ctx)
    
    bans = await ctx.app.rest.fetch_bans(ctx.guild_id)
    prebanned = [ban.user.id for ban in bans]
    
    lines = [line.split(" ") for line in str(ctx.options.data).split("\n") if line != '']
    linetuples = [[line[0], None if len(line) == 1 or "".join(line[1:]) == "" else " ".join(line[1:])] for line in lines]
    for entrynum in range(len(linetuples)):
        u = linetuples[entrynum][0]
        
        if entrynum == 0:
            if linetuples[entrynum][1] == None:
                linetuples[entrynum][1] = "Banned by <@" + str(ctx.author.id) + ">."
            else:
                linetuples[entrynum][1] = str(linetuples[entrynum][1]) + "\t - \tBanned by <@" + str(ctx.author.id) + ">."
        else:
            if linetuples[entrynum][1] == None:
                linetuples[entrynum][1] = linetuples[entrynum-1][1]
            else:
                linetuples[entrynum][1] = str(linetuples[entrynum][1]) + "\t - \tBanned by <@" + str(ctx.author.id) + ">."
    
        if int(u) in prebanned:
            await comm.send_msg(ctx,f"Skipped {u} for already being banned.")
            continue
            
        try:
            us = await ctx.app.rest.fetch_user(u)
        except:
            await comm.send_msg(ctx,f"Skipped {u} for not existing.")
            continue
        
        if "deleted" in us.username.lower():
            await comm.send_msg(ctx,f"Skipped {u} for being deleted.")
            continue
        
        if us.is_bot:
            await comm.send_msg(ctx,f"Skipped {u} for being a bot.")
            continue
            
        try:
            await ctx.app.rest.ban_user(ctx.guild_id, linetuples[entrynum][0], reason=linetuples[entrynum][1])
            await comm.send_msg(ctx,f"Banned <@{u}>.")
        except:
            await comm.send_msg(ctx,f"Could not ban {u} from {ctx.guild_id}.")
    await comm.send_msg(ctx,f"Finished.")