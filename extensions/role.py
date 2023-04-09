import lightbulb
import hikari
import comm
import random

plugin = lightbulb.Plugin('role', 'Potter sorting hat >>>')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "ONLY ROLE ID! Role to add/remove", type=int)
@lightbulb.option("user", "The user to add/remove roles to/from.")
@lightbulb.set_help("Adds or removes a role if the user already or doesn't already have said role")
@lightbulb.command("role", "Adds/removes roles")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def role(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    results = [role.id for role in roles]
    member = await ctx.app.rest.fetch_member(ctx.guild_id, u)
    if ctx.options.role not in results:
        await comm.send_msg(ctx, "That role ID is not in this server, therefore I cannot add it")
    elif ctx.options.role not in member.role_ids:
        await ctx.app.rest.add_role_to_member(ctx.guild_id, member, ctx.options.role)
        await comm.send_msg(ctx, "Added role to member")
    elif ctx.options.role in member.role_ids:
        await ctx.app.rest.remove_role_from_member(ctx.guild_id, member, ctx.options.role)
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
@lightbulb.option("role", "ONLY ROLE ID! Role to add", type=int)
@lightbulb.option("user", "The user to add roles to.")
@lightbulb.set_help("Adds a role if the user doesn't already have said role")
@lightbulb.command("add", "Adds roles to member")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    results = [role.id for role in roles]
    member = await ctx.app.rest.fetch_member(ctx.guild_id, u)
    if ctx.options.role not in results:
        await comm.send_msg(ctx, "That role ID is not in this server, therefore I cannot add it")
    elif ctx.options.role not in member.role_ids:
        await ctx.app.rest.add_role_to_member(ctx.guild_id, member, ctx.options.role)
        await comm.send_msg(ctx, "Added role to member")
    else:
        await comm.send_msg(ctx, "Member already has this role")

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "ONLY ROLE ID! Role to remove", type=int)
@lightbulb.option("user", "The user to add roles to.")
@lightbulb.set_help("Removes a role if the user doesn't already have said role")
@lightbulb.command("rmv", "Removes roles from member")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def rmv(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    results = [role.id for role in roles]
    member = await ctx.app.rest.fetch_member(ctx.guild_id, u)
    if ctx.options.role not in results:
        await comm.send_msg(ctx, "That role ID is not in this server, therefore I cannot add it")
    elif ctx.options.role in member.role_ids:
        await ctx.app.rest.remove_role_from_member(ctx.guild_id, member, ctx.options.role)
        await comm.send_msg(ctx, "Removed role from member")
    else:
        await comm.send_msg(ctx, "Member doesn't have that role so I can't remove it!")

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "ONLY ROLE ID!", type=int)
@lightbulb.command("in", "Shows users that are members of a role.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def in_role(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    rolids = [role.id for role in roles]
    if ctx.options.role not in rolids:
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
        if ctx.options.role in mems[mms].role_ids:
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
@lightbulb.option("role_2", "Role to remove from. ONLY ROLE ID!", type=int, default=None)
@lightbulb.option("role_1", "Role to remove. ONLY ROLE ID!", type=int)
@lightbulb.command("purge_role_members", "Removes a role from a group of members.", aliases=["prm"])
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def purge_role_members(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    rolids = [role.id for role in roles]
    if (ctx.options.role_1 not in rolids) or (ctx.options.role_2 != None and ctx.options.role_2 not in rolids):
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
        if (ctx.options.role_1 in mems[mms].role_ids) and (ctx.options.role_2 == None or ctx.options.role_2 in mems[mms].role_ids):
            rolemems.append(mems[mms].user.id)
    for id in rolemems:
        m = await ctx.app.rest.fetch_member(ctx.guild_id, id)
        await ctx.app.rest.remove_role_from_member(ctx.guild_id, m, ctx.options.role_1)
    msg = "Removed " + roles[rolids.index(ctx.options.role_1)].name.replace('@', '') + " role from every member "
    if ctx.options.role_2 != None:
        msg += "with the " + roles[rolids.index(ctx.options.role_2)].name.replace('@', '') + " role"
    await ctx.respond(msg)

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role_2", "Role to add from. ONLY ROLE ID!", type=int, default=None)
@lightbulb.option("role_1", "Role to add. ONLY ROLE ID!", type=int)
@lightbulb.command("add_role_members", "Adds a role to a group of people.", aliases=["arm"])
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def add_role_members(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    rolids = [role.id for role in roles]
    if (ctx.options.role_1 not in rolids) or (ctx.options.role_2 != None and ctx.options.role_2 not in rolids):
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
        if (ctx.options.role_1 not in mems[mms].role_ids) and (ctx.options.role_2 == None or ctx.options.role_2 in mems[mms].role_ids):
            rolemems.append(mems[mms].user.id)

    for id in rolemems:
        m = await ctx.app.rest.fetch_member(ctx.guild_id, id)
        await ctx.app.rest.add_role_to_member(ctx.guild_id, m, ctx.options.role_1)
    msg = "Added " + roles[rolids.index(ctx.options.role_1)].name.replace('@', '') + " role to every member "
    if ctx.options.role_2 != None:
        msg += "with the " + roles[rolids.index(ctx.options.role_2)].name.replace('@', '') + " role"
    await ctx.respond(msg)

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("list", "Lists roles in server.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def list(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    d = ""
    for r in range(len(roles)):
        d += "<@&" + str(roles[r].id) + "> : " + str(roles[r].id) + "\n"
    embed = hikari.Embed(title="Roles", description=d, color=random.randint(0x0, 0xffffff))
    await ctx.respond(embed)

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "Role to add. ONLY ROLE ID!", type=int)
@lightbulb.command("info", "Lists info on a role in server.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def info(ctx: lightbulb.Context):
    comm.log_com(ctx)
    roles = await ctx.app.rest.fetch_roles(ctx.guild_id)
    rolids = [role.id for role in roles]
    if ctx.options.role not in rolids:
        await comm.send_msg(ctx, "That role ID is not in this server")
        return
    else:
        r = roles[rolids.index(ctx.options.role)]
    d = "**Role ID**: " + str(r.id) + "\n"
    d += "**Color**: " + str(r.color) + "\n"
    d += "**Position**: " + str(r.position) + "\n"
    d += "**Permissions**: \n" + str(r.permissions).replace("|", "\n")
    embed = hikari.Embed(title=r.name.replace('@', ''), description=d, color=r.color)
    if r.icon_url != None:
        embed.set_image(r.icon_url)
    await ctx.respond(embed)
