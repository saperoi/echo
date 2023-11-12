import lightbulb
import hikari
import comm
import sqlite3
import ast
import base64

plugin = lightbulb.Plugin('role', 'Potter sorting hat >>>')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "Role to add/remove", type=hikari.Role)
@lightbulb.option("user", "The user to add/remove roles to/from.", type=hikari.Member)
@lightbulb.set_help("Adds or removes a role if the user already or doesn't already have said role")
@lightbulb.command("role", "Adds/removes roles")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def role(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.options.user.id
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    results = [role.id for role in roles]
    member = await ctx.app.rest.fetch_member(ctx.guild_id, u)
    if ctx.options.role.id not in results:
        await comm.send_msg(ctx, "That role ID is not in this server, therefore I cannot add it")
    elif ctx.options.role.id not in member.role_ids:
        await ctx.app.rest.add_role_to_member(ctx.guild_id, member, ctx.options.role.id)
        await comm.send_msg(ctx, "Added role to member")
    elif ctx.options.role.id in member.role_ids:
        await ctx.app.rest.remove_role_from_member(ctx.guild_id, member, ctx.options.role.id)
        await comm.send_msg(ctx, "Removed role from member")
    else:
        await comm.send_msg(ctx, "...smth happened pls report")

@role.set_error_handler
async def role_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID)")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "Role to add", type=hikari.Role)
@lightbulb.option("user", "The user to add roles to.", type=hikari.Member)
@lightbulb.set_help("Adds a role if the user doesn't already have said role")
@lightbulb.command("add", "Adds roles to member")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def add(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.options.user.id
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    results = [role.id for role in roles]
    member = await ctx.app.rest.fetch_member(ctx.guild_id, u)
    if ctx.options.role.id not in results:
        await comm.send_msg(ctx, "That role ID is not in this server, therefore I cannot add it")
    elif ctx.options.role.id not in member.role_ids:
        await ctx.app.rest.add_role_to_member(ctx.guild_id, member, ctx.options.role.id)
        await comm.send_msg(ctx, "Added role to member")
    else:
        await comm.send_msg(ctx, "Member already has this role")

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "Role to remove", type=hikari.Role)
@lightbulb.option("user", "The user to add roles to.", type=hikari.Member)
@lightbulb.set_help("Removes a role if the user doesn't already have said role")
@lightbulb.command("rmv", "Removes roles from member")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def rmv(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.options.user.id
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    results = [role.id for role in roles]
    member = await ctx.app.rest.fetch_member(ctx.guild_id, u)
    if ctx.options.role.id not in results:
        await comm.send_msg(ctx, "That role ID is not in this server, therefore I cannot add it")
    elif ctx.options.role.id in member.role_ids:
        await ctx.app.rest.remove_role_from_member(ctx.guild_id, member, ctx.options.role.id)
        await comm.send_msg(ctx, "Removed role from member")
    else:
        await comm.send_msg(ctx, "Member doesn't have that role so I can't remove it!")

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "The role to look in", type=hikari.Role)
@lightbulb.command("in", "Shows users that are members of a role.")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def in_role(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    rolids = [role.id for role in roles]
    if ctx.options.role.id not in rolids:
        await comm.send_msg(ctx, "That role ID is not in this server")
        return
    lazy = await ctx.app.rest.fetch_members(ctx.guild_id)
    ids = []
    for mi in range(len(lazy)):
        if lazy[mi].is_bot == False:
            ids.append(lazy[mi].user.id)
    mems = []
    for mii in ids:
        member = await ctx.app.rest.fetch_member(ctx.guild_id, mii)
        mems.append(member)
    rolemems = []
    for mms in range(len(mems)):
        if ctx.options.role.id in mems[mms].role_ids:
            rolemems.append((mems[mms].user.username, mems[mms].user.discriminator, mems[mms].user.id, mems[mms].nickname))
    msg = ""
    for i in range(len(rolemems)):
        name, tag, id, nick = rolemems[i]
        if nick == None:
            nick = name
        msg += str(i + 1) + ". " + nick + " (" + name + "#" + str(tag) + ") [" + str(id) + "]\n"
    await comm.send_msg(ctx,msg)

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role_2", "Role to remove from.", default=None, type=hikari.Role)
@lightbulb.option("role_1", "Role to remove.", type=hikari.Role)
@lightbulb.command("purge_role_members", "Removes a role from a group of members.", aliases=["prm"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def purge_role_members(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    rolids = [role.id for role in roles]
    if (ctx.options.role_1.id not in rolids) or (ctx.options.role_2.id != None and ctx.options.role_2.id not in rolids):
        await comm.send_msg(ctx, "That role ID is not in this server")
        return
    lazy = await ctx.app.rest.fetch_members(ctx.guild_id)
    ids = []
    for mi in range(len(lazy)):
        if lazy[mi].is_bot == False:
            ids.append(lazy[mi].user.id)
    mems = []
    for mii in ids:
        member = await ctx.app.rest.fetch_member(ctx.guild_id, mii)
        mems.append(member)
    rolemems = []
    for mms in range(len(mems)):
        if (ctx.options.role_1.id in mems[mms].role_ids) and (ctx.options.role_2.id == None or ctx.options.role_2.id in mems[mms].role_ids):
            rolemems.append(mems[mms].user.id)
    for id in rolemems:
        m = await ctx.app.rest.fetch_member(ctx.guild_id, id)
        await ctx.app.rest.remove_role_from_member(ctx.guild_id, m, ctx.options.role_1.id)
    msg = "Removed " + roles[rolids.index(ctx.options.role_1.id)].name.replace('@', '') + " role from every member "
    if ctx.options.role_2.id != None:
        msg += "with the " + roles[rolids.index(ctx.options.role_2.id)].name.replace('@', '') + " role"
    await ctx.respond(msg)

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role_2", "Role to add from.", default=None, type=hikari.Role)
@lightbulb.option("role_1", "Role to add.", type=hikari.Role)
@lightbulb.command("add_role_members", "Adds a role to a group of people.", aliases=["arm"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def add_role_members(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    rolids = [role.id for role in roles]
    if (ctx.options.role_1.id not in rolids) or (ctx.options.role_2.id != None and ctx.options.role_2.id not in rolids):
        await comm.send_msg(ctx, "That role ID is not in this server")
        return
    lazy = await ctx.app.rest.fetch_members(ctx.guild_id)
    ids = []
    for mi in range(len(lazy)):
        if lazy[mi].is_bot == False:
            ids.append(lazy[mi].user.id)
    mems = []
    for mii in ids:
        member = await ctx.app.rest.fetch_member(ctx.guild_id, mii)
        mems.append(member)
    rolemems = []
    for mms in range(len(mems)):
        if (ctx.options.role_1.id not in mems[mms].role_ids) and (ctx.options.role_2.id == None or ctx.options.role_2.id in mems[mms].role_ids):
            rolemems.append(mems[mms].user.id)

    for id in rolemems:
        m = await ctx.app.rest.fetch_member(ctx.guild_id, id)
        await ctx.app.rest.add_role_to_member(ctx.guild_id, m, ctx.options.role_1.id)
    msg = "Added " + roles[rolids.index(ctx.options.role_1.id)].name.replace('@', '') + " role to every member "
    if ctx.options.role_2.id != None:
        msg += "with the " + roles[rolids.index(ctx.options.role_2.id)].name.replace('@', '') + " role"
    await ctx.respond(msg)

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("list", "Lists roles in server.")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def role_list(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    d = ""
    for r in range(len(roles)):
        d += "<@&" + str(roles[r].id) + "> : " + str(roles[r].id) + "\n"
    embed = hikari.Embed(title="Roles", description=d, color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "Role to add.", type=hikari.Role)
@lightbulb.command("info", "Lists info on a role in server.")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def info(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    rolids = [role.id for role in roles]
    if ctx.options.role.id not in rolids:
        await comm.send_msg(ctx, "That role ID is not in this server")
        return
    else:
        r = roles[rolids.index(ctx.options.role.id)]
    d = "**Role ID**: " + str(r.id) + "\n"
    d += "**Color**: " + str(r.color) + "\n"
    d += "**Position**: " + str(r.position) + "\n"
    d += "**Permissions**: \n" + str(r.permissions).replace("|", "\n")
    embed = hikari.Embed(title=r.name.replace('@', ''), description=d, color=r.color)
    embed.set_footer("Ordered by: " + str(ctx.author))
    if r.icon_url != None:
        embed.set_image(r.icon_url)
    await ctx.respond(embed)

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("export", "Exports roles in server to a JSON.")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def role_list(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    roles = sorted([role for role in roles if not role.is_managed], reverse=True, key=lambda x: x.position)
    j = "{"
    for role in roles:
        j += '\n\t"' + str(role.id) + '": {' + '\n\t\t"name": "' + role.name + '", ' + '\n\t\t"color": "' + str(role.color.hex_code) + '", ' + '\n\t\t"icon_url": "' + str(role.icon_url) + '", ' + '\n\t\t"is_hoisted": "' + str(role.is_hoisted) + '", ' + '\n\t\t"unicode_emoji": "' + str(role.unicode_emoji) + '", ' + '\n\t\t"permissions": "' + str(str(role.permissions).split("|")) + '"\n\t},'
    j = j[:-1] + "\n}"
    await ctx.respond(attachment = "data:application/json;base64,{}".format(base64.b64encode(str.encode(j)).decode() ))

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "Role to add (NAME!)", type=str)
@lightbulb.option("user", "User to add role to")
@lightbulb.command("global_add", "Lists info on a role in server.", aliases = ["g_add", "gadd"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def g_add(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.options.user.id
    if ctx.guild_id not in comm.atheria_guilds:
        await ctx.respond("Only available for ATHERIA")
        return
    roles = []
    for sid in comm.atheria_guilds:
        roles.append(await ctx.app.rest.fetch_roles(sid))
    role_names = []
    for i in range(len(roles)):
        s = roles[i]
        k = []
        for j in range(len(s)):
            k.append(s[j].name)
        role_names.append(k)

    for k in range(len(roles)):
        s = []
        try:
            i = role_names[k].index(ctx.options.role)
            j = roles[k]
            await ctx.app.rest.add_role_to_member(comm.atheria_guilds[k], u, j[i])
            s.append(comm.atheria_guilds[k])
        except:
            pass
    await ctx.respond("Added role to user in following servers: " + str(s))

conrol = sqlite3.connect("./db/role.db")
currol = conrol.cursor()

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.set_help("Reaction Role command group")
@lightbulb.command("reactionrole", "Reaction role command group", aliases=["rr"])
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def reactionrole(ctx: lightbulb.Context):
    comm.log_com(ctx)
    msg = """
Here's how to use the reaction roles command module:
a//rr add [message id] [emoji] [role]
a//rr rmv [message id] [emoji]
a//rr lst [message id]
a//rr set [message id] (mode=free) (prereq=None)
    mode can be either "free", "unique", "verification", "limit", "binding", or "remove"
        free is no restriction and is the default
        unique allows you to only get one from it and removes the others immediatly
        verification only allows you to get a role, and not remove it
        limit restricts the amount you're allowed to have
        binding only allows you to get one role from a message, ever!
        remove removes a role from you
    prereq is just the role you need to have to get from a message. currently only allows one.

The command must be used in the same channel as the message.
You can put multiple roles on one emoji, but these must be done in the same message
"""
    await ctx.respond(msg)

@reactionrole.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "Role to add", type=hikari.Role)
@lightbulb.option("emoji", "The emoji to click", type=hikari.Emoji)
@lightbulb.option("message", "The message to listen to", type=hikari.Message)
@lightbulb.set_help("Adds a role if the user doesn't already have said role.\nYou must be in the same channel as the message")
@lightbulb.command("add", "Adds roles to member")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def add(ctx: lightbulb.Context):
    comm.log_com(ctx)
    emojitable = "rr_emoji_g" + str(ctx.guild_id) + "_c" + str(ctx.channel_id) + "_m" + str(ctx.options.message.id)
    ruletable = "rr_rule_g" + str(ctx.guild_id) + "_c" + str(ctx.channel_id)
    await ctx.options.message.add_reaction(ctx.options.emoji.name)
    currol.execute("CREATE TABLE IF NOT EXISTS " + emojitable + "(emoji TEXT PRIMARY KEY, role TEXT)")
    conrol.commit()
    currol.execute("SELECT * FROM " + emojitable + " WHERE emoji=?", (ctx.options.emoji.name,))
    r = currol.fetchone()
    if r == None:
        currol.execute("INSERT INTO " + emojitable + " VALUES (?, ?)", (ctx.options.emoji.name, str((ctx.options.role.id,) ) ))
        conrol.commit()
        currol.execute("CREATE TABLE IF NOT EXISTS " + ruletable + "(message TEXT PRIMARY KEY, mode TEXT, prereq TEXT)")
        currol.execute("SELECT * FROM " + ruletable + " WHERE message=?", (ctx.options.message.id,))
        if currol.fetchone() == None:
            currol.execute("INSERT INTO " + ruletable + " VALUES (?, ?, ?)", (ctx.options.message.id, "free", None) )
        conrol.commit()
    else:
        _, roleSQ = r
        roleSQ = ast.literal_eval(roleSQ)
        if ctx.options.role.id in roleSQ:
            await ctx.respond("Role already on that reaction")
            conrol.commit()
            return
        else:
            roleSQ += (ctx.options.role.id,)
            roleSQ = str(roleSQ)
            currol.execute("UPDATE " + emojitable + " SET role=? WHERE emoji=?", (roleSQ, _))
    conrol.commit()
    await ctx.respond("Created reaction role!")

@reactionrole.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("emoji", "The emoji to remove", type=hikari.Emoji)
@lightbulb.option("message", "The message to listen to", type=hikari.Message)
@lightbulb.set_help("Removes a reaction role from a message.\nYou must be in the same channel as the message")
@lightbulb.command("rmv", "Removes roles from a member")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def rmv(ctx: lightbulb.Context):
    comm.log_com(ctx)
    emojitable = "rr_emoji_g" + str(ctx.guild_id) + "_c" + str(ctx.channel_id) + "_m" + str(ctx.options.message.id)
    ruletable = "rr_rule_g" + str(ctx.guild_id) + "_c" + str(ctx.channel_id)
    currol.execute("CREATE TABLE IF NOT EXISTS " + emojitable + "(emoji TEXT PRIMARY KEY, role TEXT)")
    conrol.commit()
    currol.execute("SELECT * FROM " + emojitable + " WHERE emoji=?", (ctx.options.emoji.name,))
    if currol.fetchone() == None:
        await ctx.respond("This emoji doesn't correspond to a role.")
        return
    else:
        await ctx.options.message.remove_reaction(ctx.options.emoji.name)
        currol.execute("DELETE FROM " + emojitable + " WHERE emoji=?", (ctx.options.emoji.name,))
        conrol.commit()
    currol.execute("SELECT * FROM " + emojitable)
    if currol.fetchall() == []:
        currol.execute("DROP TABLE IF EXISTS " + emojitable)
        currol.execute("DELETE FROM " + ruletable + " WHERE message=?", (ctx.options.message.id,))
        conrol.commit()
    await ctx.respond("Successfully removed reaction.")

@reactionrole.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("message", "The message to list from", type=hikari.Message)
@lightbulb.set_help("Lists the reaction roles of a message.\nYou must be in the same channel as the message")
@lightbulb.command("lst", "Lists reaction roles of a message")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def lst(ctx: lightbulb.Context):
    comm.log_com(ctx)
    emojitable = "rr_emoji_g" + str(ctx.guild_id) + "_c" + str(ctx.channel_id) + "_m" + str(ctx.options.message.id)
    ruletable = "rr_rule_g" + str(ctx.guild_id) + "_c" + str(ctx.channel_id)
    try:
        currol.execute("SELECT * FROM " + emojitable)
    except:
        await ctx.respond("That message has no reaction roles")
        return

    desc = ""

    currol.execute("SELECT mode, prereq FROM " + ruletable + " WHERE message=?", (ctx.options.message.id,) )
    mode, prereq = currol.fetchone()
    desc += "Mode: " + mode + "\n"
    if prereq != None:
        desc += "Prereq: <@&" + prereq + ">\n"

    currol.execute("SELECT * FROM " + emojitable)
    all = currol.fetchall()
    for name, roles in all:
        desc += name + ": "
        for id in list(ast.literal_eval(roles)):
            desc += "<@&" + str(id) + ">, "
        desc += "\n"

    embed = hikari.Embed(title="Reaction Roles for that message", description=desc, color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

modes = ["free", "verification", "remove", "unique", "limit", "binding"]

@reactionrole.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("prereq", "Role to require", type=hikari.Role, default=None)
@lightbulb.option("mode", "The mode for the reaction role", choices=modes, default="free")
@lightbulb.option("message", "The message to listen to", type=hikari.Message)
@lightbulb.set_help("Edit the settings of a reaction rule.\nYou must be in the same channel as the message")
@lightbulb.command("set", "Edit the settings of a reaction role")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def set(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.mode != "limit":
        if ctx.options.mode not in modes:
            await ctx.respond("That is not a valid mode for a reaction role")
            return
        else:
            mode = ctx.options.mode
    else:
        await ctx.respond("How many roles may a user recieve from this message?")
        event = await ctx.app.wait_for(hikari.GuildMessageCreateEvent, predicate=lambda e: e.message.author == ctx.author, timeout=30)
        try:
            nr = await ctx.app.rest.fetch_message(event.message.channel_id, event.message.id)
        except:
            await ctx.respond("Didn't recieve response in time")
            return
        try:
            mode = "limit" + str(int(nr.content))
        except:
            await ctx.respond("Invalid number")
            return
    emojitable = "rr_emoji_g" + str(ctx.guild_id) + "_c" + str(ctx.channel_id) + "_m" + str(ctx.options.message.id)
    ruletable = "rr_rule_g" + str(ctx.guild_id) + "_c" + str(ctx.channel_id)
    try:
        currol.execute("SELECT * FROM " + emojitable)
    except:
        await ctx.respond("That message has no reaction roles")
        return
    if ctx.options.prereq == None:
        currol.execute("UPDATE " + ruletable + " SET mode=?, prereq=? WHERE message=?", (mode, None, ctx.options.message.id) )
    else:
        currol.execute("UPDATE " + ruletable + " SET mode=?, prereq=? WHERE message=?", (mode, str(ctx.options.prereq.id), ctx.options.message.id) )
    conrol.commit()
    await ctx.respond("Edited reaction rule settings")

@plugin.listener(hikari.GuildReactionAddEvent, bind=True)
async def on_add_reaction(plugin, event: hikari.GuildReactionAddEvent):
    user = event.user_id
    if user in comm.bot_id or user in comm.block:
        return
    guild = event.guild_id
    channel = event.channel_id
    message = event.message_id
    emoji = event.emoji_name
    message_obj = await plugin.app.rest.fetch_message(channel, message)
    emojitable = "rr_emoji_g" + str(guild) + "_c" + str(channel) + "_m" + str(message)
    ruletable = "rr_rule_g" + str(guild) + "_c" + str(channel)
    try:
        currol.execute("SELECT * FROM " + emojitable + " WHERE emoji=?", (emoji,))
    except:
        return
    r = currol.fetchone()
    if r == None:
        return
    _, roles = r
    roles = list(ast.literal_eval(roles))
    member = await plugin.app.rest.fetch_member(guild, user)

    currol.execute("SELECT mode, prereq FROM " + ruletable + " WHERE message=?", (message,))
    mode, prereq = currol.fetchone()

    if prereq != None:
        try:
            if int(prereq) not in member.role_ids:
                raise Exception
        except:
            u = await plugin.app.rest.fetch_user(user)
            await u.send("You cannot use this message because you don't have the appropriate role.")
            return
    if mode == "free":
        for roleid in roles:
            try:
                await plugin.app.rest.add_role_to_member(guild, member, roleid)
            except:
                pass
    if mode == "verification":
        await message_obj.remove_reaction(emoji=emoji, user=event.user_id)
        for roleid in roles:
            try:
                await plugin.app.rest.add_role_to_member(guild, member, roleid)
            except:
                pass

    if mode == "remove":
        await message_obj.remove_reaction(emoji=emoji, user=event.user_id)
        for roleid in roles:
            try:
                await plugin.app.rest.remove_role_from_member(guild, member, roleid)
            except:
                pass

    if mode == "unique":
        currol.execute("SELECT emoji, role FROM " + emojitable)
        r = currol.fetchall()
        roles_to_remove = ()
        emojis = []
        for e,_ in r:
            if emoji != e:
                emojis.append(e)
            for __ in list(ast.literal_eval(_)):
                if __ in member.role_ids and __ not in roles:
                    roles_to_remove += (__,)
        roles_to_remove = list(roles_to_remove)
        for em in emojis:
            try:
                await message_obj.remove_reaction(emoji=em, user=event.user_id)
            except:
                pass
        for roleid in roles_to_remove:
            try:
                await plugin.app.rest.remove_role_from_member(guild, member, roleid)
            except:
                pass
        for roleid in roles:
            try:
                await plugin.app.rest.add_role_to_member(guild, member, roleid)
            except:
                pass

    if mode[:5] == "limit":
        currol.execute("SELECT role FROM " + emojitable)
        r = currol.fetchall()
        roles_to_check = ()
        for _, in r:
            roles_to_check += ast.literal_eval(_)
        roles_to_check = list(roles_to_check)
        count = 0
        for roleid in roles_to_check:
            if roleid in member.role_ids:
                count += 1
        for roleid in roles:
            if roleid not in member.role_ids:
                count += 1
        if count >= int(mode[5:]):
            await message_obj.remove_reaction(emoji=emoji, user=event.user_id)
            u = await plugin.app.rest.fetch_user(user)
            await u.send("You cannot get more than " + mode[5:] + " roles from this message.")
            return
        for roleid in roles:
            try:
                await plugin.app.rest.add_role_to_member(guild, member, roleid)
            except:
                pass
    if mode == "binding":
        await message_obj.remove_reaction(emoji=emoji, user=event.user_id)
        currol.execute("SELECT role FROM " + emojitable)
        r = currol.fetchall()
        roles_to_check = ()
        for _, in r:
            roles_to_check += ast.literal_eval(_)
        roles_to_check = list(roles_to_check)
        try:
            for i in roles_to_check:
                if i in member.role_ids:
                    raise Exception
        except:
            u = await plugin.app.rest.fetch_user(user)
            await u.send("You cannot get any more roles from this message.")
            return
        for roleid in roles:
            try:
                await plugin.app.rest.add_role_to_member(guild, member, roleid)
            except:
                pass

@plugin.listener(hikari.GuildReactionDeleteEvent, bind=True)
async def on_rmv_reaction(plugin, event: hikari.GuildReactionDeleteEvent):
    user = event.user_id
    if user in comm.bot_id or user in comm.block:
        return
    guild = event.guild_id
    channel = event.channel_id
    message = event.message_id
    emoji = event.emoji_name
    emojitable = "rr_emoji_g" + str(guild) + "_c" + str(channel) + "_m" + str(message)
    ruletable = "rr_rule_g" + str(guild) + "_c" + str(channel)
    try:
        currol.execute("SELECT * FROM " + emojitable + " WHERE emoji=?", (emoji,))
    except:
        return
    r = currol.fetchone()
    if r == None:
        return
    _, roles = r
    roles = list(ast.literal_eval(roles))
    member = await plugin.app.rest.fetch_member(guild, user)

    currol.execute("SELECT mode, prereq FROM " + ruletable + " WHERE message=?", (message,))
    mode, prereq = currol.fetchone()
    if mode in ["free", "unique"] or mode[:5] == "limit":
        for roleid in roles:
            try:
                await plugin.app.rest.remove_role_from_member(guild, member, roleid)
            except:
                pass
    if mode in ["verification", "remove", "binding"]:
        pass
