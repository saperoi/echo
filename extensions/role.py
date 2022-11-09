import lightbulb
import hikari
import comm

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
@lightbulb.implements(lightbulb.PrefixCommandGroup)
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

@role.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "ONLY ROLE ID! Role to add", type=int)
@lightbulb.option("user", "The user to add roles to.")
@lightbulb.set_help("Adds a role if the user doesn't already have said role")
@lightbulb.command("add", "Adds roles to member")
@lightbulb.implements(lightbulb.PrefixSubGroup)
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
@lightbulb.implements(lightbulb.PrefixSubGroup)
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
